
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import SessionModel
from app.services.openf1 import fetch_sessions


def parse_datetime(value: str) -> datetime:
    # OpenF1 timestamps may end with Z, meaning UTC.
    # Python's fromisoformat accepts +00:00.
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


async def ingest_sessions(year: int, db: Session) -> dict:
    # Step 1: Fetch sessions from the external API.
    sessions = await fetch_sessions(year)

    inserted_or_updated = 0

    for item in sessions:
        # Step 2: Prepare the API record for PostgreSQL.
        record = {
            "session_key": item["session_key"],
            "meeting_key": item["meeting_key"],
            "year": item["year"],
            "session_name": item["session_name"],
            "session_type": item["session_type"],
            "date_start": parse_datetime(item["date_start"]),
            "date_end": parse_datetime(item["date_end"]),
            "circuit_key": item["circuit_key"],
            "circuit_short_name": item["circuit_short_name"],
            "country_name": item["country_name"],
            "location": item["location"],
            "is_cancelled": item["is_cancelled"],
            "raw_data": item,
        }

        # Step 3: Insert the record.
        # If the session already exists, update it instead.
        statement = insert(SessionModel).values(**record)

        statement = statement.on_conflict_do_update(
            index_elements=["session_key"],
            set_={
                "session_name": statement.excluded.session_name,
                "session_type": statement.excluded.session_type,
                "date_start": statement.excluded.date_start,
                "date_end": statement.excluded.date_end,
                "is_cancelled": statement.excluded.is_cancelled,
                "raw_data": statement.excluded.raw_data,
            },
        )

        db.execute(statement)
        inserted_or_updated += 1

    # Step 4: Commit all changes to PostgreSQL.
    db.commit()

    return {
        "year": year,
        "records_processed": inserted_or_updated,
        "status": "success",
    }
