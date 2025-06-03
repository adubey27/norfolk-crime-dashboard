import streamlit as st
import pandas as pd
import pydeck as pdk

df = pd.read_excel("Cleaned_Crime_Data_Norfolk.xlsx")
df["Date"] = pd.to_datetime(df["Date"])

st.set_page_config(page_title="Norfolk Crime Heatmap", layout="wide")
st.title("🌍 Norfolk Crime Heatmap")

st.sidebar.header("Filter Heatmap Data")
crime_types = st.sidebar.multiselect("Crime Types", df["Crime type"].unique(), default=df["Crime type"].unique())
date_range = st.sidebar.date_input("Date Range", [df["Date"].min(), df["Date"].max()])

filtered_df = df[
    (df["Crime type"].isin(crime_types)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
].dropna(subset=["Latitude", "Longitude"])

if not filtered_df.empty:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=filtered_df["Latitude"].mean(),
            longitude=filtered_df["Longitude"].mean(),
            zoom=10,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=filtered_df,
                get_position='[Longitude, Latitude]',
                opacity=0.9,
            )
        ],
    ))
else:
    st.warning("No data to display on heatmap.")