import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

# =====================================================
# Database Configuration
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "loan_predictions.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# Users Table
# =====================================================

def create_users_table():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT DEFAULT 'user',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# Predictions Table
# =====================================================

def create_table():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            gender TEXT,

            married TEXT,

            dependents TEXT,

            education TEXT,

            self_employed TEXT,

            applicant_income REAL,

            coapplicant_income REAL,

            loan_amount REAL,

            loan_term REAL,

            credit_history REAL,

            property_area TEXT,

            prediction TEXT,

            confidence REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# Register User
# =====================================================

def register_user(full_name, email, password):

    conn = get_connection()

    hashed_password = generate_password_hash(password)

    conn.execute("""

        INSERT INTO users(

            full_name,

            email,

            password

        )

        VALUES(?,?,?)

    """,

    (

        full_name,

        email,

        hashed_password

    ))

    conn.commit()
    conn.close()


# =====================================================
# Get User
# =====================================================

def get_user(email):

    conn = get_connection()

    user = conn.execute("""

        SELECT *

        FROM users

        WHERE email=?

    """,

    (email,)

    ).fetchone()

    conn.close()

    return user


# =====================================================
# Get User By ID
# =====================================================

def get_user_by_id(user_id):

    conn = get_connection()

    user = conn.execute("""

        SELECT *

        FROM users

        WHERE id=?

    """,

    (user_id,)

    ).fetchone()

    conn.close()

    return user


# =====================================================
# Save Prediction
# =====================================================

def save_prediction(
    user_id,
    applicant,
    prediction,
    confidence,
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO predictions(

            user_id,

            gender,

            married,

            dependents,

            education,

            self_employed,

            applicant_income,

            coapplicant_income,

            loan_amount,

            loan_term,

            credit_history,

            property_area,

            prediction,

            confidence

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            user_id,
            applicant["Gender"],
            applicant["Married"],
            applicant["Dependents"],
            applicant["Education"],
            applicant["Self_Employed"],
            applicant["ApplicantIncome"],
            applicant["CoapplicantIncome"],
            applicant["LoanAmount"],
            applicant["Loan_Amount_Term"],
            applicant["Credit_History"],
            applicant["Property_Area"],
            prediction,
            confidence,
        ),
    )

    prediction_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()

    return prediction_id


# =====================================================
# User Prediction History
# =====================================================

def get_user_predictions(user_id):

    conn = get_connection()

    rows = conn.execute("""

        SELECT *

        FROM predictions

        WHERE user_id=?

        ORDER BY created_at DESC

    """,

    (user_id,)

    ).fetchall()

    conn.close()

    return rows


def get_user_prediction(user_id, prediction_id):
    """Return one prediction only when it belongs to the requested user."""
    conn = get_connection()

    row = conn.execute(
        "SELECT * FROM predictions WHERE id=? AND user_id=?",
        (prediction_id, user_id),
    ).fetchone()

    conn.close()

    return row


# =====================================================
# All Predictions (Admin)
# =====================================================

def get_all_predictions():

    conn = get_connection()

    rows = conn.execute("""

        SELECT
            predictions.*,
            users.full_name,
            users.email

        FROM predictions

        LEFT JOIN users

        ON predictions.user_id = users.id

        ORDER BY predictions.created_at DESC

    """).fetchall()

    conn.close()

    return rows


# =====================================================
# Dashboard Statistics
# =====================================================

def get_dashboard_stats():

    conn = get_connection()

    total_users = conn.execute(

        "SELECT COUNT(*) FROM users"

    ).fetchone()[0]

    total_predictions = conn.execute(

        "SELECT COUNT(*) FROM predictions"

    ).fetchone()[0]

    approved = conn.execute("""

        SELECT COUNT(*)

        FROM predictions

        WHERE prediction LIKE '%Approved%'

    """).fetchone()[0]

    rejected = conn.execute("""

        SELECT COUNT(*)

        FROM predictions

        WHERE prediction LIKE '%Rejected%'

    """).fetchone()[0]

    avg_confidence = conn.execute("""

        SELECT AVG(confidence)

        FROM predictions

    """).fetchone()[0]

    conn.close()

    return {

        "total_users": total_users,

        "total_predictions": total_predictions,

        "approved": approved,

        "rejected": rejected,

        "avg_confidence": round(avg_confidence or 0, 2)

    }


# =====================================================
# Delete Prediction
# =====================================================

def delete_prediction(user_id, prediction_id):

    conn = get_connection()

    conn.execute(

        """

        DELETE FROM predictions

        WHERE id=? AND user_id=?

        """,

        (prediction_id, user_id)

    )

    conn.commit()

    conn.close()


# =====================================================
# Clear History
# =====================================================

def clear_history(user_id):

    conn = get_connection()

    conn.execute("""

        DELETE

        FROM predictions

        WHERE user_id=?

    """,

    (user_id,)

    )

    conn.commit()

    conn.close()
