import requests
from google.adk.agents import Agent
import os
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
        "report": (
          f"Resultado da classificação: {result}\n\n"
          f"O nome '{name}' foi classificado do gênero: {gender}."
        ),
      }

    return {
      "status": "success",
      "report": f"Resultado da classificação: {result}\nNenhum nome encontrado.",
    }

  except requests.exceptions.RequestException as e:
    return {"status": "error", "error_message": f"Failed to reach API: {str(e)}"}


root_agent = Agent(
  name="ner_agent",
  model="gemini-2.0-flash",
  description="Agent that classifies text using an NER API and optionally detects gender from names.",
  instruction="You always classify any incoming text using the external NER API.",
  tools=[classify_text],
)
