
import httpx

# OpenF1's public API base URL.
OPENF1_BASE_URL = "https://api.openf1.org/v1"


async def fetch_sessions(year: int) -> list[dict]:
    """
    Fetch all F1 sessions for a season from OpenF1.
    """

    # Create an async HTTP client with a timeout.
    async with httpx.AsyncClient(timeout=20.0) as client:

        response = await client.get(
            f"{OPENF1_BASE_URL}/sessions",
            params={"year": year},
        )

        # Raise an error if OpenF1 returns 4xx or 5xx.
        response.raise_for_status()

        # Convert the JSON response into Python data.
        return response.json()
