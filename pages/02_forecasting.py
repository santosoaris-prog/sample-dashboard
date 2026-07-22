import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Revenue Forecasting Models")
st.write("Time-series projection for regional tax revenues.")

# 1. Generate extended time-series data (48 months for more rows)
@st.cache_data
def generate_forecast_data():
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=48, freq="ME")
    
    # Simulate historical actuals for the first 36 months
    actuals = np.random.normal(500, 50, 36).cumsum()
    
    # Simulate forecast for all 48 months (aligning with actuals initially)
    forecast = actuals.copy()
    
    # Project the next 12 months with an upward trend and some noise
    future_trend = forecast[-1] + np.random.normal(60, 25, 12).cumsum()
    full_forecast = np.concatenate([forecast, future_trend])
    
    # Pad the actuals with NaNs (empty values) for the future 12 months
    full_actuals = np.concatenate([actuals, np.full(12, np.nan)])

    return pd.DataFrame({
        "Date": dates,
        "Actual_Revenue": full_actuals,
        "Forecast_Revenue": full_forecast
    })

df = generate_forecast_data()

# 2. Interactive sidebar controls
st.sidebar.markdown("### Forecasting Parameters")
confidence_interval = st.sidebar.slider("Confidence Interval (%)", 70, 99, 95)

# 3. Interactive Line Chart using Plotly
st.subheader(f"Revenue Projection (CI: {confidence_interval}%)")

# Melt the dataframe to make it easier for Plotly to draw multiple lines
df_melted = df.melt(id_vars=["Date"], value_vars=["Actual_Revenue", "Forecast_Revenue"], 
                    var_name="Metric", value_name="Revenue (Billions)")

fig = px.line(
    df_melted, 
    x="Date", 
    y="Revenue (Billions)", 
    color="Metric",
    title="Historical vs Projected Revenue",
    template="plotly_white"
)

# Render the chart
st.plotly_chart(fig)

# 4. Detailed Data Table
st.subheader("Raw Projection Data")
st.write("Scroll to view all 48 months of historical and forecasted data.")

# Render the dataframe using the updated 'width' parameter for Streamlit 2026+
st.dataframe(df, width='stretch')