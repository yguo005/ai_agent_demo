import streamlit as st
import json

# --- 1. SIMULATED DATA ---
# This represents the raw data from Horizon3.ai or Bright Data
SIMULATED_THREAT = {
  "finding_id": "H3-CVE-2025-12345",
  "severity": "CRITICAL",
  "host": "srv-finance-01.yourcompany.local",
  "ip_address": "10.1.10.55",
  "vulnerability": "Critical RCE in ObsoleteApp v1.2",
}

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(layout="wide")
st.title("🤖 Intelligent Incident Response Agent Demo")

# --- 3. UI LAYOUT ---
st.write("Click the button to simulate a critical threat detection and watch the AI agents work.")

# Create placeholders for the three stages
col1, col2, col3 = st.columns(3)
with col1:
    st.header("1. Threat Detected")
    raw_threat_placeholder = st.empty()
with col2:
    st.header("2. AI Context Analysis")
    analysis_placeholder = st.empty()
with col3:
    st.header("3. Remediation Action")
    action_placeholder = st.empty()

# --- 4. DEMO BUTTON ---
if st.button("Inject Critical Vulnerability Threat!", type="primary"):
    # Display the raw threat
    raw_threat_placeholder.json(SIMULATED_THREAT)

    # Show placeholders for next steps
    analysis_placeholder.info("🧠 AI agent is analyzing the threat...")
    action_placeholder.warning("⏳ Awaiting analysis before taking action...")