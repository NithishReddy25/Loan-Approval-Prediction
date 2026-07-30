from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
)

from app.database import (
    get_dashboard_stats,
    get_user_predictions,
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    stats = get_dashboard_stats()

    history = get_user_predictions(session["user_id"])

    total_predictions = stats.get("total_predictions", 0)
    approved = stats.get("approved", 0)
    rejected = stats.get("rejected", 0)

    approval_rate = 0

    if total_predictions > 0:
        approval_rate = round(
            (approved / total_predictions) * 100,
            2,
        )

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name"),
        stats=stats,
        history=history,
        total_predictions=total_predictions,
        approved=approved,
        rejected=rejected,
        approval_rate=approval_rate,
    )