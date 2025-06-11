from fastapi import APIRouter, Body
from app.models.schema import ClassifyRequest, ClassifyResponse, TokenClassification
from app.services.ner_crf import predict_entities

router = APIRouter()

@router.post(
  "/classify",
  response_model=ClassifyResponse,
  summary="Classify named entities in a string",
  description=(
    "Receives a string input and returns a list of tokens with their corresponding "
    "predicted classifications such as name, address, document, etc."
  )
)
def classify_text(request: ClassifyRequest = Body(...)) -> dict[str, list[TokenClassification]]:
  """
  Classifies entities in the provided text using a trained CRF model.

  Args:
    request (ClassifyRequest): Object containing the input text.

  Returns:
    dict[str, list[TokenClassification]]: A dictionary with a `result` key containing a list of token-classification pairs.
  """
  raw_result = predict_entities(request.text)
  return {"result": [TokenClassification(**item) for item in raw_result]}
