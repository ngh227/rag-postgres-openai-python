import os
import psycopg2
from psycopg2.extras import RealDictCursor

from scraper import get_processed_data
from dotenv import load_dotenv
import os

load_dotenv()


import os
import psycopg2

# Get database credentials from environment variables
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

connection = psycopg2.connect(
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)

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

def update_knowledge_base(conn):
    df = get_processed_data()
    with conn.cursor() as cur:
        for _, row in df.iterrows():
            cur.execute(
                "INSERT INTO knowledge_base (title, content) VALUES (%s, %s) ON CONFLICT (title) DO UPDATE SET content = EXCLUDED.content",
                (row['title'], row['content'])
            )
    conn.commit()
    print("Knowledge base updated successfully!")

# Add this function to retrieve relevant information
def get_relevant_info(conn, query):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT content FROM knowledge_base WHERE content ILIKE %s",
            ('%' + query + '%',)
        )
        results = cur.fetchall()
    return ' '.join([r[0] for r in results])

# Modify your existing init_db function to create the knowledge_base table
def init_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id SERIAL PRIMARY KEY,
            user_query TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id SERIAL PRIMARY KEY,
            title TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    conn.commit()


def get_db():
    return db
