
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DriverModel, LapModel
from app.services.driver_lap_ingestion import ingest_driver_lap_data

router = APIRouter(prefix="/api/v1/drivers", tags=["drivers"])


@router.post("/sync")
async def sync_driver_data(
    session_key: int,
    db: Session = Depends(get_db),
):
    try:
        return await ingest_driver_lap_data(db, session_key)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("")
def get_drivers(
    session_key: int,
    db: Session = Depends(get_db),
):
    drivers = (
        db.query(DriverModel)
        .filter(DriverModel.session_key == session_key)
        .order_by(DriverModel.driver_number)
        .all()
    )

    return {
        "session_key": session_key,
        "count": len(drivers),
        "drivers": drivers,
    }


@router.get("/performance")
def get_driver_performance(
    session_key: int,
    db: Session = Depends(get_db),
):
    # Exclude pit-out laps and incomplete laps from lap-time statistics.
    results = (
        db.query(
            DriverModel.driver_number,
            DriverModel.full_name,
            DriverModel.name_acronym,
            DriverModel.team_name,
            DriverModel.team_colour,
            func.count(LapModel.lap_number).label("lap_count"),
            func.min(LapModel.lap_duration).label("best_lap"),
            func.avg(LapModel.lap_duration).label("average_lap"),
            func.min(LapModel.duration_sector_1).label("best_sector_1"),
            func.min(LapModel.duration_sector_2).label("best_sector_2"),
            func.min(LapModel.duration_sector_3).label("best_sector_3"),
        )
        .join(
            LapModel,
            (DriverModel.session_key == LapModel.session_key)
            & (DriverModel.driver_number == LapModel.driver_number),
        )
        .filter(
            DriverModel.session_key == session_key,
            LapModel.lap_duration.isnot(None),
            LapModel.is_pit_out_lap.isnot(True),
        )
        .group_by(
            DriverModel.driver_number,
            DriverModel.full_name,
            DriverModel.name_acronym,
            DriverModel.team_name,
            DriverModel.team_colour,
        )
        .order_by(func.min(LapModel.lap_duration))
        .all()
    )

    return {
        "session_key": session_key,
        "count": len(results),
        "drivers": [
            {
                "driver_number": row.driver_number,
                "name": row.full_name,
                "acronym": row.name_acronym,
                "team": row.team_name,
                "team_colour": row.team_colour,
                "lap_count": row.lap_count,
                "best_lap": row.best_lap,
                "average_lap": row.average_lap,
                "best_sector_1": row.best_sector_1,
                "best_sector_2": row.best_sector_2,
                "best_sector_3": row.best_sector_3,
            }
            for row in results
        ],
    }
