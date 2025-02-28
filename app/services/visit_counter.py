import time
import threading
from ..core.redis_manager import RedisManager

class VisitCounterService:
    def __init__(self):
        """Initialize the visit counter service with in-memory batching and Redis"""
        self.redis_manager = RedisManager()
        self.buffer = {}  # In-memory buffer: {page_id: visit_count}
        self.lock = threading.Lock()  # Ensure thread safety
        self.last_flush_time = time.time()

        # Start background thread for periodic flushing
        self.flush_interval = 30  # Flush every 30 seconds
        self._start_flush_thread()

    def _start_flush_thread(self):
        """Start a background thread that flushes data to Redis periodically"""
        def flush_worker():
            while True:
                time.sleep(self.flush_interval)
                self.flush_to_redis()

        thread = threading.Thread(target=flush_worker, daemon=True)
        thread.start()

    def increment_visit(self, page_id: str) -> None:
        """
        Increment visit count for a page, accumulating in the in-memory buffer.
        
        Args:
            page_id: Unique identifier for the page.
        """
        with self.lock:
            self.buffer[page_id] = self.buffer.get(page_id, 0) + 1

    def flush_to_redis(self) -> None:
        """Flush all buffered visits to Redis"""
        with self.lock:
            if not self.buffer:
                print("[DEBUG] No visits to flush.")
                return
            
            print(f"[DEBUG] Flushing {len(self.buffer)} items to Redis: {self.buffer}")

            for page_id, count in self.buffer.items():
                self.redis_manager.increment(f"visit_count:{page_id}", count)

            self.buffer.clear()  # Clear buffer after flushing
            self.last_flush_time = time.time()

    def get_visit_count(self, page_id: str) -> dict:
        """
        Get the total visit count (Redis + buffer) for a page.
        
        Args:
            page_id: Unique identifier for the page.
        
        Returns:
            Dictionary containing the visit count and source ('batch + redis' or 'redis').
        """
        # ✅ Fetch count from Redis
        redis_count = self.redis_manager.get(f"visit_count:{page_id}") or 0

        # ✅ Fetch pending count from in-memory buffer
        with self.lock:
            buffer_count = self.buffer.get(page_id, 0)

        total_count = redis_count + buffer_count
        source = "batch + redis" if buffer_count > 0 else "redis"

        print(f"[DEBUG] Read page_id={page_id}, Redis={redis_count}, Buffer={buffer_count}, Total={total_count}")

        return {"visits": total_count, "served_via": source}
