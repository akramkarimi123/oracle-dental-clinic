# database.py
import oracledb

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = oracledb.connect(
                user="system",
                password="hikmat",
                dsn="localhost:1521/free"
            )
            print("Connected to Oracle DB")
        except Exception as e:
            print(f"Connection failed: {e}")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            print(f" Query Error: {e}")
            return None

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            rows = cursor.fetchall()
            cursor.close()
            return rows
        return []

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()

