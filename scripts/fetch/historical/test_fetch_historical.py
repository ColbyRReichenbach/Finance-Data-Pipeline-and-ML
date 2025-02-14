from fetch.historical.fetch_historical_stocks import fetch_and_store_historical_stocks
from fetch.historical.fetch_historical_indexes import fetch_and_store_historical_indexes
from fetch.historical.fetch_historical_sectors import fetch_and_store_historical_sectors

print("\n🚀 Running Historical Data Fetch Tests...\n")

print("📡 Fetching historical stock data...")
fetch_and_store_historical_stocks()

print("\n📡 Fetching historical index data...")
fetch_and_store_historical_indexes()

print("\n📡 Fetching historical sector data...")
fetch_and_store_historical_sectors()

print("\n✅ Historical Data Fetch Test Completed! Review the results above.")
