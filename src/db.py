import pyodbc
import time
from src.exceptions import DatabaseError
from src.logger import app_logger

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self, retries=3, delay=2):
        attempt = 0
        while attempt < retries:
            try:
                self.connection = pyodbc.connect(
                    "Driver={ODBC Driver 17 for SQL Server};"
                    "Server=DESKTOP-55B3BF3\\SQLEXPRESS;"
                    "Database=EcommerceDB;"
                    "Trusted_Connection=yes;"
                )
                app_logger.info("Connected to SQL Server!")
                return
            except Exception as e:
                attempt += 1
                app_logger.error(f"Database connection error (Attempt {attempt}/{retries}): {e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    raise DatabaseError("Failed to connect to database after multiple attempts.", e)

    def execute(self, query, params=None, fetch=False):
        """Execute a query with error handling."""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                rows = cursor.fetchall()
                cursor.close()
                return rows
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Exception as e:
            app_logger.error(f"Query Execution Error: {e} | Query: {query}")
            raise DatabaseError("Failed to execute query.", e)

db = Database()
