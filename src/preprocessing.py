import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import joblib


def load_data(file_path="../data/raw/train.csv"):
    return pd.read_csv(file_path)


def remove_duplicates(df):
    return df.drop_duplicates()


def drop_unnecessary_columns(df):
    return df.drop(columns=["Loan_ID"])


def save_data(df, file_path="../data/processed/loan_data_clean.csv"):
    df.to_csv(file_path, index=False)


def encode_features(df):
    label_encoder = LabelEncoder()

    categorical_columns = [
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "Property_Area",
        "Loan_Status"
    ]

    for column in categorical_columns:
        df[column] = label_encoder.fit_transform(df[column])

    return df