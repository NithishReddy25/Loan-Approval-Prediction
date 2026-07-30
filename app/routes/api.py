from flask import (
    Blueprint,
    request,
    jsonify,
)

from app.routes.prediction import build_input_dataframe, model

api_bp = Blueprint("api", __name__, url_prefix="/api")




@api_bp.route("/health", methods=["GET"])
def health():

    return jsonify(
        {
            "status": "healthy",
            "model_loaded": True,
            "service": "Loan Approval Prediction API",
        }
    ), 200




@api_bp.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        if data is None:
            return jsonify(
                {
                    "success": False,
                    "message": "JSON data is required.",
                }
            ), 400

        input_df = build_input_dataframe(data)

        prediction = model.predict(input_df)[0]

        confidence = float(model.predict_proba(input_df).max())

        result = (
            "Loan Approved"
            if prediction == "Y"
            else "Loan Rejected"
        )

        return jsonify(
            {
                "success": True,
                "prediction": result,
                "prediction_code": str(prediction),
                "confidence": round(confidence * 100, 2),
            }
        )

    except (TypeError, ValueError) as e:

        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 400

    except Exception as e:

        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 500
