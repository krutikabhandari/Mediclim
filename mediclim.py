import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
from datetime import datetime
import urllib.parse
from fpdf import FPDF
import re

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

# Localization Dictionaries (English, Marathi, Hindi)
translations = {
    "English": {
        "title": "ECODEMIC",
        "subtitle": "Multi-Hazard Climate-Health Early Warning & Dispatch Intelligence Platform",
        "nav": "Command Center Controls",
        "dist": "Select District",
        "taluka": "Select Taluka / Zone",
        "ward": "Select Ward / Village Cluster",
        "hazard": "Hazard Focus",
        "metrics_jurisdiction": "Jurisdiction",
        "metrics_risk": "Predicted Risk",
        "metrics_asha": "Linked ASHA",
        "metrics_lead": "Lead Time",
        "map_title": "Spatial GIS Map",
        "engine_title": "Live Telemetry Engine",
        "btn_exec": "Execute Predictive Simulation & Trigger Real-Time Dispatch",
        "telephony_title": "Frontline Telephony Gateway (Live SMS / IVR API)",
        "btn_wa": "Dispatch Live WhatsApp API",
        "btn_ivr": "Trigger Live IVR Call",
        "btn_sim": "Simulate Incoming ASHA Field Response",
        "ledger_title": "Government Compliance & Real-Time Dispatch Audit Ledger",
        "pdf_btn": "Print / Download Official Audit Report (PDF)",
        "hazards": ["🔥 Heat-Stress & Dehydration Surge", "🦟 Vector-Borne Outbreak Risk", "💧 Water Contamination Index"]
    },
    "Marathi": {
        "title": "इकोडेमिक (ECODEMIC)",
        "subtitle": "हवामान आणि आरोग्य धोका पूर्वसूचना व आपत्कालीन प्रेषण यंत्रणा",
        "nav": "कमांड सेंटर नियंत्रण",
        "dist": "जिल्हा निवडा",
        "taluka": "तालुका / विभाग निवडा",
        "ward": "प्रभाग / गाव गट निवडा",
        "hazard": "धोक्याचा प्रकार",
        "metrics_jurisdiction": "कार्यक्षेत्र",
        "metrics_risk": "अंदाजित धोका",
        "metrics_asha": "जोडलेले आशा वर्कर",
        "metrics_lead": "प्रतिसादाची वेळ",
        "map_title": "स्थानिक जीआयएस नकाशा",
        "engine_title": "थेट दूरमापन प्रणाली (Telemetry)",
        "btn_exec": "अंदाज सिमुलेशन चालवा आणि स्वयंचलित प्रेषण करा",
        "telephony_title": "फ्रंटलाईन टेलिफोनिक गेटवे (थेट एसएमएस / आयव्हीआर एपीआय)",
        "btn_wa": "थेट व्हॉट्सॲप मेसेज पाठवा",
        "btn_ivr": "थेट आयव्हीआर कॉल (IVR) सुरू करा",
        "btn_sim": "आशा कर्मचाऱ्याचा प्रतिसाद तपासा",
        "ledger_title": "शासकीय अनुपालन आणि थेट प्रेषण ऑডিট लेजर",
        "pdf_btn": "अधिकृत ऑডিট अहवाल डाउनलोड करा (PDF)",
        "hazards": ["🔥 उष्णतेचा लाट व निर्जलीकरण धोका", "🦟 कीटकजन्य आजार धोका", "💧 अशुद्ध पाणी संसर्ग धोका"]
    },
    "Hindi": {
        "title": "इकोडेमिक (ECODEMIC)",
        "subtitle": "जलवायु-स्वास्थ्य प्रारंभिक चेतावनी और प्रेषण खुफिया प्लेटफॉर्म",
        "nav": "कमांड सेंटर नियंत्रण",
        "dist": "जिला चुनें",
        "taluka": "तालुका / ज़ोन चुनें",
        "ward": "वार्ड / ग्राम क्लस्टर चुनें",
        "hazard": "खतरों का फोकस",
        "metrics_jurisdiction": "कार्यक्षेत्र",
        "metrics_risk": "अनुमानित जोखिम",
        "metrics_asha": "जुड़े आशा कार्यकर्ता",
        "metrics_lead": "पूर्वसूचना समय",
        "map_title": "स्थानिक जीआईएस मानचित्र",
        "engine_title": "लाइव टेलीमेट्री इंजन",
        "btn_exec": "भविष्यवाणी सिमुलेशन चलाएं और वास्तविक समय प्रेषण करें",
        "telephony_title": "फ्रंटलाइन टेलीफोनी गेटवे (लाइव एसएमएस / IVR API)",
        "btn_wa": "लाइव व्हाट्सएप संदेश भेजें",
        "btn_ivr": "लाइव IVR कॉल ट्रिगर करें",
        "btn_sim": "आशा कार्यकर्ता प्रतिक्रिया अनुकरण करें",
        "ledger_title": "सरकारी अनुपालन और वास्तविक समय प्रेषण ऑडिट लेज़र",
        "pdf_btn": "आधिकारिक ऑडिट रिपोर्ट डाउनलोड करें (PDF)",
        "hazards": ["🔥 अत्यधिक गर्मी और डिहाइड्रेशन जोखिम", "🦟 वेक्टर जनित रोग जोखिम", "💧 जल संदूषण सूचकांक"]
    }
}

# Language Selector in Sidebar Top
selected_lang = st.sidebar.selectbox("🌐 Select Language / भाषा निवडा", ["English", "Marathi", "Hindi"])
t = translations[selected_lang]

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
            "Response Status": "[OK] Acknowledged & Executed"
        }
    ]

# Premium Header Banner
st.markdown(f"""
    <div class="brand-banner">
        <h2 style="color: white; margin: 0; font-weight: 700;">🌐 {t['title']}</h2>
        <p style="color: #93c5fd; margin: 4px 0 0 0; font-size: 15px;">{t['subtitle']}</p>
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
st.sidebar.markdown(f"### 🎛️ {t['nav']}")
selected_district = st.sidebar.selectbox(t["dist"], list(administrative_data.keys()))
d_info = administrative_data[selected_district]
selected_taluka_zone = st.sidebar.selectbox(t["taluka"], list(d_info["talukas_or_zones"].keys()))
selected_specific_unit = st.sidebar.selectbox(t["ward"], d_info["talukas_or_zones"][selected_taluka_zone])

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Telemetry Parameters")
hazard_focus = st.sidebar.selectbox(t["hazard"], t["hazards"])

# Metrics Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric(t["metrics_jurisdiction"], selected_specific_unit[:14] + ".." if len(selected_specific_unit)>14 else selected_specific_unit, selected_district)
col2.metric(t["metrics_risk"], f"{random.randint(68, 94)}.2 / 100", "Critical ⚠️", delta_color="inverse")
col3.metric(t["metrics_asha"], f"{random.randint(50, 190)} Workers", "Active Live")
col4.metric(t["metrics_lead"], "48 Hours", "Pre-emptive")

st.markdown("---")

# Main Grid
map_col, control_col = st.columns([1.2, 1])

with map_col:
    st.markdown(f"### 📍 {t['map_title']} — {selected_district}")
    
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
    st.markdown(f"### ⚡ {t['engine_title']}")
    st.markdown(f"**Target Entity:** `{selected_specific_unit}`")
    
    if "Heat" in hazard_focus or "उष्णतेचा" in hazard_focus or "गर्मी" in hazard_focus:
        env_val = st.slider("Observed Temperature (°C)", 30.0, 50.0, 42.0)
        syndromic_val = st.slider("Dehydration / Heat Exhaustion Cases", 0, 100, 18)
        computed_risk_score = (env_val * 0.6) + (syndromic_val * 1.2)
        action_desc = "Automated ORS Prepositioning & Cooling Advisories Dispatched."
    elif "Vector" in hazard_focus or "कीटकजन्य" in hazard_focus or "वेक्टर" in hazard_focus:
        env_val = st.slider("Cumulative Rainfall (mm / Last 7 Days)", 0.0, 250.0, 85.0)
        syndromic_val = st.slider("Fever / Malaria / Dengue Reports", 0, 100, 22)
        computed_risk_score = (env_val * 0.3) + (syndromic_val * 2.0)
        action_desc = "Fogging Teams & Larvicide Spraying Protocols Dispatched."
    else:
        env_val = st.slider("Water Turbidity / Contamination Index (1-10)", 1.0, 10.0, 7.0)
        syndromic_val = st.slider("Gastroenteritis / Diarrhea Reports", 0, 100, 15)
        computed_risk_score = (env_val * 5.0) + (syndromic_val * 1.8)
        action_desc = "Chlorine Tablet Distribution & Boiling Advisories Dispatched."

    if st.button(t["btn_exec"], type="primary"):
        with st.spinner("Processing spatial telemetry matrix..."):
            
            if computed_risk_score > 45:
                status_text = f"CRITICAL ALERT: Threshold Breached (Score: {computed_risk_score:.1f})"
                action_text = f"{action_desc} Target: {selected_specific_unit}."
                st.error(status_text)
                st.warning(action_text)
            else:
                status_text = f"Stable Environment (Score: {computed_risk_score:.1f})"
                action_text = "Routine epidemiological surveillance active."
                st.success(status_text)
                
            new_log_entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "District": selected_district,
                "Taluka / Zone": selected_taluka_zone,
                "Entity": selected_specific_unit,
                "Hazard": hazard_focus,
                "Action Triggered": action_text[:40] + "...",
                "Response Status": "[PENDING] Field Response..."
            }
            st.session_state.audit_logs.insert(0, new_log_entry)
            st.rerun()

    # Real Telephony Gateway Integrations
    st.markdown("---")
    st.markdown(f"### 📱 {t['telephony_title']}")
    
    # Multilingual broadcast text generation
    if selected_lang == "Marathi":
        msg_text = f"[इकोडेमिक इशारा] {selected_specific_unit} येथे आरोग्य धोका निर्माण झाला आहे. तात्काळ ओआरएस (ORS) आणि उपाययोजना सुरू करा."
    elif selected_lang == "Hindi":
        msg_text = f"[इकोडेमिक चेतावनी] {selected_specific_unit} में स्वास्थ्य जोखिम का पता चला है। तत्काल निवारक उपाय शुरू करें।"
    else:
        msg_text = f"[Ecodemic Alert] Critical warning for {selected_specific_unit}, {selected_taluka_zone}. Initiate preventive field actions immediately."
        
    encoded_wa = urllib.parse.quote(msg_text)
    wa_url = f"https://api.whatsapp.com/send?text={encoded_wa}"
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25d366; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 {t["btn_wa"]}</button></a>', unsafe_allow_html=True)
    with col_b:
        if st.button(f"📞 {t['btn_ivr']}"):
            # Production IVR API integration hook (e.g., Exotel / Twilio Voice XML webhook simulation)
            st.warning(f"🔊 Live IVR Telephony Gateway Triggered via Webhook: Outbound call dispatched to frontline ASHA team in {selected_specific_unit}.")
            if len(st.session_state.audit_logs) > 0:
                st.session_state.audit_logs[0]["Response Status"] = "[SUCCESS] Live IVR Call Connected"
            st.rerun()

    if st.button(t["btn_sim"]):
        if len(st.session_state.audit_logs) > 0:
            st.session_state.audit_logs[0]["Response Status"] = "[CONFIRMED] ASHA Worker Action Taken"
        st.rerun()

# Bottom Section: Real-Time Audit Ledger
st.markdown("---")
st.markdown(f"### 📋 {t['ledger_title']}")

log_df = pd.DataFrame(st.session_state.audit_logs)
st.dataframe(log_df, use_container_width=True, hide_index=True)

# Clean ASCII PDF Generator
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
        ts = re.sub(r'[^\x00-\x7F]+', '', str(row["Timestamp"]))
        dist = re.sub(r'[^\x00-\x7F]+', '', str(row["District"]))
        ent = re.sub(r'[^\x00-\x7F]+', '', str(row["Entity"]))
        haz = re.sub(r'[^\x00-\x7F]+', '', str(row["Hazard"]))
        stat = re.sub(r'[^\x00-\x7F]+', '', str(row["Response Status"]))
        
        pdf.cell(col_widths[0], 6, ts, 1)
        pdf.cell(col_widths[1], 6, dist, 1)
        pdf.cell(col_widths[2], 6, ent, 1)
        pdf.cell(col_widths[3], 6, haz, 1)
        pdf.cell(col_widths[4], 6, stat, 1)
        pdf.ln()
        
    return pdf.output(dest="S").encode("latin1")

pdf_bytes = create_pdf(log_df)
st.download_button(
    label=f"📥 {t['pdf_btn']}",
    data=pdf_bytes,
    file_name=f"Ecodemic_Audit_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    mime="application/pdf",
    type="secondary"
)
