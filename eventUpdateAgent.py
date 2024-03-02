import sqlite3
from datetime import datetime
from database_manager.db_manager import DatabaseManager

class UpdateEvents:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_table(self):
        schema = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            currency TEXT NOT NULL,
            impact INTEGER,
            event TEXT NOT NULL,
            actual TEXT,
            forecast TEXT,
            previous TEXT,
            UNIQUE(date, time, currency, event)
        '''
        self.db_manager.create_table('upcoming_events', schema)

    def insert_upcoming_events(self, events):
        for event in events:
            columns = list(event.keys())
            values = list(event.values())
            self.db_manager.insert_item('upcoming_events', columns, values)

    def delete_past_events(self):
        sql = 'DELETE FROM upcoming_events WHERE date < ? OR (date = ? AND time < ?)'
        params = (datetime.now().strftime('%A, %B %d, %Y'), datetime.now().strftime('%A, %B %d, %Y'), datetime.now().strftime('%H:%M'))
        self.db_manager.execute_sql(sql, params)
        self.db_manager.commit()

    def update(self, events):
        self.delete_past_events()
        self.insert_upcoming_events(events)
