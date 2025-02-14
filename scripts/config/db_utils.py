import sqlite3
from config.constants import DB_PATH

def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        return None
