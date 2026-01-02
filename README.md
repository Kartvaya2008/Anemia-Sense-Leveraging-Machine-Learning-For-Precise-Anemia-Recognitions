# 🩸 Anemia Sense: Leveraging Machine Learning for Precise Anemia Recognition

Anemia Sense is a data-driven machine learning project designed to accurately detect anemia using basic blood test parameters. The system demonstrates a complete end-to-end ML workflow, including data preprocessing, exploratory analysis, model building, hyperparameter tuning, evaluation, and deployment using a simple yet effective Streamlit interface. This project aims to showcase how artificial intelligence can support early healthcare screening, especially in resource-limited environments.

🔗 **Live Web App:**  
https://anemiscan26.streamlit.app/#campaign-settings

---

## 1. Project Overview
Anemia is a condition where the body lacks enough healthy red blood cells or hemoglobin, leading to fatigue, weakness, and long-term health complications. Traditional diagnosis requires laboratory testing and manual interpretation. Anemia Sense attempts to automate this process by using machine learning algorithms to predict whether a person is anemic based on common hematology features. Although this project is not a medical substitute, it serves as a prototype for future healthcare analytics systems.

---

## 2. Dataset Description
The dataset includes important blood parameters:
- Gender  
- Hemoglobin  
- Packed Cell Volume (PCV)  
- Mean Corpuscular Volume (MCV)  
- Mean Corpuscular Hemoglobin Concentration (MCHC)  

**Target Variable:**  
- `1` → Anemic  
- `0` → Not Anemic  

Preprocessing steps included handling missing values, fixing data types, removing duplicates, and scaling numerical features.

---

## 3. Exploratory Data Analysis (EDA)
EDA revealed patterns such as distribution of hemoglobin levels, comparison between anemic and non-anemic groups, and correlation analysis. A heatmap indicated that **Hemoglobin** and **PCV** were the strongest predictors for anemia classification.

---

## 4. Model Development and Evaluation
Multiple algorithms were tested:
- Logistic Regression  
- Random Forest  
- XGBoost  
- Support Vector Machine  

**Random Forest** achieved the highest performance, with an accuracy of **92–97%**, strong precision-recall values, and a balanced confusion matrix. This model was selected as the final classifier and exported as `model.pkl` for deployment.

---

## 5. Deployment Using Streamlit
A user-friendly Streamlit application was built to allow real-time predictions. Users enter values for:
- Gender  
- Hemoglobin  
- PCV  
- MCV  
- MCHC  

The app instantly returns:
- **"You have anemia."** or  
- **"You are not anemic."**

This makes the model accessible for demonstrations and educational purposes.

---

## 6. Conclusion
Anemia Sense highlights the potential of machine learning in assisting medical diagnostics. By combining data preprocessing, model development, evaluation metrics, and an interactive frontend, the project serves as a complete ML pipeline suitable for academic, portfolio, or research use.
