"""
Application Configuration
"""

import os

# ==========================================================
# Machine Learning
# ==========================================================

RANDOM_STATE = 42
TEST_SIZE = 0.20

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

MODEL_PATH = os.path.join(MODEL_DIR, "final_pipeline.pkl")
DATA_PATH = os.path.join(DATA_DIR, "processed", "loan_data_clean.csv")

DATABASE_PATH = os.path.join(PROJECT_ROOT, "loan_predictions.db")

# ==========================================================
# Flask
# ==========================================================

SECRET_KEY = "change_this_to_a_long_random_secret_key"

DEBUG = True

HOST = "127.0.0.1"
PORT = 5000

# ==========================================================
# Prediction Labels
# ==========================================================

APPROVED_LABEL = "Loan Approved"
REJECTED_LABEL = "Loan Rejected"

# ==========================================================
# Dashboard
# ==========================================================

MAX_HISTORY_RECORDS = 100

# ==========================================================
# Report Settings
# ==========================================================

REPORT_TITLE = "AI Loan Decision Support System"
REPORT_AUTHOR = "Loan Approval Prediction"