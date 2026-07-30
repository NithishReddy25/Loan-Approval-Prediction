from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from app.database import (
    register_user,
    get_user,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not full_name or not email or not password:
            flash("Please fill all fields.", "danger")
            return render_template("register.html")

        if get_user(email):
            flash("Email already registered.", "warning")
            return render_template("register.html")

        

        register_user(
            full_name=full_name,
            email=email,
            password=password,
        )

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_user(email)

        if user is None:
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        if not check_password_hash(user["password"], password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["user_name"] = user["full_name"]
        session["user_email"] = user["email"]

        flash("Login successful.", "success")

        return redirect(url_for("prediction.home"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "info")

    return redirect(url_for("auth.login"))