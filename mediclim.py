import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Page Config for Professional Enterprise Look
st.set_page_config(page_title="CanopyRx | Govt. Health & Climate Intelligence", layout="wide")

# Government Dashboard Header Styling
st.markdown("### 🏛️ Government of Maharashtra — Public Health Department")
st.markdown("## **CanopyRx: Multi-Hazard Climate-Health Early Warning System**")
st.markdown("---")

# Sidebar - Command Center Controls
st.sidebar.header("Command Center Controls")
selected_district = st.sidebar.selectbox("Select District", ["Nashik", "Nagpur", "Pune", "Mumbai Suburban"])
hazard_focus = st.sidebar.selectbox("Hazard Focus", [
    "🔥 Heat-Stress & Dehydration Surge", 
    "🦟 Vector-Borne Outbreak Risk", 
    "💧 Water Contamination Index"
])

# Main Layout - Metrics Overview
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Wards Monitored", "42 Wards", "100% Online")
col2.metric("Predicted Risk Index", "78.4 / 100", "Critical ⚠️", delta_color="inverse")
col3.metric("ASHA Network Reach", "1,240 Workers", "Active Broadcast")
col4.metric("Lead Time Advantage", "48 Hours", "Pre-emptive")

st.markdown("---")

# Two-column Layout: Spatial Map on Left, Telemetry & Dispatch on Right
map_col, control_col = st.columns([1.2, 1])

with map_col:
    st.subheader("📍 Hyper-Local Spatial Risk Heatmap")
    
    # Create an interactive Folium map centered on Maharashtra / Nashik
    m = folium.Map(location=[19.9975, 73.7898], zoom_start=12)
    
    # Add Ward Risk Markers
    wards_data = [
        {"name": "Panchavati Ward", "lat": 20.0111, "lon": 73.7905, "risk": "High", "color": "red"},
        {"name": "CIDCO Ward", "lat": 19.9550, "lon": 73.7330, "risk": "Moderate", "color": "orange"},
        {"name": "Satpur Ward", "lat": 20.0050, "lon": 73.7250, "risk": "Safe", "color": "green"},
        {"name": "Nashik Road Ward", "lat": 19.9650, "lon": 73.8500, "risk": "High", "color": "red"}
    ]
    
    for w in wards_data:
        folium.CircleMarker(
            location=[w["lat"], w["lon"]],
            radius=12,
            popup=f"<b>{w['name']}</b><br>Risk Status: {w['risk']}",
            color=w["color"],
            fill=True,
            fill_color=w["color"],
            fill_opacity=0.7
        ).add_to(m)
        
    st_data = st_folium(m, width=500, height=400)

with control_col:
    st.subheader("⚙️ Real-Time Telemetry & Trigger Engine")
    
    selected_ward = st.selectbox("Target Ward for Simulation", [w["name"] for w in wards_data])
    
    if "Heat" in hazard_focus:
        temp_input = st.slider("Observed Surface Temperature (°C)", 35.0, 48.0, 43.5)
        humidity_input = st.slider("Relative Humidity (%)", 10, 100, 65)
        computed_score = temp_input * (humidity_input / 40)
        threshold = 70.0
    elif "Vector" in hazard_focus:
        temp_input = st.slider("Average Temp (°C)", 25.0, 40.0, 32.0)
        humidity_input = st.slider("Monsoon Moisture Index (%)", 50, 100, 85)
        computed_score = humidity_input * 0.9
        threshold = 75.0
    else:
        temp_input = st.slider("Flood/Waterlogging Severity Scale (1-10)", 1, 10, 8)
        humidity_input = st.slider("Contamination Risk Factor", 1, 10, 7)
        computed_score = temp_input * humidity_input
        threshold = 50.0

    if st.button("Execute Predictive Spatial Analysis", type="primary"):
        st.write(f"Analyzing microclimate telemetry for **{selected_ward}**...")
        
        if computed_score > threshold:
            st.error(f"🚨 ALERT: Critical Threshold Breached! Score: {computed_score:.1f}")
            st.warning("**Automated Action Protocol Dispatched:** SMS/IVR broadcast sent to local ASHA workers. Supply chain triggered for regional medical inventory prepositioning.")
        else:
            st.success(f"🟢 Stable Environment. Score: {computed_score:.1f}. No immediate surge predicted.")

# Bottom Audit Trail Log
st.markdown("---")
st.subheader("📋 Government Compliance & Dispatch Audit Log")
log_data = pd.DataFrame({
    "Timestamp": ["2026-10-16 08:30:12", "2026-10-16 06:15:00", "2026-10-15 18:40.22"],
    "Ward": ["Panchavati Ward", "Nashik Road Ward", "CIDCO Ward"],
    "Hazard Type": ["Extreme Heat", "Extreme Heat", "Vector-Borne"],
    "Action Triggered": ["Automated ORS Prepositioning SMS", "PHC Inventory Alert", "Larvicide Fogging Dispatch"],
    "Status": ["Delivered (142 ASHA units)", "Acknowledged by Medical Officer", "Completed"]
})
st.dataframe(log_data, use_container_width=True)
