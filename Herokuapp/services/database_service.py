import psycopg2
from typing import Dict, Any, List, Optional
from psycopg2.extras import RealDictCursor
from utils.log_decorators import LoggingMixin, log_database_operation, log_function_call


class DatabaseService(LoggingMixin):
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        self.connection = None
        self.logger.debug("Initialized DatabaseService")

    @log_function_call()
    def connect(self) -> None:
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.logger.info("Database connection established successfully")
        except psycopg2.Error as e:
            self.logger.error(f"Database connection failed: {e}")
            raise

    @log_function_call()
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")

    @log_database_operation("Execute SELECT query")
    @log_function_call(log_args=True, log_result=True)
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                self.logger.debug(f"Query returned {len(results)} rows")
                return [dict(row) for row in results]
        except psycopg2.Error as e:
            self.logger.error(f"Query execution failed: {e}")
            raise

    @log_database_operation("Execute UPDATE query")
    @log_function_call(log_args=True, log_result=True)
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute UPDATE/INSERT/DELETE query"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                affected_rows = cursor.rowcount
                self.logger.debug(f"Update affected {affected_rows} rows")
                return affected_rows
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Update execution failed: {e}")
            raise

    @log_database_operation("Create test user")
    @log_function_call(log_args=True, log_result=True)
    def create_test_user(self, username: str, password: str) -> int:
        """Create test user in database (mock implementation)"""
        query = """
        INSERT INTO users (username, password, created_at) 
        VALUES (%s, %s, NOW())
        RETURNING id
        """
        self.logger.info(f"Creating test user: {username}")
        return self.execute_update(query, (username, password))

    @log_database_operation("Get user by username")
    @log_function_call(log_args=True, log_result=True)
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username (mock implementation)"""
        query = "SELECT * FROM users WHERE username = %s"
        results = self.execute_query(query, (username,))
        user = results[0] if results else None
        self.logger.debug(f"User lookup for {username}: {'Found' if user else 'Not found'}")
        return user