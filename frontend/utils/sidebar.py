import streamlit as st
from frontend.utils.logout_button import logout_button
from streamlit_extras.switch_page_button import switch_page
from frontend.cookies.cookies import create_cookie_manager


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
    st.sidebar.page_link("streamlit_app.py", label="🏠 Dashboard")
    st.sidebar.page_link("pages/students.py", label="👥 Students")
    st.sidebar.page_link("pages/add_team.py", label="➕ Add Team")
    st.sidebar.page_link("pages/update_team.py", label="🔄 Update Team")

    with st.sidebar:
        logout_button(cookies)
