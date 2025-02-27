from ..core.redis_manager import RedisManager

class VisitCounterService:
    def __init__(self):
        """Initialize the visit counter service using Redis"""
        self.redis_manager = RedisManager()

    def increment_visit(self, page_id: str) -> None:
        """
        Increment visit count for a page.
        
        Args:
            page_id: Unique identifier for the page.
        """
        self.redis_manager.increment(f"visit_count:{page_id}")

    def get_visit_count(self, page_id: str) -> int:
        """
        Get the current visit count for a page.
        
        Args:
            page_id: Unique identifier for the page.
        
        Returns:
            The current visit count.
        """
        return self.redis_manager.get(f"visit_count:{page_id}")
