import sqlite3
from database import get_database_path
import uuid
import os

def create_table_users():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT UNIQUE,
        date_created TEXT,
        date_modified TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_user(name):
    user_id = str(uuid.uuid4())
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute('''
    INSERT INTO users (id, name, date_created, date_modified)
    VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    ''', (user_id, name))
    conn.commit()
    conn.close()

def is_table_users_exists():
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = c.fetchone()
    conn.close()
    return result is not None

def get_user_name():
    db_path = get_database_path()
    db_dir = os.path.dirname(db_path)
    
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    if not is_table_users_exists():
        return None
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT name FROM users')
    result = c.fetchone()
    conn.close()
    return result[0] if result else None