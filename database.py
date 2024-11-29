import sqlite3
import os
import pandas as pd
from dotenv import load_dotenv

class AttendedEvent:
    def __init__(self, userId, eventId):
        self.userId = userId
        self.eventId = eventId

    def to_dict(self):
        return {
            'userId': self.userId,
            'eventId': self.eventId
        }
    
class Venue:
    def __init__(self, id, name, cityId):
        self.id = id
        self.name = name
        self.cityId = cityId

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cityId': self.city
        }
    
class Artist:
    def __init__(self, mbid, name, sortName, desambiguation):
        self.mbid = mbid
        self.name = name
        self.sortName = sortName
        self.desambiguation = desambiguation

    def to_dict(self):
        return {
            'mbid': self.mbid,
            'name': self.name,
            'sortName': self.sortName,
            'desambiguation': self.desambiguation
        }
    
class Event:
    def __init__(self, id, versionId, eventDate, lastUpdated, artistMbid, venueId):
        self.id = id
        self.versionId = versionId
        self.eventDate = eventDate
        self.lastUpdated = lastUpdated
        self.artistMbid = artistMbid
        self.venueId = venueId

    def to_dict(self):
        return {
            'id': self.id,
            'versionId': self.versionId,
            'eventDate': self.eventDate,
            'lastUpdated': self.lastUpdated,
            'artistMbid': self.artistMbid,
            'venueId': self.venueId
        }
    
def get_database_path():
    load_dotenv()
    return os.getenv('DATABASE_URL')

def create_table_events():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        versionId TEXT,
        eventDate DATE,
        lastUpdated DATETIME,
        artistMbid TEXT,
        venueId TEXT
    )
    ''')
    conn.commit()
    conn.close()

def create_table_artists():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS artists (
        mbid TEXT PRIMARY KEY,
        name TEXT,
        sortName TEXT,
        desambiguation TEXT
    )
    ''')
    conn.commit()
    conn.close()

def is_table_events_exists():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    result = c.fetchone()
    conn.close()
    return result is not None

def create_table_venues():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS venues (
        id TEXT PRIMARY KEY,
        name TEXT,
        cityId TEXT
    )
    ''')
    conn.commit()
    conn.close()

def create_table_attended_events():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS attended_events (
        userId TEXT NOT NULL,
        eventId TEXT NOT NULL
    )
    ''')
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

def add_event(conn, event : Event):
    c = conn.cursor()
    c.execute('''
    INSERT INTO events (id, versionId, eventDate, lastUpdated, artistMbid, venueId)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (event.id, event.versionId, event.eventDate, event.lastUpdated, event.artistMbid, event.venueId))
    conn.commit()

def add_artist(conn, artist : Artist):
    c = conn.cursor()
    c.execute('''
    INSERT OR IGNORE INTO artists (mbid, name, sortName, desambiguation)
    VALUES (?, ?, ?, ?)
    ''', (artist.mbid, artist.name, artist.sortName, artist.desambiguation))
    conn.commit()

def add_venue(conn, venue : Venue):
    c = conn.cursor()
    c.execute('''
    INSERT OR IGNORE INTO venues (id, name, cityId)
    VALUES (?, ?, ?)
    ''', (venue.id, venue.name, venue.cityId))
    conn.commit()

def add_attended_event(conn, attended_event : AttendedEvent):
    c = conn.cursor()
    c.execute('''
    INSERT INTO attended_events (userId, eventId)
    VALUES (?, ?)
    ''', (attended_event.userId, attended_event.eventId))
    conn.commit()

def save_all_events_to_sqlite(df):
    userId = "IchabodCrane"
    drop_table_events()
    drop_table_artists()
    drop_table_venues()
    drop_table_attended_events()
    create_table_events()
    create_table_artists()
    create_table_venues()
    create_table_attended_events()
    conn = sqlite3.connect(get_database_path())
    for row in df.itertuples(index=False):  
        event_date = pd.to_datetime(row.eventDate).strftime('%Y-%m-%d')
        last_updated = pd.to_datetime(row.lastUpdated).strftime('%Y-%m-%d %H:%M:%S')
        add_artist(conn, Artist(row._5, row._6, row._7, row._8))
        add_venue(conn, Venue(row._10, row._11, row._12))
        add_event(conn, Event(row.id, row.versionId, event_date, last_updated, row._5,row._10))
        add_attended_event(conn, AttendedEvent(userId, row.id))
    conn.close()

def drop_table_events():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    if c.fetchone():
        c.execute('DROP TABLE events')
        conn.commit()
    conn.close()

def drop_table_artists():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='artists'")
    if c.fetchone():
        c.execute('DROP TABLE artists')
        conn.commit()
    conn.close()

def drop_table_venues():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='venues'")
    if c.fetchone():
        c.execute('DROP TABLE venues')
        conn.commit()
    conn.close()

def drop_table_attended_events():
    conn = sqlite3.connect(get_database_path())
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='attended_events'")
    if c.fetchone():
        c.execute('DROP TABLE attended_events')
        conn.commit()
    conn.close()

