"""Backward-compatible application entry point.

Run ``python run.py`` from the project root for the normal development server.
This module remains available for WSGI servers that import ``app.app:app``.
"""

from app import create_app
from app.database import create_table, create_users_table


create_users_table()
create_table()
app = create_app()


if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "127.0.0.1"),
        port=app.config.get("PORT", 5000),
        debug=app.config.get("DEBUG", True),
    )
