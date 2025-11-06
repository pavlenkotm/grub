"""
Database management module
"""

import sqlite3
from typing import Any, Dict, List, Optional, Tuple
from contextlib import contextmanager

from ..utils.logger import get_logger


class Database:
    """SQLite database manager"""

    def __init__(self, db_path: str = ":memory:"):
        """Initialize database connection

        Args:
            db_path: Path to database file (use :memory: for in-memory database)
        """
        self.db_path = db_path
        self.logger = get_logger()
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise

    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")

    @contextmanager
    def get_cursor(self):
        """Get database cursor with automatic connection management

        Yields:
            Database cursor
        """
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            cursor.close()

    def execute(self, query: str, params: Optional[Tuple] = None) -> sqlite3.Cursor:
        """Execute SQL query

        Args:
            query: SQL query string
            params: Optional query parameters

        Returns:
            Database cursor
        """
        with self.get_cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor

    def execute_many(self, query: str, params_list: List[Tuple]) -> None:
        """Execute SQL query for multiple parameter sets

        Args:
            query: SQL query string
            params_list: List of parameter tuples
        """
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)

    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict]:
        """Fetch single row from query result

        Args:
            query: SQL query string
            params: Optional query parameters

        Returns:
            Dictionary of row data or None
        """
        with self.get_cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            row = cursor.fetchone()
            return dict(row) if row else None

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict]:
        """Fetch all rows from query result

        Args:
            query: SQL query string
            params: Optional query parameters

        Returns:
            List of dictionaries containing row data
        """
        with self.get_cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """Create table with specified columns

        Args:
            table_name: Name of table to create
            columns: Dictionary of column_name: column_type
        """
        columns_def = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        self.execute(query)
        self.logger.info(f"Table '{table_name}' created")

    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """Insert row into table

        Args:
            table_name: Name of table
            data: Dictionary of column: value

        Returns:
            Last inserted row ID
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        with self.get_cursor() as cursor:
            cursor.execute(query, tuple(data.values()))
            return cursor.lastrowid

    def update(self, table_name: str, data: Dict[str, Any], where: str, where_params: Tuple) -> int:
        """Update rows in table

        Args:
            table_name: Name of table
            data: Dictionary of column: value to update
            where: WHERE clause condition
            where_params: Parameters for WHERE clause

        Returns:
            Number of affected rows
        """
        set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where}"

        with self.get_cursor() as cursor:
            cursor.execute(query, tuple(data.values()) + where_params)
            return cursor.rowcount

    def delete(self, table_name: str, where: str, where_params: Tuple) -> int:
        """Delete rows from table

        Args:
            table_name: Name of table
            where: WHERE clause condition
            where_params: Parameters for WHERE clause

        Returns:
            Number of affected rows
        """
        query = f"DELETE FROM {table_name} WHERE {where}"

        with self.get_cursor() as cursor:
            cursor.execute(query, where_params)
            return cursor.rowcount
