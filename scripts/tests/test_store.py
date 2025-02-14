from store.historical.store_historical_stocks import store_historical_stock_data
from store.historical.store_historical_indexes import store_historical_index_data
from store.historical.store_historical_sectors import store_historical_sector_data
from store.live.store_live_stocks import store_live_stock_data
from store.live.store_live_indexes import store_live_index_data
from store.live.store_live_sectors import store_live_sector_data
from store.metadata.store_stock_metadata import store_stock_metadata

import pandas as pd

print("\n🚀 Running Store Data Test...\n")

# Dummy test data
df_test = pd.DataFrame({
    "ticker": ["AAPL", "MSFT"],
    "date": ["2025-02-12", "2025-02-12"],
    "open_price": [150.5, 250.1],
    "close_price": [155.2, 255.4],
    "high_price": [156.3, 256.8],
    "low_price": [149.7, 248.6],
    "volume": [50000000, 30000000]
})

print("\n📡 Testing historical stock storage...")
store_historical_stock_data(df_test)

print("\n📡 Testing historical index storage...")
store_historical_index_data(df_test)

print("\n📡 Testing historical sector storage...")
store_historical_sector_data(df_test)

print("\n📡 Testing live stock storage...")
store_live_stock_data(df_test)

print("\n📡 Testing live index storage...")
store_live_index_data(df_test)

print("\n📡 Testing live sector storage...")
store_live_sector_data(df_test)

# Metadata test
df_metadata = pd.DataFrame({
    "ticker": ["AAPL", "MSFT"],
    "company_name": ["Apple Inc.", "Microsoft Corp."],
    "industry": ["Technology", "Software"],
    "sector": ["Information Technology", "Information Technology"],
    "website": ["https://apple.com", "https://microsoft.com"],
    "fullTimeEmployees": [154000, 181000],
    "headquarters": ["Cupertino, CA, USA", "Redmond, WA, USA"]
})

print("\n📡 Testing stock metadata storage...")
store_stock_metadata(df_metadata)

print("\n✅ Store Data Test Completed! Review the database for stored values.")
