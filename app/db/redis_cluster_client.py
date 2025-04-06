import os
import redis
from redis.cluster import RedisCluster, RedisClusterException
from typing import Any, Optional, Union, List, Dict, Set, Tuple
import json
import logging
from contextlib import contextmanager

class RedisClusterClient:
    """
    Redis Cluster client for distributed Redis deployments with sharding support.
    This client handles operations across multiple Redis nodes in a cluster.
    """
    def __init__(self, startup_nodes=None, password=None, ssl=False, 
                 decode_responses=True, skip_full_coverage_check=True):
        """
        Initialize the Redis Cluster client.
        
        Args:
            startup_nodes: List of dictionaries with host and port for cluster nodes
            password: Password for authentication
            ssl: Whether to use SSL for connections
            decode_responses: Whether to decode responses to strings
            skip_full_coverage_check: Skip checking if all slots are covered
        """
        self.startup_nodes = startup_nodes or [
            {"host": os.getenv('REDIS_CLUSTER_HOST', 'localhost'), 
             "port": int(os.getenv('REDIS_CLUSTER_PORT', 6379))}
        ]
        self.password = password or os.getenv('REDIS_CLUSTER_PASSWORD', None)
        self.ssl = ssl
        self.decode_responses = decode_responses
        self.skip_full_coverage_check = skip_full_coverage_check
        self.logger = logging.getLogger(__name__)
        self._client = None

    @property
    def client(self) -> RedisCluster:
        """
        Lazy initialization of the Redis Cluster client.
        """
        if self._client is None:
            try:
                self._client = RedisCluster(
                    startup_nodes=self.startup_nodes,
                    password=self.password,
                    ssl=self.ssl,
                    decode_responses=self.decode_responses,
                    skip_full_coverage_check=self.skip_full_coverage_check
                )
            except RedisClusterException as e:
                self.logger.error(f"Error connecting to Redis Cluster: {e}")
                raise
        return self._client

    def set(self, key: str, value: Any, expire: int = None, nx: bool = False, 
            xx: bool = False) -> bool:
        """
        Set a key-value pair with optional expiration and conditions.
        
        Args:
            key: The key to set
            value: The value to set
            expire: Expiration time in seconds
            nx: Only set if key doesn't exist
            xx: Only set if key exists
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            if nx:
                result = self.client.set(key, value, nx=True)
            elif xx:
                result = self.client.set(key, value, xx=True)
            else:
                result = self.client.set(key, value)
                
            if expire and result:
                self.client.expire(key, expire)
                
            return bool(result)
        except Exception as e:
            self.logger.error(f"Error setting key {key}: {e}")
            return False

    def get(self, key: str) -> Any:
        """
        Get a value by key.
        
        Args:
            key: The key to get
            
        Returns:
            The value or None if not found
        """
        try:
            value = self.client.get(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception as e:
            self.logger.error(f"Error getting key {key}: {e}")
            return None

    def delete(self, *keys: str) -> int:
        """
        Delete one or more keys.
        
        Args:
            *keys: Keys to delete
            
        Returns:
            int: Number of keys deleted
        """
        try:
            return self.client.delete(*keys)
        except Exception as e:
            self.logger.error(f"Error deleting keys {keys}: {e}")
            return 0

    def exists(self, *keys: str) -> int:
        """
        Check if one or more keys exist.
        
        Args:
            *keys: Keys to check
            
        Returns:
            int: Number of keys that exist
        """
        try:
            return self.client.exists(*keys)
        except Exception as e:
            self.logger.error(f"Error checking keys {keys}: {e}")
            return 0

    def set_hash(self, name: str, mapping: dict) -> bool:
        """
        Set hash field-value pairs.
        
        Args:
            name: Hash name
            mapping: Dictionary of field-value pairs
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            return bool(self.client.hmset(name, mapping))
        except Exception as e:
            self.logger.error(f"Error setting hash {name}: {e}")
            return False

    def get_hash(self, name: str) -> dict:
        """
        Get all hash field-value pairs.
        
        Args:
            name: Hash name
            
        Returns:
            dict: Dictionary of field-value pairs
        """
        try:
            return self.client.hgetall(name)
        except Exception as e:
            self.logger.error(f"Error getting hash {name}: {e}")
            return {}

    def get_hash_field(self, name: str, field: str) -> Any:
        """
        Get a specific field from a hash.
        
        Args:
            name: Hash name
            field: Field name
            
        Returns:
            The field value or None if not found
        """
        try:
            return self.client.hget(name, field)
        except Exception as e:
            self.logger.error(f"Error getting hash field {name}.{field}: {e}")
            return None

    def delete_hash(self, name: str, *fields: str) -> int:
        """
        Delete one or more hash fields.
        
        Args:
            name: Hash name
            *fields: Fields to delete
            
        Returns:
            int: Number of fields deleted
        """
        try:
            return self.client.hdel(name, *fields)
        except Exception as e:
            self.logger.error(f"Error deleting hash fields {fields}: {e}")
            return 0

    def push_list(self, name: str, *values: Any) -> int:
        """
        Push values to a list.
        
        Args:
            name: List name
            *values: Values to push
            
        Returns:
            int: New length of the list
        """
        try:
            values = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in values]
            return self.client.rpush(name, *values)
        except Exception as e:
            self.logger.error(f"Error pushing to list {name}: {e}")
            return 0

    def get_list(self, name: str, start: int = 0, end: int = -1) -> List[Any]:
        """
        Get list values.
        
        Args:
            name: List name
            start: Start index
            end: End index
            
        Returns:
            List of values
        """
        try:
            values = self.client.lrange(name, start, end)
            return [json.loads(v) if v.startswith('{') or v.startswith('[') else v 
                   for v in values]
        except Exception as e:
            self.logger.error(f"Error getting list {name}: {e}")
            return []

    def add_to_set(self, name: str, *values: Any) -> int:
        """
        Add values to a set.
        
        Args:
            name: Set name
            *values: Values to add
            
        Returns:
            int: Number of values added
        """
        try:
            values = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in values]
            return self.client.sadd(name, *values)
        except Exception as e:
            self.logger.error(f"Error adding to set {name}: {e}")
            return 0

    def get_set(self, name: str) -> Set[Any]:
        """
        Get all members of a set.
        
        Args:
            name: Set name
            
        Returns:
            Set of values
        """
        try:
            values = self.client.smembers(name)
            return {json.loads(v) if v.startswith('{') or v.startswith('[') else v 
                   for v in values}
        except Exception as e:
            self.logger.error(f"Error getting set {name}: {e}")
            return set()

    def publish(self, channel: str, message: Any) -> int:
        """
        Publish a message to a channel.
        
        Args:
            channel: Channel name
            message: Message to publish
            
        Returns:
            int: Number of clients that received the message
        """
        try:
            if isinstance(message, (dict, list)):
                message = json.dumps(message)
            return self.client.publish(channel, message)
        except Exception as e:
            self.logger.error(f"Error publishing to channel {channel}: {e}")
            return 0

    def subscribe(self, channel: str):
        """
        Subscribe to a channel.
        
        Args:
            channel: Channel name
            
        Returns:
            PubSub object
        """
        try:
            pubsub = self.client.pubsub()
            pubsub.subscribe(channel)
            return pubsub
        except Exception as e:
            self.logger.error(f"Error subscribing to channel {channel}: {e}")
            return None

    def get_cluster_nodes(self) -> List[Dict[str, Any]]:
        """
        Get information about all nodes in the cluster.
        
        Returns:
            List of dictionaries with node information
        """
        try:
            return self.client.cluster_nodes()
        except Exception as e:
            self.logger.error(f"Error getting cluster nodes: {e}")
            return []

    def get_cluster_slots(self) -> List[Tuple[int, int, List[Dict[str, Any]]]]:
        """
        Get information about slot assignments in the cluster.
        
        Returns:
            List of tuples with slot information
        """
        try:
            return self.client.cluster_slots()
        except Exception as e:
            self.logger.error(f"Error getting cluster slots: {e}")
            return []

    def get_key_slot(self, key: str) -> int:
        """
        Get the slot number for a key.
        
        Args:
            key: The key to get the slot for
            
        Returns:
            int: Slot number
        """
        try:
            return self.client.keyslot(key)
        except Exception as e:
            self.logger.error(f"Error getting slot for key {key}: {e}")
            return -1

    def get_node_for_key(self, key: str) -> Dict[str, Any]:
        """
        Get the node that owns a key.
        
        Args:
            key: The key to get the node for
            
        Returns:
            Dictionary with node information
        """
        try:
            slot = self.get_key_slot(key)
            if slot == -1:
                return {}
                
            slots = self.get_cluster_slots()
            for start, end, nodes in slots:
                if start <= slot <= end:
                    return nodes[0] if nodes else {}
                    
            return {}
        except Exception as e:
            self.logger.error(f"Error getting node for key {key}: {e}")
            return {}

    def close(self):
        """
        Close the Redis Cluster connection.
        """
        if self._client:
            self._client.close()
            self._client = None 