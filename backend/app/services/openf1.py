
import httpx

OPENF1_BASE_URL = "https://api.openf1.org/v1"


async def fetch_sessions(year: int) -> list[dict]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{OPENF1_BASE_URL}/sessions",
            params={"year": year},
        )
        response.raise_for_status()
        return response.json()


async def fetch_drivers(session_key: int) -> list[dict]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{OPENF1_BASE_URL}/drivers",
            params={"session_key": session_key},
        )
        response.raise_for_status()
        return response.json()


async def fetch_laps(session_key: int) -> list[dict]:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            f"{OPENF1_BASE_URL}/laps",
            params={"session_key": session_key},
        )
        response.raise_for_status()
        return response.json()
