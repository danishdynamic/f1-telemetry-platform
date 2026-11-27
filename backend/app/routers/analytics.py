
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SessionModel

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/summary")
def get_summary(year: int = 2025, db: Session = Depends(get_db)):
    # Count stored sessions by session type.
    results = (
        db.query(
            SessionModel.session_type,
            func.count(SessionModel.session_key),
        )
        .filter(SessionModel.year == year)
        .group_by(SessionModel.session_type)
        .all()
    )

    counts = {
        session_type: count
        for session_type, count in results
    }

    total = sum(counts.values())

    return {
        "year": year,
        "total_sessions": total,
        "sessions_by_type": counts,
    }


@router.get("/meetings")
def get_meetings(year: int = 2025, db: Session = Depends(get_db)):
    # Group sessions into race weekends / event meetings.
    meetings = (
        db.query(
            SessionModel.meeting_key,
            SessionModel.country_name,
            SessionModel.location,
            SessionModel.circuit_short_name,
            func.count(SessionModel.session_key).label("session_count"),
        )
        .filter(SessionModel.year == year)
        .group_by(
            SessionModel.meeting_key,
            SessionModel.country_name,
            SessionModel.location,
            SessionModel.circuit_short_name,
        )
        .order_by(SessionModel.meeting_key)
        .all()
    )

    return {
        "year": year,
        "count": len(meetings),
        "meetings": [
            {
                "meeting_key": row.meeting_key,
                "country": row.country_name,
                "location": row.location,
                "circuit": row.circuit_short_name,
                "session_count": row.session_count,
            }
            for row in meetings
        ],
    }
