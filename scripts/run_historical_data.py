import config
from fetch.fetch_historical_indexes import fetch_historical_indexes
from fetch.fetch_historical_stocks import fetch_historical_stocks
from fetch.fetch_historical_sectors import fetch_historical_sectors
from store.store_historical_indexes import store_historical_indexes
from store.store_historical_stocks import store_historical_stocks
from store.store_historical_sectors import store_historical_sectors


def main():
    print("📊 Fetching and storing historical index data...")
    index_data = fetch_historical_indexes()
    store_historical_indexes(index_data)

    print("📈 Fetching and storing historical stock data...")
    stock_data = fetch_historical_stocks()
    store_historical_stocks(stock_data)

    print("📊 Fetching and storing historical sector data...")
    sector_data = fetch_historical_sectors()
    store_historical_sectors(sector_data)

    print("✅ All historical data has been successfully stored!")


if __name__ == "__main__":
    main()
