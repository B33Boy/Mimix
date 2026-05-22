# bot/db.py
import random
import sqlite3
from pathlib import Path

DB_PATH = Path("data/messages.db")


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                content TEXT NOT NULL,
                channel TEXT,
                timestamp TEXT
            )
        """)


def save_messages(messages: list[dict]):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO messages (author, content, channel, timestamp) VALUES (:author, :content, :channel, :timestamp)",
            messages
        )


def get_style_samples(author: str, k: int = 20) -> list[str]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT content FROM messages WHERE author = ? AND length(content) > 5",
            (author,)
        ).fetchall()
    # Random sample is better than ordered — more style diversity
    sample = random.sample(rows, min(k, len(rows)))
    return [row[0] for row in sample]
