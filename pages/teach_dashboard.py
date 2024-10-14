import streamlit as st

from frontend.sidebar.sidebar import set_sidebar

st.set_page_config(
    page_title="Which-Group-What-Project",
    layout="wide",
    page_icon=":material/dashboard:",
)

set_sidebar()
st.title(":material/dashboard: Teacher Dashboard")
st.subheader("Pending Requests", anchor=None)
st.write("You currently have no pending requests.")

requests = [
    {"team_id": 1, "name": "John Doe"},
    {"team_id": 2, "name": "Jane Doe"},
    {"team_id": 3, "name": "John Smith"},
    {"team_id": 4, "name": "Jane Smith"},
]

for i in requests:
    st.expander(f"Team: {i['team_id']} Leader: ({i['name']})", expanded=False)
st.divider()

st.subheader("Students not in a group", anchor=None)
st.write("You currently have no students not in a group.")
