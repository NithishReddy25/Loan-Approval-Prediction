from pathlib import Path

import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

# -----------------------------
# Project Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Load Model and Dataset
# -----------------------------
model = joblib.load(BASE_DIR / "models" / "final_pipeline.pkl")

df = pd.read_csv(BASE_DIR / "data" / "raw" / "train.csv")

# -----------------------------
# Prepare Features
# -----------------------------
X = df.drop(
    ["Loan_Status", "Loan_ID"],
    axis=1
)

classifier = model.named_steps["classifier"]
preprocessor = model.named_steps["preprocessor"]

X_transformed = preprocessor.transform(X)

# -----------------------------
# SHAP Explainer
# -----------------------------
explainer = shap.TreeExplainer(classifier)

# Compatible with newer SHAP versions
shap_values = explainer(X_transformed)

feature_names = preprocessor.get_feature_names_out()

# -----------------------------
# Summary Plot
# -----------------------------
shap.summary_plot(
    shap_values,
    X_transformed,
    feature_names=feature_names
)

# -----------------------------
# Explain Single Applicant
# -----------------------------
sample = X.iloc[[0]]

sample_transformed = preprocessor.transform(sample)

sample_shap = explainer(sample_transformed)

# -----------------------------
# Waterfall Plot
# -----------------------------
shap.plots.waterfall(sample_shap[0])

plt.show()