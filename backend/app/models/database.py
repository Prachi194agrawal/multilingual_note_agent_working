import sqlite3
import json
from datetime import datetime

DATABASE_PATH = "transcripts.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transcriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        language TEXT,
        transcript TEXT NOT NULL,
        summary TEXT,
        action_items TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def save_transcription(filename, language, transcript, summary="", action_items=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if action_items is None:
        action_items = []
    
    cursor.execute(
        "INSERT INTO transcriptions (filename, language, transcript, summary, action_items) VALUES (?, ?, ?, ?, ?)",
        (filename, language, transcript, summary, json.dumps(action_items))
    )
    
    transcription_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return transcription_id

def get_transcription(transcription_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transcriptions WHERE id = ?", (transcription_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return dict(row)
    return None

def search_transcriptions(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM transcriptions WHERE transcript LIKE ? OR summary LIKE ?",
        (f"%{query}%", f"%{query}%")
    )
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]

def get_all_transcriptions():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transcriptions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]