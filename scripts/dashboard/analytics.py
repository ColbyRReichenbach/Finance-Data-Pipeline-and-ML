import pandas as pd
from config.db_utils import get_db_connection


def compute_moving_averages(ticker, windows=[50, 100, 200]):
    """Computes moving averages for a stock."""
    conn = get_db_connection()

    # ✅ Fetch stock price data
    query = f"SELECT datetime, close_price FROM live_stocks WHERE ticker = '{ticker}' ORDER BY datetime ASC"
    df = pd.read_sql(query, conn)
    conn.close()

    # ✅ Ensure datetime format is correct
    df["datetime"] = pd.to_datetime(df["datetime"]).dt.tz_localize(None)  # Remove timezone

    # ✅ Compute Moving Averages
    for window in windows:
        df[f"SMA_{window}"] = df["close_price"].rolling(window=window).mean()

    # ✅ Return only the necessary columns
    return df[["datetime"] + [f"SMA_{w}" for w in windows]]


def compute_rsi(ticker, window=14):
    """Computes RSI for a stock."""
    conn = get_db_connection()
    query = f"SELECT date, close_price FROM historical_stocks WHERE ticker = '{ticker}' ORDER BY date ASC"
    df = pd.read_sql(query, conn)
    conn.close()

    df["date"] = pd.to_datetime(df["date"], utc=True)  # ✅ Ensure UTC timezone

    delta = df["close_price"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df


def compute_macd(ticker, short_window=12, long_window=26, signal_window=9):
    """Computes MACD and Signal Line for a stock."""
    conn = get_db_connection()
    query = f"SELECT date, close_price FROM historical_stocks WHERE ticker = '{ticker}' ORDER BY date ASC"
    df = pd.read_sql(query, conn)
    conn.close()

    df["date"] = pd.to_datetime(df["date"], utc=True)  # ✅ Ensure UTC timezone

    df["EMA_12"] = df["close_price"].ewm(span=short_window, adjust=False).mean()
    df["EMA_26"] = df["close_price"].ewm(span=long_window, adjust=False).mean()
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["Signal_Line"] = df["MACD"].ewm(span=signal_window, adjust=False).mean()

    return df


def compute_bollinger_bands(ticker, window=20, num_std=2):
    """Computes Bollinger Bands for a stock from live data."""
    conn = get_db_connection()

    # ✅ Fetch stock data from live_stocks table
    query = f"SELECT datetime, close_price FROM live_stocks WHERE ticker = '{ticker}' ORDER BY datetime ASC"
    df = pd.read_sql(query, conn)
    conn.close()

    # ✅ Ensure datetime is in correct format
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    df.sort_values("datetime", inplace=True)

    # ✅ Compute Bollinger Bands
    df["middle_band"] = df["close_price"].rolling(window=window).mean()
    df["std_dev"] = df["close_price"].rolling(window=window).std()
    df["upper_band"] = df["middle_band"] + (df["std_dev"] * num_std)
    df["lower_band"] = df["middle_band"] - (df["std_dev"] * num_std)

    # ✅ Return `datetime` instead of `date`
    return df[["datetime", "middle_band", "upper_band", "lower_band"]]


def detect_anomalies(ticker):
    """Detects anomalies in price and volume using Z-score method."""
    df = fetch_historical_data(ticker)
    if df is None:
        return None

    # Price Anomaly Detection
    df["Price_Change"] = df["close_price"].pct_change()
    df["Price_Z_Score"] = (df["Price_Change"] - df["Price_Change"].mean()) / df["Price_Change"].std()
    df["Price_Anomaly"] = df["Price_Z_Score"].abs() > 3  # Flagging anomalies

    # Volume Anomaly Detection
    df["Volume_Z_Score"] = (df["volume"] - df["volume"].mean()) / df["volume"].std()
    df["Volume_Anomaly"] = df["Volume_Z_Score"].abs() > 3

    return df[df["Price_Anomaly"] | df["Volume_Anomaly"]]


def compute_correlation(stock_ticker, benchmark_ticker):
    """Computes correlation between a stock and its sector/index."""
    conn = get_db_connection()

    query_stock = f"SELECT date, close_price FROM historical_stocks WHERE ticker = '{stock_ticker}' ORDER BY date ASC"
    query_benchmark = f"SELECT date, close_price FROM historical_indexes WHERE symbol = '{benchmark_ticker}' ORDER BY date ASC"

    df_stock = pd.read_sql(query_stock, conn)
    df_benchmark = pd.read_sql(query_benchmark, conn)

    conn.close()

    if df_stock.empty or df_benchmark.empty:
        return None

    df = pd.merge(df_stock, df_benchmark, on="date", suffixes=("_stock", "_benchmark"))
    correlation = df["close_price_stock"].corr(df["close_price_benchmark"])

    return correlation


def prepare_forecasting_data(ticker):
    """Prepares data for ML forecasting models."""
    df = fetch_historical_data(ticker)
    if df is None:
        return None

    # Feature Engineering
    df["Returns"] = df["close_price"].pct_change()
    df["SMA_50"] = df["close_price"].rolling(50, min_periods=1).mean()
    df["SMA_200"] = df["close_price"].rolling(200, min_periods=1).mean()
    df["Volatility"] = df["Returns"].rolling(50, min_periods=1).std()

    return df


def run_all_analytics():
    """Runs all analytics for every stock in the database."""
    from config.constants import STOCK_TICKERS, INDEX_TICKERS

    for ticker in STOCK_TICKERS:
        print(f"📈 Running analytics for {ticker}...")
        compute_moving_averages(ticker)
        compute_rsi(ticker)
        compute_macd(ticker)
        compute_bollinger_bands(ticker)
        detect_anomalies(ticker)

    for index in INDEX_TICKERS:
        for stock in STOCK_TICKERS:
            correlation = compute_correlation(stock, index)
            if correlation is not None:
                print(f"🔗 Correlation of {stock} with {index}: {correlation:.2f}")

    print("✅ Analytics complete!")


if __name__ == "__main__":
    run_all_analytics()
