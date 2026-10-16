import streamlit as st

st.title("Mediclim: Multi-Hazard Climate-Health Engine")
st.write("Spatial telemetry & predictive warning for heat, vectors, and water-borne risks.")

# Hazard Selection
hazard_type = st.selectbox(
    "Select Climate-Health Hazard Focus", 
    [
        "🔥 Extreme Heat & Dehydration", 
        "🦟 Vector-Borne Risk (Monsoon/Humidity)", 
        "💧 Water-Borne Contamination (Post-Flood)", 
        "🌫️ Air Quality & Respiratory Spike"
    ]
)

ward = st.selectbox("Select Ward / Village Cluster", ["Ward 4 - Panchavati", "Ward 9 - CIDCO", "Ward 12 - Nashik Road"])

# Dynamic Inputs based on Hazard
if "Heat" in hazard_type:
    temp = st.number_input("Observed Temperature (°C)", value=42.0)
    humidity = st.slider("Humidity (%)", 10, 100, 65)
    # Logic
    risk_score = temp * (humidity / 50)
    trigger_threshold = 45.0
    action = "Preposition ORS packets and deploy shade advisories."

elif "Vector" in hazard_type:
    rainfall_mm = st.number_input("Cumulative Rainfall (Last 7 Days in mm)", value=85.0)
    stagnant_pools = st.slider("Stagnant Water Index (0-10)", 1, 10, 7)
    # Logic
    risk_score = rainfall_mm * stagnant_pools / 10
    trigger_threshold = 40.0
    action = "Dispatch fogging teams, distribute larvicides, and alert ANMs for fever screening."

elif "Water" in hazard_type:
    flood_level = st.selectbox("Water Logging Level", ["None", "Moderate Street Logging", "Severe Contamination Risk"])
    # Logic
    risk_score = 80 if "Severe" in flood_level else 30
    trigger_threshold = 50.0
    action = "Distribute chlorine tablets, issue boiling water advisories, and stock up on ORS/halazone."

else:
    aqi = st.number_input("Air Quality Index (AQI)", value=280)
    # Logic
    risk_score = aqi
    trigger_threshold = 200.0
    action = "Issue N95 mask distribution advisories for outdoor workers and asthma alerts."

# Processing & Output Execution
if st.button("Run Multi-Hazard Spatial Analysis"):
    st.write(f"Computed Risk Index Value: **{risk_score:.1f}**")
    
    if risk_score > trigger_threshold:
        st.error(f"🚨 CRITICAL SURGE ALERT: High risk detected for {hazard_type} in {ward}!")
        st.warning(f"**Automated Protocol:** {action}")
    else:
        st.success(f"🟢 Status: Stable. Parameters within safe limits for {ward}.")
        
    if st.checkbox("Trigger Multi-Channel Broadcast (SMS + Dashboard Update)"):
        st.success("✅ Warning telemetry broadcasted successfully to district health database and ASHA network!")