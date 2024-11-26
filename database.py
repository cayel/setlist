import sqlite3
import os
import uuid
import pandas as pd

DATA_FILE = 'attended_events.setlist'

def get_database_path():
    local_storage_path = os.path.expanduser('~/setlist')
    os.makedirs(local_storage_path, exist_ok=True)
    db_path = os.path.join(local_storage_path, 'setlist.db')
    return db_path

def get_data_file_path():
    local_storage_path = os.path.expanduser('~/setlist')
    os.makedirs(local_storage_path, exist_ok=True)
    return os.path.join(local_storage_path, DATA_FILE)

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

def is_table_users_exists():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    result = c.fetchone()
    conn.close()
    return result is not None

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

def get_user_name():
    if not is_table_users_exists():
        return None
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute('SELECT name FROM users')
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def delete_user(name):
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def update_user_date_modified(name):
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute('''
    UPDATE users
    SET date_modified = CURRENT_TIMESTAMP
    WHERE name = ?
    ''', (name,))
    conn.commit()
    conn.close()

def load_all_events():
    if not os.path.exists(get_data_file_path()):
        return pd.DataFrame()
    else:
        df = pd.read_csv(get_data_file_path())
        # convert eventDate to datetime
        df['eventDate'] = pd.to_datetime(df['eventDate'])
        return df
    
def save_all_events(df):
    df.to_csv(get_data_file_path(), index=False)