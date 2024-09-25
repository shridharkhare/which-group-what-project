import streamlit as st
from frontend.utils.logout_button import logout_button


def set_sidebar(user: dict, cookies):

    st.sidebar.title("Which-Group-What-Project")
    st.sidebar.write(f"Welcome, {user['full_name']}!")
    st.sidebar.image(user["avatar_url"], width=200)
    st.sidebar.page_link("streamlit_app.py", label="🏠 Dashboard")
    st.sidebar.page_link("pages/students.py", label="👥 Students")
    st.sidebar.page_link("pages/add_team.py", label="➕ Add Team")
    st.sidebar.page_link("pages/update_team.py", label="🔄 Update Team")

    with st.sidebar:
        logout_button(cookies)
