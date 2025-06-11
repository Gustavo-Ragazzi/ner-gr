import os
import pandas as pd
from functools import lru_cache
from typing import Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "nomes.csv")

@lru_cache(maxsize=1)
def get_name_to_gender_dict() -> Dict[str, str]:
  """
  Load the name-to-gender mapping from the CSV dataset.
  Only names with high confidence (ratio >= 0.9) are included.

  Returns:
    Dict[str, str]: Mapping of UPPERCASE first names to "M" or "F"
  """
  df = pd.read_csv(CSV_PATH, usecols=["first_name", "classification", "ratio"])
  df = df[df["ratio"] >= 0.9]
  return dict(zip(df["first_name"].str.upper(), df["classification"]))

def detect_gender(name: str) -> str:
  """
  Detect the gender of a given first name based on the Brazil.IO dataset.

  Args:
    name (str): First name to classify

  Returns:
    str: "male", "female", or "unknown"
  """
  gender = get_name_to_gender_dict().get(name.upper())
  match gender:
    case "M":
      return "male"
    case "F":
      return "female"
    case _:
      return "unknown"
