from fastapi import APIRouter, Query
from app.utils.gender_lookup import detect_gender

router = APIRouter()

@router.get(
  "/gender",
  summary="Detect gender from first name",
  description="Receives a first name and returns its most likely gender based on Brazilian census data."
)
def get_gender(name: str = Query(..., description="First name to classify")) -> dict[str, str]:
  """
  Detects gender for a given first name using preloaded Brazil.IO data.

  Args:
    name (str): The name to analyze.

  Returns:
    dict[str, str]: A dictionary with the name and its predicted gender ("male", "female", or "unknown").
  """
  return {
    "name": name,
    "gender": detect_gender(name)
  }
