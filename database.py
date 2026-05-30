#!/usr/bin/env python3
"""
Database abstraction layer for Catacomb.

Supports both SQLite (local development) and Postgres (production).
Provides unified interface for all database operations.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and DATABASE_URL.startswith('postgres'):
    import psycopg2
    from psycopg2 import sql, pool
    USE_POSTGRES = True
else:
    import sqlite3
    USE_POSTGRES = False


class Database:
    """Unified database interface for SQLite and Postgres."""
    
    def __init__(self, db_url: Optional[str] = None):
        """
        Initialize database connection.
        
        Args:
            db_url: Database URL. If None, uses DATABASE_URL env var or SQLite default.
        """
        self.db_url = db_url or DATABASE_URL or 'outcome_ledger.db'
        self._pool = None
        
        if USE_POSTGRES:
            self._init_postgres_pool()
        else:
            self._init_sqlite()
    
    def _init_postgres_pool(self):
        """Initialize Postgres connection pool."""
        if not self.db_url:
            raise ValueError("DATABASE_URL required for Postgres")
        
        self._pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=self.db_url
        )
        logger.info("Initialized Postgres connection pool")
    
    def _init_sqlite(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_url)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.close()
        logger.info(f"Initialized SQLite database: {self.db_url}")
    
    @contextmanager
    def get_connection(self):
        """Get database connection from pool or create new one."""
        if USE_POSTGRES:
            conn = self._pool.getconn()
            try:
                yield conn
            finally:
                self._pool.putconn(conn)
        else:
            conn = sqlite3.connect(self.db_url)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
            finally:
                conn.close()
    
    def execute(self, query: str, params: Optional[tuple] = None) -> Any:
        """
        Execute a query and return results.
        
        Args:
            query: SQL query
            params: Query parameters
            
        Returns:
            Query results (for SELECT) or row count (for INSERT/UPDATE/DELETE)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if USE_POSTGRES:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    conn.commit()
                    return cursor.rowcount
            else:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    return [dict(row) for row in cursor.fetchall()]
                else:
                    conn.commit()
                    return cursor.rowcount
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Execute a query multiple times.
        
        Args:
            query: SQL query
            params_list: List of parameter tuples
            
        Returns:
            Total row count
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if USE_POSTGRES:
                cursor.executemany(query, params_list)
                conn.commit()
                return cursor.rowcount
            else:
                cursor.executemany(query, params_list)
                conn.commit()
                return cursor.rowcount
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insert a row into a table.
        
        Args:
            table: Table name
            data: Column names and values
            
        Returns:
            Row count (1 if successful)
        """
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join(['%s'] * len(values) if USE_POSTGRES else ['?'] * len(values))
        
        query = f"""
            INSERT INTO {table} ({', '.join(columns)})
            VALUES ({placeholders})
        """
        
        return self.execute(query, tuple(values))
    
    def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """
        Update rows in a table.
        
        Args:
            table: Table name
            data: Column names and values to update
            where: WHERE clause conditions
            
        Returns:
            Row count
        """
        set_clause = ', '.join([f"{k} = %s" if USE_POSTGRES else f"{k} = ?" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" if USE_POSTGRES else f"{k} = ?" for k in where.keys()])
        
        query = f"""
            UPDATE {table}
            SET {set_clause}
            WHERE {where_clause}
        """
        
        params = tuple(list(data.values()) + list(where.values()))
        return self.execute(query, params)
    
    def select(self, table: str, where: Optional[Dict[str, Any]] = None, 
               limit: Optional[int] = None, order_by: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Select rows from a table.
        
        Args:
            table: Table name
            where: WHERE clause conditions
            limit: Maximum number of rows
            order_by: ORDER BY clause
            
        Returns:
            List of rows as dictionaries
        """
        query = f"SELECT * FROM {table}"
        params = []
        
        if where:
            where_clause = ' AND '.join([f"{k} = %s" if USE_POSTGRES else f"{k} = ?" for k in where.keys()])
            query += f" WHERE {where_clause}"
            params.extend(where.values())
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            if USE_POSTGRES:
                query += f" LIMIT {limit}"
            else:
                query += f" LIMIT {limit}"
        
        return self.execute(query, tuple(params) if params else None)
    
    def delete(self, table: str, where: Dict[str, Any]) -> int:
        """
        Delete rows from a table.
        
        Args:
            table: Table name
            where: WHERE clause conditions
            
        Returns:
            Row count
        """
        where_clause = ' AND '.join([f"{k} = %s" if USE_POSTGRES else f"{k} = ?" for k in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        return self.execute(query, tuple(where.values()))
    
    def close(self):
        """Close database connections."""
        if USE_POSTGRES and self._pool:
            self._pool.closeall()
            logger.info("Closed Postgres connection pool")


# Global database instance
_db = None


def get_database() -> Database:
    """Get global database instance."""
    global _db
    if _db is None:
        _db = Database()
    return _db


def close_database():
    """Close global database instance."""
    global _db
    if _db:
        _db.close()
        _db = None
