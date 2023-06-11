from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class Scraper:
    def __init__(self, url):
        self.url = url
        options = Options()
        options.headless = False
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    def fetch_page(self):
        self.driver.get(self.url)
        time.sleep(5)

        # Click the 'This Week' button using JavaScript
        self.driver.execute_script("document.getElementById('timeFrame_thisWeek').click();")

        time.sleep(5)

        html = self.driver.page_source
        self.driver.quit()
        return html


    def extract_table_data(self, table):
        data = []
        
        rows = table.find_all('tr', class_='js-event-item')
        
        for row in rows:
            date = row.find_previous('td', class_='theDay').get_text(strip=True)
            time = row.find('td', class_='first left time js-time').get_text(strip=True)


            currency = row.find('td', class_='left flagCur noWrap').get_text(strip=True)
            impact = len(row.find_all('i', class_='grayFullBullishIcon'))
            event = row.find('td', class_='left event').get_text(strip=True)
            actual = row.select_one('td.bold.act').get_text(strip=True) if row.select_one('td.bold.act') else None
            forecast = row.select_one('td.fore').get_text(strip=True) if row.select_one('td.fore') else None
            previous = row.select_one('td.prev').get_text(strip=True) if row.select_one('td.prev') else None

            row_data = {
                'Date': date,
                'Time': time,
                'Currency': currency,
                'Impact': impact,
                'Event': event,
                'Actual': actual,
                'Forecast': forecast,
                'Previous': previous
            }

            data.append(row_data)
        
        return data
    

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find(id='economicCalendarData')
        table_data = self.extract_table_data(table)
        return table_data


    def scrape(self):
        html = self.fetch_page()
        table_data = self.parse_page(html)

        # Write data to JSON
        with open('table_data.json', 'w') as jsonfile:
            json.dump(table_data, jsonfile, indent=4)

        print(table_data)


