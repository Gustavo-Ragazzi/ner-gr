from pydantic import BaseModel
from typing import List

class TokenClassification(BaseModel):
  token: str
  classification: str

class ClassifyRequest(BaseModel):
  text: str

class ClassifyResponse(BaseModel):
  result: List[TokenClassification]
