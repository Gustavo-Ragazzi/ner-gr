import os
import pycrfsuite
from app.utils.ner_utils import sent2features

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "ner-crf.model")
_tagger = None

def load_model():
  global _tagger
  if _tagger is None:
    _tagger = pycrfsuite.Tagger() # type: ignore
    _tagger.open(MODEL_PATH)
  return _tagger

def predict_entities(text: str):
  tagger = load_model()
  tokens = text.split()
  features = sent2features([(t, '') for t in tokens])
  labels = tagger.tag(features)
  return [{"token": t, "classification": l} for t, l in zip(tokens, labels)]
