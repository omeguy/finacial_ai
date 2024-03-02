from datetime import datetime
from finacial_ai.database_manager.db_manager import DatabaseManager
import logging

logging.basicConfig(filename='agent.log', level=logging.ERROR)


class TodayEventAgent:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_table(self):
        """
        Creates the 'today_events' table in the database.
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
            self.db_manager.create_table('today_events', schema)
        except Exception as e:
            logging.error(f'TodayEventAgent: Error creating table: {str(e)}')

    def fetch_events(self):
        """
        Fetches the economic events for the current date from the 'economic_events' table.
        Returns:
            list: List of tuples containing the fetched economic events.
        """
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            sql = 'SELECT * FROM economic_events WHERE date = ?'
            self.db_manager.execute_sql(sql, (today,))
            return self.db_manager.fetchall()
        except Exception as e:
            logging.error(f'TodayEventAgent: Error fetching events: {str(e)}')
            return []

    def insert_today_events(self, events):
        """
        Inserts the fetched economic events into the 'today_events' table.
        Args:
            events (list): List of tuples containing the economic events.
        """
        columns = ['id', 'date', 'time', 'currency', 'impact', 'event', 'actual', 'forecast', 'previous']
        try:
            for event in events:
                values = list(event)
                self.db_manager.insert_item('today_events', columns, values)
        except Exception as e:
            logging.error(f'TodayEventAgent: Error inserting events: {str(e)}')

    def delete_past_events(self):
        """
        Deletes the past events from the 'today_events' table.
        """
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            sql = 'DELETE FROM today_events WHERE date < ?'
            params = (today,)
            self.db_manager.execute_sql(sql, params)
            self.db_manager.commit()
        except Exception as e:
            logging.error(f'TodayEventAgent: Error deleting past events: {str(e)}')

    def run(self):
        """
        Executes the agent by creating the table, fetching events, deleting past events, and inserting today's events.
        """
        self.create_table()
        events = self.fetch_events()
        self.delete_past_events()
        self.insert_today_events(events)


if __name__ == "__main__":
    db_manager = DatabaseManager('financial_ai.db')
    today_event_agent = TodayEventAgent(db_manager)
    today_event_agent.run()
