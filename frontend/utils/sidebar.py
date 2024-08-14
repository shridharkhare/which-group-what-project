import streamlit as st


def set_sidebar(user: dict):

    st.sidebar.title("Which-Group-What-Project")
    st.sidebar.write(f"Welcome, {user['full_name']}!")
    st.sidebar.image(user["avatar_url"], width=100)
    st.sidebar.page_link("streamlit_app.py", label="🏠 Home")
    st.sidebar.page_link("pages/students.py", label="👥 Students")
    st.sidebar.page_link("pages/add_team.py", label="➕ Add Team")
