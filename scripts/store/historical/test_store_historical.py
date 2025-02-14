import sqlite3
import pandas as pd
from store.historical.store_historical_stocks import store_historical_stock_data
from store.historical.store_historical_indexes import store_historical_index_data
from store.historical.store_historical_sectors import store_historical_sector_data
from config.db_utils import DB_PATH

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Sample historical stock data
stock_data = pd.DataFrame({
    "ticker": ["AAPL", "MSFT"],
    "date": ["2025-02-12", "2025-02-12"],
    "open": [150.0, 300.0],
    "close": [152.0, 305.0],
    "high": [155.0, 310.0],
    "low": [149.0, 299.0],
    "volume": [1000000, 2000000]
})

# Sample historical index data
index_data = pd.DataFrame({
    "symbol": ["^GSPC", "^IXIC"],
    "date": ["2025-02-12", "2025-02-12"],
    "open": [4000.0, 14000.0],
    "close": [4050.0, 14200.0],
    "high": [4100.0, 14500.0],
    "low": [3980.0, 13800.0],
    "volume": [3000000, 4000000]
})

# Sample historical sector data
sector_data = pd.DataFrame({
    "sector": ["Technology", "Healthcare"],
    "date": ["2025-02-12", "2025-02-12"],
    "open": [500.0, 600.0],
    "close": [510.0, 620.0],
    "high": [520.0, 630.0],
    "low": [490.0, 590.0],
    "volume": [500000, 600000]
})

# Store data
store_historical_stock_data(stock_data)
store_historical_index_data(index_data)
store_historical_sector_data(sector_data)

# Verify stored data
print("\n🔍 Verifying stored historical stock data:")
cursor.execute("SELECT * FROM historical_stocks LIMIT 5")
print(cursor.fetchall())

print("\n🔍 Verifying stored historical index data:")
cursor.execute("SELECT * FROM historical_indexes LIMIT 5")
print(cursor.fetchall())

print("\n🔍 Verifying stored historical sector data:")
cursor.execute("SELECT * FROM historical_sectors LIMIT 5")
print(cursor.fetchall())

conn.close()
print("\n✅ Historical data storage test completed successfully!")
