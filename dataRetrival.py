from finacial_ai.database_manager.db_manager import DatabaseManager
from datetime import datetime, timedelta

class DataRetriever:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_today_events(self):
        today = datetime.now().strftime('%Y-%m-%d')
        return self.db_manager.get_data('economic_events', f"date = '{today}'")

    def get_today_upcoming_events(self):
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now().strftime('%H:%M:%S')
        return self.db_manager.get_data('economic_events', f"date = '{today}' AND time > '{now}'")

    def get_today_past_events(self):
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now().strftime('%H:%M:%S')
        return self.db_manager.get_data('economic_events', f"date = '{today}' AND time <= '{now}'")

    def get_today_news(self):
        today = datetime.now().strftime('%Y-%m-%d')
        return self.db_manager.get_data('news', f"date = '{today}'")

    def get_week_events(self):
        today = datetime.now().strftime('%Y-%m-%d')
        one_week_later = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        return self.db_manager.get_data('economic_events', f"date >= '{today}' AND date <= '{one_week_later}'")

    def get_future_events(self, days):
        today = datetime.now().strftime('%Y-%m-%d')
        future_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        return self.db_manager.get_data('economic_events', f"date >= '{today}' AND date <= '{future_date}'")

if __name__ == "__main__":
    db_manager = DatabaseManager('financial_ai.db')
    data_retriever = DataRetriever(db_manager)


    # Get events for the next three days and print them
    future_events = data_retriever.get_future_events(3)
    print("Economic events for the next three days:")
    for event in future_events:
        print(event)
