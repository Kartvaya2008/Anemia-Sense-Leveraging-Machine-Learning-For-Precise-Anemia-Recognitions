# 🩸 Anemia Sense — ML-Powered Anemia Detection

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge" />
</p>

<p align="center">
  <b>Leveraging Machine Learning for Precise Anemia Recognition</b><br/>
  A complete end-to-end ML system for early anemia screening using blood test parameters.
</p>

<p align="center">
  🔗 <a href="https://anemiscan26.streamlit.app/#campaign-settings"><strong>View Live Web App »</strong></a>
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Installation Guide](#-installation-guide)
- [How to Run](#-how-to-run)
- [Usage Examples](#-usage-examples)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🧬 Overview

**Anemia Sense** is a data-driven machine learning project designed to accurately detect anemia using basic blood test parameters. It demonstrates a complete end-to-end ML workflow including:

- Data preprocessing & exploratory data analysis (EDA)
- Model building & hyperparameter tuning
- Model evaluation & performance metrics
- Interactive deployment via a Streamlit web interface

> ⚠️ **Disclaimer:** This project is a research prototype and is **not a substitute for professional medical diagnosis**. Always consult a qualified healthcare provider.

---

## 🚨 Problem Statement

Anemia is a widespread condition where the body lacks sufficient healthy red blood cells or hemoglobin, leading to fatigue, weakness, and long-term health complications. Traditional diagnosis requires laboratory testing and expert manual interpretation — a barrier in resource-limited healthcare environments.

**Anemia Sense** attempts to automate early-stage screening using machine learning, making preliminary detection faster, more accessible, and cost-effective.

---

## ✨ Key Features

| Feature | Description |
|--------|-------------|
| 🔍 **Anemia Prediction** | Predicts anemia status (Anemic / Not Anemic) from blood parameters |
| 📊 **Exploratory Data Analysis** | Visual insights into the dataset distributions and correlations |
| 🤖 **Multiple ML Models** | Trains and compares several classification algorithms |
| 🎯 **Hyperparameter Tuning** | Optimizes model performance using grid/random search |
| 📈 **Model Evaluation** | Detailed metrics — accuracy, precision, recall, F1-score, ROC-AUC |
| 🌐 **Streamlit Web App** | Clean, interactive UI for real-time predictions |
| 🧪 **Beginner Friendly** | Well-commented code ideal for learning ML workflows |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Pandas** | Data loading, manipulation, and preprocessing |
| **NumPy** | Numerical computations |
| **Matplotlib / Seaborn** | Data visualization and EDA |
| **Scikit-learn** | ML model building, training, evaluation, and tuning |
| **Streamlit** | Interactive web application deployment |
| **Joblib / Pickle** | Model serialization and loading |

---

## 📂 Dataset

The dataset contains the following hematological features:

| Feature | Description |
|---------|-------------|
| `Gender` | Biological sex of the individual |
| `Hemoglobin` | Hemoglobin level in blood (g/dL) |
| `Packed Cell Volume (PCV)` | Percentage of blood volume occupied by RBCs |
| `Mean Corpuscular Volume (MCV)` | Average volume of a red blood cell (fL) |
| `Mean Corpuscular Hemoglobin Concentration (MCHC)` | Concentration of hemoglobin in RBCs (g/dL) |

**Target Variable:**

- `1` → **Anemic**
- `0` → **Not Anemic**

---

## 🗂️ Project Structure

```
anemia-sense/
│
├── data/
│   └── anemia_dataset.csv          # Raw dataset
│
├── notebooks/
│   └── anemia_analysis.ipynb       # EDA + model training notebook
│
├── models/
│   └── anemia_model.pkl            # Trained and serialized ML model
│
├── app/
│   └── app.py                      # Streamlit web application
│
├── src/
│   ├── preprocess.py               # Data cleaning & feature engineering
│   ├── train.py                    # Model training script
│   └── evaluate.py                 # Evaluation metrics & plots
│
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── LICENSE                         # License file
```

---

## ⚙️ Installation Guide

Follow these steps to set up the project locally:

### 1. Prerequisites

Make sure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- pip (comes with Python)

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/anemia-sense.git
cd anemia-sense
```

### 3. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Run the Streamlit Web App

```bash
streamlit run app/app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

### Run the Training Pipeline

```bash
python src/train.py
```

### Explore the Notebook

```bash
jupyter notebook notebooks/anemia_analysis.ipynb
```

---

## 💡 Usage Examples

### Making a Prediction via the Web App

1. Open the Streamlit app in your browser.
2. Enter the patient's blood parameters in the input fields:
   - Gender
   - Hemoglobin level
   - Packed Cell Volume (PCV)
   - Mean Corpuscular Volume (MCV)
   - Mean Corpuscular Hemoglobin Concentration (MCHC)
3. Click **"Predict"**.
4. The app will display whether the patient is **Anemic** or **Not Anemic** along with a confidence score.

### Prediction via Python Script

```python
import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/anemia_model.pkl")

# Input sample (Gender encoded: 0=Female, 1=Male)
sample = pd.DataFrame([{
    "Gender": 1,
    "Hemoglobin": 10.5,
    "PCV": 32,
    "MCV": 75,
    "MCHC": 30.2
}])

# Predict
prediction = model.predict(sample)
print("Anemic" if prediction[0] == 1 else "Not Anemic")
```

---

## 📸 Screenshots

> 🖼️ *Screenshots coming soon — add images to the `assets/` folder and update paths below.*

| Home / Input Screen | Prediction Result |
|---------------------|-------------------|
| ![Home Screen](assets/screenshot_home.png) | ![Result Screen](assets/screenshot_result.png) |

---

## 🤝 Contributing

Contributions are welcome and greatly appreciated! Here's how to get started:

1. **Fork** the repository
2. **Create** a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make** your changes and commit them:
   ```bash
   git commit -m "Add: your feature description"
   ```
4. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** on the main repository

### 📌 Contribution Guidelines

- Follow PEP 8 Python style conventions
- Write clear, descriptive commit messages
- Add comments to new functions and complex logic
- Update the README if you add new features or change setup steps
- Be respectful and constructive in all discussions

---

## 📄 License

> 📝 *This project is currently unlicensed. A license will be added soon.*

<!-- Uncomment and update when ready:
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
-->

---

## 👤 Author

**Your Name**

<p>
  <a href="https://github.com/your-username">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  <a href="https://linkedin.com/in/your-profile">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="mailto:your.email@example.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
</p>

> 💬 *If you found this project helpful, please consider giving it a ⭐ on GitHub — it means a lot!*

---

<p align="center">
  Made with ❤️ and Python &nbsp;|&nbsp; Anemia Sense © 2024
</p>
