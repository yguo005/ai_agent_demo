import redis
import json
import os
from typing import Dict, Any, Optional
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisPacer:
    """Redis-based communication backbone for agent-to-agent messaging"""
    
    def __init__(self):
        # Try to connect to Redis (local or cloud)
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            logger.info(f"Connected to Redis at {redis_url}")
        except redis.ConnectionError:
            logger.warning("Redis not available, using in-memory fallback")
            self.redis_client = None
            self._memory_store = {}
    
    def publish(self, channel: str, message: Dict[Any, Any]) -> bool:
        """Publish a message to a Redis channel"""
        try:
            message_str = json.dumps(message, default=str)
            
            if self.redis_client:
                result = self.redis_client.publish(channel, message_str)
                logger.info(f"Published to {channel}: {len(message_str)} chars")
                return result > 0
            else:
                # Fallback to in-memory store for demo purposes
                if channel not in self._memory_store:
                    self._memory_store[channel] = []
                self._memory_store[channel].append(message)
                logger.info(f"Stored in memory for {channel}: {len(message_str)} chars")
                return True
                
        except Exception as e:
            logger.error(f"Failed to publish to {channel}: {e}")
            return False
    
    def subscribe_once(self, channel: str, timeout: int = 10) -> Optional[Dict[Any, Any]]:
        """Subscribe to a channel and return the first message received"""
        try:
            if self.redis_client:
                pubsub = self.redis_client.pubsub()
                pubsub.subscribe(channel)
                
                # Skip the subscription confirmation message
                pubsub.get_message(timeout=1)
                
                # Wait for actual message
                for i in range(timeout):
                    message = pubsub.get_message(timeout=1)
                    if message and message['type'] == 'message':
                        data = json.loads(message['data'])
                        logger.info(f"Received from {channel}: {type(data)}")
                        pubsub.unsubscribe(channel)
                        return data
                    time.sleep(1)
                
                pubsub.unsubscribe(channel)
                return None
            else:
                # Fallback to in-memory store
                if channel in self._memory_store and self._memory_store[channel]:
                    message = self._memory_store[channel].pop(0)
                    logger.info(f"Retrieved from memory for {channel}")
                    return message
                return None
                
        except Exception as e:
            logger.error(f"Failed to subscribe to {channel}: {e}")
            return None
    
    def listen_continuously(self, channel: str, callback_func):
        """Listen to a channel continuously and call callback for each message"""
        try:
            if self.redis_client:
                pubsub = self.redis_client.pubsub()
                pubsub.subscribe(channel)
                logger.info(f"Listening continuously to {channel}")
                
                for message in pubsub.listen():
                    if message['type'] == 'message':
                        try:
                            data = json.loads(message['data'])
                            callback_func(data)
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")
            else:
                logger.warning("Continuous listening not available in memory mode")
                
        except Exception as e:
            logger.error(f"Failed to listen to {channel}: {e}")

# Global pacer instance
pacer = RedisPacer()

# Convenience functions
def publish_threat_raw(threat_data: Dict[Any, Any]) -> bool:
    """Publish raw threat data"""
    return pacer.publish("threat-raw", threat_data)

def publish_threat_analyzed(analysis_data: Dict[Any, Any]) -> bool:
    """Publish analyzed threat data"""
    return pacer.publish("threat-analyzed", analysis_data)

def subscribe_threat_raw(timeout: int = 10) -> Optional[Dict[Any, Any]]:
    """Subscribe to raw threat data"""
    return pacer.subscribe_once("threat-raw", timeout)

def subscribe_threat_analyzed(timeout: int = 10) -> Optional[Dict[Any, Any]]:
    """Subscribe to analyzed threat data"""
    return pacer.subscribe_once("threat-analyzed", timeout)

if __name__ == "__main__":
    # Test the pacer
    print("Testing Redis Pacer...")
    
    test_message = {"test": "Hello from pacer!", "timestamp": time.time()}
    
    if pacer.publish("test-channel", test_message):
        print("✅ Published test message")
        
        received = pacer.subscribe_once("test-channel", timeout=5)
        if received:
            print(f"✅ Received: {received}")
        else:
            print("❌ No message received")
    else:
        print("❌ Failed to publish test message")
