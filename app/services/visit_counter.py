class VisitCounterService:
    def __init__(self):
        """Initialize the visit counter service with an in-memory store"""
        self.visit_counts = {}

    def increment_visit(self, page_id: str) -> None:
        """
        Increment visit count for a page
        
        Args:
            page_id: Unique identifier for the page
        """
        if page_id in self.visit_counts:
            self.visit_counts[page_id] += 1
        else:
            self.visit_counts[page_id] = 1

    def get_visit_count(self, page_id: str) -> int:
        """
        Get current visit count for a page
        
        Args:
            page_id: Unique identifier for the page
            
        Returns:
            Current visit count
        """
        return self.visit_counts.get(page_id, 0)
