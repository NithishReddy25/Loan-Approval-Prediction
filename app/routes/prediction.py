import joblib
import numpy as np
import pandas as pd

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for,
)

from app.config import MODEL_PATH
from app.database import save_prediction
from app.shap_explainer import get_shap_values

NUMERIC_FEATURES = {
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
}


CATEGORICAL_CHOICES = {
    "Gender": {"Male", "Female"},
    "Married": {"Yes", "No"},
    "Dependents": {"0", "1", "2", "3+"},
    "Education": {"Graduate", "Not Graduate"},
    "Self_Employed": {"Yes", "No"},
    "Property_Area": {"Rural", "Semiurban", "Urban"},
}

prediction_bp = Blueprint("prediction", __name__)


# -------------------------------------------------
# Load Model
# -------------------------------------------------

model = joblib.load(MODEL_PATH)


def build_input_dataframe(data):
    """Validate and order input using the schema saved in the trained pipeline."""
    values = {}

    for feature in model.feature_names_in_:
        value = data.get(feature)
        if value is None or value == "":
            raise ValueError(f"{feature} is required.")

        if feature in NUMERIC_FEATURES:
            value = float(value)
            if value < 0:
                raise ValueError(f"{feature} cannot be negative.")
        elif value not in CATEGORICAL_CHOICES[feature]:
            raise ValueError(f"Invalid {feature} value: {value}.")

        values[feature] = value

    return pd.DataFrame([values], columns=model.feature_names_in_)


# -------------------------------------------------
# Home Page
# -------------------------------------------------

@prediction_bp.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("index.html")




@prediction_bp.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

        input_df = build_input_dataframe(request.form)

        prediction = model.predict(input_df)[0]

        probability = float(np.max(model.predict_proba(input_df)))

        confidence = round(probability * 100, 2)

        label = "Approved" if prediction == "Y" else "Rejected"

        shap_table, shap_error = get_shap_values(
            model,
            input_df,
            prediction,
        )

        prediction_id = save_prediction(
            user_id=session["user_id"],
            applicant=input_df.iloc[0].to_dict(),
            prediction=label,
            confidence=confidence,
        )

        return render_template(
            "result.html",
            prediction=label,
            confidence=confidence,
            applicant=input_df.iloc[0].to_dict(),
            shap_table=shap_table,
            shap_error=shap_error,
            prediction_id=prediction_id,
        )

    except (TypeError, ValueError) as e:
        flash(str(e), "danger")
        return redirect(url_for("prediction.home"))

    except Exception:
        return render_template(
            "result.html",
            prediction="Error",
            confidence=0,
            shap_table=None,
            shap_error=None,
        )
