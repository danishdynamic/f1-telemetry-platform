import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pendulum
import requests

from airflow.decorators import dag, task


# Airflow containers reach FastAPI by its Compose service name.
API_BASE_URL = "http://backend:8000/api/v1"
YEAR = 2025


def _extract_list(payload, key: str) -> list:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        items = payload.get(key, [])
        return items if isinstance(items, list) else []
    return []


@dag(
    dag_id="f1_race_ingestion",
    description="Sync F1 sessions, save bronze snapshots, ingest drivers and laps, and validate data",
    schedule=None,  # Run manually for now
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["f1", "ingestion", "bronze"],
)
def f1_race_ingestion():

    @task
    def sync_sessions():
        response = requests.post(
            f"{API_BASE_URL}/sessions/sync",
            params={"year": YEAR},
            timeout=120,
        )
        response.raise_for_status()
        logging.info("Session sync response: %s", response.json())

    @task
    def select_latest_race():
        response = requests.get(
            f"{API_BASE_URL}/sessions",
            params={"year": YEAR},
            timeout=60,
        )
        response.raise_for_status()

        sessions = _extract_list(response.json(), "sessions")

        races = [
            session
            for session in sessions
            if session.get("session_type") == "Race"
            and not session.get("is_cancelled", session.get("cancelled", False))
        ]

        if not races:
            raise ValueError(f"No race sessions found for {YEAR}")

        # ISO date strings sort chronologically.
        latest_race = max(
            races,
            key=lambda session: session.get("date_start") or "",
        )

        session_key = latest_race["session_key"]

        logging.info(
            "Selected race: %s, session_key=%s",
            latest_race.get("session_name"),
            session_key,
        )

        return session_key

    @task
    def save_bronze_snapshot(session_key: int):
        # Store raw API responses without modifying the records.
        bronze_dir = (
            Path("/opt/airflow/data/bronze")
            / f"year={YEAR}"
            / f"session_key={session_key}"
        )
        bronze_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

        endpoints = {
            "drivers": "drivers",
            "laps": "laps",
        }

        for filename, endpoint in endpoints.items():
            response = requests.get(
                f"https://api.openf1.org/v1/{endpoint}",
                params={"session_key": session_key},
                timeout=120,
            )
            response.raise_for_status()

            records = response.json()
            output_file = bronze_dir / f"{filename}_{timestamp}.json"

            with output_file.open("w", encoding="utf-8") as file:
                json.dump(records, file, indent=2)

            logging.info(
                "Saved %s raw records to %s",
                len(records),
                output_file,
            )

        return str(bronze_dir)

    @task
    def ingest_drivers_and_laps(session_key: int):
        response = requests.post(
            f"{API_BASE_URL}/drivers/sync",
            params={"session_key": session_key},
            timeout=300,
        )
        response.raise_for_status()

        result = response.json()
        logging.info("Driver/lap ingestion result: %s", result)

        return result

    @task
    def validate_ingested_data(session_key: int):
        # Confirm driver records were stored.
        drivers_response = requests.get(
            f"{API_BASE_URL}/drivers",
            params={"session_key": session_key},
            timeout=60,
        )
        drivers_response.raise_for_status()
        drivers = _extract_list(drivers_response.json(), "drivers")

        if not drivers:
            raise ValueError("Data quality failed: no drivers found")

        # Confirm lap-performance records were generated.
        performance_response = requests.get(
            f"{API_BASE_URL}/drivers/performance",
            params={"session_key": session_key},
            timeout=60,
        )
        performance_response.raise_for_status()
        performance = _extract_list(performance_response.json(), "drivers")

        if not performance:
            raise ValueError("Data quality failed: no performance data")

        logging.info(
            "Data quality passed: %s drivers, %s performance records",
            len(drivers),
            len(performance),
        )

        return {
            "drivers_checked": len(drivers),
            "performance_records_checked": len(performance),
        }

    sessions_synced = sync_sessions()
    race_session_key = select_latest_race()

    sessions_synced >> race_session_key

    bronze_snapshot = save_bronze_snapshot(race_session_key)

    ingestion_result = ingest_drivers_and_laps(race_session_key)
    quality_result = validate_ingested_data(race_session_key)

    race_session_key >> bronze_snapshot
    bronze_snapshot >> ingestion_result
    ingestion_result >> quality_result


f1_race_ingestion()