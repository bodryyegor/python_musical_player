import os
import sqlite3

class DBManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db_path = os.path.abspath(os.path.join("data", f"user_{self.user_id}.db"))
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Music (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                duration INTEGER
            )
        """)
        self.connection.commit()

    def insert(self, title, artist, duration):
        self.cursor.execute(
            "INSERT INTO Music (title, artist, duration) VALUES (?, ?, ?)",
            (title, artist, duration)
        )
        self.connection.commit()

    def select_all(self):
        self.cursor.execute("SELECT * FROM Music")
        return self.cursor.fetchall()

    def clear_db(self):
        self.cursor.execute("DELETE FROM Music")
        self.connection.commit()

    def filter_by_duration(self, min_time, max_time):
        self.cursor.execute(
            "SELECT * FROM Music WHERE duration >= ? AND duration <= ?", (min_time, max_time)
        )
        return self.cursor.fetchall()
