import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_utils import get_db_connection, update_knowledge_base

def main():
    conn = get_db_connection()
    update_knowledge_base(conn)
    conn.close()

if __name__ == "__main__":
    main()