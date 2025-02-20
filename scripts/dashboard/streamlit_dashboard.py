import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from plotly.subplots import make_subplots

from dashboard.analytics import compute_moving_averages, compute_bollinger_bands
from get_data import get_sector_list, get_stock_metadata, get_live_stock_data
from config.db_utils import get_db_connection

# 🎯 Set Page Config
st.set_page_config(page_title="Live Finance Dashboard", layout="wide")


def fetch_and_compute_percent_change(table_name, group_by_col, timeframe_days):
    """Fetch latest live data and compute percent change for close price, volume, and high price."""
    conn = get_db_connection()

    # Get the latest available data (including high_price)
    query_latest = f"""
        SELECT {group_by_col}, close_price, volume
        FROM {table_name}
        WHERE datetime = (SELECT MAX(datetime) FROM {table_name})
    """
    df_latest = pd.read_sql(query_latest, conn)

    # Get the first available price within the selected timeframe
    start_date = (datetime.utcnow() - timedelta(days=timeframe_days)).strftime('%Y-%m-%d %H:%M:%S')
    query_historical = f"""
        SELECT {group_by_col}, close_price AS close_price_historical
        FROM {table_name}
        WHERE datetime = (
            SELECT MIN(datetime) FROM {table_name} WHERE datetime >= '{start_date}'
        )
    """
    df_historical = pd.read_sql(query_historical, conn)

    # Compute total volume traded over the selected timeframe
    query_volume = f"""
        SELECT {group_by_col}, SUM(volume) AS total_volume, MAX(high_price) AS high_price
        FROM {table_name}
        WHERE datetime >= '{start_date}'
        GROUP BY {group_by_col}
    """
    df_volume = pd.read_sql(query_volume, conn)
    conn.close()

    # Merge DataFrames
    df = pd.merge(df_latest, df_historical, on=group_by_col, how="left")
    df = pd.merge(df, df_volume, on=group_by_col, how="left")  # Add total volume & high price

    # Compute Percent Change for Close Price
    df["percent_change"] = ((df["close_price"] - df["close_price_historical"]) / df["close_price_historical"]) * 100
    df["percent_change"] = df["percent_change"].round(2)  # Round to 2 decimal places

    return df  # Now includes `high_price` (not high price change)


# 📊 Sidebar Filters
st.sidebar.header("Filter Options")
sectors = get_sector_list()
selected_sector = st.sidebar.selectbox("Select a Sector", ["All Sectors"] + sectors)

stocks = []
if selected_sector and selected_sector != "All Sectors":
    stock_metadata = get_stock_metadata()
    stocks = stock_metadata[stock_metadata["sector"] == selected_sector]["ticker"].tolist()

selected_stock = st.sidebar.selectbox("Select a Stock", ["All Stocks"] + stocks)

timeframes = {"1 Week": 7, "1 Month": 30, "3 Months": 90}
selected_timeframe = st.sidebar.selectbox("Select Timeframe", list(timeframes.keys()))

# 📌 Get Selected Timeframe in Days
days = timeframes[selected_timeframe]

# 🔹 Default View: Major Indexes & Sector Heatmap

# Index Name Mapping
INDEX_NAMES = {
    "^GSPC": "S&P 500",
    "^IXIC": "Nasdaq 100",
    "^DJI": "Dow Jones"
}
if selected_sector == "All Sectors" and selected_stock == "All Stocks":
    st.title("Market Overview")

    # 🔍 Fetch & Compute Index Percent Change
    index_data = fetch_and_compute_percent_change("live_indexes", "symbol", days)

    if not index_data.empty:
        st.subheader("Major Index Performance")

        cols = st.columns(len(index_data))  # Create 3 equal-width columns

        for i, row in index_data.iterrows():
            index_name = INDEX_NAMES.get(row["symbol"], row["symbol"])  # Get full name
            percent_change = row["percent_change"]

            # Set color based on performance
            color = "green" if percent_change > 0 else "red"

            # HTML + CSS for styling the boxes
            index_box = f"""
            <div style="
                border: 3px solid {color};
                background-color: {color};
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                width: 100%;
            ">
                {index_name} <br>
                {percent_change:+.2f}%
            </div>
            """

            # Display each index in a separate box
            cols[i].markdown(index_box, unsafe_allow_html=True)

    # 🔥 Dynamic Sector Performance Treemap (Now with Dynamic Volume!)
    st.subheader("Sector Performance Treemap")

    sector_data = fetch_and_compute_percent_change("live_sectors", "sector", days)

    if not sector_data.empty and "total_volume" in sector_data.columns:
        fig = px.treemap(
            sector_data,
            path=["sector"],  # Keep hierarchy at the sector level
            values="total_volume",  # Box size is now based on total volume in timeframe
            color="percent_change",  # Color by % Change
            color_continuous_scale="RdYlGn",
            branchvalues="remainder",
            hover_data={
                "sector": False,
                "percent_change": ":.2f",
                "total_volume": ":,.0f",  # Show dynamically summed volume
            },
            title="Box sizes are relational to volume"
        )

        # 🔥 Keep Treemap Square
        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            autosize=False,
            width=700,
            height=700
        )

        # Show the Treemap
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("❌ Volume data is missing, please check the database.")


# 🔹 Sector Selected, No Stock (Show Mini Trend Charts)
elif selected_sector != "All Sectors" and selected_stock == "All Stocks":
    import plotly.express as px
    import plotly.graph_objects as go

    # Fetch all stock-level data from live_stocks
    stock_data = fetch_and_compute_percent_change("live_stocks", "ticker", days)

    # Fetch stock metadata (for sector filtering)
    stock_metadata = get_stock_metadata()

    # Merge stock data with metadata to get sector information
    stock_data = stock_data.merge(stock_metadata, on="ticker", how="left")

    # Filter only stocks that belong to the selected sector
    sector_stocks = stock_data[stock_data["sector"] == selected_sector]

    if not sector_stocks.empty:
        st.title(f"{selected_sector} Sector Overview")

        # Compute sector-wide metrics
        avg_change = sector_stocks["percent_change"].mean()
        total_volume = sector_stocks["total_volume"].sum()
        high_price = sector_stocks["high_price"].max()

        # Assign colors based on performance
        vol_color = "green" if total_volume > sector_stocks["total_volume"].sum() else "red"
        change_color = "green" if avg_change > 0 else "red"
        high_price_color = "lightgrey"  # High price does not change, so neutral color

        # Display summary boxes
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="padding:10px; border-radius:10px; background-color:{vol_color}; color:white; text-align:center;">
                <h3>Total Volume</h3>
                <h2>{total_volume:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="padding:10px; border-radius:10px; background-color:{change_color}; color:white; text-align:center;">
                <h3>Avg % Change</h3>
                <h2>{avg_change:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="padding:10px; border-radius:10px; background-color:{high_price_color}; color:white; text-align:center;">
                <h3>High Price</h3>
                <h2>${high_price:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

        # Sector Comparison Chart
        st.subheader("📊 Compare This Sector to Others")

        # Sidebar selector for comparison metric
        comparison_metric = st.radio(
            "Select Metric to Compare",
            ["Total Volume", "Percent Change", "High Price"],
            horizontal=True
        )

        # Fetch all sector-wide data
        sector_comparison = fetch_and_compute_percent_change("live_sectors", "sector", days)

        # Select the correct metric
        if comparison_metric == "Total Volume":
            comparison_column = "total_volume"
            title = "Sector-Wide Total Volume Comparison"
        elif comparison_metric == "Percent Change":
            comparison_column = "percent_change"
            title = "Sector-Wide % Change Comparison"
        else:
            comparison_column = "high_price"
            title = "Sector-Wide High Price Comparison"

        # Create bar chart for sector-wide comparison
        fig = px.bar(
            sector_comparison,
            x="sector",
            y=comparison_column,
            color=comparison_column,
            color_continuous_scale="Blues" if comparison_metric == "High Price" else "RdYlGn",
            title=title,
            labels={comparison_column: comparison_metric},
        )
        fig.update_layout(xaxis_title="Sector", yaxis_title=comparison_metric)
        st.plotly_chart(fig, use_container_width=True)


# 🔹 Stock Selected (Show Stock Data & Technicals)
else:
    st.title(f"📊 {selected_stock} Stock Analysis")

    # ✅ Fetch Live Stock Data (15-Minute Intervals)
    stock_df = get_live_stock_data(days, selected_stock)

    import plotly.graph_objects as go
    import plotly.express as px

    # ✅ Check if stock data is available
    if stock_df is None or stock_df.empty:
        st.warning("⚠️ No stock data available for this stock.")
    else:
        # ✅ Ensure required columns exist
        required_columns = {"datetime", "open_price", "high_price", "low_price", "close_price", "volume"}
        if not required_columns.issubset(stock_df.columns):
            st.warning(f"⚠️ Missing columns in stock data: {required_columns - set(stock_df.columns)}")
        else:
            # ✅ Ensure datetime is properly recognized & remove timezone
            stock_df["datetime"] = pd.to_datetime(stock_df["datetime"]).dt.tz_localize(None)

            # ✅ Remove weekends & non-trading hours
            stock_df = stock_df[stock_df["datetime"].dt.weekday < 5]  # Remove weekends
            market_open = stock_df["datetime"].dt.time >= pd.to_datetime("09:30").time()
            market_close = stock_df["datetime"].dt.time <= pd.to_datetime("16:00").time()
            stock_df = stock_df[market_open & market_close]

            # ✅ Define start date & filter data
            start_date = datetime.utcnow() - timedelta(days=days)
            stock_df = stock_df[stock_df["datetime"] >= start_date]

            # ✅ Ensure stock_df is not empty after filtering
            if stock_df.empty:
                st.warning("⚠️ No stock data available after filtering.")
            else:
                # 📌 **Fix X-Axis for Long Timeframes**
                stock_df["date_only"] = stock_df["datetime"].dt.date  # Extract only the date
                if days <= 7:  # 1 Week or 5-Day View (Keep 15-minute intervals)
                    x_tick_vals = stock_df["datetime"]
                    x_tick_text = stock_df["datetime"].dt.strftime("%b %d, %H:%M")  # Example: Feb 19, 14:30
                else:  # 1 Month or 3 Months View (Show one label per day)
                    x_tick_data = stock_df.groupby("date_only")["datetime"].first().reset_index()
                    x_tick_vals = x_tick_data["datetime"]  # Select first datetime of each day
                    x_tick_text = x_tick_data["date_only"].astype(str)  # Format as "YYYY-MM-DD"

                # 📌 **Inline Toggle Buttons**
                col1, col2, col3 = st.columns([1, 1, 1])

                with col1:
                    show_candlestick = st.checkbox("📉 Candlestick", value=True)

                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.05)

                # ✅ Candlestick Chart (Only if toggled on)
                if show_candlestick:
                    fig.add_trace(go.Candlestick(
                        x=stock_df["datetime"],
                        open=stock_df["open_price"],
                        high=stock_df["high_price"],
                        low=stock_df["low_price"],
                        close=stock_df["close_price"],
                        name="Candlestick",
                        increasing=dict(line=dict(color="green"), fillcolor="green"),
                        decreasing=dict(line=dict(color="red"), fillcolor="red")
                    ), row=1, col=1)

                # ✅ Volume Chart (Stacked Below Price)
                fig.add_trace(go.Bar(
                    x=stock_df["datetime"],
                    y=stock_df["volume"],
                    name="Volume",
                    marker=dict(
                        color=["green" if c > o else "red" for c, o in
                               zip(stock_df["close_price"], stock_df["open_price"])]
                    ),
                    opacity=0.6
                ), row=2, col=1)

                # ✅ Update Layout to Match Desired Look & Move Range Slider Below Volume
                fig.update_layout(
                    title=f"{selected_stock} Stock Price & Volume",
                    template="plotly_dark",  # ✅ Dark mode theme
                    xaxis=dict(
                        title="",
                        type="category",
                        tickmode="array",
                        tickvals=x_tick_vals,
                        ticktext=x_tick_text,
                        tickangle=-45  # ✅ Rotate for better readability
                    ),
                    xaxis2=dict(
                        title="Time",
                        rangeslider=dict(visible=True),  # ✅ Enable range slider below volume chart
                        type="category",
                        tickmode="array",
                        tickvals=x_tick_vals,
                        ticktext=x_tick_text,
                        tickangle=-45
                    ),
                    yaxis=dict(title="Stock Price", tickmode="linear"),
                    yaxis2=dict(title="Volume", showgrid=False),
                    legend=dict(x=0, y=1),
                    height=800
                )

                # 📌 Show Combined Chart
                st.plotly_chart(fig, use_container_width=True)


st.sidebar.markdown("🚀 **Live updates every 15 minutes**")
