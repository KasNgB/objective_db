import os
import sqlite3
from db import engine, DB_URL

def verify_database():
    # Check if database file exists
    db_path = "sql/app.db"
    if os.path.exists(db_path):
        print(f"✓ Database file exists at: {os.path.abspath(db_path)}")
        
        # Check file size
        size = os.path.getsize(db_path)
        print(f"✓ Database file size: {size} bytes")
        
        # Try to connect and list tables
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"✓ Tables in database: {[t[0] for t in tables]}")
            
            # Check if our tables exist
            for table_name in ['images', 'analysis']:
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
                result = cursor.fetchone()
                if result:
                    print(f"✓ Table '{table_name}' exists")
                else:
                    print(f"✗ Table '{table_name}' missing")
            
            conn.close()
        except Exception as e:
            print(f"✗ Error accessing database: {e}")
    else:
        print(f"✗ Database file not found at: {os.path.abspath(db_path)}")
    
    print(f"\nSQLAlchemy URL: {DB_URL}")
    print(f"For dadbod, try: sqlite:{os.path.abspath(db_path)}")

if __name__ == "__main__":
    verify_database()
