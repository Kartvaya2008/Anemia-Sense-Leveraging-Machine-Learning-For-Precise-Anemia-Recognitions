# Anemia Sense: Leveraging Machine Learning for Precise Anemia Recognition

## Project Level
Intermediate

## Category
Machine Learning

## Developer
KR

## Mentor
Revanth

---

## 1. Project Overview

Anemia Sense is a machine learning-based application that predicts whether a person is anemic based on simple blood test values. The project focuses on early detection, faster screening, and assisting healthcare analysis. This system is designed for educational use and demonstrates how machine learning can support medical decision-making.

---

## 2. Objectives

- Build an ML model to classify anemia.
- Clean and preprocess medical dataset.
- Perform Exploratory Data Analysis (EDA).
- Train and evaluate multiple machine learning algorithms.
- Deploy a working web application using Streamlit or Flask.
- Provide an interactive interface for user input and predictions.

---

## 3. Understanding Anemia

Anemia is a condition where the body lacks enough red blood cells or hemoglobin. It affects oxygen transport, energy levels, and overall health. Early recognition can help patients receive timely treatment.

---

## 4. Dataset Description

The dataset includes the following features:

| Feature | Description |
|--------|-------------|
| Gender | 0 = Male, 1 = Female |
| Hemoglobin (Hb) | Hemoglobin level (g/dL) |
| PCV | Packed Cell Volume (%) |
| MCV | Mean Corpuscular Volume (fL) |
| MCHC | Mean Corpuscular Hemoglobin Concentration (g/dL) |

Target Variable:
- 1 = Anemic
- 0 = Not Anemic

---

## 5. Machine Learning Workflow

1. Data Collection  
2. Data Cleaning and Preprocessing  
3. Exploratory Data Analysis  
4. Feature Engineering  
5. Model Training  
6. Model Evaluation  
7. Deployment using Streamlit or Flask  

---

## 6. Model Selection and Training

Various machine learning models were tested, including:

- Logistic Regression  
- Random Forest Classifier  
- XGBoost  
- Support Vector Machine  
- Neural Network (optional)

Random Forest performed the best and was selected as the final model. The final trained model is saved as `model.pkl`.

---

## 7. Model Performance

The performance was evaluated using:

- Accuracy Score  
- Precision  
- Recall  
- F1-Score  
- Confusion Matrix

The model achieved an accuracy between 92% and 97%.

Screenshots of the heatmap, evaluation metrics, and application interface are located in the `screenshots/` folder.

---

## 8. Web Application (Streamlit/Flask)

The application allows users to enter:

- Gender  
- Hemoglobin  
- PCV  
- MCV  
- MCHC  

After entering the values, the model predicts whether the person is anemic.

The deployment script is available in `app.py`.

---

## 9. Project Structure

Anemia-Sense-ML/
│
├── app.py
├── model/
│ └── anemia_model.pkl
├── notebook/
│ └── anemia_training.ipynb
├── data/
│ └── anemia_dataset.csv
├── templates/
│ ├── index.html
│ └── result.html
├── static/
│ └── style.css
├── screenshots/
├── docs/
│ └── Anemia_Sense_Report.pdf
├── requirements.txt
└── README.md




