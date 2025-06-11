from fastapi import APIRouter

router = APIRouter()

@router.get(
  "/health",
  summary="Health check endpoint",
  description="Simple endpoint to verify if the API is running and responsive."
)
def health_check() -> dict[str, str]:
  """
  Health check endpoint.

  Returns:
    dict[str, str]: A dictionary indicating the service is operational.
  """
  return {"status": "ok"}
