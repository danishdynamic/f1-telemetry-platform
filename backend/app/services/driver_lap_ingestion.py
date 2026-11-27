
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import DriverModel, LapModel
from app.services.openf1 import fetch_drivers, fetch_laps


def parse_datetime(value):
    if not value:
        return None

    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def upsert_records(db: Session, model, records: list[dict], key_columns: list):
    if not records:
        return 0

    # Insert all records in one batch.
    statement = insert(model).values(records)

    update_values = {
        column.name: getattr(statement.excluded, column.name)
        for column in model.__table__.columns
        if column.name not in key_columns
    }

    statement = statement.on_conflict_do_update(
        index_elements=[
            getattr(model, column) for column in key_columns
        ],
        set_=update_values,
    )

    db.execute(statement)
    return len(records)


async def ingest_driver_lap_data(db: Session, session_key: int):
    # Fetch sequentially to stay within API request limits.
    drivers = await fetch_drivers(session_key)
    laps = await fetch_laps(session_key)

    driver_records = []

    for item in drivers:
        driver_records.append({
            "session_key": item["session_key"],
            "driver_number": item["driver_number"],
            "meeting_key": item.get("meeting_key"),
            "full_name": item.get("full_name"),
            "first_name": item.get("first_name"),
            "last_name": item.get("last_name"),
            "name_acronym": item.get("name_acronym"),
            "team_name": item.get("team_name"),
            "team_colour": item.get("team_colour"),
            "headshot_url": item.get("headshot_url"),
            "raw_data": item,
        })

    lap_records = []

    for item in laps:
        lap_records.append({
            "session_key": item["session_key"],
            "driver_number": item["driver_number"],
            "lap_number": item["lap_number"],
            "meeting_key": item.get("meeting_key"),
            "date_start": parse_datetime(item.get("date_start")),
            "lap_duration": item.get("lap_duration"),
            "duration_sector_1": item.get("duration_sector_1"),
            "duration_sector_2": item.get("duration_sector_2"),
            "duration_sector_3": item.get("duration_sector_3"),
            "i1_speed": item.get("i1_speed"),
            "i2_speed": item.get("i2_speed"),
            "st_speed": item.get("st_speed"),
            "is_pit_out_lap": item.get("is_pit_out_lap"),
            "raw_data": item,
        })

    try:
        driver_count = upsert_records(
            db,
            DriverModel,
            driver_records,
            ["session_key", "driver_number"],
        )

        lap_count = upsert_records(
            db,
            LapModel,
            lap_records,
            ["session_key", "driver_number", "lap_number"],
        )

        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "session_key": session_key,
        "drivers_processed": driver_count,
        "laps_processed": lap_count,
    }
