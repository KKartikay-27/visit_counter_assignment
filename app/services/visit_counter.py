import time
from ..core.redis_manager import RedisManager

class VisitCounterService:
    def __init__(self):
        """Initialize the visit counter service using Redis and in-memory caching"""
        self.redis_manager = RedisManager()
        self.cache = {}  # In-memory cache: {page_id: (count, expiry_time)}

    def increment_visit(self, page_id: str) -> None:
        """
        Increment visit count for a page. Writes go directly to Redis.
        
        Args:
            page_id: Unique identifier for the page.
        """
        self.redis_manager.increment(f"visit_count:{page_id}")
        # Don't update the cache immediately to ensure consistency

    def get_visit_count(self, page_id: str) -> dict:
        """
        Get the current visit count for a page, using cache with fallback to Redis.
        
        Args:
            page_id: Unique identifier for the page.
        
        Returns:
            Dictionary containing the visit count and source ('in_memory' or 'redis').
        """
        current_time = time.time()

        # ✅ 1. Check if cached and still valid
        if page_id in self.cache:
            count, expiry = self.cache[page_id]
            if current_time < expiry:
                return {"visits": count, "served_via": "in_memory"}

        # ❌ 2. Cache miss or expired → Fetch from Redis
        count = self.redis_manager.get(f"visit_count:{page_id}")
        
        # ✅ 3. Update cache with a TTL of 5 seconds
        self.cache[page_id] = (count, current_time + 5)

        return {"visits": count, "served_via": "redis"}
