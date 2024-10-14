import streamlit as st
from frontend.sidebar.sidebar import set_sidebar

st.set_page_config(
    page_title="Which-Group-What-Project",
    layout="wide",
    page_icon=":material/dashboard:",
)

set_sidebar()

st.title(":material/dashboard: My Dashboard")

info, requests = st.columns(2)

with info:
    if st.session_state.user["user_type"] == "student":
        student_id = st.session_state.user["student_id"]
        st.subheader("Your roll number is " + student_id)
    st.write("Welcome to your dashboard!")
    st.write("You are currently not in a team.")

with requests:
    st.subheader("Pending Requests", anchor=None)

st.write("You currently have no pending requests.")
