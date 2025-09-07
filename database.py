import sqlite3

DB_FILE = 'maritime_news.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            published TEXT,
            source TEXT,
            language TEXT,
            read_status INTEGER DEFAULT 0,
            valid_status INTEGER DEFAULT 0,
            image_url TEXT,
            ai_analysis TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS custom_websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_article(article):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO articles (title, link, published, source, language, image_url, ai_analysis)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (article['title'], article['link'], article['published'], article['source'], article['language'], article.get('image_url', ''), article['ai_analysis']))
    conn.commit()
    conn.close()