"""
Main orchestration script for the Intelligent Incident Response Agent
Coordinates all three agents in the pipeline
"""

import time
import threading
import logging
import argparse
from typing import Optional
import signal
import sys

# Import all agents
from agent_monitor import ThreatMonitor
from agent_analyzer import ContextAnalyzer  
from agent_orchestrator import RemediationOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class IncidentResponsePipeline:
    """Main pipeline coordinator for the three-agent system"""
    
    def __init__(self):
        self.monitor = ThreatMonitor()
        self.analyzer = ContextAnalyzer()
        self.orchestrator = RemediationOrchestrator()
        self.running = False
        self.threads = []
    
    def run_single_threat(self, source: str = "horizon3") -> bool:
        """Run a single threat through the entire pipeline"""
        logger.info("🚀 Starting single threat pipeline execution")
        
        try:
            # Step 1: Detect threat
            logger.info("Step 1: Detecting threat...")
            if not self.monitor.detect_threat(source):
                logger.error("❌ Threat detection failed")
                return False
            
            # Step 2: Analyze threat  
            logger.info("Step 2: Analyzing threat...")
            analysis = self.analyzer.analyze_threat(timeout=30)
            if not analysis:
                logger.error("❌ Threat analysis failed")
                return False
            
            # Step 3: Remediate threat
            logger.info("Step 3: Remediating threat...")
            remediation = self.orchestrator.remediate_threat(timeout=30)
            if not remediation:
                logger.error("❌ Threat remediation failed")
                return False
            
            logger.info("✅ Pipeline execution completed successfully!")
            logger.info(f"   Final Action: {remediation.get('action_type', 'unknown')}")
            logger.info(f"   Status: {remediation.get('status', 'unknown')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            return False
    
    def run_analyzer_listener(self):
        """Run analyzer in continuous listening mode"""
        logger.info("🧠 Starting analyzer listener...")
        while self.running:
            try:
                analysis = self.analyzer.analyze_threat(timeout=30)  # Increased timeout for AI processing
                if analysis:
                    logger.info(f"✅ Analysis completed: {analysis.get('recommended_action')}")
            except Exception as e:
                logger.error(f"Analyzer error: {e}")
            time.sleep(2)  # Reduced frequency to avoid spam
    
    def run_orchestrator_listener(self):
        """Run orchestrator in continuous listening mode"""
        logger.info("⚙️ Starting orchestrator listener...")
        while self.running:
            try:
                remediation = self.orchestrator.remediate_threat(timeout=15)  # Increased timeout
                if remediation:
                    logger.info(f"✅ Remediation completed: {remediation.get('status')}")
            except Exception as e:
                logger.error(f"Orchestrator error: {e}")
            time.sleep(2)  # Reduced frequency to avoid spam
    
    def start_continuous_mode(self):
        """Start all agents in continuous listening mode"""
        logger.info("🚀 Starting continuous pipeline mode")
        self.running = True
        
        # Start analyzer and orchestrator listeners
        analyzer_thread = threading.Thread(target=self.run_analyzer_listener, daemon=True)
        orchestrator_thread = threading.Thread(target=self.run_orchestrator_listener, daemon=True)
        
        analyzer_thread.start()
        orchestrator_thread.start()
        
        self.threads = [analyzer_thread, orchestrator_thread]
        
        logger.info("✅ All listeners started. Pipeline ready for threats.")
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
            self.stop()
    
    def stop(self):
        """Stop the pipeline"""
        logger.info("🛑 Stopping pipeline...")
        self.running = False
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=5)
        
        logger.info("✅ Pipeline stopped")
    
    def demo_mode(self):
        """Run demo with all threat sources"""
        logger.info("🎭 Starting demo mode - processing all threat sources")
        
        # Start listeners
        self.start_continuous_mode_async()
        
        # Inject threats with delays
        threat_sources = ["horizon3", "bright_data", "test"]
        
        for i, source in enumerate(threat_sources, 1):
            logger.info(f"📡 Demo {i}/{len(threat_sources)}: Injecting {source} threat")
            
            if self.monitor.detect_threat(source):
                logger.info(f"✅ {source} threat injected successfully")
            else:
                logger.error(f"❌ Failed to inject {source} threat")
            
            # Wait between injections - increased time for AI processing
            if i < len(threat_sources):
                logger.info("⏳ Waiting for pipeline to process...")
                time.sleep(45)  # Increased wait time for AI processing
        
        # Let final threat process
        logger.info("⏳ Waiting for final threat to complete...")
        time.sleep(60)  # Increased final wait time
        
        self.stop()
        logger.info("🎭 Demo mode completed")
    
    def start_continuous_mode_async(self):
        """Start continuous mode without blocking"""
        self.running = True
        
        analyzer_thread = threading.Thread(target=self.run_analyzer_listener, daemon=True)
        orchestrator_thread = threading.Thread(target=self.run_orchestrator_listener, daemon=True)
        
        analyzer_thread.start()
        orchestrator_thread.start()
        
        self.threads = [analyzer_thread, orchestrator_thread]

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    logger.info("Received interrupt signal, shutting down...")
    sys.exit(0)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Intelligent Incident Response Agent Pipeline")
    parser.add_argument(
        "--mode", 
        choices=["single", "continuous", "demo"],
        default="single",
        help="Pipeline execution mode"
    )
    parser.add_argument(
        "--source",
        choices=["horizon3", "bright_data", "test"],
        default="horizon3", 
        help="Threat source for single mode"
    )
    
    args = parser.parse_args()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create pipeline
    pipeline = IncidentResponsePipeline()
    
    try:
        if args.mode == "single":
            logger.info(f"Running single threat pipeline with source: {args.source}")
            success = pipeline.run_single_threat(args.source)
            sys.exit(0 if success else 1)
            
        elif args.mode == "continuous":
            logger.info("Running continuous pipeline mode")
            pipeline.start_continuous_mode()
            
        elif args.mode == "demo":
            logger.info("Running demo mode")
            pipeline.demo_mode()
            
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        pipeline.stop()
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 INTELLIGENT INCIDENT RESPONSE AGENT PIPELINE")
    print("=" * 60)
    print()
    
    main()
