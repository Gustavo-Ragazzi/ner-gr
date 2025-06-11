from fastapi import APIRouter, Body
from app.models.schema import ClassifyRequest, ClassifyResponse, TokenClassification
from app.services.ner_crf import predict_entities

router = APIRouter()

@router.post(
  "/classify",
  response_model=ClassifyResponse,
  summary="Classify named entities in a string",
  description="Returns a list of tokens with their predicted entity classifications."
)
def classify_text(request: ClassifyRequest = Body(...)) -> dict[str, list[TokenClassification]]:
  raw_result = predict_entities(request.text)
  structured_result = [TokenClassification(**item) for item in raw_result]
  return {"result": structured_result}
