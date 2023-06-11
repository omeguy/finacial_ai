import sqlite3
from sqlite3 import Error


class DatabaseManager:
    def __init__(self, db_name=None):
        self.conn = None
        self.cursor = None
        if db_name:
            self.open(db_name)

    def open(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except Error as e:
            print(e)

    def create_table(self):
        self.execute_sql('''
            CREATE TABLE IF NOT EXISTS news(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                link TEXT NOT NULL,
                posted_time TEXT,
                UNIQUE(title, link)
            )
        ''')
        self.commit()

    def insert_news_item(self, title, link, posted_time):
        self.execute_sql('''
            INSERT OR IGNORE INTO news(title, link, posted_time)
            VALUES(?, ?, ?)
        ''', (title, link, posted_time))
        self.commit()

    def get_news_items(self):
        self.execute_sql('SELECT * FROM news')
        return self.fetchall()

    def execute_sql(self, sql, params=None):
        self.cursor.execute(sql, params if params else [])

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.cursor.fetchall()
