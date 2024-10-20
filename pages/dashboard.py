import streamlit as st
import datetime
from streamlit_extras.row import row
from streamlit_extras.switch_page_button import switch_page

from frontend.sidebar.sidebar import set_sidebar
from backend.stud_dash import get_requests, accept_request, reject_request
from backend.team import get_my_team, send_team_for_approval, unlock_team
from frontend.utils.utils import convert_timestamp


st.set_page_config(
    page_title="Which-Group-What-Project",
    layout="wide",
    page_icon=":material/dashboard:",
)

set_sidebar()
student_id = st.session_state.user["student_id"]
st.title(":material/dashboard: Dashboard - " + student_id)


@st.dialog("Send team for approval?")
def approval_dialog(team_id):
    st.write(
        "Your team will be **locked** and sent for approval. \n \n Do you want to proceed?"
    )
    btn_row = row(2)
    if btn_row.button("Yes", type="secondary", use_container_width=True):
        send_team_for_approval(team_id)
        st.rerun()
    if btn_row.button("No", type="primary", use_container_width=True):
        st.rerun()


@st.dialog("Unlock team?")
def unlock_dialog(team_id):
    st.markdown(
        ":material/warning: **Unlocking team will revert the team's approval status.** \n \n **Do you want to proceed?**"
    )
    btn_row = row(2)
    if btn_row.button("Yes", type="secondary", use_container_width=True):
        unlock_team(team_id)
        st.rerun()
    if btn_row.button("No", type="primary", use_container_width=True):
        st.rerun()


def show_team_details(team_details, team_members):
    st.markdown("### Team " + team_details["team_id"])
    st.markdown("- **Project Topic:**")
    with st.container(border=True):
        st.write(team_details["topic"])
    st.markdown("- **Number of Members:**  " + str(team_details["no_mem"]))
    team_members_markdown = "- **Team Members:** \n"

    # team_members_markdown = ""
    for member in team_members:
        if member["student_id"] == team_details["leader_id"]:
            team_members_markdown += (
                f"  - **{member['name']}** (Leader) - *{member['student_id']}*\n"
            )
        else:
            team_members_markdown += (
                f"  - {member['name']} - *{member['student_id']}*\n"
            )

    st.markdown(team_members_markdown)


def show_approval_details(team_details):
    if team_details["is_approved"]:
        time = team_details["is_approved_time"]

        converted_date = convert_timestamp(time)

        st.success(
            f"Your team was approved on : {converted_date}",
            icon=":material/check_circle:",
        )

    elif team_details["leader_okay"] is True:

        st.info("Your team is sent for approval", icon=":material/hourglass_top:")

    elif team_details["leader_id"] == st.session_state.user["student_id"]:
        if st.button(
            ":material/edit: Edit team details",
            type="secondary",
        ):
            switch_page("edit_team")

        if st.button(
            " :material/forward: Send team for approval",
            type="secondary",
        ):
            approval_dialog(team_details["team_id"])

    if team_details["is_approved"] or team_details["leader_okay"]:
        if st.button(
            " :material/lock_open_right: Unlock Team",
            key="unlock_team",
            type="secondary",
        ):
            unlock_dialog(team_details["team_id"])


def dashboard_left(team_details, team_members):
    if team_details:
        show_team_details(team_details, team_members)
        st.divider()
        show_approval_details(team_details)
    else:
        st.warning("You are not in a team yet!")


def dashboard_right():
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
                converted_date = convert_timestamp(time)

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


def main():

    info, requests = st.columns(2, gap="small")
    team_details, team_members = get_my_team(student_id)

    with info:
        with st.container(border=True, height=600):
            dashboard_left(team_details, team_members)

    with requests:
        with st.container(border=True, height=600):
            dashboard_right()


if __name__ == "__main__":
    main()
