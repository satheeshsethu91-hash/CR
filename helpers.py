import sqlite3
import os
import bcrypt

# Database path
DB_FILE = os.path.join("/home/appuser", "app_data.db")

# Connect to the database
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# -------------------------------
# Create tables if they don't exist
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash BLOB NOT NULL,
    role TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    published DATETIME DEFAULT CURRENT_TIMESTAMP,
    read_status INTEGER DEFAULT 0,
    valid_status INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT UNIQUE NOT NULL
)
""")

conn.commit()

# -------------------------------
# User management
# -------------------------------
def add_user(username, password, role="client"):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()

def check_user(username, password):
    cursor.execute("SELECT password_hash, role FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if row:
        stored_hash, role = row
        # Ensure stored_hash is bytes
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')
        if bcrypt.checkpw(password.encode(), stored_hash):
            return role  # Login successful
    return None

# -------------------------------
# Article management
# -------------------------------
def add_article(title, link):
    cursor.execute("INSERT INTO articles (title, link) VALUES (?, ?)", (title, link))
    conn.commit()

def get_articles():
    cursor.execute("SELECT * FROM articles ORDER BY published DESC")
    return cursor.fetchall()

def update_read_status(article_id, status):
    cursor.execute("UPDATE articles SET read_status=? WHERE id=?", (status, article_id))
    conn.commit()

def update_valid_status(article_id, status):
    cursor.execute("UPDATE articles SET valid_status=? WHERE id=?", (status, article_id))
    conn.commit()

# -------------------------------
# Keyword management
# -------------------------------
def add_keyword(keyword):
    cursor.execute("INSERT OR IGNORE INTO keywords (keyword) VALUES (?)", (keyword,))
    conn.commit()

def get_keywords():
    cursor.execute("SELECT keyword FROM keywords")
    return [k[0] for k in cursor.fetchall()]

# -------------------------------
# Initialize default admin
# -------------------------------
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

cursor.execute("SELECT * FROM users WHERE username=?", (DEFAULT_ADMIN_USERNAME,))
if not cursor.fetchone():
    add_user(DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, role="admin")
