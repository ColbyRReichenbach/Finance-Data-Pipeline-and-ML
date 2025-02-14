import streamlit as st
import pandas as pd
import plotly.express as px
from config.db_utils import get_db_connection


# Fetch Data from DB
def fetch_live_stock_data():
    conn = get_db_connection()
    query = "SELECT * FROM live_stocks ORDER BY datetime DESC LIMIT 100"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def fetch_historical_stock_data():
    conn = get_db_connection()
    query = "SELECT * FROM historical_stocks WHERE date >= date('now', '-1 year')"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Streamlit App Layout
st.title("📈 Live Financial Dashboard")

# Dropdowns for Stock Selection
selected_stock = st.selectbox("Select Stock", ["AAPL", "MSFT", "GOOGL"])

# Live Stock Price Chart
st.subheader(f"{selected_stock} - Live Stock Prices")
df_live = fetch_live_stock_data()
df_live = df_live[df_live['ticker'] == selected_stock]

fig_live = px.line(df_live, x='datetime', y='close_price', title="Live Prices")
st.plotly_chart(fig_live)

# Historical Stock Overlay
st.subheader(f"{selected_stock} - Historical Performance")
df_hist = fetch_historical_stock_data()
df_hist = df_hist[df_hist['ticker'] == selected_stock]

fig_hist = px.line(df_hist, x='date', y='close_price', title="Historical Prices")
st.plotly_chart(fig_hist)
