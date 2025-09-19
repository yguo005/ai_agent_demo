#!/usr/bin/env python3
"""
Simple Demo Script - Sequential processing of threats
Avoids the complexity of concurrent listeners
"""

import time
import logging
from agent_monitor import ThreatMonitor
from agent_analyzer import ContextAnalyzer
from agent_orchestrator import RemediationOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_sequential_demo():
    """Run demo processing threats sequentially"""
    
    print("=" * 80)
    print("🤖 INTELLIGENT INCIDENT RESPONSE AGENT - SEQUENTIAL DEMO")
    print("=" * 80)
    print()
    
    # Initialize agents
    logger.info("🚀 Initializing agents...")
    monitor = ThreatMonitor()
    analyzer = ContextAnalyzer()
    orchestrator = RemediationOrchestrator()
    
    # Demo scenarios
    scenarios = [
        {
            "name": "Critical RCE Attack",
            "source": "horizon3",
            "description": "Critical remote code execution on Finance server"
        },
        {
            "name": "Malware Detection", 
            "source": "bright_data",
            "description": "Suspicious executable on Web server"
        },
        {
            "name": "SSL Certificate Issue",
            "source": "test", 
            "description": "Expired certificate on Database server"
        }
    ]
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*20} SCENARIO {i}/{len(scenarios)}: {scenario['name']} {'='*20}")
        print(f"📋 {scenario['description']}")
        print()
        
        try:
            # Step 1: Threat Detection
            logger.info(f"🚨 Step 1: Detecting {scenario['source']} threat...")
            detection_success = monitor.detect_threat(scenario['source'])
            
            if not detection_success:
                logger.error(f"❌ Failed to detect {scenario['source']} threat")
                continue
            
            logger.info(f"✅ Threat detected successfully")
            
            # Step 2: AI Analysis
            logger.info("🧠 Step 2: Analyzing threat with AI...")
            analysis_start = time.time()
            analysis = analyzer.analyze_threat(timeout=60)  # Long timeout for AI
            analysis_time = time.time() - analysis_start
            
            if not analysis:
                logger.error("❌ Threat analysis failed")
                continue
                
            logger.info(f"✅ Analysis completed in {analysis_time:.1f}s")
            logger.info(f"   Recommended Action: {analysis.get('recommended_action', 'unknown')}")
            logger.info(f"   Urgency: {analysis.get('urgency', 'unknown')}")
            
            # Step 3: Remediation
            logger.info("⚙️ Step 3: Executing remediation...")
            remediation_start = time.time()
            remediation = orchestrator.remediate_threat(timeout=30)
            remediation_time = time.time() - remediation_start
            
            if not remediation:
                logger.error("❌ Remediation failed")
                continue
                
            logger.info(f"✅ Remediation completed in {remediation_time:.1f}s")
            logger.info(f"   Status: {remediation.get('status', 'unknown')}")
            logger.info(f"   Action Type: {remediation.get('action_type', 'unknown')}")
            
            # Store results
            result = {
                'scenario': scenario['name'],
                'source': scenario['source'],
                'analysis_time': analysis_time,
                'remediation_time': remediation_time,
                'recommended_action': analysis.get('recommended_action', 'unknown'),
                'status': remediation.get('status', 'unknown'),
                'success': True
            }
            results.append(result)
            
            print(f"✅ Scenario {i} completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Scenario {i} failed: {str(e)}")
            results.append({
                'scenario': scenario['name'],
                'source': scenario['source'], 
                'success': False,
                'error': str(e)
            })
        
        # Brief pause between scenarios
        if i < len(scenarios):
            logger.info("⏳ Preparing next scenario...")
            time.sleep(3)
    
    # Summary
    print(f"\n{'='*30} DEMO SUMMARY {'='*30}")
    successful = sum(1 for r in results if r.get('success', False))
    print(f"📊 Scenarios processed: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {len(results) - successful}")
    
    if successful > 0:
        avg_analysis_time = sum(r.get('analysis_time', 0) for r in results if r.get('success')) / successful
        avg_remediation_time = sum(r.get('remediation_time', 0) for r in results if r.get('success')) / successful
        
        print(f"⏱️ Average analysis time: {avg_analysis_time:.1f}s")
        print(f"⚙️ Average remediation time: {avg_remediation_time:.1f}s")
        
        print("\n📋 Actions taken:")
        for r in results:
            if r.get('success'):
                print(f"  • {r['scenario']}: {r.get('recommended_action', 'unknown')} → {r.get('status', 'unknown')}")
    
    print("\n🎉 Demo completed!")
    return results

if __name__ == "__main__":
    try:
        results = run_sequential_demo()
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        logger.error(f"Demo error: {e}")
