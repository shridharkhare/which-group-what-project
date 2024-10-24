import streamlit as st
import json

from frontend.utils.logout_button import logout_button
from streamlit_extras.switch_page_button import switch_page
from backend.team import get_my_team_id


def set_sidebar():
    if "user" not in st.session_state:
        switch_page("streamlit_app")
    user = st.session_state.user
    cookies = st.session_state.cookies

    if not cookies.ready():
        st.stop()

    if user["user_type"] == "student":
        team_id = get_my_team_id(user["student_id"])
        if team_id:
            is_in_team = True
        else:
            is_in_team = False

    st.sidebar.title("Which-Group-What-Project")
    st.sidebar.write(f"Welcome, {user['full_name']}!")
    st.sidebar.image(user["avatar_url"], width=100)

    # Open and read the JSON file
    with open("frontend/sidebar/sidebar.json", "r") as file:
        data = dict(json.load(file))

        for key in data:
            if user["user_type"] == key:
                for item in data[key]:
                    if key == "student" and is_in_team and item["name"] == "Add Team":
                        st.sidebar.page_link(
                            label=item["name"],
                            page=item["link"],
                            icon=item["icon"],
                            disabled=True,
                        )
                    else:
                        st.sidebar.page_link(
                            label=item["name"], page=item["link"], icon=item["icon"]
                        )

    with st.sidebar:
        logout_button(cookies)
