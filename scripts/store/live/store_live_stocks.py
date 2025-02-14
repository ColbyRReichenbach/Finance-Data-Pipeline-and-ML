import sqlite3
import pandas as pd
from config.db_utils import get_db_connection

def store_live_stock_data(df):
    """Stores real-time stock data into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    df.to_sql("live_stocks", conn, if_exists="append", index=False)

    print(f"✅ Stored {len(df)} rows of live stock data.")
    conn.close()
