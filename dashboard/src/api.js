const API_BASE_URL = "http://127.0.0.1:8000";

export async function getTopSignals(limit = 10) {
  const response = await fetch(
    `${API_BASE_URL}/signals/top?n=${limit}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch top signals");
  }

  return response.json();
}