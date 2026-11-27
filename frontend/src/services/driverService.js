
const API_URL = "http://localhost:8000/api/v1";

// Fetch all available sessions for a season.
export async function getSessions(year) {
  const response = await fetch(
    `${API_URL}/sessions?year=${year}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch sessions");
  }

  return response.json();
}

// Fetch driver performance for a selected session.
export async function getDriverPerformance(sessionKey) {
  const response = await fetch(
    `${API_URL}/drivers/performance?session_key=${sessionKey}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch driver performance");
  }

  return response.json();
}
