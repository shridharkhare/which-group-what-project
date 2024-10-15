import streamlit as st
import datetime
from streamlit_extras.row import row

from frontend.sidebar.sidebar import set_sidebar
from backend.stud_dash import get_requests, accept_request, reject_request
from backend.team import get_my_team, send_team_for_approval

st.set_page_config(
    page_title="Which-Group-What-Project",
    layout="wide",
    page_icon=":material/dashboard:",
)

set_sidebar()

st.title(":material/dashboard: My Dashboard")

info, requests = st.columns(
    2,
    gap="small",
)

with info:
    with st.container(border=True, height=530):
        if (
            st.session_state.user["user_type"] == "student"
            or st.session_state.user["user_type"] == "admin"
        ):
            student_id = st.session_state.user["student_id"]
            st.subheader("Your roll number is " + student_id)
            st.write("Welcome to your dashboard!")

        team_details, team_members = get_my_team(st.session_state.user["student_id"])
        if team_details:
            st.write(team_details)
            st.write("Your team members are:")
            for member in team_members:
                st.write(member)
        else:
            st.write("You are not in a team yet.")

        if st.button(
            "Send team for approval",
            type="secondary",
        ):
            send_team_for_approval(team_details["team_id"])

with requests:
    with st.container(border=True, height=530):
        st.subheader("Pending Requests", anchor=None)
        # st.divider()

        requests = get_requests(st.session_state.user["student_id"])

        if requests:
            for request in requests:
                with st.expander(
                    f"From: **{request['students']['name'].title()}**",
                    expanded=False,
                ):
                    time = request["created_at"]
                    converted_date = datetime.datetime.strptime(
                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                    ).strftime("%d %b %y, %I:%M %p")

                    st.write(f"Requested at: {converted_date}")

                    btn_row = row(2)
                    if btn_row.button(
                        "Accept",
                        use_container_width=True,
                        type="secondary",
                    ):
                        accept_request(request["id"], request["sender_id"])
                    if btn_row.button(
                        "Reject",
                        use_container_width=True,
                        type="primary",
                    ):
                        reject_request(request["id"])

        else:
            st.write("No pending requests")
