import streamlit as st


def get_students():
    supabase = st.session_state.supabase
    try:
        data = (
            supabase.table("students")
            .select("*")
            .order("div", desc=False)
            .order("roll_no", desc=True)
            .execute()
        )
    except Exception as e:
        st.error(f"Failed to fetch students: {e}")
        return {}

    return data.data
