import sqlite3
import os
import streamlit as st

# Use a persistent, writable path for Streamlit Cloud
DB_FILE = os.path.join("/home/appuser", "articles.db")

# Connect to the database (it will create the file if it doesn't exist)
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Ensure the table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    published DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Function to fetch all articles
def get_articles():
    cursor.execute("SELECT * FROM articles ORDER BY published DESC")
    return cursor.fetchall()

# Function to insert a new article
def add_article(title, link):
    cursor.execute("INSERT INTO articles (title, link) VALUES (?, ?)", (title, link))
    conn.commit()

# Example usage with Streamlit
st.title("Marine Casualty Articles")

# Add new article (optional)
with st.form("add_article_form"):
    new_title = st.text_input("Title")
    new_link = st.text_input("Link")
    submitted = st.form_submit_button("Add Article")
    if submitted and new_title and new_link:
        add_article(new_title, new_link)
        st.success("Article added!")

# Display articles
articles = get_articles()
if articles:
    for article in articles:
        st.write(f"- [{article[1]}]({article[2]}) — {article[3]}")
else:
    st.info("No articles found yet.")
