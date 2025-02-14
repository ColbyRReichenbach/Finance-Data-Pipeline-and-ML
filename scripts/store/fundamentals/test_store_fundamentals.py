import sqlite3
from config.db_utils import DB_PATH

def test_store_fundamentals():
    """Tests if fundamental data is stored correctly."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM stock_fundamentals LIMIT 5;")
    rows = cursor.fetchall()

    if rows:
        print("✅ Stock fundamentals stored correctly!")
        for row in rows:
            print(row)
    else:
        print("❌ No data found in stock_fundamentals. Check your fetch & store scripts.")

    conn.close()

if __name__ == "__main__":
    test_store_fundamentals()
