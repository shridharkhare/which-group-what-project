import streamlit as st
from backend.team import update_student


def get_requests(student_id):
    supabase = st.session_state.supabase

    # Get all requests for the student
    # We are using the student_id to filter the requests
    # We are also using the status column to filter the requests
    # We are only interested in requests that are not yet approved
    try:
        requests = (
            supabase.table("team_req")
            .select("id, students(name), status, created_at, sender_id")
            .eq("receiver_id", student_id)
            .is_("status", "null")
            .execute()
        )
        print(requests)
        return requests.data
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def check_team(leader_id):
    # Check if team corresponding to the leader_id exists and has less than 4 members
    supabase = st.session_state.supabase
    try:
        team = (
            supabase.table("teams")
            .select("team_id, no_mem")
            .eq("leader_id", leader_id)
            .execute()
        )
        print(team.data)
        if team.data:
            no_members = team.data[0]["no_mem"]
            if no_members < 4:
                return team.data[0]["team_id"]
            else:
                return None
        else:
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def reject_request(request_id):
    supabase = st.session_state.supabase

    # Update the request status to rejected
    try:
        response = (
            supabase.table("team_req")
            .update({"status": False})
            .eq("id", request_id)
            .execute()
        )
        st.rerun()
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def accept_request(request_id, leader_id):
    supabase = st.session_state.supabase

    # Update the request status to appr
    team_id = check_team(leader_id)
    if not team_id:
        st.error("Team is full")
        reject_request(request_id)
        return None
    else:
        current_user_id = st.session_state.user["student_id"]
        update_student(current_user_id, team_id)
        try:
            response = (
                supabase.table("team_req")
                .update({"status": True})
                .eq("id", request_id)
                .execute()
            )
            st.rerun()
            return response
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None
