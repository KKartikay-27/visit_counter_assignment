import hashlib
from bisect import bisect
from typing import List, Dict

class ConsistentHash:
    def __init__(self, nodes: List[str], virtual_nodes: int = 100):
        self.nodes = nodes
        self.virtual_nodes = virtual_nodes
        self.hash_ring = {}
        self.sorted_keys = []
        
        for node in nodes:
            self.add_node(node)

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node: str):
        """Add a new node with virtual nodes to the hash ring"""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}-{i}"
            hash_value = self._hash(virtual_key)
            self.hash_ring[hash_value] = node
            self.sorted_keys.append(hash_value)
        
        self.sorted_keys.sort()

    def remove_node(self, node: str):
        """Remove a node and its virtual nodes from the hash ring"""
        self.sorted_keys = [
            hash_val for hash_val in self.sorted_keys if self.hash_ring[hash_val] != node
        ]
        self.hash_ring = {k: v for k, v in self.hash_ring.items() if v != node}

    def get_node(self, key: str) -> str:
        """Find the correct node for the given key"""
        if not self.hash_ring:
            raise ValueError("No nodes available")
        
        hash_val = self._hash(key)
        idx = bisect(self.sorted_keys, hash_val)
        if idx == len(self.sorted_keys):
            idx = 0  # Wrap around
        
        return self.hash_ring[self.sorted_keys[idx]]
