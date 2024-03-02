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

    def create_table(self, table_name, schema):
        self.execute_sql(f'''
            CREATE TABLE IF NOT EXISTS {table_name}(
                {schema}
            )
        ''')
        self.commit()

    def insert_item(self, table_name, columns, values):
        columns_str = ', '.join(columns)
        placeholders = ', '.join('?' for _ in values)
        self.execute_sql(f'''
            INSERT OR IGNORE INTO {table_name}({columns_str})
            VALUES({placeholders})
        ''', values)
        self.commit()

    def get_data(self, table_name, where=None):
        """
        Fetches data from a specified table.
        Optionally, a WHERE clause can be provided to filter the results.
        :param table_name: Name of the table to fetch data from
        :param where: Optional WHERE clause to filter results (string)
        :return: The fetched data
        """
        if where:
            sql = f"SELECT * FROM {table_name} WHERE {where}"
        else:
            sql = f"SELECT * FROM {table_name}"

        self.execute_sql(sql)
        return self.fetchall()


    def get_items(self, table_name):
        self.execute_sql(f'SELECT * FROM {table_name}')
        return self.fetchall()

    def execute_sql(self, sql, params=None):
        self.cursor.execute(sql, params if params else [])

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.cursor.fetchall()
