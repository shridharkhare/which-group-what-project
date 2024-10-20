import streamlit as st

from frontend.sidebar.sidebar import set_sidebar

from backend.teach_dash import get_teams
from frontend.utils.utils import convert_timestamp
from backend.students import get_students
from backend.team import get_team_by_id


st.set_page_config(
    page_title="Report", layout="wide", page_icon=":material/assessment:"
)
set_sidebar()

appr_team_ids = []


def show_approved_teams(appr_teams, div, batch):
    if not appr_teams:
        st.subheader("You currently have no approved teams.")
        return

    for team in appr_teams:
        appr_team_ids.append(team["team_id"])
        del team["leader_okay_time"]

        team["leader"] = team["students"]["name"]

        team["approved_at"] = convert_timestamp(team.pop("is_approved_time"))

        team["number_of_members"] = team.pop("no_mem")
        team["batch"] = team.pop("students")["batch"]

    for team in appr_teams:
        for key in list(team.keys()):
            new_key = key.replace("_", " ").title()
            team[new_key] = team.pop(key)

    appr_teams = [
        team for team in appr_teams if team["Div"] == div and team["Batch"] == batch
    ]

    st.subheader(f"You currently have {len(appr_teams)} approved teams in this batch.")
    st.dataframe(appr_teams, use_container_width=True)

    # st.write(appr_teams)


def show_students_not_in_team(div, batch):
    unassigned_students = get_students(filter_team=True)
    if not unassigned_students:
        st.subheader("All students are in a team.")
        return

    for student in unassigned_students:
        for key in list(student.keys()):
            new_key = key.replace("_", " ").title()
            student[new_key] = student.pop(key)
        del student["Team Id"]

    unassigned_students = [
        student
        for student in unassigned_students
        if student["Div"] == div and student["Batch"] == batch
    ]

    st.subheader(f"There are {len(unassigned_students)} students not in a team.")

    st.dataframe(unassigned_students, use_container_width=True, height=500)


def display_one_team(team_details, team_members):
    with st.container(border=True):

        st.markdown("### Team " + team_details["team_id"])

        st.markdown(f"- **Project Topic:** {team_details["topic"]}")

        st.markdown("- **Number of Members:**  " + str(team_details["no_mem"]))

        team_members_markdown = "- **Team Members:** \n"

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


def main():
    st.title(":material/assessment: Report")
    teams, students, team_details = st.tabs(
        ["Approved Teams", "Students Not in a Team", "Search Team Details"]
    )
    appr_teams = get_teams(True)

    with teams:

        st.subheader("Select division")
        div = st.radio(
            "Select division",
            ["A", "B", "C"],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
        )

        st.subheader("Select batch")
        batch = st.radio(
            "Select batch",
            [1, 2, 3],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
        )

        show_approved_teams(appr_teams, div, batch)

    with students:

        st.subheader("Select division")
        div = st.radio(
            "Select division",
            ["A", "B", "C"],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            key="div",
        )

        st.subheader("Select batch")
        batch = st.radio(
            "Select batch",
            [1, 2, 3],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            key="batch",
        )

        show_students_not_in_team(div, batch)

    with team_details:
        st.subheader("Search Team Details")
        team_id = st.selectbox(
            "Enter team ID",
            (appr_team_ids),
        )

        team_details, team_members = None, None

        if st.button("Search"):
            team_details, team_members = get_team_by_id(team_id)

        if team_details and team_members:
            display_one_team(team_details, team_members)


if __name__ == "__main__":
    main()
