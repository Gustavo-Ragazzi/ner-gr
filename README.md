# Named Entity Recognition + Google ADK Agent

This project is a demonstration of a machine learning pipeline combined with public data integration and Google ADK (Agent Development Kit). It uses a custom-trained CRF (Conditional Random Fields) model to extract structured information from free-form text and augment it with gender prediction using a public dataset.

---

## Objective

This project was created as part of a technical challenge from a company. The challenge involved:

* Building a classical machine learning model
* Integrating a public data source
* Using the Google Agent Development Kit (ADK)
* Returning structured predictions from natural language text

⏳ Due to a limited time constraint, the solution was implemented in approximately **8 hours**, focusing on functionality rather than polish. There is plenty of room for improvement (accuracy, Docker setup, linters, UI/UX, etc.).

---

## Project Structure

```
ner-gr/
├── api/                  # FastAPI application serving classification endpoints
├── adk/                  # ADK agent implementation
├── notebooks/            # Training notebook for the CRF model
├── .gitignore
└── README.md             # You're here
```

---

## Installation & Usage

This project uses **Poetry** for dependency management and **Makefiles** for simplified execution. You can use the Makefile or run the commands manually.

### 1. Clone the project

```bash
git clone https://github.com/Gustavo-Ragazzi/ner-gr.git
cd ner-gr
```

### 2. Install dependencies with Poetry

```bash
cd api
poetry install
```

```bash
cd ../adk
poetry install
```

### 3. Run the API and the Agent (in two separate terminals)

```bash
cd api
make run
```

```bash
cd adk
make run
```

> 🔧 Alternatively, you can run the API manually with:
>
> ```bash
> uvicorn app.main:app --reload --port 8001
> ```

> 📌 You **do not need** to run or modify the `notebooks/` folder – the trained model is already included in the `api/models/` directory.

---

## The NER Model (CRF)

The model used is a **Conditional Random Field (CRF)** trained to extract semantic entities from free text, such as names, address components, and contextual tags.

* Training was performed using the notebook `notebooks/train_ner_crf.ipynb`.
* It uses custom features like:

  * Word casing and structure
  * CPF/CNPJ format validation
  * Word prefixes/suffixes
* Output: A `.model` file used by the API for prediction

### Example Usage

**Request**

```
POST http://127.0.0.1:8001/classify
{
  "text": "Meu nome é Gustavo Ragazzi Amorim, moro na rua Sergipe, número 430, bairro Tereza Cristina da cidade São Joaquim de Bicas - MG"
}
```

**Response**

```json
{
  "result": [
    { "token": "Meu", "classification": "LX" },
    { "token": "Gustavo", "classification": "full_name" },
    { "token": "rua", "classification": "street_type" },
    { "token": "Sergipe,", "classification": "street_name" },
    { "token": "MG", "classification": "address_state" }
    ...
  ]
}
```

---

## Public Data Integration (Gender Detection)

This project uses a **public Brazilian dataset** to detect the likely gender associated with a given name. The dataset was sourced from:

🔗 [https://brasil.io/dataset/genero-nomes/nomes/](https://brasil.io/dataset/genero-nomes/nomes/)

### How it works

* A `.csv` file from the dataset is downloaded and stored in `api/app/data/nomes.csv`
* When a `full_name` token is extracted, the ADK agent makes a second request to:

  ```
  GET /gender?name=Gustavo
  ```
* This returns a gender prediction based on the dataset.

---

## Web Interface (ADK)

The **Agent** runs separately under the `adk/` directory and communicates with the FastAPI backend.

### Interface Flow

1. You start both services (`api` and `adk`)
2. The agent sends a POST to `/classify` with a free-form text
3. It parses the result and, if it finds a token classified as `full_name`, it calls `/gender?name=<firstName>`
4. Final result includes both extracted entities and the predicted gender.

---

## Environment Setup for Vertex AI (ADK)

To run the ADK component, you must set up your environment for Google Cloud.

### 1. Create a `.env` file

Place it in:

```
adk/named_entity_recognition/.env
```

Use the same structure as the provided `example.env`. Variables include:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=
GOOGLE_CLOUD_LOCATION=us-central1
API_URL=http://127.0.0.1:8001/
```

### 2. Authenticate with GCP

```bash
gcloud auth application-default login
```

This will open a browser to complete authentication.

> 💡 Refer to the official setup guide if needed:
> [https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart?hl=pt-br](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart?hl=pt-br)

---

## 🧪 Testing the System

You can test the full flow by editing the sample input in `agent.py` or creating a curl request to the FastAPI endpoint. Try something like:

```
Rua Irineu Ferreira da Silva, 231 Taubaté São Paulo CEP
```

The system will return structured tokens and the detected gender for the first full name.

---

## Final Notes

This was a limited-scope proof-of-concept project. Several improvements could be made with more time:

* Improve model accuracy and tagging schema
* Add Docker containers for each service
* Apply code formatting and linting
* Add tests and better exception handling

Despite that, the project accomplishes the goal of demonstrating a custom ML classifier, public data augmentation, and integration with Google’s Agent Development Kit.
