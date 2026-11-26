
import httpx

from fastapi import APIRouter, HTTPException, Query

from app.services.openf1 import fetch_sessions


# A router groups related API endpoints.
router = APIRouter(
    prefix="/api/v1/sessions",
    tags=["Sessions"],
)


@router.get("")
async def get_sessions(
    year: int = Query(default=2025, ge=2023, le=2026)
):
    """
    Return Formula 1 sessions for the requested season.
    """

    try:
        # Call our OpenF1 client function.
        sessions = await fetch_sessions(year)

        return {
            "year": year,
            "count": len(sessions),
            "sessions": sessions,
        }

    except httpx.HTTPStatusError as error:
        # OpenF1 responded with an HTTP error.
        raise HTTPException(
            status_code=502,
            detail="OpenF1 returned an error",
        ) from error

    except httpx.RequestError as error:
        # Network error, timeout, or connection failure.
        raise HTTPException(
            status_code=503,
            detail="Could not connect to OpenF1",
        ) from error
