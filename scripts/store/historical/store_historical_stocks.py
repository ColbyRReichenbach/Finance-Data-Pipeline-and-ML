import sqlite3
import pandas as pd
from config.db_utils import get_db_connection

def store_historical_stock_data(df):
    """Stores cleaned historical stock data into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    df.to_sql("historical_stocks", conn, if_exists="append", index=False)

    print(f"✅ Stored {len(df)} rows of historical stock data.")
    conn.close()
