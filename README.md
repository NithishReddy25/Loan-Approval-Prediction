#  Loan-Approval-Prediction

A modern **Loan-Approval-Prediction** built using **Flask**, **Scikit-learn**, **Random Forest**, and **SHAP Explainability**. This application predicts whether a loan application is likely to be approved based on applicant information while providing confidence scores, feature importance, prediction history, and an interactive dashboard.

---

##  Table of Contents

* Overview
* Features
* Pages
* Tech Stack
* Machine Learning Workflow
* Project Structure
* Installation
* Usage
* Dataset
* Model Performance
* Future Improvements
* Contributing
* License
* Author

---

#  Overview

Financial institutions receive thousands of loan applications every day. Evaluating these applications manually is time-consuming and prone to inconsistencies.

This project uses a **Machine Learning pipeline** to automate the loan approval prediction process based on applicant details such as:

* Gender
* Marital Status
* Education
* Applicant Income
* Co-applicant Income
* Loan Amount
* Loan Term
* Credit History
* Property Area
* Employment Status

The application not only predicts whether a loan should be approved but also explains **why** the prediction was made using **SHAP (SHapley Additive exPlanations)**.

---

#  Features

###  Authentication

* User Registration
* Secure Login
* Logout
* Session Management

###  Prediction

* Loan Approval Prediction
* Random Forest Machine Learning Model
* Confidence Score
* Real-time Prediction

###  Dashboard

* Total Predictions
* Approved Loans
* Rejected Loans
* Approval Rate
* Interactive Statistics

###  Explainable AI

* SHAP Feature Importance
* Model Interpretation


###  Prediction History

* Save Predictions
* View Previous Predictions
* Delete History
* User-specific Records

### UI

* Responsive Design
* Modern Interface
* Mobile Friendly
* Bootstrap 5
* Clean Dashboard

---

#  Pages

## Login Page

## Registration Page

## Home Page

## Dashboard

## Prediction Result

## Prediction History




#  Tech Stack

## Backend

* Python
* Flask
* SQLite


## Machine Learning

* Scikit-learn
* Random Forest Classifier
* Pipeline
* ColumnTransformer
* OneHotEncoder
* StandardScaler
* SHAP

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Bootstrap Icons

## Data Processing

* Pandas
* NumPy

---

# 🧠 Machine Learning Workflow

```
Dataset
    │
    ▼
Data Cleaning
    │
    ▼
Feature Engineering
    │
    ▼
Preprocessing
    │
    ├── StandardScaler
    └── OneHotEncoder
    │
    ▼
Random Forest Classifier
    │
    ▼
Prediction
    │
    ▼
SHAP Explainability
```

---

# 📂 Project Structure

```
Loan-Approval-Prediction/
│
├── app/
│   ├── routes/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   ├── config.py
│   ├── database.py
│   ├── shap_explainer.py
│   └── __init__.py
│
├── data/
│
├── models/
│   └── final_pipeline.pkl
│
├── screenshots/
│
├── requirements.txt
├── README.md
├── LICENSE
├── run.py
└── train_pipeline.py
```

---

#  Installation

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Loan-Approval-Prediction.git
```

---

## 2. Open Project

```bash
cd Loan-Approval-Prediction
```

---

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run Application

```bash
python run.py
```

---

## 6. Open Browser

```
http://127.0.0.1:5000
```

---

#  Usage

1. Register a new account.
2. Log in securely.
3. Fill in the applicant details.
4. Click **Predict Loan Approval**.
5. View:

   * Prediction Result
   * Confidence Score
   * SHAP Feature Importance
6. Open the Dashboard to analyze prediction statistics.
7. View Prediction History.

---

#  Dataset

This project is trained using the **Loan Prediction Dataset** available on Kaggle.

Dataset includes:

* Applicant Income
* Coapplicant Income
* Credit History
* Education
* Property Area
* Loan Amount
* Loan Term
* Marital Status
* Gender
* Self Employment
* Dependents
* Loan Status

---

#  Machine Learning Model

Algorithm:

* Random Forest Classifier

Pipeline:

* ColumnTransformer
* StandardScaler
* OneHotEncoder
* RandomForestClassifier

Advantages:

* Handles categorical and numerical data
* Good generalization
* Robust against overfitting
* High prediction accuracy

---

#  Explainable AI (SHAP)

This project integrates **SHAP (SHapley Additive Explanations)** to improve model transparency.

Benefits:

* Understand model decisions
* Visualize feature importance
* Increase trust in predictions
* Improve debugging and analysis

---

#  Security Features

* Password Authentication
* User Sessions
* Protected Routes
* User-specific Prediction History

---

#  Future Improvements

* Deploy to Cloud (Render/Railway/Azure)
* PDF Report Generation
* Email Prediction Reports
* Admin Dashboard
* Multiple Machine Learning Models
* Loan Eligibility Score
* REST API
* Docker Support
* CI/CD Pipeline
* Dark Mode

---

#  Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new branch.

```bash
git checkout -b feature-name
```

3. Commit changes.

```bash
git commit -m "Added new feature"
```

4. Push changes.

```bash
git push origin feature-name
```

5. Create a Pull Request.

---

#  License

This project is licensed under the **MIT License**.

---

#  Author

**Nithish Reddy**

If you found this project useful, consider giving it a ⭐ on GitHub.

---

#  Support

If you like this project:

 Star the repository

 Fork the project

 Share your feedback

Happy Coding! 
