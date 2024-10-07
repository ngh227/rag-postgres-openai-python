import os

import psycopg2
from psycopg2.extras import RealDictCursor


class DBConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def disconnect(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("PostgreSQL connection is closed")

    def execute(self, query, params=None):
        if not self.conn or self.conn.closed:
            self.connect()
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)
            self.conn.rollback()

    def fetch_one(self, query, params=None):
        if not self.conn or self.conn.closed:
            self.connect()
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except (Exception, psycopg2.Error) as error:
            print("Error fetching data:", error)

    def fetch_all(self, query, params=None):
        if not self.conn or self.conn.closed:
            self.connect()
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error fetching data:", error)


db = DBConnection()


def get_db():
    return db
