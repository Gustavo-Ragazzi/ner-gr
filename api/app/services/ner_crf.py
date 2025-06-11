import os
import pycrfsuite
from typing import List, Dict
from app.utils.ner_utils import sent2features

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "ner-crf.model")
_tagger: pycrfsuite.Tagger | None = None  # type: ignore

def load_model() -> pycrfsuite.Tagger: # type: ignore
  """
  Load and cache the CRF model from disk.

  Returns:
    pycrfsuite.Tagger: The loaded CRF tagger instance.
  """
  global _tagger
  if _tagger is None:
    _tagger = pycrfsuite.Tagger()  # type: ignore
    _tagger.open(MODEL_PATH) # type: ignore
  return _tagger

def predict_entities(text: str) -> List[Dict[str, str]]:
  """
  Predict named entity classifications for tokens in the input text.

  Args:
    text (str): Input string to be tokenized and classified.

  Returns:
    List[Dict[str, str]]: A list of dictionaries, each containing a token and its classification.
  """
  tagger = load_model()
  tokens = text.split()
  features = sent2features([(t, '') for t in tokens])
  labels = tagger.tag(features)
  return [{"token": t, "classification": l} for t, l in zip(tokens, labels)]
