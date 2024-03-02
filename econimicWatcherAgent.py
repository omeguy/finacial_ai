from datetime import datetime
from finacial_ai.database_manager.db_manager import DatabaseManager
import schedule
import time

class EconomicWatcher:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def fetch_upcoming_events(self):
        # Fetch events from the today_events table that are supposed to happen in the current minute
        now = datetime.now().strftime('%H:%M')
        sql = '''
            SELECT * FROM today_events
            WHERE time = ?
        '''
        self.db_manager.execute_sql(sql, (now,))
        return self.db_manager.fetchall()
    
    def delete_processed_events(self, events):
        sql = 'DELETE FROM today_events WHERE id = ?'
        for event in events:
            self.db_manager.execute_sql(sql, (event['id'],))
        self.db_manager.commit()


    def run(self):
        # Fetch today's events
        events = self.fetch_upcoming_events()

        # If there are any events, process them and print the events
        if events:
            for event in events:
                print(event)
                # TODO: Do something with the event here, e.g., sending a notification or doing some analysis

            # After processing the events, delete them from the database
            self.delete_processed_events(events)


if __name__ == "__main__":
    db_manager = DatabaseManager('financial_ai.db')
    watcher = EconomicWatcher(db_manager)
    schedule.every(1).minutes.do(watcher.run)

    while True:
        schedule.run_pending()
        time.sleep(1)
