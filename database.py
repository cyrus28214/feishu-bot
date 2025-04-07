import sqlite3
import lark_oapi as lark

DEFAULT_DB_PATH = 'database/sessions.db'

class Database:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                sender_id TEXT PRIMARY KEY, 
                session TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
            conn.commit()

    def get_session(self, sender_id: str) -> str:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT session FROM sessions WHERE sender_id = ?
                ''', (sender_id,))
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as e:
            lark.logger.error(f"Error getting session for sender_id {sender_id} in accessing database: {e}")
            return None

    def add_session(self, sender_id: str, session: str)-> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO sessions (sender_id, session) VALUES (?, ?)
                ''', (sender_id, session))
                conn.commit()
        except sqlite3.Error as e:
            lark.logger.error(f"Error adding session for sender_id {sender_id} in accessing database: {e}")
            
