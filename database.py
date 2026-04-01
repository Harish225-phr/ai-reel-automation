"""
SQLite Database for AI Reel Generator
Stores video generation history, progress, and metadata
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from threading import Lock

DB_PATH = Path(__file__).parent / "reel_generator.db"
db_lock = Lock()


def init_database():
    """Initialize database with required tables"""
    with db_lock:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Videos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                prompt TEXT NOT NULL,
                language TEXT NOT NULL,
                status TEXT NOT NULL,
                video_file TEXT,
                duration TEXT,
                file_size TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                error_message TEXT
            )
        """)
        
        # Progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                step TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos (id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("[DB] Database initialized")


def create_video_record(video_id: str, prompt: str, language: str):
    """Create a new video generation record"""
    with db_lock:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO videos (id, prompt, language, status)
            VALUES (?, ?, ?, 'processing')
        """, (video_id, prompt, language))
        
        conn.commit()
        conn.close()
        print(f"[DB] Created record: {video_id}")


def update_video_status(video_id: str, status: str, video_file: str = None, 
                       duration: str = None, file_size: str = None, 
                       error_message: str = None):
    """Update video generation status"""
    with db_lock:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        completed_at = datetime.now() if status in ['complete', 'error'] else None
        
        cursor.execute("""
            UPDATE videos 
            SET status = ?, video_file = ?, duration = ?, file_size = ?, 
                error_message = ?, completed_at = ?
            WHERE id = ?
        """, (status, video_file, duration, file_size, error_message, completed_at, video_id))
        
        conn.commit()
        conn.close()
        print(f"[DB] Updated {video_id}: {status}")


def add_progress(video_id: str, step: str, status: str, message: str = None):
    """Add progress update for a video"""
    with db_lock:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO progress (video_id, step, status, message)
            VALUES (?, ?, ?, ?)
        """, (video_id, step, status, message))
        
        conn.commit()
        conn.close()


def get_video(video_id: str):
    """Get video record by ID"""
    with db_lock:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None


def get_all_videos(limit: int = 50):
    """Get recent video history"""
    with db_lock:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM videos 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


def get_video_progress(video_id: str):
    """Get all progress updates for a video"""
    with db_lock:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM progress 
            WHERE video_id = ? 
            ORDER BY timestamp ASC
        """, (video_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


if __name__ == '__main__':
    init_database()
    print("[DB] Database ready!")
