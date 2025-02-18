import os
import sys

# 🚀 Ensure Python finds 'config' and other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.get_data import get_sector_list, get_stock_metadata, get_live_data, get_live_stock_data, \
    get_historical_data
from config.db_utils import get_db_connection

# 🏗️ Page Configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 📌 Sidebar Filters
st.sidebar.header("📌 Dashboard Filters")

# 🚀 Get stock metadata
conn = get_db_connection()
stock_metadata = pd.read_sql("SELECT ticker, sector FROM stock_metadata", conn)
conn.close()

# 🔹 Select a sector (Optional)
sectors = stock_metadata["sector"].dropna().unique().tolist()
selected_sector = st.sidebar.selectbox("📌 Select a Sector (Optional)", ["All Sectors"] + sectors)

# 🔹 Determine stock list based on sector selection
if selected_sector == "All Sectors":
    stock_list = stock_metadata["ticker"].unique().tolist()
else:
    stock_list = stock_metadata[stock_metadata["sector"] == selected_sector]["ticker"].unique().tolist()

# 🔹 Select a stock
selected_stock = st.sidebar.selectbox("📌 Select a Stock", stock_list)

# 🔹 Select a Timeframe
timeframe_options = {
    "1 Day": 1,
    "5 Days": 5,
    "1 Week": 7,
    "1 Month": 30
}
selected_timeframe_label = st.sidebar.radio("📊 Choose Timeframe", list(timeframe_options.keys()))
selected_timeframe = timeframe_options[selected_timeframe_label]

# 📊 Fetch stock data based on selected timeframe
live_stocks = get_live_stock_data(selected_timeframe)

# 📌 **Stock-Specific Live Data**
stock_data = live_stocks[live_stocks["ticker"] == selected_stock].sort_values("datetime")

# 📊 **Main Panel - Stock Overview**
st.title(f"📊 {selected_stock} Performance ({selected_timeframe_label})")

col1, col2, col3 = st.columns(3)

if not stock_data.empty:
    latest_price = stock_data.iloc[-1]["close_price"]
    earliest_price = stock_data.iloc[0]["close_price"]  # First price in the dataset

    # ✅ Calculate Percent Change
    percent_change = ((latest_price - earliest_price) / earliest_price) * 100 if earliest_price else 0

    latest_volume = stock_data.iloc[-1]["volume"]

    with col1:
        st.metric("💰 Current Price", f"${latest_price:,.2f}")

    with col2:
        st.metric(f"📉 {selected_timeframe_label} Change", f"{percent_change:.2f}%", delta=percent_change)

    with col3:
        st.metric("📊 Trading Volume", f"{latest_volume:,}")
else:
    st.warning(f"No live data available for {selected_stock} in the last {selected_timeframe_label}.")

# 📈 **Stock Price Movement (Dynamic Timeframe)**
st.subheader(f"📈 Stock Price Trend ({selected_timeframe_label})")

if not stock_data.empty:
    stock_data["datetime"] = pd.to_datetime(stock_data["datetime"])

    # Adjust Y-Axis range for better visualization
    min_price, max_price = stock_data["close_price"].min(), stock_data["close_price"].max()
    price_padding = (max_price - min_price) * 0.05  # **5% padding** for better visualization

    # ✅ **Dynamically Set Tick Interval**
    price_range = max_price - min_price
    if price_range > 10:
        tick_step = 1
    elif price_range > 5:
        tick_step = 0.5
    else:
        tick_step = 0.1  # **Fine-grained resolution for small moves**

    fig_price = px.line(
        stock_data,
        x="datetime",
        y="close_price",
        labels={"datetime": "Time", "close_price": "Stock Price"},
        title=f"{selected_stock} Stock Price Trend ({selected_timeframe_label})",
        template="plotly_dark"
    )
    fig_price.update_yaxes(range=[min_price - price_padding, max_price + price_padding], dtick=tick_step)

    st.plotly_chart(fig_price, use_container_width=True)
else:
    st.warning(f"No price data available in the last {selected_timeframe_label}.")

# 📊 **Trading Volume Chart (Dynamic Timeframe)**
st.subheader(f"📊 Trading Volume ({selected_timeframe_label})")

if not stock_data.empty:
    # Adjust Y-Axis dynamically for visibility
    min_vol, max_vol = stock_data["volume"].min(), stock_data["volume"].max()
    volume_padding = (max_vol - min_vol) * 0.1  # Add padding for better scaling

    fig_volume = px.bar(
        stock_data,
        x="datetime",
        y="volume",
        labels={"datetime": "Time", "volume": "Volume"},
        title=f"{selected_stock} Trading Volume ({selected_timeframe_label})",
        template="plotly_dark"
    )
    fig_volume.update_yaxes(range=[min_vol - volume_padding, max_vol + volume_padding])

    st.plotly_chart(fig_volume, use_container_width=True)
else:
    st.warning(f"No volume data available in the last {selected_timeframe_label}.")


# 🚀 Forecasting & Anomaly Detection Panel
if view_option == "Forecast & Anomaly Detection":
    st.title("🔮 Forecasting & Anomaly Detection")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📈 Forecasted Price for {selected_stock}")
        st.write("⚠️ *Forecasting model not implemented yet.*")

    with col2:
        st.subheader("🚨 Anomaly Detection Alerts")
        st.write("⚠️ *Anomaly detection will highlight unusual market behavior.*")

# 🎯 Final Notes
st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Developed for Live Market Monitoring & Analysis**")
