import sqlite3
from store.metadata.store_stock_metadata import store_stock_metadata
from config.db_utils import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Sample metadata
metadata = {
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "industry": "Technology",
    "website": "https://www.apple.com",
    "fullTimeEmployees": 154000,
    "headquarters": "Cupertino, CA"
}

store_stock_metadata(metadata)

print("\n🔍 Verifying stored metadata:")
cursor.execute("SELECT * FROM stock_metadata LIMIT 5")
print(cursor.fetchall())

conn.close()
print("\n✅ Metadata storage test completed successfully!")
