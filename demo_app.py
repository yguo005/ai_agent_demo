"""
Streamlit Demo Interface for the Intelligent Incident Response Agent
Real-time visualization of the three-agent pipeline
"""

import streamlit as st
import json
import time
import threading
from datetime import datetime
import pandas as pd

# Import agents
from agent_monitor import ThreatMonitor
from agent_analyzer import ContextAnalyzer
from agent_orchestrator import RemediationOrchestrator
from pacer import pacer

# Configure page
st.set_page_config(
    page_title="AI Incident Response Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'pipeline_history' not in st.session_state:
    st.session_state.pipeline_history = []
if 'current_pipeline' not in st.session_state:
    st.session_state.current_pipeline = None

def initialize_agents():
    """Initialize all agents"""
    if 'monitor' not in st.session_state:
        st.session_state.monitor = ThreatMonitor()
        st.session_state.analyzer = ContextAnalyzer()
        st.session_state.orchestrator = RemediationOrchestrator()

def format_json_display(data, title="Data"):
    """Format JSON data for nice display"""
    if data:
        with st.expander(f"📋 {title}", expanded=True):
            st.json(data)
    else:
        st.info(f"⏳ Waiting for {title.lower()}...")

def run_pipeline_step(source="horizon3"):
    """Execute the pipeline step by step with real-time updates"""
    
    # Create placeholders for each step
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🚨 1. Threat Detection")
        threat_placeholder = st.empty()
        
    with col2:
        st.subheader("🧠 2. AI Analysis")
        analysis_placeholder = st.empty()
        
    with col3:
        st.subheader("⚙️ 3. Remediation")
        remediation_placeholder = st.empty()
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Threat Detection
        status_text.text("🚨 Detecting threat...")
        progress_bar.progress(10)
        
        # Step 1: Threat Detection - Store the threat data for display
        threat_data = None
        if st.session_state.monitor.detect_threat(source):
            # Get the last detected threat for display (without consuming from queue)
            from simulated_data import HORIZON3_THREAT, BRIGHT_DATA_THREAT, TEST_THREATS
            threat_sources = {
                "horizon3": HORIZON3_THREAT,
                "bright_data": BRIGHT_DATA_THREAT,
                "test": TEST_THREATS[0]
            }
            threat_data = threat_sources.get(source, HORIZON3_THREAT).copy()
            
            with threat_placeholder.container():
                st.success("✅ Threat Detected!")
                st.json(threat_data)
            
            progress_bar.progress(33)
            status_text.text("🧠 Analyzing threat with AI...")
            
            # Step 2: AI Analysis - Let analyzer get data from queue
            analysis_data = st.session_state.analyzer.analyze_threat(timeout=30)
            
            if analysis_data:
                with analysis_placeholder.container():
                    st.success("✅ Analysis Complete!")
                    
                    # Show key insights
                    st.metric("Recommended Action", analysis_data.get('recommended_action', 'Unknown'))
                    st.metric("Urgency", analysis_data.get('urgency', 'Unknown'))
                    
                    # Show full analysis
                    with st.expander("📊 Full Analysis", expanded=False):
                        st.json(analysis_data)
                
                progress_bar.progress(66)
                status_text.text("⚙️ Executing remediation...")
                
                # Step 3: Remediation
                remediation_data = st.session_state.orchestrator.remediate_threat(timeout=30)
                
                if remediation_data:
                    with remediation_placeholder.container():
                        st.success("✅ Remediation Complete!")
                        
                        # Show action summary
                        st.metric("Action Status", remediation_data.get('status', 'Unknown'))
                        st.metric("Action Type", remediation_data.get('action_type', 'Unknown'))
                        
                        # Show details
                        if 'details' in remediation_data:
                            st.write("**Actions Taken:**")
                            for detail in remediation_data['details']:
                                st.write(f"• {detail}")
                        
                        # Show next steps
                        if 'next_steps' in remediation_data:
                            with st.expander("📋 Next Steps", expanded=True):
                                for step in remediation_data['next_steps']:
                                    st.write(f"• {step}")
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Pipeline execution completed successfully!")
                    
                    # Add to history
                    pipeline_result = {
                        'timestamp': datetime.now().isoformat(),
                        'source': source,
                        'threat': threat_data,
                        'analysis': analysis_data,
                        'remediation': remediation_data
                    }
                    st.session_state.pipeline_history.append(pipeline_result)
                    
                    return True
                else:
                    remediation_placeholder.error("❌ Remediation failed")
            else:
                analysis_placeholder.error("❌ Analysis failed")
        else:
            threat_placeholder.error("❌ Threat detection failed")
            
    except Exception as e:
        st.error(f"Pipeline error: {str(e)}")
        
    progress_bar.progress(0)
    status_text.text("❌ Pipeline execution failed")
    return False

def main():
    """Main Streamlit app"""
    
    # Initialize agents
    initialize_agents()
    
    # Header
    st.title("🤖 Intelligent Incident Response Agent")
    st.markdown("**AI-Powered Cybersecurity Pipeline with Three Intelligent Agents**")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Threat source selection
        threat_source = st.selectbox(
            "Select Threat Source:",
            ["horizon3", "bright_data", "test"],
            help="Choose which simulated threat to inject"
        )
        
        # Action buttons
        if st.button("🚨 Inject Critical Threat", type="primary", use_container_width=True):
            st.session_state.current_pipeline = threat_source
        
        if st.button("🔄 Clear History", use_container_width=True):
            st.session_state.pipeline_history = []
            st.rerun()
        
        # System status
        st.header("📊 System Status")
        
        # Check Redis connection
        redis_status = "🟢 Connected" if pacer.redis_client else "🟡 Memory Mode"
        st.metric("Redis", redis_status)
        
        # Check AI services
        ai_status = "🟢 Ready" if st.session_state.analyzer.openai_client else "🟡 Fallback Mode"
        st.metric("AI Services", ai_status)
        
        # Pipeline statistics
        if st.session_state.pipeline_history:
            st.metric("Completed Pipelines", len(st.session_state.pipeline_history))
            
            # Recent actions
            recent_actions = [p['analysis']['recommended_action'] for p in st.session_state.pipeline_history[-5:]]
            action_counts = pd.Series(recent_actions).value_counts()
            
            st.write("**Recent Actions:**")
            for action, count in action_counts.items():
                st.write(f"• {action}: {count}")
    
    # Main content area
    if st.session_state.current_pipeline:
        st.header(f"🚀 Pipeline Execution: {st.session_state.current_pipeline.title()}")
        
        # Run the pipeline
        success = run_pipeline_step(st.session_state.current_pipeline)
        
        if success:
            st.balloons()
        
        # Clear current pipeline
        st.session_state.current_pipeline = None
    
    else:
        # Welcome screen
        st.header("🎯 How It Works")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🚨 Agent 1: Monitor")
            st.write("""
            - Detects threats from security tools
            - Simulates Horizon3.ai and Bright Data feeds
            - Publishes raw threat data to pipeline
            """)
        
        with col2:
            st.subheader("🧠 Agent 2: Analyzer")
            st.write("""
            - Enriches threats with business context
            - Uses AI to analyze impact and urgency
            - Recommends appropriate actions
            """)
        
        with col3:
            st.subheader("⚙️ Agent 3: Orchestrator")
            st.write("""
            - Executes remediation actions
            - Calls security APIs automatically
            - Provides detailed action reports
            """)
        
        st.info("👆 Select a threat source in the sidebar and click 'Inject Critical Threat' to start!")
    
    # Pipeline History
    if st.session_state.pipeline_history:
        st.header("📈 Pipeline History")
        
        # Show recent executions
        for i, pipeline in enumerate(reversed(st.session_state.pipeline_history[-5:]), 1):
            with st.expander(f"Pipeline {len(st.session_state.pipeline_history) - i + 1}: {pipeline['source'].title()} - {pipeline['timestamp'][:19]}", expanded=False):
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Threat:**")
                    st.write(f"• Host: {pipeline['threat'].get('host', 'Unknown')}")
                    st.write(f"• Severity: {pipeline['threat'].get('severity', 'Unknown')}")
                    st.write(f"• Type: {pipeline['threat'].get('vulnerability', pipeline['threat'].get('threat_type', 'Unknown'))}")
                
                with col2:
                    st.write("**Analysis:**")
                    st.write(f"• Action: {pipeline['analysis'].get('recommended_action', 'Unknown')}")
                    st.write(f"• Urgency: {pipeline['analysis'].get('urgency', 'Unknown')}")
                    st.write(f"• Impact: {pipeline['analysis'].get('business_impact', 'Unknown')[:50]}...")
                
                with col3:
                    st.write("**Remediation:**")
                    st.write(f"• Status: {pipeline['remediation'].get('status', 'Unknown')}")
                    st.write(f"• Type: {pipeline['remediation'].get('action_type', 'Unknown')}")
                    st.write(f"• Steps: {len(pipeline['remediation'].get('details', []))} actions")

if __name__ == "__main__":
    main()
