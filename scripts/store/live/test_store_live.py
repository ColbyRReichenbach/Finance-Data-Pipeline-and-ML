import sqlite3
import pandas as pd
from store.live.store_live_stocks import store_live_stock_data
from store.live.store_live_indexes import store_live_index_data
from store.live.store_live_sectors import store_live_sector_data
from config.db_utils import DB_PATH

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Sample live stock data
live_stock_data = pd.DataFrame({
    "ticker": ["AAPL", "MSFT"],
    "datetime": ["2025-02-12 10:30:00", "2025-02-12 10:30:00"],
    "open": [152.5, 305.5],
    "close": [153.0, 306.0],
    "high": [155.5, 310.5],
    "low": [150.5, 300.5],
    "volume": [500000, 700000]
})

# Sample live index data
live_index_data = pd.DataFrame({
    "symbol": ["^GSPC", "^IXIC"],
    "datetime": ["2025-02-12 10:30:00", "2025-02-12 10:30:00"],
    "open": [4020.0, 14100.0],
    "close": [4030.0, 14150.0],
    "high": [4050.0, 14200.0],
    "low": [4010.0, 14050.0],
    "volume": [3500000, 4500000]
})

# Sample live sector data
live_sector_data = pd.DataFrame({
    "sector": ["Technology", "Healthcare"],
    "datetime": ["2025-02-12 10:30:00", "2025-02-12 10:30:00"],
    "open": [510.0, 620.0],
    "close": [515.0, 625.0],
    "high": [520.0, 630.0],
    "low": [505.0, 615.0],
    "volume": [550000, 650000]
})

# Store data
store_live_stock_data(live_stock_data)
store_live_index_data(live_index_data)
store_live_sector_data(live_sector_data)

# Verify stored data
print("\n🔍 Verifying stored live stock data:")
cursor.execute("SELECT * FROM live_stocks LIMIT 5")
print(cursor.fetchall())

print("\n🔍 Verifying stored live index data:")
cursor.execute("SELECT * FROM live_indexes LIMIT 5")
print(cursor.fetchall())

print("\n🔍 Verifying stored live sector data:")
cursor.exec
