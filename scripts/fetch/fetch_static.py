from config.constants import INDEX_TICKERS, STOCK_TICKERS, SECTOR_ETFS
from fetch.historical.fetch_historical_stocks import fetch_historical_stock_data
from fetch.historical.fetch_historical_indexes import fetch_historical_index_data
from fetch.historical.fetch_historical_sectors import fetch_historical_sector_data
from fetch.metadata.fetch_stock_metadata import fetch_stock_metadata


def fetch_static():
    """Fetches all static data once"""
    print("📡 Fetching historical stock, sector, and index data...")

    # ✅ Fetch historical stocks (loop through each ticker)
    historical_stocks = []
    for ticker in STOCK_TICKERS:
        print(f"📡 Fetching historical data for {ticker}...")
        stock_data = fetch_historical_stock_data(ticker)
        if stock_data is not None:
            historical_stocks.append(stock_data)

    # ✅ Fetch historical indexes (loop through each index symbol)
    historical_indexes = []
    for index in INDEX_TICKERS:
        print(f"📡 Fetching historical data for index {index}...")
        index_data = fetch_historical_index_data(index)
        if index_data is not None:
            historical_indexes.append(index_data)

    # ✅ Fetch historical sectors (loop through each sector ETF)
    historical_sectors = []
    for sector_name, etf_symbol in SECTOR_ETFS.items():
        print(f"📡 Fetching historical data for sector {sector_name} ({etf_symbol})...")
        sector_data = fetch_historical_sector_data(sector_name, etf_symbol)
        if sector_data is not None:
            historical_sectors.append(sector_data)

    # ✅ Fetch metadata for stocks (loop through each ticker)
    metadata_stocks = []
    for ticker in STOCK_TICKERS:
        print(f"📊 Fetching metadata for {ticker}..")
        stock_data = fetch_stock_metadata(ticker)
        if stock_data is not None:
            metadata_stocks.append(stock_data)

    print("✅ Static data fetch completed successfully!")


if __name__ == "__main__":
    fetch_static()
