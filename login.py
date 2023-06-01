import streamlit as st
import hashlib
import sqlite3
from query import run_query_app

def create_user_table():
    conn = sqlite3.connect('user_credentials.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()



def login():
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_button = st.button("Login")

    if submit_button:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect('user_credentials.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_password))
        user = c.fetchone()
        conn.close()

        if user:
            st.success("Login successful!")
            return user[1]  # Return the username
        else:
            st.error("Invalid email or password.")
            return None




