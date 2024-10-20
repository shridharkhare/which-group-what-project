import streamlit as st

supabase = st.session_state.supabase


def get_students(filter_team=False):
    try:
        query = supabase.table("students").select("*")

        if filter_team:
            query = query.is_("team_id", "null")

        data = query.order("student_id", desc=False).execute()
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
        query = (
            supabase.table("students")
            .select("div, roll_no, name, batch, teams!students_team_id_fkey(team_no)")
            .match({"div": div})
        )

        if batch.isdigit():
            query = query.match({"batch": batch}).order("roll_no", desc=False)
        else:
            query = query.order("student_id", desc=False)

        data = query.execute()
        flatten_teams(data)
    except Exception as e:
        st.error(f"Failed to fetch students: {e}")
        return {}

    return data.data
