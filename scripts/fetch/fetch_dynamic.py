import time
from config.constants import INDEX_TICKERS, STOCK_TICKERS, SECTOR_ETFS, LIVE_INTERVAL, FUNDAMENTAL_INTERVAL
from fetch.live.fetch_live_stocks import fetch_live_stock_data
from fetch.live.fetch_live_indexes import fetch_live_index_data
from fetch.live.fetch_live_sectors import fetch_live_sector_data
from fetch.fundamentals.fetch_fundamentals import fetch_and_store_fundamentals


def fetch_dynamic():
    """Fetches all live & fundamental data at scheduled intervals."""
    while True:
        print("📡 Fetching live stock, sector, and index data...")

        # ✅ Fetch live stock data (loop through each ticker)
        live_stocks = []
        for ticker in STOCK_TICKERS:
            print(f"📡 Fetching live data for {ticker}...")
            stock_data = fetch_live_stock_data(ticker)  # ✅ Pass one ticker at a time
            if stock_data is not None:
                live_stocks.append(stock_data)

        # ✅ Fetch live index data (loop through each index symbol)
        live_indexes = []
        for index in INDEX_TICKERS:
            print(f"📡 Fetching live data for index {index}...")
            index_data = fetch_live_index_data(index)
            if index_data is not None:
                live_indexes.append(index_data)

        # ✅ Fetch live sector data (loop through each sector ETF)
        live_sectors = []
        for sector_name, etf_symbol in SECTOR_ETFS.items():
            print(f"📡 Fetching live data for sector {sector_name} ({etf_symbol})...")
            sector_data = fetch_live_sector_data(sector_name, etf_symbol)
            if sector_data is not None:
                live_sectors.append(sector_data)

        print("📊 Fetching fundamental data (if needed)...")
        fetch_and_store_fundamentals(STOCK_TICKERS, fetch_interval=FUNDAMENTAL_INTERVAL)  # Change to "weekly" or "quarterly"

        print("✅ Fetching complete. Waiting for next cycle...")
        time.sleep(LIVE_INTERVAL)  # Wait 15 minutes (900 seconds) before fetching live data again


if __name__ == "__main__":
    fetch_dynamic()
