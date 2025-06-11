import requests
import os
from datetime import datetime
from google.adk.agents import Agent
from dotenv import load_dotenv

load_dotenv()

def classify_text(text: str) -> dict:
  """Calls the /classify endpoint and returns its result."""
  try:
    response = requests.post(f"{os.getenv("API_URL")}/classify", json={"text": text}, timeout=10)
    response.raise_for_status()
    result = response.json().get("result", [])

    full_name_entry = next((item for item in result if item["classification"] == "full_name"), None)

    if full_name_entry:
      name = full_name_entry["token"]
      gender_response = requests.get(f"{os.getenv("API_URL")}/gender", params={"name": name}, timeout=10)
      gender_response.raise_for_status()
      gender = gender_response.json().get("gender", "fail")
      return {
        "status": "success",
        "extracted_data": result,
        "gender_phrase": f"The name '{name}' was classified as: {gender}.",
      }

    return {
      "status": "success",
      "extracted_data": result,
      "gender_phrase": None,
    }

  except requests.exceptions.RequestException as e:
    return {"status": "error", "error_message": f"Failed to reach API: {str(e)}"}


def get_greeting():
  current_hour = datetime.now().hour
  if 5 <= current_hour < 12:
    return "Good morning"
  if 12 <= current_hour < 18:
    return "Good afternoon"
  return "Good evening"

root_agent = Agent(
  name="ner_agent",
  model="gemini-2.0-flash",
  description="Agent that extracts registration data using NER.",
  instruction=f"""
  1. Greet the user with "{get_greeting()}". Then say: "I'm here to extract your registration data from natural language using Named Entity Recognition (NER)."
  2. Ask the user to provide their registration details (e.g. name, CPF/CNPJ, address).
  3. Once you receive the input, use the `classify_text` tool to extract tokens and their classifications.
  4. After receiving the response from the tool, print each token with its classification in this exact format:
    **token**: classification
    - one item per line
    - keep the original order of tokens
  5. If the response includes a field called `gender_phrase`, print it in a new paragraph after listing the tokens.
  6. Do not group tokens into entities like "Name: Gustavo Silva Pereira". Print each token individually as instructed.
  7. Do not add commentary or summaries. Only output the formatted list and the gender phrase (if available).
  """,
  tools=[classify_text],
)
