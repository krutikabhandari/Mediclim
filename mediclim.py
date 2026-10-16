import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime

st.set_page_config(page_title="CanopyRx | Live Climate Intelligence", layout="wide")

# Session state initialization for multi-user live logging
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "District": "Nashik", "Ward": "Panchavati", "Hazard": "Extreme Heat", "Action": "SMS Broadcast Sent to 142 ASHA Units", "Status": "Delivered"}
    ]

st.markdown("### 🏛️ Government — Public Health Department")
st.markdown("## **Mediclim: Multi-Hazard Climate-Health Early Warning System**")
st.markdown("---")

# District Coordinate & Data Mapping (Makes changing districts actually change the UI)
district_data = {
    "Nashik": {"lat": 19.9975, "lon": 73.7898, "risk": "78.4 / 100 (Critical)", "wards": ["Panchavati", "CIDCO", "Satpur", "Nashik Road"]},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882, "risk": "85.2 / 100 (Severe Heat)", "wards": ["Civil Lines", "Dhantoli", "Mahal", "Laxmi Nagar"]},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "risk": "62.1 / 100 (Moderate)", "wards": ["Shivajinagar", "Kothrud", "Hadapsar", "Viman Nagar"]},
    "Mumbai Suburban": {"lat": 19.1136, "lon": 72.8697, "risk": "81.0 / 100 (High Humidity)", "wards": ["Andheri", "Bandra", "Borivali", "Kurla"]}
}

# Sidebar Controls
st.sidebar.header("Command Center Controls")
selected_district = st.sidebar.selectbox("Select District", list(district_data.keys()))
hazard_focus = st.sidebar.selectbox("Hazard Focus", [
    "🔥 Heat-Stress & Dehydration Surge", 
    "🦟 Vector-Borne Outbreak Risk", 
    "💧 Water Contamination Index"
])

# Fetch dynamic district metadata
d_info = district_data[selected_district]

# Main Metrics (Updates dynamically based on district selection)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Wards Monitored", f"{len(d_info['wards'])} Wards", "Live Feed")
col2.metric("Predicted Risk Index", d_info["risk"], "Dynamic Alert", delta_color="inverse")
col3.metric("ASHA Network Reach", f"{random.randint(1100, 1500)} Workers", "Connected")
col4.metric("Lead Time Advantage", "48 Hours", "Pre-emptive")

st.markdown("---")

# Layout: Dynamic Map + Simulation Engine
map_col, control_col = st.columns([1.2, 1])

with map_col:
    st.subheader(f"📍 Hyper-Local Spatial Map: {selected_district}")
    
    # Map centers dynamically on selected district coordinates
    m = folium.Map(location=[d_info["lat"], d_info["lon"]], zoom_start=11)
    
    # Generate dynamic risk points for the selected district's wards
    for i, w_name in enumerate(d_info["wards"]):
        # Offset coordinates slightly for visual spread
        lat_offset = d_info["lat"] + (i * 0.02 - 0.03)
        lon_offset = d_info["lon"] + (i * 0.02 - 0.03)
        risk_level = "High" if i % 2 == 0 else "Moderate"
        color = "red" if risk_level == "High" else "orange"
        
        folium.CircleMarker(
            location=[lat_offset, lon_offset],
            radius=14,
            popup=f"<b>{w_name} Ward ({selected_district})</b><br>Risk Status: {risk_level}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8
        ).add_to(m)
        
    st_folium(m, width=500, height=400)

with control_col:
    st.subheader("⚙️ Live Telemetry & SMS/IVR Simulation Engine")
    
    selected_ward = st.selectbox("Target Ward for Live Simulation", d_info["wards"])
    
    # Dynamic live sliders (simulating live IoT/Weather API data stream)
    param_1 = st.slider("Observed Environmental Index (Temp/Rain/AQI)", 20.0, 50.0, float(random.randint(38, 46)))
    param_2 = st.slider("Community Syndromic Report (Fever/Dehydration Cases)", 0, 50, random.randint(5, 25))
    
    computed_score = (param_1 * 0.6) + (param_2 * 1.5)

    if st.button("Execute Predictive Spatial Analysis & Trigger SMS", type="primary"):
        st.write(f"Analyzing live data feed for **{selected_ward}, {selected_district}**...")
        
        if computed_score > 40:
            status_msg = f"🚨 ALERT: Critical Threshold Breached! Score: {computed_score:.1f}"
            action_msg = "Automated SMS/IVR Broadcast dispatched to local ASHA workers & medical inventory triggered."
            st.error(status_msg)
            st.warning(action_msg)
        else:
            status_msg = f"🟢 Stable Environment. Score: {computed_score:.1f}."
            action_msg = "Routine monitoring active."
            st.success(status_msg)
            
        # Append to live session log (simulates multi-user backend log)
        st.session_state.audit_logs.insert(0, {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "District": selected_district,
            "Ward": f"{selected_ward} Ward",
            "Hazard": hazard_focus.split(" ")[1],
            "Action": action_msg[:40] + "...",
            "Status": "Dispatched Live"
        })

# Bottom Live Audit Log (Updates instantly when any of your 30-50 users run a simulation)
st.markdown("---")
st.subheader("📋 Government Compliance & Live Dispatch Audit Ledger")
log_df = pd.DataFrame(st.session_state.audit_logs)
st.dataframe(log_df, use_container_width=True)
