from fetch.live.fetch_live_stocks import fetch_and_store_live_stocks
from fetch.live.fetch_live_indexes import fetch_and_store_live_indexes
from fetch.live.fetch_live_sectors import fetch_and_store_live_sectors
import pandas as pd

pd.set_option('display.max_columns', None)

print("\n🚀 Running Live Data Fetch Tests...\n")

print("📡 Fetching live stock data...")
fetch_and_store_live_stocks()

print("\n📡 Fetching live index data...")
fetch_and_store_live_indexes()

print("\n📡 Fetching live sector data...")
fetch_and_store_live_sectors()

print("\n✅ Live Data Fetch Test Completed! Review the results above.")
