import pyodbc

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=DESKTOP-BNC6SIM\\SQLEXPRESS;"
                "Database=EcommerceDB;"
                "Trusted_Connection=yes;"
            )
            print("Connected to SQL Server!")
        except Exception as e:
            print("Database connection error:", e)

    def execute(self, query, params=None, fetch=False):
        """Execute a query.

        fetch=True for SELECT statements to return rows
        fetch=False for INSERT/UPDATE/DELETE statements
        """
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
            print("Query Execution Error:", e)
            return None

db = Database()
