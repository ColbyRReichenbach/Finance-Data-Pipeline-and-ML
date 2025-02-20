# 🎯 Fetch Data Functions
import pandas as pd
from datetime import datetime, timedelta
from config.db_utils import get_db_connection


def get_live_data(table_name, group_by_col):
    """Fetch the most recent entry per sector or stock from live data tables, removing unwanted columns."""
    conn = get_db_connection()
    query = f"""
        SELECT * FROM {table_name} AS t1
        WHERE datetime = (SELECT MAX(datetime) FROM {table_name} WHERE {group_by_col} = t1.{group_by_col})
    """
    df = pd.read_sql(query, conn)
    conn.close()

    df.drop(columns=["id", "datetime"], errors="ignore", inplace=True)
    return df


# 🎯 Fetch Stock Data with Dynamic Timeframe
def get_live_stock_data(timeframe, selected_stock):
    """Fetch 15-minute interval stock data for a given stock within the selected timeframe."""
    conn = get_db_connection()

    # ✅ Ensure timeframe is an integer
    timeframe = int(timeframe)  # Convert to integer if it’s a string

    # ✅ Calculate start datetime based on timeframe
    start_time = (datetime.utcnow() - timedelta(days=timeframe)).strftime('%Y-%m-%d %H:%M:%S')

    query = f"""
        SELECT ticker, open_price, high_price, low_price, close_price, volume, datetime
        FROM live_stocks
        WHERE datetime >= '{start_time}' 
        AND ticker = '{selected_stock}'
        ORDER BY datetime ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    return df




def get_historical_data(ticker):
    """Fetch historical stock data"""
    conn = get_db_connection()
    query = f"SELECT * FROM historical_stocks WHERE ticker = '{ticker}' ORDER BY date DESC LIMIT 500"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_sector_list():
    """Fetch unique sectors"""
    conn = get_db_connection()
    query = "SELECT DISTINCT sector FROM stock_metadata"
    df = pd.read_sql(query, conn)
    conn.close()
    return df["sector"].dropna().tolist()


def get_stock_metadata():
    """Fetch stock tickers with corresponding sectors"""
    conn = get_db_connection()
    query = "SELECT ticker, sector FROM stock_metadata"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
