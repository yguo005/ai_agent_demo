import streamlit as st
import json
from openai import OpenAI
from remediation_orchestrator_agent import agent_orchestrator

# Get API Key from environment variable
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ Please set your OPENAI_API_KEY environment variable")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# --- 1. SIMULATED DATA ---
# This represents the raw data from Horizon3.ai or Bright Data
SIMULATED_THREAT = {
  "finding_id": "H3-CVE-2025-12345",
  "severity": "CRITICAL",
  "host": "srv-finance-01.yourcompany.local",
  "ip_address": "10.1.10.55",
  "vulnerability": "Critical RCE in ObsoleteApp v1.2",
}

def agent_analyzer(raw_threat_json):
    """This function is our Context Analyzer Agent."""
    # We fake the LlamaIndex knowledge base lookup by hardcoding the context.
    hardcoded_knowledge = """
    - The server at IP 10.1.10.55 is 'srv-finance-01'.
    - This is a critical asset owned by the Finance department.
    - It contains employee PII and processes quarterly earnings reports.
    - The system owner is Alice.
    """

    prompt = f"""
    You are a security analyst AI. Transform this raw threat data into actionable business context.

    Raw Threat Data:
    {json.dumps(raw_threat_json, indent=2)}

    Internal Knowledge Base Information:
    {hardcoded_knowledge}

    IMPORTANT: Respond with ONLY a valid JSON object. No explanations, no markdown formatting, no code blocks. Just the raw JSON.

    Provide a JSON object with exactly these three keys:
    - "summary": a human-readable explanation of the threat and its business impact
    - "recommended_action": a short action like "isolate_host", "patch_system", or "monitor_closely"
    - "slack_message": a friendly message for the security team

    Example format:
    {{"summary": "Critical vulnerability found...", "recommended_action": "isolate_host", "slack_message": "Alert message..."}}
    """

    response = client.chat.completions.create(
        model="gpt-4o-2024-11-20", 
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    message = response.choices[0].message.content

    # Clean the response - remove any markdown formatting or extra text
    message = message.strip()
    
    # If the response is wrapped in code blocks, extract the JSON
    if message.startswith("```"):
        # Find JSON content between code blocks
        lines = message.split('\n')
        json_lines = []
        in_json = False
        for line in lines:
            if line.startswith("```") and not in_json:
                in_json = True
                continue
            elif line.startswith("```") and in_json:
                break
            elif in_json:
                json_lines.append(line)
        message = '\n'.join(json_lines).strip()
    
    # Find JSON object if there's extra text
    start = message.find('{')
    end = message.rfind('}') + 1
    if start != -1 and end > start:
        message = message[start:end]

    # Return the AI's response as a Python dictionary
    return json.loads(message)

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
    # Step 1: Display raw threat
    raw_threat_placeholder.json(SIMULATED_THREAT)
    analysis_placeholder.info("🧠 AI agent is analyzing...")
    action_placeholder.warning("⏳ Awaiting analysis...")

    try:
        # Step 2: AI Analysis
        ai_analysis = agent_analyzer(SIMULATED_THREAT)
        ai_analysis["threat_data"] = SIMULATED_THREAT  # Pass threat data to orchestrator
        analysis_placeholder.json(ai_analysis)
        action_placeholder.info("⚙️ Orchestrator is executing action...")

        # Step 3: Remediation Orchestration
        final_action = agent_orchestrator(ai_analysis)
        action_placeholder.json(final_action)
        
    except Exception as e:
        analysis_placeholder.error(f"❌ Analysis failed: {str(e)}")
        action_placeholder.error("❌ Unable to determine action due to analysis failure")