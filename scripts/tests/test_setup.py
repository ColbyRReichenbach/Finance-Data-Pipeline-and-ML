import sqlite3
from config.db_utils import DB_PATH


def test_database():
    """Tests if all tables exist in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n🔍 Checking if all required tables exist...\n")

    required_tables = [
        "historical_stocks",
        "historical_indexes",
        "historical_sectors",
        "live_stocks",
        "live_indexes",
        "live_sectors",
        "stock_metadata",
        "stock_fundamentals",
        "stock_anomalies",
        "stock_forecasts"
    ]

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existing_tables = {table[0] for table in cursor.fetchall()}

    all_tables_exist = True
    for table in required_tables:
        if table in existing_tables:
            print(f"✅ Table exists: {table}")
        else:
            print(f"❌ Missing table: {table}")
            all_tables_exist = False

    conn.close()

    if all_tables_exist:
        print("\n🎉 All tables exist! Database structure is correct.")
    else:
        print("\n⚠️ Some tables are missing! Run `setup_database.py` to recreate them.")


if __name__ == "__main__":
    test_database()
