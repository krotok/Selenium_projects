import psycopg2
import logging
from typing import Dict, Any, List, Optional
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        self.connection = None

    def connect(self) -> None:
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            logger.info("Database connection established")
        except psycopg2.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except psycopg2.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute UPDATE/INSERT/DELETE query"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor.rowcount
        except psycopg2.Error as e:
            self.connection.rollback()
            logger.error(f"Update execution failed: {e}")
            raise

    def create_test_user(self, username: str, password: str) -> int:
        """Create test user in database (mock implementation)"""
        query = """
        INSERT INTO users (username, password, created_at) 
        VALUES (%s, %s, NOW())
        RETURNING id
        """
        return self.execute_update(query, (username, password))

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username (mock implementation)"""
        query = "SELECT * FROM users WHERE username = %s"
        results = self.execute_query(query, (username,))
        return results[0] if results else None