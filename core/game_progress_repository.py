import json
import os
import sqlite3

from core.game_progress import game_initial_data
from core.user_progress_status import UserProgressStatus


class GameProgressRepository:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._db_name = kwargs.get('db_name', 'game_progress_db.sqlite3')
            cls._instance.create_database()
            cls._instance.preload_current_data()
        return cls._instance

    def create_database(self):
        if not os.path.exists(self._db_name):
            with open(self._db_name, 'w'):
                pass
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY,
                    progress_data TEXT
                )
            ''')
        cursor.execute('SELECT COUNT(*) FROM user_progress')
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute('INSERT INTO user_progress (progress_data) VALUES (?)', (json.dumps(game_initial_data),))
            conn.commit()
        conn.close()

    def preload_current_data(self):
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT progress_data FROM user_progress ORDER BY id DESC LIMIT 1')
        data = cursor.fetchone()
        conn.close()
        if data:
            self._current_progress = json.loads(data[0])
        else:
            self._current_progress = None

    def update_progress(self, progress_data):
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_progress (progress_data) VALUES (?)', (json.dumps(progress_data),))
        conn.commit()
        conn.close()

    def get_current_progress(self):
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT progress_data FROM user_progress ORDER BY id DESC LIMIT 1')
        data = cursor.fetchone()
        conn.close()
        if data:
            return json.loads(data[0])
        else:
            return None

    def progress_landing_tutorial(self):
        self._current_progress["landing_tutorials"]["current"] += 1
        self.update_progress(self._current_progress)

    def progress_level_tutorials(self):
        self._current_progress["level_tutorials"]["current"] += 1
        self.update_progress(self._current_progress)