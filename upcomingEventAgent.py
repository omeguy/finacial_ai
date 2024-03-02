from datetime import datetime
from finacial_ai.database_manager.db_manager import DatabaseManager
import logging

logging.basicConfig(filename='agent.log', level=logging.ERROR)


class UpcomingEvents:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_table(self):
        """
        Creates the 'upcoming_events' table in the database.
        """
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
        try:
            self.db_manager.create_table('upcoming_events', schema)
        except Exception as e:
            logging.error(f'UpcomingEvents: Error creating table: {str(e)}')

    def fetch_events(self):
        """
        Fetches the upcoming economic events from the 'economic_events' table.
        Returns:
            list: List of tuples containing the upcoming economic events.
        """
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            now = datetime.now().strftime('%H:%M:%S')
            sql = '''
                SELECT * FROM economic_events
                WHERE date > ? OR (date = ? AND time > ?)
            '''
            self.db_manager.execute_sql(sql, (today, today, now))
            return self.db_manager.fetchall()
        except Exception as e:
            logging.error(f'UpcomingEvents: Error fetching events: {str(e)}')
            return []

    def insert_upcoming_events(self, events):
        """
        Inserts the upcoming economic events into the 'upcoming_events' table.
        Args:
            events (list): List of tuples containing the upcoming economic events.
        """
        columns = ['id', 'date', 'time', 'currency', 'impact', 'event', 'actual', 'forecast', 'previous']
        try:
            for event in events:
                values = list(event)
                self.db_manager.insert_item('upcoming_events', columns, values)
        except Exception as e:
            logging.error(f'UpcomingEvents: Error inserting events: {str(e)}')

    def delete_past_events(self):
        """
        Deletes the past events from the 'upcoming_events' table.
        """
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            now = datetime.now().strftime('%H:%M:%S')
            sql = 'DELETE FROM upcoming_events WHERE date < ? OR (date = ? AND time < ?)'
            params = (today, today, now)
            self.db_manager.execute_sql(sql, params)
            self.db_manager.commit()
        except Exception as e:
            logging.error(f'UpcomingEvents: Error deleting past events: {str(e)}')

    def run(self):
        """
        Executes the agent by creating the table, fetching upcoming events, deleting past events, and inserting upcoming events.
        """
        self.create_table()
        events = self.fetch_events()
        self.delete_past_events()
        self.insert_upcoming_events(events)


if __name__ == "__main__":
    db_manager = DatabaseManager('financial_ai.db')
    upcoming_events = UpcomingEvents(db_manager)
    upcoming_events.run()
