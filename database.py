import sqlite3
from pathlib import Path
from models import ResearchItem

# Use Pathlib to get directory positions
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "research_radar.db"

class DatabaseManager:
    """Class containing all functions related to 
    database management"""

    # Create data dir if it doesn't exist and call create_tables()
    def __init__(self, db_path = DB_PATH):
        self.db_path = db_path
        DATA_DIR.mkdir(exist_ok=True)
        self.create_tables()

    # Quick function to connect to the SQL database
    def connect(self):
        return sqlite3.connect(self.db_path)
    
    # Create a table if one doesn't exist already
    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            table_name = 'items'
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))

            if cursor.fetchone():
                print("Table exists!")
                return
            else:
                print("Table does not exist.")

            # Make a new table called items
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    source TEXT NOT NULL,
                    summary TEXT,
                    tags TEXT,
                    saved INTEGER DEFAULT 0,
                    read INTEGER DEFAULT 0
                )
            """)

    # Use data object to add an item to the table
    def add_item(self, item: ResearchItem):
        tags_text = ",".join(item.tags)

        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR IGNORE INTO items
                (title, url, source, summary, tags, saved, read)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
            item.title,
            item.url, 
            item.source,
            item.summary,
            tags_text,
            int(item.saved),
            int(item.read)))

    # Selects all items from the table
    def get_all_items(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, title, url, source, summary, tags, saved, read
                FROM items
                ORDER BY id DESC
            """)

            rows = cursor.fetchall()

        return rows