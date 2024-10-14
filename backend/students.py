import streamlit as st

supabase = st.session_state.supabase


def get_all_students():
    try:
        data = (
            supabase.table("students")
            .select("*")
            .order("student_id", desc=False)
            .execute()
        )
        return data.data
    except Exception as e:
        st.error(f"Failed to fetch students: {e}")
        return {}


def flatten_teams(data):
    for student in data.data:
        if student["teams"]:
            student["team_no"] = student["teams"]["team_no"]
        else:
            student["team_no"] = None
        del student["teams"]


@st.cache_data(show_spinner=True)
def get_student_by_batch(div, batch):
    try:
        # If batch is not a number, return all students from the division
        if not batch.isdigit():
            data = (
                supabase.table("students")
                .select(
                    "div, roll_no, name, batch, teams!students_team_id_fkey(team_no)"
                )
                .match({"div": div})
                .order("student_id", desc=False)
                .execute()
            )
            flatten_teams(data)

        else:
            data = (
                supabase.table("students")
                .select(
                    "div",
                    "roll_no",
                    "name",
                    "batch",
                    "teams!students_team_id_fkey(team_no)",
                )
                .match({"div": div, "batch": batch})
                .order("roll_no", desc=False)
                .execute()
            )
            flatten_teams(data)
    except Exception as e:
        st.error(f"Failed to fetch students: {e}")
        return {}

    return data.data
