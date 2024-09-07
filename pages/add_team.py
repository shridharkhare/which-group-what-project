import streamlit as st
from frontend.utils.sidebar import set_sidebar
from backend.team import get_student_status
from backend.team import add_team

set_sidebar(st.session_state.user)

st.title("Add Team")


def read_data():

    st.subheader("Select the number of students in the team", divider=True)
    num_students = st.radio(
        "Number of students",
        [1, 2, 3, 4],
        horizontal=True,
        label_visibility="collapsed",
    )

    # def team_div():
    st.subheader("Select the division of the team", divider=True)
    div = st.radio(
        "Division", ["A", "B"], horizontal=True, label_visibility="collapsed"
    )

    st.subheader(f"Enter roll-no of team members", divider=True)
    roll_calls = []

    for i in range(num_students):
        roll = st.number_input(
            f"Roll No of member {i+1}",
            value=None,
            placeholder=f"eg. {21+i}",
            min_value=1,
            format="%d",
        )
        status = get_student_status(roll, div)
        if status:
            st.write(status[0])
            if status[1] is not None:
                st.warning(f"Student is already part of a team")
        roll_calls.append(roll)  # Remember to clear this on update or clear button

    st.subheader("Enter the topic name")
    topic = st.text_input(
        label="Topic name", label_visibility="collapsed", placeholder="eg. Project 2232"
    )

    st.subheader("Enter roll no of the leader")
    leader_id = st.number_input(
        "eg. 21", value=None, placeholder="eg. 21", min_value=1, format="%d"
    )

    data = {
        "div": div,
        "leader_id": leader_id,
        "topic": topic,
        "roll_calls": roll_calls,
    }
    # st.write(data)

    if st.button("Submit"):
        submit_form(data, leader_id, roll_calls)
    else:
        pass

    if st.button("Clear"):
        data = {}
        st.write("Cleared")
        st.write(data)
        st.rerun()


def submit_form(data, leader_id, roll_calls):
    # If any roll number is NULL
    if None in roll_calls:
        st.warning("Please enter roll numbers for all students")
        return

    # If project name is NULL:
    if data["topic"] == "":
        st.warning("Please enter a project name")
        return

    # If roll number is not unique
    if len(roll_calls) != len(set(roll_calls)):
        st.warning("Roll numbers should be unique")
        return

    # If leader is not part of the team
    if leader_id not in roll_calls:
        st.warning("Leader should be part of the team")
        return

    add_team(data)
    st.success("Team added successfully")


def main():
    read_data()


if __name__ == "__main__":
    # main()
    st.write("Add Team")
    read_data()
