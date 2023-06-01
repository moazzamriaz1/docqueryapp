import streamlit as st
from signup import signup
from login import login
from query import run_query_app
from streamlit_option_menu import option_menu



def main():

   
    st.title("Document Query System")


    # Step 1: Initialize session state variables
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'login_successful' not in st.session_state:
        st.session_state['login_successful'] = False

    # Step 2: Check if user is logged in
    if st.session_state['username'] is None:
        # User is not logged in, display login and signup options
        selection = option_menu(
            menu_title="Main Menu",
            options=["Login", "Signup"],
            icons=["person", "person"],
            menu_icon="cast",
            default_index=1
        )

        if selection == "Login":
            st.session_state['username'] = login()
            if st.session_state['username']:
                st.session_state['login_successful'] = True
        elif selection == "Signup":
            signup()



    # Step 3: Check if user is logged in successfully
    if 'login_successful' in st.session_state and st.session_state['login_successful']:
        # User is logged in, display welcome message and query page
        if 'username' in st.session_state and st.session_state['username']:
            st.subheader(f"Welcome, {st.session_state['username']}!")
            run_query_app(st.session_state['username'])

if st.sidebar.button("Logout"):
     st.session_state['username'] = None
     st.session_state['login_successful'] = False
     st.empty()  # Clear the contents of the page

if __name__ == '__main__':
    main()
