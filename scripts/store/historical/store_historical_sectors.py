import sqlite3
import pandas as pd
from config.db_utils import get_db_connection

def store_historical_sector_data(df):
    """Stores historical sector data into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    df.to_sql("historical_sectors", conn, if_exists="append", index=False)

    print(f"✅ Stored {len(df)} rows of historical sector data.")
    conn.close()
