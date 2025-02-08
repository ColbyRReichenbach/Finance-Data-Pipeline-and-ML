import sqlite3
import pandas as pd
import config

def store_historical_sectors(sector_data):
    """
    Insert historical sector data into SQLite.
    :param sector_data: Dictionary {sector: DataFrame}
    """
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    for sector, data in sector_data.items():
        print(f"🔍 Checking data for {sector}:")
        print(data.head())  # Debugging: Print first rows

        for _, row in data.iterrows():
            date = str(row["Date"])  # Convert to string
            performance_percent = float(row["Close"]) if not pd.isna(row["Close"]) else None  # Use Close as a proxy

            try:
                cursor.execute("""
                INSERT OR IGNORE INTO sectors_historical 
                (sector_name, date, performance_percent)
                VALUES (?, ?, ?)""",
                (sector, date, performance_percent))
            except Exception as e:
                print(f"❌ Error inserting row: {e}")
                print(f"Data: {sector}, {date}, {performance_percent}")

    conn.commit()
    conn.close()
    print("✅ Sector historical data stored successfully!")
