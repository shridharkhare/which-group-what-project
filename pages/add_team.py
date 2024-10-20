import streamlit as st
from frontend.sidebar.sidebar import set_sidebar
from backend.team import get_student_status
from backend.team import add_team

st.set_page_config(
    page_title="Add Team", layout="wide", page_icon=":material/group_add:"
)
set_sidebar()

st.title(":material/group_add: Add Team")


def read_data():

    st.subheader("Select the number of students in the team", divider=True)
    num_students = st.radio(
        "Number of students in the team",
        [2, 3, 4],
        horizontal=True,
        label_visibility="collapsed",
    )

    leader_id = st.session_state.user["student_id"]
    leader_roll = int(leader_id[-2:])
    div = leader_id[2]
    roll_calls = []

    st.subheader("Select the division of the team", divider=True)
    div = st.radio(
        "Division",
        ["A", "B"],
        horizontal=True,
        label_visibility="collapsed",
        index=0 if div == "A" else 1,
        disabled=True,
    )

    st.subheader(f"Enter Roll no of team members", divider=True)

    st.write(f"Leader Roll No: {leader_roll}")

    for i in range(num_students - 1):
        roll = st.number_input(
            f"Roll No of member {i+2}",
            value=None,
            placeholder=f"eg. {21+i}",
            min_value=1,
            max_value=71 if div == "A" else 72,
            format="%d",
        )

        status = get_student_status(roll, div)

        if status:
            st.write(status[0])
            if status[1] is not None:
                st.warning(f"Student is already part of a team")
            else:
                roll_calls.append(roll)

    st.subheader("Enter the topic name")
    topic = st.text_input(
        label="Topic name", label_visibility="collapsed", placeholder="eg. Project 2232"
    )

    data = {
        "div": div,
        "leader_id": leader_id,
        "topic": topic,
        "roll_calls": roll_calls,
    }
    # st.write(data)

    if st.button("Submit"):
        submit_form(data)
    else:
        pass

    if st.button("Clear"):
        data = {}
        st.write("Cleared")
        st.write(data)
        st.rerun()


def submit_form(data):
    # If any roll number is NULL
    if None in data["roll_calls"]:
        st.warning("Please enter roll numbers for all students")
        return

    # If project name is NULL:
    if data["topic"] == "":
        st.warning("Please enter a project name")
        return

    # If roll number is not unique
    if len(data["roll_calls"]) != len(set(data["roll_calls"])):
        st.warning("Roll numbers should be unique")
        return

    add_team(data)
    st.success("Team added successfully")


def main():
    read_data()


if __name__ == "__main__":
    main()
