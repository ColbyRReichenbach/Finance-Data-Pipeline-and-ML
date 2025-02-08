import yfinance as yf
import pandas as pd
import config


def fetch_historical_stocks(start="2000-01-01", end="2024-01-01"):
    """
    Fetch historical data for stocks and include sector information.
    :return: Dictionary {symbol: (DataFrame, sector)}
    """
    stock_data = {}

    for symbol in config.STOCK_SYMBOLS:
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(start=start, end=end)

            if data.empty:
                print(f"⚠ No data found for {symbol}")
                continue

            data.reset_index(inplace=True)
            data["symbol"] = symbol

            # Fetch the sector dynamically from Yahoo Finance
            sector = stock.info.get("sector", "Unknown")

            stock_data[symbol] = (data, sector)
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")

    return stock_data
