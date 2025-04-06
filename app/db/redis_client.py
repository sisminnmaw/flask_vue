import os
import redis
from typing import Any, Optional, Union, List
import json
import logging
from contextlib import contextmanager

class RedisClient:
    def __init__(self, host=None, port=None, db=0, password=None):
        self.host = host or os.getenv('REDIS_HOST', 'localhost')
        self.port = port or int(os.getenv('REDIS_PORT', 6379))
        self.db = db
        self.password = password or os.getenv('REDIS_PASSWORD', None)
        self.logger = logging.getLogger(__name__)
        self._client = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )
        return self._client

    def set(self, key: str, value: Any, expire: int = None) -> bool:
        """
        Set a key-value pair with optional expiration
        """
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            self.client.set(key, value)
            if expire:
                self.client.expire(key, expire)
            return True
        except Exception as e:
            self.logger.error(f"Error setting key {key}: {e}")
            return False

    def get(self, key: str) -> Any:
        """
        Get a value by key
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

    def delete(self, key: str) -> bool:
        """
        Delete a key
        """
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            self.logger.error(f"Error deleting key {key}: {e}")
            return False

    def exists(self, key: str) -> bool:
        """
        Check if a key exists
        """
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            self.logger.error(f"Error checking key {key}: {e}")
            return False

    def set_hash(self, name: str, mapping: dict) -> bool:
        """
        Set hash field-value pairs
        """
        try:
            return bool(self.client.hmset(name, mapping))
        except Exception as e:
            self.logger.error(f"Error setting hash {name}: {e}")
            return False

    def get_hash(self, name: str) -> dict:
        """
        Get all hash field-value pairs
        """
        try:
            return self.client.hgetall(name)
        except Exception as e:
            self.logger.error(f"Error getting hash {name}: {e}")
            return {}

    def delete_hash(self, name: str, *fields: str) -> int:
        """
        Delete one or more hash fields
        """
        try:
            return self.client.hdel(name, *fields)
        except Exception as e:
            self.logger.error(f"Error deleting hash fields {fields}: {e}")
            return 0

    def push_list(self, name: str, *values: Any) -> int:
        """
        Push values to a list
        """
        try:
            values = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in values]
            return self.client.rpush(name, *values)
        except Exception as e:
            self.logger.error(f"Error pushing to list {name}: {e}")
            return 0

    def get_list(self, name: str, start: int = 0, end: int = -1) -> List[Any]:
        """
        Get list values
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
        Add values to a set
        """
        try:
            values = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in values]
            return self.client.sadd(name, *values)
        except Exception as e:
            self.logger.error(f"Error adding to set {name}: {e}")
            return 0

    def get_set(self, name: str) -> set:
        """
        Get all members of a set
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
        Publish a message to a channel
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
        Subscribe to a channel
        """
        try:
            pubsub = self.client.pubsub()
            pubsub.subscribe(channel)
            return pubsub
        except Exception as e:
            self.logger.error(f"Error subscribing to channel {channel}: {e}")
            return None

    def close(self):
        """
        Close the Redis connection
        """
        if self._client:
            self._client.close()
            self._client = None 