import os
import sqlite3

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    import psycopg
    PH = "%s"   # Postgres placeholder
else:
    PH = "?"    # SQLite placeholder


def get_connection():
    if DATABASE_URL:
        return psycopg.connect(DATABASE_URL)
    return sqlite3.connect("leaderboard.db")


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    if DATABASE_URL:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                xp INTEGER NOT NULL
            )
        """)
    else:
        cur.execute("""
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
    cur = conn.cursor()
    cur.execute(f"INSERT INTO scores (name, xp) VALUES ({PH}, {PH})", (name, xp))
    conn.commit()
    conn.close()


def get_top_scores(limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT name, xp FROM scores ORDER BY xp DESC LIMIT {PH}", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [{"name": row[0], "xp": row[1]} for row in rows]


def clear_scores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM scores")
    conn.commit()
    conn.close()