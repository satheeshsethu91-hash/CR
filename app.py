import streamlit as st
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('maritime_news.db')
    return conn

st.title("🛳 Maritime Casualty Incident Dashboard")

mode = st.sidebar.selectbox("Select Mode", ["Dashboard", "Admin"])

if mode == "Admin":
    password = st.text_input("Enter admin password:", type="password")
    if password == "admin123":
        st.header("⚡ Admin Configuration")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Keywords Management
        st.subheader("Manage Keywords")
        new_keyword = st.text_input("New Keyword")
        if st.button("Add Keyword"):
            cursor.execute("INSERT OR IGNORE INTO keywords (keyword) VALUES (?)", (new_keyword,))
            conn.commit()
            st.success(f"Keyword '{new_keyword}' added.")

        keywords = cursor.execute("SELECT id, keyword FROM keywords").fetchall()
        for k in keywords:
            if st.button(f"Delete '{k[1]}'", key=f"del-keyword-{k[0]}"):
                cursor.execute("DELETE FROM keywords WHERE id=?", (k[0],))
                conn.commit()
                st.success(f"Keyword '{k[1]}' deleted.")

        # Custom Websites Management
        st.subheader("Manage Custom Websites")
        new_name = st.text_input("New Site Name")
        new_url = st.text_input("New Site URL")
        if st.button("Add Website"):
            cursor.execute("INSERT INTO custom_websites (name, url) VALUES (?, ?)", (new_name, new_url))
            conn.commit()
            st.success(f"Website '{new_name}' added.")

        sites = cursor.execute("SELECT id, name, url FROM custom_websites").fetchall()
        for s in sites:
            if st.button(f"Delete '{s[1]}'", key=f"del-site-{s[0]}"):
                cursor.execute("DELETE FROM custom_websites WHERE id=?", (s[0],))
                conn.commit()
                st.success(f"Website '{s[1]}' deleted.")

        conn.close()
    else:
        st.warning("🔒 Enter correct admin password")
else:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles ORDER BY published DESC")
    articles = cursor.fetchall()

    total_articles = len(articles)
    validated_articles = sum(1 for a in articles if a[7] == 1)
    unvalidated_articles = total_articles - validated_articles

    st.write(f"📊 Total Articles: {total_articles}")
    st.write(f"✅ Validated Articles: {validated_articles}")
    st.write(f"❌ Unvalidated Articles: {unvalidated_articles}")

    for art in articles:
        st.subheader(art[1])
        st.write(f"Published: {art[3]} | Source: {art[4]} | Language: {art[5]}")
        st.write(f"[Source Link]({art[2]})")
        st.write(f"AI Analysis: {art[9]}")

        col1, col2 = st.columns(2)
        if col1.button(f"{'Mark as Unread' if art[6] == 1 else 'Mark as Read'}", key=f"read-{art[0]}"):
            cursor.execute("UPDATE articles SET read_status = ? WHERE id = ?", (0 if art[6] == 1 else 1, art[0]))
            conn.commit()
        if col2.button(f"{'Mark as Invalid' if art[7] == 1 else 'Mark as Valid'}", key=f"valid-{art[0]}"):
            cursor.execute("UPDATE articles SET valid_status = ? WHERE id = ?", (0 if art[7] == 1 else 1, art[0]))
            conn.commit()

    conn.close()