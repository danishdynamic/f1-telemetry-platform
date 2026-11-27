
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import SessionModel
from app.services.openf1 import fetch_sessions


def parse_datetime(value: str) -> datetime:
    # Convert API timestamps such as "...Z" into Python-compatible UTC.
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


async def ingest_sessions(db: Session, year: int) -> int:
    records = await fetch_sessions(year)

    for record in records:
        values = {
            "session_key": record["session_key"],
            "meeting_key": record["meeting_key"],
            "year": record["year"],
            "session_name": record["session_name"],
            "session_type": record["session_type"],
            "date_start": parse_datetime(record["date_start"]),
            "date_end": parse_datetime(record["date_end"]),
            "circuit_key": record["circuit_key"],
            "circuit_short_name": record["circuit_short_name"],
            "country_name": record["country_name"],
            "location": record["location"],
            "is_cancelled": record.get("is_cancelled", False),
            "raw_data": record,
        }

        # Insert new sessions; update existing ones by session_key.
        statement = insert(SessionModel).values(**values)

        statement = statement.on_conflict_do_update(
            index_elements=[SessionModel.session_key],
            set_={
                key: value
                for key, value in values.items()
                if key != "session_key"
            },
        )

        db.execute(statement)

    db.commit()
    return len(records)
