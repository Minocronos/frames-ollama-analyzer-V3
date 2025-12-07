import sqlite3
import datetime
import os
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "history.db"):
        """Initialize the database manager with a file path."""
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        """Create a database connection."""
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Create the necessary tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create analyses table with rating and comment
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                image_name TEXT,
                mode TEXT,
                style TEXT,
                model TEXT,
                prompt_content TEXT,
                rating INTEGER DEFAULT 0,
                comment TEXT DEFAULT ""
            )
        ''')
        
        # Migration: Check if columns exist (in case DB was already created without them)
        try:
            cursor.execute('ALTER TABLE analyses ADD COLUMN rating INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass # Column likely exists
            
        try:
            cursor.execute('ALTER TABLE analyses ADD COLUMN comment TEXT DEFAULT ""')
        except sqlite3.OperationalError:
            pass # Column likely exists
        
        conn.commit()
        conn.close()

    def save_analysis(self, image_name: str, mode: str, prompt_content: str, 
                     style: Optional[str] = None, model: str = "Unknown",
                     rating: int = 0, comment: str = ""):
        """
        Save a new analysis result to the database with user feedback.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO analyses (timestamp, image_name, mode, style, model, prompt_content, rating, comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, image_name, mode, style, model, prompt_content, rating, comment))
        
        conn.commit()
        conn.close()
        print(f"✅ Analysis saved to DB: {image_name} (Rating: {rating}/5)")

    def get_history(self, limit: int = 50) -> List[Dict]:
        """
        Retrieve the most recent analyses.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analyses 
            ORDER BY id DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append(dict(row))
            
        return history

    def delete_analysis(self, analysis_id: int):
        """
        Delete a specific analysis by ID.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM analyses WHERE id = ?', (analysis_id,))
        
        conn.commit()
        conn.close()
        print(f"🗑️ Deleted analysis ID: {analysis_id}")
