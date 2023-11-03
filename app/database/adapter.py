# Sqlite3 Database Adapter
import sqlite3


class Sqlite3Adapter:
    def __init__(self, database):
        self.database = database
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def fetch(self, query):
        # If table doesn't exist, return empty list
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError:
            return []

    def close(self):
        self.connection.close()
