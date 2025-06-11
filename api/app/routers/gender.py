from fastapi import APIRouter, Query
from app.utils.gender_lookup import detect_gender

router = APIRouter()

@router.get("/gender", summary="Detect gender from first name")
def get_gender(name: str = Query(..., description="First name to classify")):
  """
  Receives a single first name and returns the most probable gender.
  """
  return {
    "name": name,
    "gender": detect_gender(name)
  }
