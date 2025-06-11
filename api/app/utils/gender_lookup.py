import pandas as pd
from functools import lru_cache
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "nomes.csv")

@lru_cache(maxsize=1)
def get_name_to_gender_dict() -> dict[str, str]:
  df = pd.read_csv(CSV_PATH, usecols=["first_name", "classification", "ratio"])
  df = df[df["ratio"] >= 0.9]  # mantém nomes com alta confiança
  return dict(zip(df["first_name"].str.upper(), df["classification"]))

def detect_gender(name: str) -> str:
  """
  Detect the gender of a given first name based on the Brazil.IO dataset.
  Dataset available on https://brasil.io/dataset/genero-nomes/nomes/

  Args:
    name (str): First name to classify

  Returns:
    str: "male", "female", or "unknown"
  """
  raw = get_name_to_gender_dict().get(name.upper())
  match raw:
    case "M": return "male"
    case "F": return "female"
    case _:   return "unknown"
