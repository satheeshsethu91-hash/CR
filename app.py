import streamlit as st
from helpers import *

# -------------------------------
# Login system
# -------------------------------
st.title("Marine Casualty Incident Aggregator")

if "login" not in st.session_state:
    st.session_state.login = False
if "role" not in st.session_state:
    st.session_state.role = None

def login():
    username = st.session_state.username
    password = st.session_state.password
    role = check_user(username, password)
    if role:
        st.session_state.login = True
        st.session_state.role = role
        st.success(f"Logged in as {role}")
    else:
        st.error("Invalid username or password")

if not st.session_state.login:
    st.text_input("Username", key="username")
    st.text_input("Password", type="password", key="password")
    st.button("Login", on_click=login)
else:
    st.sidebar.write(f"Logged in as **{st.session_state.role}**")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"login": False, "role": None}))

    # -------------------------------
    # Admin section
    # -------------------------------
    if st.session_state.role == "admin":
        st.header("Admin Panel")

        # Add new user
        with st.expander("Add New User"):
            new_username = st.text_input("Username", key="new_user")
            new_password = st.text_input("Password", type="password", key="new_pass")
            new_role = st.selectbox("Role", ["client", "admin"], key="new_role")
            if st.button("Add User", key="add_user_btn"):
                add_user(new_username, new_password, new_role)
                st.success("User added!")

        # Manage keywords
        with st.expander("Manage Keywords"):
            new_keyword = st.text_input("New Keyword", key="new_kw")
            if st.button("Add Keyword", key="add_kw_btn"):
                add_keyword(new_keyword)
                st.success("Keyword added!")

    # -------------------------------
    # Articles section
    # -------------------------------
    st.header("Articles")

    # Add new article (Admin only)
    if st.session_state.role == "admin":
        with st.expander("Add Article"):
            title = st.text_input("Title", key="art_title")
            link = st.text_input("Link", key="art_link")
            if st.button("Add Article", key="add_article_btn"):
                if title and link:
                    add_article(title, link)
                    st.success("Article added!")

    # Display articles
    articles = get_articles()
    for art in articles:
        id, title, link, published, read_status, valid_status = art
        col1, col2, col3 = st.columns([5,1,1])
        with col1:
            st.markdown(f"[{title}]({link}) — {published}")
        with col2:
            if st.button("Mark Read" if not read_status else "Mark Unread", key=f"read_{id}"):
                update_read_status(id, 1 if not read_status else 0)
        with col3:
            if st.button("Valid" if valid_status else "Invalid", key=f"valid_{id}"):
                update_valid_status(id, 1 if not valid_status else 0)

    # Daily summary (Admin only)
    if st.session_state.role == "admin":
        st.header("Daily Summary")
        total = len(articles)
        unread = sum(1 for a in articles if a[4]==0)
        invalid = sum(1 for a in articles if a[5]==0)
        st.write(f"Total Articles: {total}")
        st.write(f"Unread Articles: {unread}")
        st.write(f"Invalid Articles: {invalid}")
