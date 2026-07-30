"""
Application Initialization
"""

from flask import Flask

from app.config import (
    SECRET_KEY,
    DEBUG
)


def create_app():
    app = Flask(__name__)

    # -----------------------------
    # Configuration
    # -----------------------------
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG

    # -----------------------------
    # Register Blueprints
    # -----------------------------
    from app.routes.auth import auth_bp
    from app.routes.prediction import prediction_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.history import history_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(api_bp)

    # -----------------------------
    # Error Handlers
    # -----------------------------
    @app.errorhandler(404)
    def page_not_found(error):
        return (
            __import__("flask").render_template("404.html"),
            404
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            __import__("flask").render_template("500.html"),
            500
        )

    return app