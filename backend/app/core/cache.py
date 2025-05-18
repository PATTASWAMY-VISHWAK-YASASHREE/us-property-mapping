import os
import json
import logging
from typing import Any, Optional, Union

# Try to import Redis, but make it optional
redis_cache = None
try:
    import redis.asyncio as redis
    
    # Get Redis configuration from environment variables
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Create Redis client
    redis_cache = redis.from_url(REDIS_URL)
    
    logging.info(f"Redis cache initialized with URL: {REDIS_URL}")
except ImportError:
    logging.warning("Redis package not installed. Caching will be disabled.")
except Exception as e:
    logging.error(f"Failed to initialize Redis cache: {e}")

class Cache:
    """Cache utility class that works with or without Redis"""
    
    def __init__(self):
        self.local_cache = {}
        self.enabled = redis_cache is not None
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled:
            return self.local_cache.get(key)
        
        try:
            value = await redis_cache.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logging.error(f"Error getting from cache: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: int = 300) -> bool:
        """Set value in cache with expiration in seconds"""
        if not self.enabled:
            self.local_cache[key] = value
            return True
        
        try:
            serialized = json.dumps(value)
            await redis_cache.set(key, serialized, ex=expire)
            return True
        except Exception as e:
            logging.error(f"Error setting cache: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.enabled:
            if key in self.local_cache:
                del self.local_cache[key]
            return True
        
        try:
            await redis_cache.delete(key)
            return True
        except Exception as e:
            logging.error(f"Error deleting from cache: {e}")
            return False
    
    async def flush(self) -> bool:
        """Clear all cache"""
        if not self.enabled:
            self.local_cache = {}
            return True
        
        try:
            await redis_cache.flushdb()
            return True
        except Exception as e:
            logging.error(f"Error flushing cache: {e}")
            return False

# Create a cache instance
cache = Cache()