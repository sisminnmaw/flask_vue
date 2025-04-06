import os
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional, Union, Tuple
import logging
from contextlib import contextmanager

class MySQLClient:
    def __init__(self, host=None, port=None, user=None, password=None, database=None):
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.port = port or int(os.getenv('DB_PORT', 3306))
        self.user = user or os.getenv('DB_USER', 'root')
        self.password = password or os.getenv('DB_PASSWORD', '')
        self.database = database or os.getenv('DB_NAME', 'flask_vue')
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            yield conn
        except Error as e:
            self.logger.error(f"Error connecting to MySQL: {e}")
            raise
        finally:
            if conn and conn.is_connected():
                conn.close()

    def execute_raw(self, query: str, params: tuple = None) -> Tuple[List[Dict[str, Any]], int]:
        """
        Execute a raw SQL query and return results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    result = cursor.fetchall()
                    return result, cursor.rowcount
                else:
                    conn.commit()
                    return [], cursor.rowcount
            except Error as e:
                self.logger.error(f"Error executing query: {e}")
                raise
            finally:
                cursor.close()

    def fetch_all(self, table: str, conditions: Dict[str, Any] = None, 
                 order_by: str = None, limit: int = None, 
                 columns: List[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch all records from a table with optional filtering and ordering
        """
        if not self._is_valid_table_name(table):
            raise ValueError("Invalid table name")

        query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table}"
        params = []

        if conditions:
            where_clauses = []
            for key, value in conditions.items():
                where_clauses.append(f"{key} = %s")
                params.append(value)
            query += " WHERE " + " AND ".join(where_clauses)

        if order_by:
            query += f" ORDER BY {order_by}"

        if limit:
            query += f" LIMIT {limit}"

        result, _ = self.execute_raw(query, tuple(params))
        return result

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert a record into a table and return the last insert ID
        """
        if not self._is_valid_table_name(table):
            raise ValueError("Invalid table name")

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, tuple(data.values()))
                conn.commit()
                return cursor.lastrowid
            except Error as e:
                self.logger.error(f"Error inserting record: {e}")
                raise
            finally:
                cursor.close()

    def update(self, table: str, data: Dict[str, Any], 
               conditions: Dict[str, Any]) -> int:
        """
        Update records in a table based on conditions
        """
        if not self._is_valid_table_name(table):
            raise ValueError("Invalid table name")

        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        params = tuple(list(data.values()) + list(conditions.values()))
        _, affected_rows = self.execute_raw(query, params)
        return affected_rows

    def delete(self, table: str, conditions: Dict[str, Any]) -> int:
        """
        Delete records from a table based on conditions
        """
        if not self._is_valid_table_name(table):
            raise ValueError("Invalid table name")

        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        _, affected_rows = self.execute_raw(query, tuple(conditions.values()))
        return affected_rows

    def begin_transaction(self):
        """
        Start a new transaction
        """
        conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        conn.start_transaction()
        return conn

    def _is_valid_table_name(self, table: str) -> bool:
        """
        Basic validation for table names to prevent SQL injection
        """
        return bool(table and table.isalnum() and not table.isspace())

    def table_exists(self, table: str) -> bool:
        """
        Check if a table exists in the database
        """
        query = """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = %s
            AND table_name = %s
        """
        result, _ = self.execute_raw(query, (self.database, table))
        return result[0]['COUNT(*)'] > 0

    def get_table_columns(self, table: str) -> List[str]:
        """
        Get column names for a table
        """
        query = """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s
            AND TABLE_NAME = %s
        """
        result, _ = self.execute_raw(query, (self.database, table))
        return [row['COLUMN_NAME'] for row in result] 