import logging
from finacial_ai.webscraper.web_scraper import WeeklyScraper
from finacial_ai.database_manager.db_manager import DatabaseManager
from datetime import datetime, timedelta

logging.basicConfig(filename='scraper.log', level=logging.ERROR)


class WeeklyEconomicEvents:
    def __init__(self, scraper, db_manager):
        self.weekly_scraper = scraper
        self.db_manager = db_manager

    def create_table(self):
        """
        Creates the 'economic_events' table in the database.
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
            self.db_manager.create_table('economic_events', schema)
            logging.info('Weekly: Table "economic_events" created successfully.')
        except Exception as e:
            logging.error(f'Weekly: Error creating table: {str(e)}')

    def fetch_events(self):
        """
        Fetches the economic events by scraping the website using the WeeklyScraper.
        Returns:
            list: List of dictionaries containing the scraped economic events.
        """
        try:
            html = self.weekly_scraper.fetch_page()
            table_data = self.weekly_scraper.parse_weekly_events_page(html)
            return table_data
        except Exception as e:
            logging.error(f'Weekly: Error fetching events: {str(e)}')
            return []

    @staticmethod
    def convert_date(date_str):
        """
        Converts the date string to the desired format.
        Args:
            date_str (str): Date string to be converted.
        Returns:
            str: Converted date string in the format '%Y-%m-%d'.
        """
        try:
            date = datetime.strptime(date_str, '%A, %B %d, %Y')
            return date.strftime('%Y-%m-%d')
        except Exception as e:
            logging.error(f'Weekly: Error converting date: {str(e)}')
            return ''

    @staticmethod
    def convert_time(time_str):
        """
        Converts the time string to the desired format.
        Args:
            time_str (str): Time string to be converted.
        Returns:
            str: Converted time string in the format '%H:%M:%S'.
        """
        try:
            if time_str.lower() == 'tentative':
                return time_str
            else:
                time = datetime.strptime(time_str, '%H:%M')
                return time.strftime('%H:%M:%S')
        except Exception as e:
            logging.error(f'Weekly: Error converting time: {str(e)}')
            return ''

    def update_events(self):
        events = self.fetch_events()
        for event in events:
            try:
                # Convert the date and time before inserting the event into the database
                event['Date'] = self.convert_date(event['Date'])
                event['Time'] = self.convert_time(event['Time'])

                columns = list(event.keys())
                values = list(event.values())
                self.db_manager.insert_item('economic_events', columns, values)
            except Exception as e:
                logging.error(f'Weekly: Error updating events: {str(e)}')

    def run(self):
        self.create_table()
        self.update_events()


if __name__ == "__main__":
    db_manager = DatabaseManager('financial_ai.db')  # Replace 'financial_ai.db' with the path to your SQLite database file
    scraper = WeeklyScraper('https://www.investing.com/economic-calendar/')
    weekly_events = WeeklyEconomicEvents(scraper, db_manager)
    weekly_events.run()
