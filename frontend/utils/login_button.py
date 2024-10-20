import streamlit as st
from backend.auth_flow import return_google_login_link
from frontend.utils.browser import nav_to


# Function to show login button
def login_button():
    st.write(
        "A new tab will open to authenticate with Google. You may need to allow pop-ups."
    )
    st.write("Please close this tab after logging in.")
    login_button = st.button("Continue with Google :material/login:", type="primary")

    if login_button:
        url = return_google_login_link()
        # st.write(url)
        nav_to(url)
