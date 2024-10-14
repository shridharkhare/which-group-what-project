import streamlit as st
import json

from frontend.utils.logout_button import logout_button
from streamlit_extras.switch_page_button import switch_page


def set_sidebar():
    if "user" not in st.session_state:
        switch_page("streamlit_app")
    user = st.session_state.user
    cookies = st.session_state.cookies

    if not cookies.ready():
        st.stop()

    st.sidebar.title("Which-Group-What-Project")
    st.sidebar.write(f"Welcome, {user['full_name']}!")
    st.sidebar.image(user["avatar_url"], width=100)

    # Open and read the JSON file
    with open("frontend/sidebar/sidebar.json", "r") as file:
        data = dict(json.load(file))

        for key in data:
            if user["user_type"] == key:
                for item in data[key]:
                    st.sidebar.page_link(
                        label=item["name"], page=item["link"], icon=item["icon"]
                    )

    with st.sidebar:
        logout_button(cookies)
