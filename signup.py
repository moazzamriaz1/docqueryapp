import streamlit as st
import hashlib
import sqlite3

def signup():
    st.subheader("Signup")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if len(password) < 8:
        st.warning("Password must be at least 8 characters long.")
        return

    if st.button("Signup"):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn = sqlite3.connect('user_credentials.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, hashed_password))
        conn.commit()
        conn.close()
        st.success("Signup successful! Please login.")
