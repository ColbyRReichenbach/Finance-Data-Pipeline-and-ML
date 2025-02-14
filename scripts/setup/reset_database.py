import sqlite3
import os
from config.db_utils import DB_PATH
from setup.setup_database import create_tables


def reset_database():
    """Drops all tables and recreates them from scratch."""
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("⚠️  Dropping all tables...")

        # Drop tables if they exist
        tables_to_drop = [
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

        for table in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {table};")
            print(f"🗑  Dropped table: {table}")

        conn.commit()
        conn.close()

        print("✅ Tables dropped successfully!")

    print("🚀 Recreating tables...")
    create_tables()
    print("✅ Database reset and recreated successfully!")


if __name__ == "__main__":
    reset_database()
