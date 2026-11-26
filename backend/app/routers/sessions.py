
import httpx

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SessionModel
from app.services.session_ingestion import ingest_sessions


router = APIRouter(
    prefix="/api/v1/sessions",
    tags=["Sessions"],
)


@router.post("/sync")
async def sync_sessions(
    year: int = Query(default=2025, ge=2023, le=2026),
    db: Session = Depends(get_db),
):
    # This endpoint fetches data from OpenF1
    # and saves it into PostgreSQL.
    try:
        result = await ingest_sessions(year, db)
        return result

    except httpx.HTTPError as error:
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail="OpenF1 request failed",
        ) from error

    except Exception as error:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Session ingestion failed",
        ) from error


@router.get("")
def get_sessions(
    year: int = Query(default=2025, ge=2023, le=2026),
    db: Session = Depends(get_db),
):
    # This endpoint reads data from PostgreSQL.
    sessions = (
        db.query(SessionModel)
        .filter(SessionModel.year == year)
        .order_by(SessionModel.date_start)
        .all()
    )

    return {
        "year": year,
        "count": len(sessions),
        "sessions": sessions,
    }
