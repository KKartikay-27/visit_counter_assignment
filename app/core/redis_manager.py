import redis
from ..core.config import settings
from ..core.consistent_hash import ConsistentHash

class RedisManager:
    def __init__(self):
        """Initialize Redis connections and hashing"""
        self.nodes = settings.REDIS_NODES.split(",")
        self.consistent_hash = ConsistentHash(self.nodes, settings.VIRTUAL_NODES)
        self.redis_clients = {node: redis.Redis.from_url(node, decode_responses=True) for node in self.nodes}

    def _get_redis_instance(self, key: str):
        """Get the correct Redis instance for a given key"""
        node = self.consistent_hash.get_node(key)
        return self.redis_clients[node], node

    def increment(self, key: str, amount: int = 1):
        """Increment a counter in the correct Redis shard"""
        redis_client, node = self._get_redis_instance(key)
        redis_client.incrby(key, amount)
        return node  # Return node to track the source

    def get(self, key: str):
        """Retrieve the value from the correct Redis shard"""
        redis_client, node = self._get_redis_instance(key)
        value = redis_client.get(key)
        return int(value) if value else 0, node  # Return node info
