import yfinance as yf
import pandas as pd
import config

def fetch_historical_sectors():
    """
    Fetch historical data for sectors using ETF proxies.
    :return: Dictionary {sector_name: DataFrame}
    """
    sector_data = {}

    for sector in config.SECTOR_NAMES:  # ✅ Iterate over a list instead of .items()
        try:
            print(f"📊 Fetching data for sector: {sector}")

            # Map sector names to ETFs (Yahoo Finance does not provide sector indexes directly)
            sector_etf_map = {
                "Technology": "XLK",
                "Financial Services": "XLF",
                "Consumer Cyclical": "XLY",
                "Healthcare": "XLV",
                "Communication Services": "XLC",
                "Industrials": "XLI",
                "Consumer Defensive": "XLP",
                "Energy": "XLE",
                "Real Estate": "XLRE",
                "Basic Materials": "XLB",
                "Utilities": "XLU"
            }

            etf_symbol = sector_etf_map.get(sector)
            if not etf_symbol:
                print(f"⚠ No ETF mapping found for sector: {sector}")
                continue

            etf = yf.Ticker(etf_symbol)
            data = etf.history(period="max")  # Fetch all available data

            if data.empty:
                print(f"⚠ No data found for ETF: {etf_symbol} (sector: {sector})")
                continue

            data.reset_index(inplace=True)
            sector_data[sector] = data

        except Exception as e:
            print(f"❌ Error fetching data for sector {sector}: {e}")

    return sector_data
