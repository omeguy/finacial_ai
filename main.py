from web_scraper import Scraper

url = 'https://www.investing.com/economic-calendar/'

def main():
    # Create an instance of the WebScraper class
    scraper = Scraper(url)

    # Start the scraping process
    scraper.scrape()


if __name__ == "__main__":
    main()
