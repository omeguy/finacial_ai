from webscraper.web_scraper import Scraper
from db_manager import DatabaseManager

    
class EconomicEvents:
    def __init__(self, scraper, db_manager):
        self.scraper = scraper
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
        self.db_manager.create_table('economic_events', schema)

    def fetch_events(self):
        return self.scraper.scrape()


    def update_events(self):
        events = self.fetch_events()
        for event in events:
            columns = list(event.keys())
            values = list(event.values())
            self.db_manager.insert_item('economic_events', columns, values)
