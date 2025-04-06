import unittest
from unittest.mock import patch, MagicMock
from app.db.mysql_client import MySQLClient
import os

class TestMySQLClient(unittest.TestCase):
    def setUp(self):
        self.client = MySQLClient(
            host='localhost',
            port=3306,
            user='test_user',
            password='test_password',
            database='test_db'
        )

    @patch('mysql.connector.connect')
    def test_connection(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        with self.client.get_connection() as conn:
            self.assertEqual(conn, mock_conn)
            mock_connect.assert_called_once_with(
                host='localhost',
                port=3306,
                user='test_user',
                password='test_password',
                database='test_db'
            )

    @patch('mysql.connector.connect')
    def test_execute_raw_select(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'test'}]
        mock_cursor.rowcount = 1
        
        result, count = self.client.execute_raw("SELECT * FROM test_table")
        
        self.assertEqual(result, [{'id': 1, 'name': 'test'}])
        self.assertEqual(count, 1)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM test_table", ())
        mock_conn.commit.assert_not_called()

    @patch('mysql.connector.connect')
    def test_execute_raw_insert(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        mock_cursor.rowcount = 1
        
        result, count = self.client.execute_raw(
            "INSERT INTO test_table (name) VALUES (%s)",
            ('test',)
        )
        
        self.assertEqual(result, [])
        self.assertEqual(count, 1)
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO test_table (name) VALUES (%s)",
            ('test',)
        )
        mock_conn.commit.assert_called_once()

    def test_fetch_all(self):
        with patch.object(self.client, 'execute_raw') as mock_execute:
            mock_execute.return_value = ([{'id': 1, 'name': 'test'}], 1)
            
            result = self.client.fetch_all(
                'test_table',
                conditions={'name': 'test'},
                order_by='id DESC',
                limit=10
            )
            
            self.assertEqual(result, [{'id': 1, 'name': 'test'}])
            mock_execute.assert_called_once()

    def test_insert(self):
        with patch.object(self.client, 'get_connection') as mock_get_conn:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_conn.return_value.__enter__.return_value = mock_conn
            
            mock_cursor.lastrowid = 1
            
            result = self.client.insert('test_table', {'name': 'test'})
            
            self.assertEqual(result, 1)
            mock_cursor.execute.assert_called_once()
            mock_conn.commit.assert_called_once()

    def test_update(self):
        with patch.object(self.client, 'execute_raw') as mock_execute:
            mock_execute.return_value = ([], 1)
            
            result = self.client.update(
                'test_table',
                {'name': 'new_name'},
                {'id': 1}
            )
            
            self.assertEqual(result, 1)
            mock_execute.assert_called_once()

    def test_delete(self):
        with patch.object(self.client, 'execute_raw') as mock_execute:
            mock_execute.return_value = ([], 1)
            
            result = self.client.delete('test_table', {'id': 1})
            
            self.assertEqual(result, 1)
            mock_execute.assert_called_once()

    def test_table_exists(self):
        with patch.object(self.client, 'execute_raw') as mock_execute:
            mock_execute.return_value = ([{'COUNT(*)': 1}], 1)
            
            result = self.client.table_exists('test_table')
            
            self.assertTrue(result)
            mock_execute.assert_called_once()

    def test_get_table_columns(self):
        with patch.object(self.client, 'execute_raw') as mock_execute:
            mock_execute.return_value = ([{'COLUMN_NAME': 'id'}, {'COLUMN_NAME': 'name'}], 2)
            
            result = self.client.get_table_columns('test_table')
            
            self.assertEqual(result, ['id', 'name'])
            mock_execute.assert_called_once()

if __name__ == '__main__':
    unittest.main() 