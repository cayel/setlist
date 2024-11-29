import sqlite3
import pandas as pd
from database import get_database_path

def drop_table_events():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    if c.fetchone():
        c.execute('DROP TABLE events')
        conn.commit()
    conn.close()

def load_attended_events(userId):
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check if the attended_events table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='attended_events'")
    if not c.fetchone():
        conn.close()
        return pd.DataFrame(columns=['eventId', 'eventDate', 'artists.name', 'venues.name'])
    
    c.execute('''
    SELECT eventId, events.eventDate, artists.name, venues.name
    FROM attended_events
    JOIN events ON attended_events.eventId = events.id
    JOIN artists ON events.artistMbid = artists.mbid
    JOIN venues ON events.venueId = venues.id
    WHERE attended_events.userId = ?
    ''', (userId,))
    result = c.fetchall()
    conn.close()
    df = pd.DataFrame(result, columns=['eventId', 'eventDate', 'artists.name', 'venues.name'])
    return df