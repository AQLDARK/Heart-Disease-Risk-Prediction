import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd
import logging
import bcrypt
from datetime import datetime, timedelta
from ml.config import get_config

logger = logging.getLogger(__name__)
config = get_config()

DB_PATH = Path(config.DB_PATH)

FEATURES = [
    "age","sex","cp","trestbps","chol","fbs","restecg",
    "thalach","exang","oldpeak","slope","ca","thal"
]


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # 1) Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Patient',
            created_at TEXT NOT NULL
        )
    """)

    # 2) Subscriptions table (per user)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plan TEXT NOT NULL,
            status TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # 3) Predictions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,

            user_id INTEGER,
            age INTEGER,
            sex INTEGER,
            cp INTEGER,
            trestbps INTEGER,
            chol INTEGER,
            fbs INTEGER,
            restecg INTEGER,
            thalach INTEGER,
            exang INTEGER,
            oldpeak REAL,
            slope INTEGER,
            ca INTEGER,
            thal INTEGER,

            probability REAL NOT NULL,
            label TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    
    create_default_admin()


def get_subscription():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT plan FROM subscriptions ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if row:
        return row[0]
    return "Free"


def set_subscription(plan: str):
    from datetime import datetime, timedelta

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO subscriptions VALUES (
            NULL, ?, ?, ?, ?, ?
        )
    """, (
        "user",
        plan,
        "active",
        datetime.now().isoformat(),
        (datetime.now() + timedelta(days=30)).isoformat()
    ))

    conn.commit()
    conn.close()

def save_prediction(user_dict: dict, probability: float, label: str):
    """Save prediction to database with error handling."""
    try:
        conn = get_conn()
        cur = conn.cursor()

        values = [user_dict.get(f) for f in FEATURES]
        cur.execute(
            f"""
            INSERT INTO predictions (
                created_at, {",".join(FEATURES)}, probability, label
            ) VALUES (
                ?, {",".join(["?"] * len(FEATURES))}, ?, ?
            )
            """,
            [datetime.now().isoformat()] + values + [float(probability), str(label)]
        )

        conn.commit()
        logger.info(f"Prediction saved: label={label}, probability={probability:.3f}")
        
    except Exception as e:
        logger.error(f"Failed to save prediction: {e}")
        raise RuntimeError(f"Prediction save failed: {e}") from e
    finally:
        conn.close()

def load_predictions(limit: int = 500) -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY id DESC LIMIT ?",
        conn,
        params=(limit,)
    )
    conn.close()
    return df


def _hash_password(password: str) -> str:
    """Hash password using bcrypt (industry-standard, secure)."""
    try:
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    except Exception as e:
        logger.error(f"Password hashing failed: {e}")
        raise RuntimeError(f"Failed to hash password: {e}") from e


def _verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return False

def create_user(full_name: str, email: str, password: str, role: str = "Patient"):
    """Create a new user account with bcrypt password hashing."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        if not full_name or not email or not password:
            raise ValueError("All fields (full_name, email, password) are required")
        
        password_hash = _hash_password(password)
        
        cur.execute(
            "INSERT INTO users (full_name, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
            (full_name.strip(), email.lower().strip(), password_hash, role, datetime.now().isoformat())
        )
        user_id = cur.lastrowid

        # default Free plan
        cur.execute(
            "INSERT INTO subscriptions (user_id, plan, status, start_date, end_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, "Free", "active", datetime.now().isoformat(), (datetime.now() + timedelta(days=3650)).isoformat())
        )

        conn.commit()
        logger.info(f"User created: {email}")
        return user_id

    except sqlite3.IntegrityError as e:
        conn.rollback()
        logger.warning(f"User creation failed (email exists): {email}")
        raise ValueError("EMAIL_EXISTS") from e
    except Exception as e:
        logger.error(f"User creation failed: {e}")
        raise
    finally:
        conn.close()

def authenticate_user(email: str, password: str):
    """Authenticate user with email and bcrypt password."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, full_name, email, password_hash, role FROM users WHERE email = ?",
            (email.lower().strip(),)
        )
        row = cur.fetchone()
        conn.close()
        
        if not row:
            logger.warning(f"Login attempt with non-existent email: {email}")
            return None

        user_id, full_name, email_db, pw_hash, role = row
        
        if not _verify_password(password, pw_hash):
            logger.warning(f"Failed login attempt for user: {email}")
            return None

        logger.info(f"User authenticated: {email}")
        return {"user_id": user_id, "full_name": full_name, "email": email_db, "role": role}
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None

def get_subscription_for_user(user_id: int) -> str:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT plan FROM subscriptions WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else "Free"

def set_subscription_for_user(user_id: int, plan: str):
    conn = get_conn()
    cur = conn.cursor()
    now = datetime.now()
    cur.execute(
        "INSERT INTO subscriptions (user_id, plan, status, start_date, end_date) VALUES (?, ?, ?, ?, ?)",
        (user_id, plan, "active", now.isoformat(), (now + timedelta(days=30)).isoformat())
    )
    conn.commit()
    conn.close()

def create_default_admin():
    conn = get_conn()
    cur = conn.cursor()

    # Check if admin already exists
    cur.execute(
        "SELECT id FROM users WHERE email = ?",
        ("admin@system.com",)
    )

    if cur.fetchone():
        conn.close()
        return  # already created

    from datetime import datetime, timedelta

    # Create admin user
    password = "admin123"
    password_hash = _hash_password(password)

    cur.execute("""
        INSERT INTO users (
            full_name,
            email,
            password_hash,
            role,
            created_at
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        "System Administrator",
        "admin@system.com",
        password_hash,
        "Administrator",
        datetime.now().isoformat()
    ))

    admin_id = cur.lastrowid

    # Give premium subscription
    cur.execute("""
        INSERT INTO subscriptions (
            user_id,
            plan,
            status,
            start_date,
            end_date
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        admin_id,
        "Premium",
        "active",
        datetime.now().isoformat(),
        (datetime.now() + timedelta(days=3650)).isoformat()
    ))

    conn.commit()
    conn.close()
