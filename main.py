from web_scraper import Scraper
from db_manager import DatabaseManager
from economic_events import EconomicEvents

def main():
    db_manager = DatabaseManager('financial_ai.db')
    scraper = Scraper('https://www.investing.com/economic-calendar/')
    economic_events = EconomicEvents(scraper, db_manager)

    economic_events.create_table()
    economic_events.update_events()
if __name__ == "__main__":
    main()
