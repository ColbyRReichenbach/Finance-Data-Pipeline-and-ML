import yfinance as yf
import pandas as pd
import config


def fetch_historical_indexes(start="2000-01-01", end="2024-01-01"):
    """
    Fetch historical data for indexes.
    :return: Dictionary {symbol: DataFrame}
    """
    index_data = {}
    for symbol in config.INDEX_SYMBOLS:
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(start=start, end=end)

            if data.empty:
                print(f"⚠ No data found for {symbol}")
                continue

            data.reset_index(inplace=True)
            data["symbol"] = symbol
            index_data[symbol] = data
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")

    return index_data
