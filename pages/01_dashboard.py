import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

st.title("Regional Public Finance Overview")

# 1. Performance Caching (Now with Coordinates)
@st.cache_data
def load_tax_data():
    return pd.DataFrame({
        "Region": ["DKI Jakarta", "West Java", "East Java"],
        "Lat": [-6.2088, -6.9147, -7.2504],
        "Lon": [106.8456, 107.6098, 112.7688],
        "Tax_Revenue_B": np.random.randint(500, 1500, 3),
        "Budget_Absorption": np.random.uniform(60.0, 95.0, 3)
    })

data = load_tax_data()

# 2. Bordered Containers and Columns
st.subheader("Performance Indicators")
kpi_container = st.container(border=True)

with kpi_container:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Regional Revenue", f"Rp {data['Tax_Revenue_B'].sum():,} B", "+4.2%")
    col2.metric("Average Absorption", f"{data['Budget_Absorption'].mean():.1f}%", "-1.1%")
    
# 3. Tabs for Domain Isolation
tab_map, tab_raw = st.tabs(["Geospatial Distribution", "Tax Return Aggregates"])

with tab_map:
    st.write("Interactive map showing regional revenue distribution:")
    
    # Initialize the Folium map centered on Indonesia with OpenStreetMap base
    m = folium.Map(location=[-6.9, 110.0], zoom_start=6, tiles="OpenStreetMap")
    
    # Iterate through the dataframe and add a marker for each region
    for index, row in data.iterrows():
        folium.Marker(
            location=[row["Lat"], row["Lon"]],
            popup=f"{row['Region']}\nRevenue: Rp {row['Tax_Revenue_B']} B",
            tooltip=row["Region"],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
    
    # Render the Folium map in Streamlit
    st_folium(m, width=800, height=500)
    
with tab_raw:
    # Render interactive dataframes using the updated 2026 parameter
    st.dataframe(data, width='stretch')