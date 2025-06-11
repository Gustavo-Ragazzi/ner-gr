# 📓 NER CRF Training Notebook

This notebook demonstrates how to train and evaluate a **Named Entity Recognition (NER)** model using **Conditional Random Fields (CRFs)** with the `python-crfsuite` library.

## 📁 Structure

The notebook is organized into the following sections:

1. **Library installation**
2. **Importing libraries**
3. **Data loading and preprocessing** (expects `ampla_crf.xlsx`, not included in the repository)
4. **Helper functions**:
   - Feature extraction
   - CPF and CNPJ validation as custom features
5. **Model training and saving**
6. **Evaluation using `sklearn` metrics**
7. **Entity prediction with a `predict_entities` utility**

## 🚀 How to Run

1. Place your dataset file crf.xlsx inside the directory (you must provide it manually).

2. Run the notebook train_ner_crf.ipynb to generate the file ner-crf.model.

## 🧪 Example Usage

sample = "Rua Irineu Ferreira da Silva, 231 Taubaté São Paulo CEP"
result = predict_entities(sample)

Output: [{'token': 'Rua', 'classification': 'address'}, ...]

## ❗ Notes
- This notebook is not required to run the API. It is intended only for model training and experimentation.
- The trained model file (ner-crf.model) must be manually moved to api/models/ in order to be used by the API.

