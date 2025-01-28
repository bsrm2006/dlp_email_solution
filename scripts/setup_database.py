import os
import sqlite3
from backend.config import DLPConfig

def initialize_database():
    """
    Initialize SQLite database for DLP solution
    """
    db_path = DLPConfig.DATABASE_CONFIG['path']
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create exceptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exceptions (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            value TEXT NOT NULL,
            expiration DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            level TEXT,
            message TEXT,
            details TEXT
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database initialized at {db_path}")

if __name__ == '__main__':
    initialize_database()