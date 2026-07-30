"""SHAP explanations for the saved preprocessing-and-classifier pipeline."""

import numpy as np
import pandas as pd

try:
    import shap
except ImportError:  # Keep prediction available if the optional package is absent.
    shap = None


def get_shap_values(model, input_df, prediction):
    """Return the strongest feature contributions for the predicted class.

    SHAP's current API returns values shaped as
    ``(samples, features, classes)`` for a multiclass classifier. The old
    implementation selected only the first sample, leaving a two-dimensional
    array and causing the result table to fail silently.
    """
    if shap is None:
        return None, "SHAP is not installed. Install the project requirements to enable explanations."

    try:
        preprocessor = model.named_steps["preprocessor"]
        classifier = model.named_steps["classifier"]
        transformed_input = preprocessor.transform(input_df)
        feature_names = preprocessor.get_feature_names_out()

        # One row is tiny, so converting a possible sparse matrix is safe and
        # avoids compatibility problems between SHAP and sparse transformers.
        if hasattr(transformed_input, "toarray"):
            transformed_input = transformed_input.toarray()

        explanation = shap.TreeExplainer(classifier)(transformed_input)
        values = np.asarray(explanation.values)
        class_index = list(classifier.classes_).index(prediction)

        if values.ndim == 3 and values.shape[1] == len(feature_names):
            contributions = values[0, :, class_index]
        elif values.ndim == 3 and values.shape[2] == len(feature_names):
            contributions = values[0, class_index, :]
        elif values.ndim == 2:
            contributions = values[0]
        else:
            raise ValueError(f"Unexpected SHAP values shape: {values.shape}")

        result = pd.DataFrame(
            {"Feature": feature_names, "SHAP_Value": contributions}
        )
        result["Importance"] = result["SHAP_Value"].abs()

        result = result.sort_values("Importance", ascending=False).head(15)
        maximum_importance = result["Importance"].max()
        result["Bar_Width"] = (
            (result["Importance"] / maximum_importance * 100)
            if maximum_importance > 0
            else 0
        )

        return result, None
    except Exception as error:
        return None, f"Could not generate SHAP explanation: {error}"
