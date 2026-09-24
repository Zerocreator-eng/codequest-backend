import sqlite3

DB_FILE = "leaderboard.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """Creates the scores table if it doesn't exist yet. Safe to call every startup."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            xp INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_score(name: str, xp: int):
    conn = get_connection()
    conn.execute("INSERT INTO scores (name, xp) VALUES (?, ?)", (name, xp))
    conn.commit()
    conn.close()


def get_top_scores(limit: int = 10):
    conn = get_connection()
    rows = conn.execute(
        "SELECT name, xp FROM scores ORDER BY xp DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [{"name": row["name"], "xp": row["xp"]} for row in rows]
    
def clear_scores():
    conn = get_connection()
    conn.execute("DELETE FROM scores")
    conn.commit()
    conn.close()
