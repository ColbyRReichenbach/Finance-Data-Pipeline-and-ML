
import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# 🚀 Ensure Python finds 'config' and other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.db_utils import get_db_connection
from analytics import compute_moving_averages, compute_rsi, compute_macd, compute_bollinger_bands, detect_anomalies

# 🏗️ Page Configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom Styling
st.markdown("""
    <style>
        .big-font {font-size:20px !important;}
        .stMarkdown {text-align: center;}
        table { width: 100%; }
    </style>
""", unsafe_allow_html=True)


# 🎯 Fetch Data Functions
def get_live_data(table_name, group_by_col):
    """Fetch the most recent entry per sector or stock from live data tables."""
    conn = get_db_connection()
    query = f"""
        SELECT * FROM {table_name} AS t1
        WHERE datetime = (SELECT MAX(datetime) FROM {table_name} WHERE {group_by_col} = t1.{group_by_col})
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # 🔥 Remove unnecessary columns
    columns_to_remove = ["id", "datetime"]
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors="ignore")

    return df


def get_live_stock_data():
    """Fetch live stock data and join with sector information."""
    conn = get_db_connection()
    query = """
        SELECT live_stocks.*, stock_metadata.sector
        FROM live_stocks
        JOIN stock_metadata ON live_stocks.ticker = stock_metadata.ticker
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_sector_list():
    """Fetch unique sectors from stock metadata."""
    conn = get_db_connection()
    query = "SELECT DISTINCT sector FROM stock_metadata"
    df = pd.read_sql(query, conn)
    conn.close()
    return df["sector"].dropna().tolist()


def get_stock_metadata():
    """Fetch stock tickers with corresponding sectors."""
    conn = get_db_connection()
    query = "SELECT ticker, sector FROM stock_metadata"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# 📌 Sidebar Filters
st.sidebar.header("📌 Dashboard Filters")

# 🚀 Get sector and stock data
sectors = get_sector_list()
stock_metadata = get_stock_metadata()

# 🔹 Select a sector (Optional)
selected_sector = st.sidebar.selectbox(
    "📌 Select a Sector (Optional)", ["All Sectors"] + sectors, key="sector_select"
)

# 🔹 Filter stocks based on selected sector
if selected_sector == "All Sectors":
    stock_list = stock_metadata["ticker"].unique().tolist()
else:
    stock_list = stock_metadata[stock_metadata["sector"] == selected_sector]["ticker"].unique().tolist()

# 🔹 Select a stock (Only one dropdown)
selected_stock = st.sidebar.selectbox("📌 Select a Stock", stock_list, key="stock_select")

# 🔹 Choose Data View
view_option = st.sidebar.selectbox("Choose Data View", ["Live Market", "Forecast & Anomaly Detection"], key="view_option")

# 📊 **Left Panel - Sector & Stock Tables**
st.sidebar.subheader("📊 Live Sector Performance")
live_sectors = get_live_data("live_sectors", "sector")
st.sidebar.dataframe(live_sectors)

st.sidebar.subheader("📈 Live Stock Performance")
live_stocks = get_live_stock_data()

# 🔹 Show only latest data per stock
latest_stocks = live_stocks.sort_values(by="datetime", ascending=False).drop_duplicates(subset=["ticker"])
st.sidebar.dataframe(latest_stocks)

# 📈 **Main Panel - Stock Chart with Indicators**
st.title(f"📊 {selected_stock} Performance Overview")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Stock Price Movement with Indicators")

    # 🔥 Fetch Stock Data with Indicators
    stock_data = compute_moving_averages(selected_stock)
    stock_data = compute_bollinger_bands(selected_stock)
    stock_data["date"] = pd.to_datetime(stock_data["date"], utc=True)

    fig_stock = px.line(
        stock_data, x="date", y=["close_price", "Upper_Band", "Lower_Band"],
        labels={"date": "Date", "close": "Stock Price"},
        title=f"{selected_stock} Price with Moving Averages & Bollinger Bands",
        template="plotly_dark"
    )
    st.plotly_chart(fig_stock, use_container_width=True)

with col2:
    st.subheader("📊 RSI & MACD Indicators")

    rsi_data = compute_rsi(selected_stock)
    macd_data = compute_macd(selected_stock)

    if rsi_data is not None:
        fig_rsi = px.line(rsi_data, x="date", y="RSI", title="Relative Strength Index (RSI)", template="plotly_dark")
        st.plotly_chart(fig_rsi, use_container_width=True)
    else:
        st.warning(f"⚠️ No RSI data available for {selected_stock}")

    if macd_data is not None:
        fig_macd = px.line(macd_data, x="date", y=["MACD", "Signal_Line"], title="MACD Indicator", template="plotly_dark")
        st.plotly_chart(fig_macd, use_container_width=True)
    else:
        st.warning(f"⚠️ No MACD data available for {selected_stock}")

# 🚀 Forecasting & Anomaly Detection Panel
if view_option == "Forecast & Anomaly Detection":
    st.title("🔮 Forecasting & Anomaly Detection")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📈 Forecasted Price for {selected_stock}")

        # 🔥 Placeholder for ML Forecasting Data (To Be Implemented)
        # forecasted_data = get_forecasted_data(selected_stock)
        # fig_forecast = px.line(
        #     forecasted_data, x="date", y="predicted_price",
        #     title=f"{selected_stock} Price Forecast",
        #     labels={"date": "Date", "predicted_price": "Predicted Price"}
        # )
        # st.plotly_chart(fig_forecast, use_container_width=True)

        st.write("⚠️ *Forecasting model not implemented yet. This will display predicted prices.*")

    with col2:
        st.subheader("🚨 Anomaly Detection Alerts")

        anomalies = detect_anomalies(selected_stock)
        if anomalies is not None and not anomalies.empty:
            st.dataframe(anomalies[["date", "close_price", "volume", "Price_Anomaly", "Volume_Anomaly"]])
        else:
            st.write("✅ No significant anomalies detected.")

# 🎯 Final Notes
st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Developed for Live Market Monitoring & Analysis**")
