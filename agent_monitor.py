"""
Agent 1: Threat Detection Monitor
Ingests threats from various sources and publishes to the pipeline
"""

import time
import logging
from typing import Dict, Any
from pacer import publish_threat_raw
from simulated_data import HORIZON3_THREAT, BRIGHT_DATA_THREAT, TEST_THREATS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatMonitor:
    """Monitors for threats from various security tools"""
    
    def __init__(self):
        self.sources = {
            "horizon3": HORIZON3_THREAT,
            "bright_data": BRIGHT_DATA_THREAT,
            "test": TEST_THREATS[0]
        }
    
    def detect_threat(self, source: str = "horizon3") -> bool:
        """
        Simulate threat detection from a specific source
        In a real implementation, this would poll APIs or receive webhooks
        """
        try:
            if source not in self.sources:
                logger.error(f"Unknown threat source: {source}")
                return False
            
            threat_data = self.sources[source].copy()
            
            # Add detection metadata
            threat_data.update({
                "detected_at": time.time(),
                "detection_source": "ThreatMonitor",
                "pipeline_id": f"pipe-{int(time.time())}"
            })
            
            logger.info(f"🚨 THREAT DETECTED from {source}:")
            logger.info(f"   Host: {threat_data.get('host', 'unknown')}")
            logger.info(f"   Severity: {threat_data.get('severity', 'unknown')}")
            logger.info(f"   Type: {threat_data.get('vulnerability', threat_data.get('threat_type', 'unknown'))}")
            
            # Publish to the pipeline
            success = publish_threat_raw(threat_data)
            
            if success:
                logger.info(f"✅ Published threat to pipeline: {threat_data['pipeline_id']}")
            else:
                logger.error(f"❌ Failed to publish threat: {threat_data['pipeline_id']}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error detecting threat: {e}")
            return False
    
    def detect_all_sources(self) -> int:
        """Detect threats from all available sources"""
        successful = 0
        for source in self.sources.keys():
            if self.detect_threat(source):
                successful += 1
            time.sleep(1)  # Small delay between detections
        
        logger.info(f"Detected {successful}/{len(self.sources)} threats successfully")
        return successful
    
    def start_monitoring(self, interval: int = 30):
        """
        Start continuous monitoring (for production use)
        For demo purposes, we'll just detect once
        """
        logger.info(f"Starting continuous monitoring (interval: {interval}s)")
        try:
            while True:
                self.detect_all_sources()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")

# Create global monitor instance
monitor = ThreatMonitor()

def detect_threat(source: str = "horizon3") -> bool:
    """Convenience function to detect a single threat"""
    return monitor.detect_threat(source)

def detect_critical_threat() -> bool:
    """Detect the most critical threat for demo purposes"""
    return detect_threat("horizon3")

if __name__ == "__main__":
    print("=== Threat Monitor Agent Test ===")
    
    # Test detection from different sources
    for source in ["horizon3", "bright_data", "test"]:
        print(f"\nTesting {source} detection...")
        success = detect_threat(source)
        print(f"Result: {'✅ Success' if success else '❌ Failed'}")
        time.sleep(2)
    
    print("\n=== Monitor Test Complete ===")
