import sqlite3
from datetime import date

DB_PATH = "data/habits.db"

def init_db():
    """Initialize the database and create tables if not exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create habits table
    c.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Create entries table
    c.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            habit_id INTEGER,
            date TEXT,
            PRIMARY KEY (habit_id, date),
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    """)

    conn.commit()
    conn.close()

def save_habits(habits: list[str]):
    """Save new habits to the database."""
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for habit in habits:
        # Avoid duplicate habits
        c.execute("SELECT * FROM habits WHERE name = ?", (habit,))
        if not c.fetchone():
            c.execute("INSERT INTO habits (name, created_at) VALUES (?, ?)", (habit, today))

    conn.commit()
    conn.close()

def get_today_habits():
    """Get all habits with today's completion status."""
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT h.id, h.name,
        CASE WHEN e.date IS NOT NULL THEN 1 ELSE 0 END as done
        FROM habits h
        LEFT JOIN entries e ON h.id = e.habit_id AND e.date = ?
    """, (today,))

    results = c.fetchall()
    conn.close()
    return results  # List of (habit_id, habit_text, done)

def mark_habit_done(habit_id: int, day: str):
    """Mark a habit as done for today."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT OR IGNORE INTO entries (habit_id, date)
        VALUES (?, ?)
    """, (habit_id, day))

    conn.commit()
    conn.close()

def get_habit_status(habit_id: int, day: str) -> bool:
    """Check if a habit is marked done on a given date."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM entries WHERE habit_id = ? AND date = ?", (habit_id, day))
    result = c.fetchone()

    conn.close()
    return result is not None