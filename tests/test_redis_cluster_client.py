import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from app.db.redis_cluster_client import RedisClusterClient
import json

class TestRedisClusterClient(unittest.TestCase):
    def setUp(self):
        # Create a mock Redis Cluster instance
        self.mock_redis = MagicMock()
        
        # Create the RedisClusterClient instance
        self.client = RedisClusterClient(
            startup_nodes=[{"host": "localhost", "port": 6379}],
            password="test_password"
        )
        
        # Patch the client property to return our mock
        self.client_patcher = patch.object(
            RedisClusterClient, 'client',
            new_callable=PropertyMock,
            return_value=self.mock_redis
        )
        self.client_patcher.start()

    def tearDown(self):
        self.client_patcher.stop()


    def test_set_and_get_string(self):
        # Test setting a string value
        self.client.set('test_key', 'test_value')
        self.mock_redis.set.assert_called_once_with('test_key', 'test_value')
        
        # Test getting a string value
        self.mock_redis.get.return_value = 'test_value'
        result = self.client.get('test_key')
        self.assertEqual(result, 'test_value')
        self.mock_redis.get.assert_called_once_with('test_key')

    def test_set_and_get_json(self):
        test_data = {'name': 'test', 'value': 123}
        
        # Test setting a JSON value
        self.client.set('test_key', test_data)
        self.mock_redis.set.assert_called_once_with(
            'test_key',
            json.dumps(test_data)
        )
        
        # Test getting a JSON value
        self.mock_redis.get.return_value = json.dumps(test_data)
        result = self.client.get('test_key')
        self.assertEqual(result, test_data)
        self.mock_redis.get.assert_called_once_with('test_key')

    def test_set_with_conditions(self):
        # Test setting with NX condition (only if key doesn't exist)
        self.client.set('test_key', 'test_value', nx=True)
        self.mock_redis.set.assert_called_with('test_key', 'test_value', nx=True)
        
        # Reset mock
        self.mock_redis.reset_mock()
        
        # Test setting with XX condition (only if key exists)
        self.client.set('test_key', 'test_value', xx=True)
        self.mock_redis.set.assert_called_with('test_key', 'test_value', xx=True)
        
        # Reset mock
        self.mock_redis.reset_mock()
        
        # Test setting with expiration
        self.client.set('test_key', 'test_value', expire=60)
        self.mock_redis.set.assert_called_with('test_key', 'test_value')
        self.mock_redis.expire.assert_called_with('test_key', 60)

    def test_delete(self):
        self.mock_redis.delete.return_value = 2
        
        result = self.client.delete('key1', 'key2')
        self.assertEqual(result, 2)
        self.mock_redis.delete.assert_called_once_with('key1', 'key2')

    def test_exists(self):
        self.mock_redis.exists.return_value = 2
        
        result = self.client.exists('key1', 'key2')
        self.assertEqual(result, 2)
        self.mock_redis.exists.assert_called_once_with('key1', 'key2')

    def test_hash_operations(self):
        test_hash = {'field1': 'value1', 'field2': 'value2'}
        
        # Test setting hash
        self.client.set_hash('test_hash', test_hash)
        self.mock_redis.hmset.assert_called_once_with('test_hash', test_hash)
        
        # Test getting hash
        self.mock_redis.hgetall.return_value = test_hash
        result = self.client.get_hash('test_hash')
        self.assertEqual(result, test_hash)
        self.mock_redis.hgetall.assert_called_once_with('test_hash')
        
        # Test getting hash field
        self.mock_redis.hget.return_value = 'value1'
        result = self.client.get_hash_field('test_hash', 'field1')
        self.assertEqual(result, 'value1')
        self.mock_redis.hget.assert_called_once_with('test_hash', 'field1')
        
        # Test deleting hash fields
        self.mock_redis.hdel.return_value = 1
        result = self.client.delete_hash('test_hash', 'field1')
        self.assertEqual(result, 1)
        self.mock_redis.hdel.assert_called_once_with('test_hash', 'field1')

    def test_list_operations(self):
        test_values = ['value1', 'value2']
        
        # Test pushing to list
        self.client.push_list('test_list', *test_values)
        self.mock_redis.rpush.assert_called_once_with('test_list', *test_values)
        
        # Test getting list
        self.mock_redis.lrange.return_value = test_values
        result = self.client.get_list('test_list')
        self.assertEqual(result, test_values)
        self.mock_redis.lrange.assert_called_once_with('test_list', 0, -1)

    def test_set_operations(self):
        test_values = ['value1', 'value2']
        
        # Test adding to set
        self.client.add_to_set('test_set', *test_values)
        self.mock_redis.sadd.assert_called_once_with('test_set', *test_values)
        
        # Test getting set
        self.mock_redis.smembers.return_value = set(test_values)
        result = self.client.get_set('test_set')
        self.assertEqual(result, set(test_values))
        self.mock_redis.smembers.assert_called_once_with('test_set')

    def test_pubsub_operations(self):
        # Test publishing
        self.mock_redis.publish.return_value = 1
        result = self.client.publish('test_channel', 'test_message')
        self.assertEqual(result, 1)
        self.mock_redis.publish.assert_called_once_with('test_channel', 'test_message')
        
        # Test subscribing
        mock_pubsub = MagicMock()
        self.mock_redis.pubsub.return_value = mock_pubsub
        result = self.client.subscribe('test_channel')
        self.assertEqual(result, mock_pubsub)
        self.mock_redis.pubsub.assert_called_once()
        mock_pubsub.subscribe.assert_called_once_with('test_channel')

    

if __name__ == '__main__':
    unittest.main() 