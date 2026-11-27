
import httpx

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SessionModel
from app.services.session_ingestion import ingest_sessions

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


@router.post("/sync")
async def sync_sessions(year: int = 2025, db: Session = Depends(get_db)):
    try:
        processed = await ingest_sessions(db, year)

        return {
            "year": year,
            "records_processed": processed,
            "status": "success",
        }

    except httpx.HTTPError as exc:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail=f"OpenF1 API request failed: {exc}",
        )

    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("")
def get_sessions(year: int = 2025, db: Session = Depends(get_db)):
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
