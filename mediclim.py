import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime
import urllib.parse

# Page Configuration for Premium Government SaaS Look
st.set_page_config(
    page_title="Ecodemic | National Health Climate Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling (Inspired by Seva Civic-Tech Portals)
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f3f4f6; }
    .stMetric { background-color: #111827; padding: 18px; border-radius: 12px; border: 1px solid #1f2937; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .stSelectbox, .stSlider { background-color: #111827; border-radius: 8px; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; letter-spacing: -0.025em; }
    .brand-banner { background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); padding: 20px; border-radius: 12px; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Real-Time Dispatch Audit Ledger
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            "District": "Nashik", 
            "Taluka / Zone": "Nashik Taluka (Urban)", 
            "Entity": "Panchavati Ward", 
            "Hazard": "Extreme Heat", 
            "Action Triggered": "Automated ORS Prepositioning SMS", 
            "Status": "✅ Dispatched (142 ASHA Units)"
        }
    ]

# Premium Header Banner
st.markdown("""
    <div class="brand-banner">
        <h2 style="color: white; margin: 0; font-weight: 700;">🌐 ECODEMIC</h2>
        <p style="color: #93c5fd; margin: 5px 0 0 0; font-size: 16px;">Multi-Hazard Climate-Health Early Warning & Dispatch Intelligence Platform</p>
    </div>
""", unsafe_allow_html=True)

# Comprehensive Administrative Hierarchy (Strictly per Government Records)
administrative_data = {
    "Nashik": {
        "lat": 19.9975, "lon": 73.7898,
        "talukas_or_zones": {
            "Nashik Taluka (Urban Municipal Corporation)": ["Panchavati Ward", "Satpur Ward", "CIDCO Ward", "Nashik Road Ward", "Ambad Ward", "Dwarka Ward"],
            "Nashik Rural (Tehsil Villages)": ["Mhasrul Village Cluster", "Ozar Village Cluster", "Adgaon Village Cluster", "Makhmalabad Cluster"],
            "Trimbakeshwar Taluka": ["Trimbak Rural", "Anjaneri Cluster", "Harsh Nagar Cluster", "Prakashe Slopes"],
            "Igatpuri Taluka": ["Igatpuri Town", "Ghoti Village Cluster", "Kasarwadi Cluster", "Bhandardara Border Units"],
            "Dindori Taluka": ["Dindori Tehsil HQ", "Vani Village Cluster", "Khedgaon Cluster", "Nanegaon Cluster"],
            "Malegaon Taluka": ["Malegaon City Ward 1-10", "Camp Area", "Soygaon Cluster", "Token Village Cluster"]
        }
    },
    "Nagpur": {
        "lat": 21.1458, "lon": 79.0882,
        "talukas_or_zones": {
            "Nagpur Urban (NMC Wards)": ["Civil Lines", "Dhantoli", "Laxmi Nagar", "Mahal Zone", "Sataranjipura"],
            "Nagpur Rural Tehsil": ["Kadani Cluster", "Gumgaon Cluster", "Kelod Village Units"],
            "Katol Taluka": ["Katol Municipal Ward", "Palsi Cluster", "Metpanjra Cluster"],
            "Saoner Taluka": ["Saoner Town", "Khapa Cluster", "Dhapewada Cluster"]
        }
    },
    "Pune": {
        "lat": 18.5204, "lon": 73.8567,
        "talukas_or_zones": {
            "Pune City (PMC Wards)": ["Shivajinagar", "Kothrud", "Hadapsar", "Viman Nagar", "Aundh-Baner"],
            "Haveli Taluka": ["Wagholi Cluster", "Manjari Cluster", "Nanded Village Units"],
            "Baramati Taluka": ["Baramati City", "Malegaon Bk Cluster", "Pandare Cluster"]
        }
    },
    "Mumbai Suburban": {
        "lat": 19.1136, "lon": 72.8697,
        "talukas_or_zones": {
            "Andheri Zone (K-East/West)": ["Andheri West Ward", "Jogeshwari West", "Vile Parle East"],
            "Bandra Zone (H-East/West)": ["Bandra Reclamation", "Khar West", "Santacruz Station Zone"],
            "Borivali Zone (R-Central/North)": ["Borivali West", "Dahisar Riverbed Cluster", "Kandivali Industrial Pocket"]
        }
    }
}

# Sidebar Navigation
st.sidebar.markdown("### 🎛️ Command Center Controls")
selected_district = st.sidebar.selectbox("Select District", list(administrative_data.keys()))
d_info = administrative_data[selected_district]
selected_taluka_zone = st.sidebar.selectbox("Select Taluka / Sub-Division / Zone", list(d_info["talukas_or_zones"].keys()))
selected_specific_unit = st.sidebar.selectbox("Select Specific Ward / Village Cluster", d_info["talukas_or_zones"][selected_taluka_zone])

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Telemetry Parameters")
hazard_focus = st.sidebar.selectbox("Hazard Focus", [
    "🔥 Heat-Stress & Dehydration Surge", 
    "🦟 Vector-Borne Outbreak Risk", 
    "💧 Water Contamination Index"
])

# Premium Top Metrics Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("Selected Jurisdiction", selected_specific_unit, selected_district)
col2.metric("Predicted Risk Index", f"{random.randint(68, 94)}.2 / 100", "Critical Alert ⚠️", delta_color="inverse")
col3.metric("Linked ASHA Units", f"{random.randint(50, 190)} Workers", "Active Live Feed")
col4.metric("Pre-emptive Lead Time", "48 Hours", "Automated Protocol")

st.markdown("---")

# Main Grid Layout: Interactive GIS Map & Live Simulation Engine
map_col, control_col = st.columns([1.3, 1])

with map_col:
    st.markdown(f"### 📍 Spatial GIS Telemetry Map — {selected_district}")
    
    m = folium.Map(location=[d_info["lat"], d_info["lon"]], zoom_start=11, tiles="OpenStreetMap")
    units_in_zone = d_info["talukas_or_zones"][selected_taluka_zone]
    for i, unit_name in enumerate(units_in_zone):
        lat_offset = d_info["lat"] + ((i % 3) * 0.02 - 0.02)
        lon_offset = d_info["lon"] + ((i // 3) * 0.02 - 0.02)
        
        is_selected = (unit_name == selected_specific_unit)
        marker_color = "#ef4444" if is_selected else "#f59e0b"
        marker_radius = 16 if is_selected else 10
        
        folium.CircleMarker(
            location=[lat_offset, lon_offset],
            radius=marker_radius,
            popup=f"<b>{unit_name}</b><br>Zone: {selected_taluka_zone}<br>Status: Active Monitoring",
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.9
        ).add_to(m)
        
    st_folium(m, width=540, height=420)

with control_col:
    st.markdown("### ⚡ Live Multi-Parameter Telemetry Engine")
    st.markdown(f"**Target Entity:** `{selected_specific_unit} ({selected_taluka_zone})`")
    
    param_temp_rain = st.slider("Observed Environmental Index (Temp °C / Rainfall mm / AQI)", 25.0, 55.0, float(random.randint(41, 47)))
    syndromic_count = st.slider("Weekly Syndromic Reports (Fever / Dehydration Cases)", 0, 100, random.randint(15, 38))
    
    computed_risk_score = (param_temp_rain * 0.5) + (syndromic_count * 1.2)

    if st.button("Execute Predictive Simulation & Trigger Real-Time Dispatch", type="primary"):
        with st.spinner("Processing telemetry through spatial correlation matrix..."):
            
            if computed_risk_score > 45:
                status_text = f"🚨 CRITICAL ALERT: Threshold Breached (Score: {computed_risk_score:.1f})"
                action_text = f"Automated SMS/IVR broadcast & ORS inventory prepositioned for {selected_specific_unit}."
                st.error(status_text)
                st.warning(action_text)
            else:
                status_text = f"🟢 Stable Environment (Score: {computed_risk_score:.1f})"
                action_text = "Routine epidemiological surveillance active."
                st.success(status_text)
                
            # Instant Real-Time Ledger Update
            new_log_entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "District": selected_district,
                "Taluka / Zone": selected_taluka_zone,
                "Entity": selected_specific_unit,
                "Hazard": hazard_focus.split(" ")[1],
                "Action Triggered": action_text[:45] + "...",
                "Status": "⚡ Live Dispatched"
            }
            st.session_state.audit_logs.insert(0, new_log_entry)
            st.rerun()

    # Frontline Telephony Gateway Simulation Widget
    st.markdown("---")
    st.markdown("### 📱 Frontline Telephony Gateway (SMS / IVR)")
    msg_text = f"[Ecodemic Alert] Critical {hazard_focus.split(' ')[1]} warning for {selected_specific_unit}, {selected_taluka_zone}. Initiate preventive field action."
    encoded_msg = urllib.parse.quote(msg_text)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"[📲 Test SMS Dispatch Link](https://wa.me/?text={encoded_msg})", unsafe_allow_html=True)
    with col_b:
        if st.button("🔊 Simulate IVR Voice Call"):
            st.info("📞 Outbound IVR audio triggered: *'Attention ASHA unit, climate hazard warning active for your sector. Please initiate doorstep advisories.'*")

# Bottom Section: Real-Time Government Compliance Audit Ledger
st.markdown("---")
st.markdown("### 📋 Government Compliance & Real-Time Dispatch Audit Ledger")
st.markdown("*Every simulation executed across the active pilot network logs instantly below in real time for compliance and verification.*")

log_df = pd.DataFrame(st.session_state.audit_logs)
st.dataframe(log_df, use_container_width=True, hide_index=True)
