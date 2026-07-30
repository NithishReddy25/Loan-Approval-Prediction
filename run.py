from app import create_app
from app.database import create_users_table, create_table

app = create_app()

# Create database tables
create_users_table()
create_table()

if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "127.0.0.1"),
        port=app.config.get("PORT", 5000),
        debug=app.config.get("DEBUG", True),
    )