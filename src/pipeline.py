import pandas as pd

import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import OneHotEncoder

from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier


BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "data" / "raw" / "train.csv")

X = df.drop(["Loan_Status", "Loan_ID"], axis=1)

y = df["Loan_Status"]

categorical_features = X.select_dtypes(
    include="object"
).columns

numerical_features = X.select_dtypes(
    exclude="object"
).columns

print(categorical_features)

print(numerical_features)

numerical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),

        (
            "scaler",
            StandardScaler()
        )
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),

        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)

preprocessor = ColumnTransformer(

    transformers=[

        (
            "num",
            numerical_pipeline,
            numerical_features
        ),

        (
            "cat",
            categorical_pipeline,
            categorical_features
        )

    ]
)

model = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "classifier",
            RandomForestClassifier(
                random_state=42
            )
        )

    ]
)

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42
)

model.fit(

    X_train,

    y_train
)

predictions = model.predict(X_test)

from sklearn.metrics import accuracy_score

accuracy = accuracy_score(

    y_test,

    predictions
)

print(accuracy)

joblib.dump(model, BASE_DIR / "models" / "final_pipeline.pkl")
