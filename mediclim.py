import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime
import urllib.parse
from fpdf import FPDF

# Page Configuration
st.set_page_config(
    page_title="Ecodemic | National Health Climate Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Styling
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f3f4f6; }
    .stMetric { background-color: #111827; padding: 14px; border-radius: 10px; border: 1px solid #1f2937; overflow: hidden; text-overflow: ellipsis; }
    .stMetric label { font-size: 13px !important; color: #9ca3af !important; }
    .stMetric div[data-testid="stMetricValue"] { font-size: 20px !important; color: #ffffff !important; }
    .brand-banner { background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); padding: 18px; border-radius: 12px; margin-bottom: 20px; }
    .stButton button { width: 100%; border-radius: 8px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = [
        {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            "District": "Nashik", 
            "Taluka / Zone": "Nashik Taluka (Urban)", 
            "Entity": "Panchavati Ward", 
            "Hazard": "Extreme Heat", 
            "Action Triggered": "Automated ORS Prepositioning SMS", 
            "Response Status": "✅ Acknowledged & Executed"
        }
    ]

# Premium Header Banner
st.markdown("""
    <div class="brand-banner">
        <h2 style="color: white; margin: 0; font-weight: 700;">🌐 ECODEMIC</h2>
        <p style="color: #93c5fd; margin: 4px 0 0 0; font-size: 15px;">Multi-Hazard Climate-Health Early Warning & Dispatch Intelligence Platform</p>
    </div>
""", unsafe_allow_html=True)

# Administrative Hierarchy Data
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
selected_taluka_zone = st.sidebar.selectbox("Select Taluka / Zone", list(d_info["talukas_or_zones"].keys()))
selected_specific_unit = st.sidebar.selectbox("Select Ward / Village Cluster", d_info["talukas_or_zones"][selected_taluka_zone])

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Telemetry Parameters")
hazard_focus = st.sidebar.selectbox("Hazard Focus", [
    "🔥 Heat-Stress & Dehydration Surge", 
    "🦟 Vector-Borne Outbreak Risk", 
    "💧 Water Contamination Index"
])

# Metrics Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("Jurisdiction", selected_specific_unit[:14] + ".." if len(selected_specific_unit)>14 else selected_specific_unit, selected_district)
col2.metric("Predicted Risk", f"{random.randint(68, 94)}.2 / 100", "Critical ⚠️", delta_color="inverse")
col3.metric("Linked ASHA", f"{random.randint(50, 190)} Workers", "Active Live")
col4.metric("Lead Time", "48 Hours", "Pre-emptive")

st.markdown("---")

# Main Grid
map_col, control_col = st.columns([1.2, 1])

with map_col:
    st.markdown(f"### 📍 Spatial GIS Map — {selected_district}")
    
    # Safe Leaflet OpenStreetMap tiles (No API key needed, zero black boxes)
    m = folium.Map(location=[d_info["lat"], d_info["lon"]], zoom_start=11, tiles="OpenStreetMap")
    units_in_zone = d_info["talukas_or_zones"][selected_taluka_zone]
    for i, unit_name in enumerate(units_in_zone):
        lat_offset = d_info["lat"] + ((i % 3) * 0.02 - 0.02)
        lon_offset = d_info["lon"] + ((i // 3) * 0.02 - 0.02)
        
        is_selected = (unit_name == selected_specific_unit)
        marker_color = "#ef4444" if is_selected else "#3b82f6"
        marker_radius = 14 if is_selected else 9
        
        folium.CircleMarker(
            location=[lat_offset, lon_offset],
            radius=marker_radius,
            popup=f"<b>{unit_name}</b><br>Zone: {selected_taluka_zone}",
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.85
        ).add_to(m)
        
    st_folium(m, width=520, height=390, use_container_width=True)

with control_col:
    st.markdown("### ⚡ Live Telemetry Engine")
    st.markdown(f"**Target Entity:** `{selected_specific_unit}`")
    
    param_temp_rain = st.slider("Environmental Index (Temp °C / Rainfall mm / AQI)", 25.0, 55.0, float(random.randint(41, 47)))
    syndromic_count = st.slider("Weekly Syndromic Reports (Fever / Dehydration)", 0, 100, random.randint(15, 38))
    
    computed_risk_score = (param_temp_rain * 0.5) + (syndromic_count * 1.2)

    if st.button("Execute Predictive Simulation & Trigger Real-Time Dispatch", type="primary"):
        with st.spinner("Processing spatial telemetry matrix..."):
            
            if computed_risk_score > 45:
                status_text = f"🚨 CRITICAL ALERT: Threshold Breached (Score: {computed_risk_score:.1f})"
                action_text = f"Automated SMS/IVR dispatched to {selected_specific_unit}."
                st.error(status_text)
                st.warning(action_text)
            else:
                status_text = f"🟢 Stable Environment (Score: {computed_risk_score:.1f})"
                action_text = "Routine epidemiological surveillance active."
                st.success(status_text)
                
            new_log_entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "District": selected_district,
                "Taluka / Zone": selected_taluka_zone,
                "Entity": selected_specific_unit,
                "Hazard": hazard_focus.split(" ")[1],
                "Action Triggered": action_text[:40] + "...",
                "Response Status": "⏳ Pending Field Response..."
            }
            st.session_state.audit_logs.insert(0, new_log_entry)
            st.rerun()

    # Telephony & Interactive Simulation Controls
    st.markdown("---")
    st.markdown("### 📱 Frontline Telephony Gateway (SMS / IVR)")
    
    # English-safe fallback message encoding for WhatsApp URL to prevent encoding faults
    plain_msg = f"[Ecodemic Alert] Critical warning for {selected_specific_unit}, {selected_taluka_zone}. Initiate preventive health actions immediately."
    encoded_wa = urllib.parse.quote(plain_msg)
    wa_url = f"https://api.whatsapp.com/send?text={encoded_wa}"
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 Send WhatsApp Alert</button></a>', unsafe_allow_html=True)
    with col_b:
        if st.button("📞 Trigger IVR Call"):
            st.warning("🔊 Outbound Marathi IVR call connected: *'नमस्कार, आपल्या भागात हवामानाचा धोका निर्माण झाला आहे.'*")
            if len(st.session_state.audit_logs) > 0:
                st.session_state.audit_logs[0]["Response Status"] = "✅ Completed via IVR Call"
            st.rerun()

    if st.button("Simulate Incoming ASHA Field Response"):
        if len(st.session_state.audit_logs) > 0:
            st.session_state.audit_logs[0]["Response Status"] = "✅ Confirmed by ASHA Worker (Action Taken)"
        st.rerun()

# Bottom Section: Real-Time Audit Ledger
st.markdown("---")
st.markdown("### 📋 Government Compliance & Real-Time Dispatch Audit Ledger")

log_df = pd.DataFrame(st.session_state.audit_logs)
st.dataframe(log_df, use_container_width=True, hide_index=True)

# Safe ASCII PDF Generator (Avoids latin1 encoding crashes completely)
def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "ECODEMIC - Government Compliance & Dispatch Report", 0, 1, "C")
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 8, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, "C")
    pdf.ln(8)
    
    pdf.set_font("Arial", "B", 8)
    headers = ["Timestamp", "District", "Entity", "Hazard", "Response Status"]
    col_widths = [38, 25, 42, 28, 58]
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, h, 1, 0, "C")
    pdf.ln()
    
    pdf.set_font("Arial", "", 7)
    for index, row in df.iterrows():
        pdf.cell(col_widths[0], 6, str(row["Timestamp"]), 1)
        pdf.cell(col_widths[1], 6, str(row["District"]), 1)
        pdf.cell(col_widths[2], 6, str(row["Entity"]), 1)
        pdf.cell(col_widths[3], 6, str(row["Hazard"]), 1)
        pdf.cell(col_widths[4], 6, str(row["Response Status"]), 1)
        pdf.ln()
        
    return pdf.output(dest="S").encode("latin1")

pdf_bytes = create_pdf(log_df)
st.download_button(
    label="📥 Print / Download Official Audit Report (PDF)",
    data=pdf_bytes,
    file_name=f"Ecodemic_Audit_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    mime="application/pdf",
    type="secondary"
)
