from fastapi import FastAPI
from app.routers import health, ner, gender

app = FastAPI(
  title="ML Classifier API",
  description="API to classify strings and detect gender.",
  version="1.0.0"
)

app.include_router(health.router)
app.include_router(ner.router)
app.include_router(gender.router)
