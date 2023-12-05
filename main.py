import streamlit as st
from admin_dash import admin_login
from user_dash import user_login

def run():
    user_or_admin = st.radio("Select User or Admin", ["User", "Admin"])

    if user_or_admin == "User":
        user_login()
    elif user_or_admin == "Admin":
        admin_login()

run()
