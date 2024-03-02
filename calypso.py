from agents.econimicWatcherAgent import EconomicWatcher
from agents.economicEventAgent import EconomicEvents
from agents.eventUpdateAgent import UpdateEvents
from agents.todayEventAgent import TodayEventAgent
from agents.upcomingEventAgent import UpcomingEvents
from database_manager.db_manager import DatabaseManager

class Calypso:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.event_update_agent = EconomicEvents(self.db_manager)
        self.econimic_watcher_agent = EconomicWatcher(self.db_manager)
        self.today_event_agent = TodayEventAgent(self.db_manager)
        self.event_update_agent = UpcomingEvents(self.db_manager)
        self.upcoming_event_agent = UpcomingEvents(self.db_manager)

    def run_agents(self):
        # Weekly scraping of the website for new events
        self.weekly_scrape_agent.scrape_website()

        # Update events in the database
        self.event_update_agent.update_events()

        # Analyze events and their potential impact
        self.event_analysis_agent.analyze_events()

        # Notify the user about upcoming events and their importance
        self.user_notification_agent.send_notifications()

if __name__ == "__main__":
    calypso = Calypso()
    calypso.run()
