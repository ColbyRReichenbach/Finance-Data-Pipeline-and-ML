import sqlite3
import pandas as pd
from config.db_utils import get_db_connection

def store_stock_metadata(metadata_df):
    """Stores stock metadata into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    metadata_df.to_sql("stock_metadata", conn, if_exists="replace", index=False)

    print(f"✅ Stored metadata for {len(metadata_df)} stocks.")
    conn.close()
