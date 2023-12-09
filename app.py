import streamlit as st
from admin_dash import admin_login
from user_dash import user_login

def run():
    # Set page title and favicon
    st.set_page_config(
        page_title="User and Admin Login",
        page_icon="🔐",
        layout="wide"
    )

    # Add a title in the main area of the page
    st.title("Welcome to your Resume Analyser")

    # Create a sidebar with a title and a user/admin selection dropdown
    st.sidebar.title("Select User Type")
    user_or_admin = st.sidebar.selectbox("Choose User or Admin", ["User", "Admin"])

    # Create a separator for better visual separation
    st.sidebar.markdown("---")

    # Based on the user's selection, display the appropriate login form
    if user_or_admin == "User":
        st.sidebar.success("You selected User")
        user_login()
    elif user_or_admin == "Admin":
        st.sidebar.warning("You selected Admin")
        admin_login()

if __name__ == "__main__":
    run()
