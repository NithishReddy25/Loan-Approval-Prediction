from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    Response,
)

import csv
from io import StringIO

import pandas as pd

from app.database import (
    get_user_predictions,
    get_user_prediction,
    delete_prediction,
    clear_history,
)

history_bp = Blueprint("history", __name__)

EXPORT_FIELDS = (
    "id", "created_at", "prediction", "confidence", "gender", "married",
    "dependents", "education", "self_employed", "applicant_income",
    "coapplicant_income", "loan_amount", "loan_term", "credit_history",
    "property_area",
)
from app.routes.prediction import model
from app.shap_explainer import get_shap_values


def csv_download(rows, filename):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=EXPORT_FIELDS)
    writer.writeheader()
    writer.writerows({field: row[field] for field in EXPORT_FIELDS} for row in rows)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


def saved_applicant(row):
    """Convert a stored database row back into the pipeline input schema."""
    return {
        "Gender": row["gender"],
        "Married": row["married"],
        "Dependents": row["dependents"],
        "Education": row["education"],
        "Self_Employed": row["self_employed"],
        "ApplicantIncome": row["applicant_income"],
        "CoapplicantIncome": row["coapplicant_income"],
        "LoanAmount": row["loan_amount"],
        "Loan_Amount_Term": row["loan_term"],
        "Credit_History": row["credit_history"],
        "Property_Area": row["property_area"],
    }


@history_bp.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    predictions = get_user_predictions(session["user_id"])

    return render_template(
        "history.html",
        predictions=predictions,
    )


@history_bp.route("/history/download")
def download_history():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    rows = get_user_predictions(session["user_id"])
    return csv_download(rows, "loan_prediction_history.csv")


@history_bp.route("/history/download/<int:prediction_id>")
def download_prediction(prediction_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    row = get_user_prediction(session["user_id"], prediction_id)
    if row is None:
        flash("Prediction record was not found.", "danger")
        return redirect(url_for("history.history"))

    return csv_download([row], f"loan_prediction_{prediction_id}.csv")


@history_bp.route("/history/<int:prediction_id>")
def view_prediction(prediction_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    row = get_user_prediction(session["user_id"], prediction_id)
    if row is None:
        flash("Prediction record was not found.", "danger")
        return redirect(url_for("history.history"))

    applicant = saved_applicant(row)
    shap_table = None
    shap_error = "This older record does not contain all application details for SHAP."

    if all(value is not None for value in applicant.values()):
        input_df = pd.DataFrame([applicant], columns=model.feature_names_in_)
        prediction_code = "Y" if row["prediction"] == "Approved" else "N"
        shap_table, shap_error = get_shap_values(model, input_df, prediction_code)

    return render_template(
        "result.html",
        prediction=row["prediction"],
        confidence=row["confidence"],
        applicant=applicant,
        shap_table=shap_table,
        shap_error=shap_error,
        prediction_id=row["id"],
    )


@history_bp.route("/history/delete/<int:prediction_id>")
def delete_history(prediction_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    delete_prediction(session["user_id"], prediction_id)

    flash(
        "Prediction deleted successfully.",
        "success",
    )

    return redirect(url_for("history.history"))


@history_bp.route("/history/clear")
def clear_prediction_history():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    clear_history(session["user_id"])

    flash(
        "History cleared successfully.",
        "success",
    )

    return redirect(url_for("history.history"))
