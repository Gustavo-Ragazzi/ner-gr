from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, ner, gender

app = FastAPI(
  title="ML Classifier API",
  description="API to classify named entities and detect gender in Brazilian text.",
  version="1.0.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ner.router)
app.include_router(gender.router)
