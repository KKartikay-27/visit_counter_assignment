import time
import threading
from ..core.redis_manager import RedisManager

class VisitCounterService:
    def __init__(self):
        self.redis_manager = RedisManager()
        self.buffer = {}  # In-memory buffer
        self.lock = threading.Lock()
        self.flush_interval = 30
        self._start_flush_thread()

    def _start_flush_thread(self):
        """Background thread to flush data to Redis"""
        def flush_worker():
            while True:
                time.sleep(self.flush_interval)
                self.flush_to_redis()

        thread = threading.Thread(target=flush_worker, daemon=True)
        thread.start()

    def increment_visit(self, page_id: str):
        """Increment visit count in-memory"""
        with self.lock:
            self.buffer[page_id] = self.buffer.get(page_id, 0) + 1

    def flush_to_redis(self):
        """Flush buffered visits to Redis"""
        with self.lock:
            if not self.buffer:
                return
            
            for page_id, count in self.buffer.items():
                node = self.redis_manager.increment(f"visit_count:{page_id}", count)

            self.buffer.clear()

    def get_visit_count(self, page_id: str):
        """Fetch total visit count from in-memory + Redis"""
        with self.lock:
            buffer_count = self.buffer.get(page_id, 0)

        redis_count, node = self.redis_manager.get(f"visit_count:{page_id}")

        total_count = redis_count + buffer_count
        source = (
            "in_memory" if buffer_count > 0 
            else "redis_7070" if "7070" in node 
            else "redis_7071"
        )

        return {"visits": total_count, "served_via": source}
