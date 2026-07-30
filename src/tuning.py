import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    RandomizedSearchCV
)

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

df = pd.read_csv("../data/raw/train.csv")

X = df.drop(
    ["Loan_Status", "Loan_ID"],
    axis=1
)

y = df["Loan_Status"]

numeric_features = X.select_dtypes(
    exclude="object"
).columns

categorical_features = X.select_dtypes(
    include="object"
).columns

numeric_pipeline = Pipeline(
    [
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
    [
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
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
            numeric_pipeline,
            numeric_features
        ),

        (
            "cat",
            categorical_pipeline,
            categorical_features
        )

    ]
)

pipeline = Pipeline(
    [

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

param_grid = {

    "classifier__n_estimators":[
        100,
        200,
        300
    ],

    "classifier__max_depth":[
        5,
        10,
        20,
        None
    ],

    "classifier__min_samples_split":[
        2,
        5,
        10
    ],

    "classifier__min_samples_leaf":[
        1,
        2,
        4
    ]

}

grid = GridSearchCV(

    estimator=pipeline,

    param_grid=param_grid,

    cv=5,

    scoring="accuracy",

    n_jobs=-1,

    verbose=2

)

grid.fit(
    X,
    y
)

print(
    grid.best_params_
)

print(
    grid.best_score_
)

best_model = grid.best_estimator_

joblib.dump(

    best_model,

    "../models/final_pipeline.pkl"

)