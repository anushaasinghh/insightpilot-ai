import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "insightpilot.db")


def _get_conn():
    """Get a database connection. Creates the database file if it doesn't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Create the messages table if it doesn't exist.
    Called once at app startup.
    Schema:
      - id: auto-increment primary key
      - session_id: unique string per user session (uuid4)
      - role: 'user' or 'assistant'
      - content: the message text
      - timestamp: when the message was saved
    """
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT    NOT NULL,
            role       TEXT    NOT NULL,
            content    TEXT    NOT NULL,
            timestamp  TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def save_message(session_id: str, role: str, content: str):
    """
    Save a single message to the database.
    Uses parameterised query (?) to prevent SQL injection.
    """
    conn = _get_conn()
    conn.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()


def load_history(session_id: str) -> list:
    """
    Load all messages for a given session_id, ordered by time.
    Returns a list of dicts: [{'role': 'user', 'content': '...'}, ...]
    """
    conn = _get_conn()
    rows = conn.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,)
    ).fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]


def clear_history(session_id: str):
    """Delete all messages for a session. Used by the 'Clear Chat' button."""
    conn = _get_conn()
    conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()


def get_all_sessions() -> list:
    """
    Return a list of all session IDs and their message counts.
    Useful for debugging and admin views.
    """
    conn = _get_conn()
    rows = conn.execute(
        "SELECT session_id, COUNT(*) as msg_count, MAX(timestamp) as last_active "
        "FROM messages GROUP BY session_id ORDER BY last_active DESC"
    ).fetchall()
    conn.close()
    return [{"session_id": r[0], "msg_count": r[1], "last_active": r[2]} for r in rows]