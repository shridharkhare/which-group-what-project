import streamlit as st
from frontend.sidebar.sidebar import set_sidebar
from streamlit_extras.row import row
from streamlit_extras.switch_page_button import switch_page

from backend.team import get_my_team, update_topic, remove_member, remove_team

st.set_page_config(
    page_title="Edit-Team",
    layout="wide",
    page_icon=":material/edit:",
)

set_sidebar()
st.title(":material/edit: Edit Team")


@st.dialog("Delete Team")
def confirm_delete(team_id):
    st.write(
        "Are you sure you want to delete this team? \n This action cannot be undone."
    )
    btn_row = row(2)

    if btn_row.button("Yes, delete this team", key="yes", use_container_width=True):
        remove_team(team_id)
        st.switch_page("dashboard")
    if btn_row.button("No", key="no", use_container_width=True, type="primary"):
        st.rerun()


def edit_team_form(team_details, team_members):
    team_id = team_details["team_id"]
    project_topic = st.text_input(
        ":material/edit: Project topic", value=team_details["topic"]
    )
    if st.button("Update project topic"):
        update_topic(team_id, project_topic)
        st.rerun()

    st.write("Team members:")
    for i, member in enumerate(team_members):
        mem_row = row(2)

        mem_row.text(f"{i+1}. {member['name']} ({member['student_id']})")

        if member["student_id"] == team_details["leader_id"]:
            mem_row.button(
                f"Remove this member", key=member["student_id"], disabled=True
            )
        else:
            if mem_row.button(
                f":material/person_remove: Remove this member", key=member["student_id"]
            ):
                remove_member(member["student_id"])
                st.rerun()

    but_row = row(2)

    if but_row.button(":material/arrow_back_ios: Back to dashboard"):
        switch_page("dashboard")

    if but_row.button(":material/group_remove: Remove this team"):
        confirm_delete(team_id)


def main():
    leader_id = st.session_state.user["student_id"]

    team_details, team_members = get_my_team(leader_id)

    div, team_id = team_details["div"], team_details["team_id"]

    st.subheader(f"Team {team_id} of division {div}")
    edit_team_form(team_details, team_members)


if __name__ == "__main__":
    main()
