import redis
from typing import Optional
from ..core.config import settings

class RedisManager:
    def __init__(self):
        """Initialize Redis connection"""
        self.redis_client = redis.Redis.from_url(
            settings.REDIS_NODES.split(",")[0],  # Connect to the first available Redis node
            decode_responses=True,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB
        )

    def increment(self, key: str, amount: int = 1) -> int:
        """
        Increment a counter in Redis.
        
        Args:
            key: The Redis key to increment.
            amount: The amount to increment by.
        
        Returns:
            The new counter value.
        """
        return self.redis_client.incrby(key, amount)

    def get(self, key: str) -> Optional[int]:
        """
        Get a value from Redis.
        
        Args:
            key: The Redis key to retrieve.
        
        Returns:
            The current value of the key, or 0 if not found.
        """
        value = self.redis_client.get(key)
        return int(value) if value else 0
