import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="NYC Taxi Analytics",
    page_icon="🚕",
    layout="wide"
)

# ── Load Data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    hourly = pd.read_csv("data/hourly_demand.csv")
    fare = pd.read_csv("data/avg_fare_by_day.csv")
    sample = pd.read_csv("data/sample_data.csv")
    return hourly, fare, sample

hourly, fare, sample = load_data()

# ── Header ────────────────────────────────────────────────────────────
st.title("🚕 NYC Yellow Taxi Analytics Dashboard")
st.markdown("**Data:** January 2024 | **Pipeline:** PySpark 3.4.3 | **Records Processed:** 2.7M+")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Trips", "2,721,041")
col2.metric("Avg Weekday Fare", "$18.61")
col3.metric("Avg Weekend Fare", "$17.84")
col4.metric("Peak Hour", "6 PM")

st.divider()

# ── Row 1: Hourly Demand ──────────────────────────────────────────────
st.subheader("🕐 Hourly Trip Demand")
fig_hourly = px.bar(
    hourly,
    x="pickup_hour",
    y="trip_count",
    color="trip_count",
    color_continuous_scale="Oranges",
    labels={"pickup_hour": "Hour of Day", "trip_count": "Number of Trips"},
    title="Trip Volume by Hour (January 2024)"
)
fig_hourly.update_layout(showlegend=False)
st.plotly_chart(fig_hourly, use_container_width=True)

# ── Row 2: Fare and Duration side by side ─────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("💵 Avg Fare: Weekday vs Weekend")
    fig_fare = px.bar(
        fare,
        x="day_type",
        y="avg(fare_amount)",
        color="day_type",
        color_discrete_map={"Weekday": "#f4a423", "Weekend": "#1f77b4"},
        labels={"day_type": "Day Type", "avg(fare_amount)": "Average Fare ($)"},
        title="Average Fare by Day Type"
    )
    fig_fare.update_layout(showlegend=False)
    st.plotly_chart(fig_fare, use_container_width=True)

with col2:
    st.subheader("⏱️ Avg Trip Duration: Weekday vs Weekend")
    fig_dur = px.bar(
        fare,
        x="day_type",
        y="avg(trip_duration_mins)",
        color="day_type",
        color_discrete_map={"Weekday": "#f4a423", "Weekend": "#1f77b4"},
        labels={"day_type": "Day Type", "avg(trip_duration_mins)": "Avg Duration (mins)"},
        title="Average Trip Duration by Day Type"
    )
    fig_dur.update_layout(showlegend=False)
    st.plotly_chart(fig_dur, use_container_width=True)

# ── Row 3: Fare Distribution ──────────────────────────────────────────
st.subheader("📊 Fare Amount Distribution")
fig_dist = px.histogram(
    sample,
    x="fare_amount",
    nbins=50,
    range_x=[0, 80],
    color_discrete_sequence=["#f4a423"],
    labels={"fare_amount": "Fare Amount ($)"},
    title="Distribution of Fare Amounts (1% sample = ~27,000 trips)"
)
st.plotly_chart(fig_dist, use_container_width=True)

# ── Row 4: Raw Sample Data ────────────────────────────────────────────
st.subheader("🔍 Sample Data Explorer")
st.dataframe(
    sample[["tpep_pickup_datetime", "tpep_dropoff_datetime",
            "trip_distance", "fare_amount", "pickup_hour",
            "trip_duration_mins", "day_type"]].head(100),
    use_container_width=True
)

st.divider()
st.caption("Built with PySpark + Streamlit | NYC TLC Open Data | Chinmay Agrawal")