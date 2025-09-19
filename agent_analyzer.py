"""
Agent 2: Context Analysis Agent
Enriches raw threat data with business context using AI and knowledge base
"""

import os
import time
import logging
from typing import Dict, Any, Optional
import json

# AI and Knowledge Base imports
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.openai import OpenAIEmbedding
import anthropic

# Pacer imports
from pacer import subscribe_threat_raw, publish_threat_analyzed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextAnalyzer:
    """Analyzes threats and enriches them with business context"""
    
    def __init__(self):
        self.anthropic_client = None
        self.query_engine = None
        self.setup_ai_services()
        self.setup_knowledge_base()
    
    def setup_ai_services(self):
        """Initialize AI services (OPENAI_API_KEY)"""
        try:
            anthropic_key = os.getenv('OPENAI_API_KEY')
            openai_key = os.getenv('OPENAI_API_KEY')
            
            if anthropic_key:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
                logger.info("✅ Anthropic client initialized")
            else:
                logger.warning("⚠️ OPENAI_API_KEY not found - using fallback analysis")
            
            if openai_key:
                # Configure LlamaIndex settings
                Settings.llm = Anthropic(api_key=anthropic_key) if anthropic_key else None
                Settings.embed_model = OpenAIEmbedding(api_key=openai_key)
                logger.info("✅ LlamaIndex settings configured")
            else:
                logger.warning("⚠️ OPENAI_API_KEY not found - knowledge base disabled")
                
        except Exception as e:
            logger.error(f"Error setting up AI services: {e}")
    
    def setup_knowledge_base(self):
        """Initialize the knowledge base using LlamaIndex"""
        try:
            if os.path.exists("knowledge_base.md") and Settings.embed_model:
                # Load and index the knowledge base
                documents = SimpleDirectoryReader(
                    input_files=["knowledge_base.md"]
                ).load_data()
                
                # Create vector index
                index = VectorStoreIndex.from_documents(documents)
                self.query_engine = index.as_query_engine()
                
                logger.info("✅ Knowledge base indexed and ready")
            else:
                logger.warning("⚠️ Knowledge base not available")
                
        except Exception as e:
            logger.error(f"Error setting up knowledge base: {e}")
    
    def query_knowledge_base(self, query: str) -> str:
        """Query the knowledge base for relevant information"""
        try:
            if self.query_engine:
                response = self.query_engine.query(query)
                return str(response)
            else:
                # Fallback knowledge for demo
                fallback_knowledge = {
                    "10.1.10.55": "srv-finance-01: Critical Finance server containing PII and earnings data. Owner: Alice.",
                    "192.168.1.100": "web-server-02: Public web server. Owner: Bob. Has load balancer backup.",
                    "10.0.0.50": "db-server-01: Customer database server. Owner: Carol. High business impact."
                }
                
                for ip, info in fallback_knowledge.items():
                    if ip in query:
                        return info
                
                return "No specific information found about this asset."
                
        except Exception as e:
            logger.error(f"Error querying knowledge base: {e}")
            return "Knowledge base query failed."
    
    def analyze_with_ai(self, raw_threat: Dict[Any, Any], context_info: str) -> Dict[Any, Any]:
        """Use Anthropic AI to analyze threat with business context"""
        try:
            if not self.anthropic_client:
                return self.fallback_analysis(raw_threat)
            
            prompt = f"""You are a world-class security analyst AI. Transform this raw threat data into actionable business context.

Raw Threat Data:
{json.dumps(raw_threat, indent=2)}

Internal Knowledge Base Information:
{context_info}

Based on all this information, provide a summary in the following JSON format:
{{
  "summary": "A human-readable summary of the threat and its business impact.",
  "severity_justification": "Explain why this is high, medium, or low severity based on business context.",
  "recommended_action": "A clear, single action to take (e.g., 'isolate_host', 'patch_system', 'reset_credentials', 'monitor_closely').",
  "notification_message": "A friendly message to post in the #security-alerts Slack channel.",
  "business_impact": "Specific business impact if this threat is realized.",
  "urgency": "immediate, high, medium, or low"
}}

Respond with ONLY the JSON object, no additional text."""

            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse the AI response
            ai_response = response.content[0].text.strip()
            
            # Clean up response if needed
            if ai_response.startswith("```json"):
                ai_response = ai_response.replace("```json", "").replace("```", "").strip()
            
            analysis = json.loads(ai_response)
            logger.info("✅ AI analysis completed successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self.fallback_analysis(raw_threat)
    
    def fallback_analysis(self, raw_threat: Dict[Any, Any]) -> Dict[Any, Any]:
        """Provide basic analysis when AI is not available"""
        severity = raw_threat.get('severity', 'MEDIUM').upper()
        host = raw_threat.get('host', 'unknown')
        ip = raw_threat.get('ip_address', 'unknown')
        
        # Simple rule-based analysis
        if severity == 'CRITICAL':
            action = "isolate_host"
            urgency = "immediate"
        elif severity == 'HIGH':
            action = "patch_system"
            urgency = "high"
        else:
            action = "monitor_closely"
            urgency = "medium"
        
        return {
            "summary": f"{severity} threat detected on {host} ({ip}). Requires {urgency} attention.",
            "severity_justification": f"Classified as {severity} by detection system.",
            "recommended_action": action,
            "notification_message": f"🚨 {severity} threat on {host}. Taking action: {action}",
            "business_impact": "Potential system compromise and data breach.",
            "urgency": urgency
        }
    
    def analyze_threat(self, timeout: int = 30) -> Optional[Dict[Any, Any]]:
        """Main analysis function - listens for raw threats and analyzes them"""
        try:
            logger.info("🧠 Waiting for raw threat data...")
            
            # Subscribe to raw threat channel
            raw_threat = subscribe_threat_raw(timeout)
            
            if not raw_threat:
                logger.warning("No threat data received within timeout")
                return None
            
            logger.info(f"📥 Received threat: {raw_threat.get('pipeline_id', 'unknown')}")
            
            # Query knowledge base for context
            ip_address = raw_threat.get('ip_address', '')
            host = raw_threat.get('host', '')
            
            knowledge_query = f"What do you know about {host} or IP {ip_address}? Include business impact, owner, and criticality."
            context_info = self.query_knowledge_base(knowledge_query)
            
            logger.info("🔍 Queried knowledge base for context")
            
            # Analyze with AI
            analysis = self.analyze_with_ai(raw_threat, context_info)
            
            # Add metadata
            analysis.update({
                "original_threat": raw_threat,
                "analyzed_at": time.time(),
                "analyzer_version": "1.0",
                "pipeline_id": raw_threat.get('pipeline_id', f"pipe-{int(time.time())}")
            })
            
            # Publish analyzed threat
            success = publish_threat_analyzed(analysis)
            
            if success:
                logger.info(f"✅ Published analysis: {analysis['pipeline_id']}")
                logger.info(f"   Recommended Action: {analysis.get('recommended_action', 'unknown')}")
                logger.info(f"   Urgency: {analysis.get('urgency', 'unknown')}")
            else:
                logger.error(f"❌ Failed to publish analysis")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in threat analysis: {e}")
            return None

# Global analyzer instance
analyzer = ContextAnalyzer()

def analyze_threat(timeout: int = 30) -> Optional[Dict[Any, Any]]:
    """Convenience function to analyze a single threat"""
    return analyzer.analyze_threat(timeout)

if __name__ == "__main__":
    print("=== Context Analyzer Agent Test ===")
    
    # Test knowledge base
    test_query = "What do you know about IP 10.1.10.55?"
    context = analyzer.query_knowledge_base(test_query)
    print(f"Knowledge Base Test: {context}")
    
    # Test analysis (will wait for threat data)
    print("\nWaiting for threat data to analyze...")
    analysis = analyze_threat(timeout=10)
    
    if analysis:
        print("✅ Analysis completed:")
        print(f"   Action: {analysis.get('recommended_action')}")
        print(f"   Summary: {analysis.get('summary')}")
    else:
        print("❌ No analysis performed (no threat data received)")
    
    print("\n=== Analyzer Test Complete ===")
