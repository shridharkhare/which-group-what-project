import streamlit as st
from backend.team import get_team_members


def get_unapproved_teams():
    supabase = st.session_state.supabase
    try:
        response = (
            supabase.from_("teams")
            .select("team_id, students!teams_leader_id_fkey(name), no_mem, topic")
            .match({"is_approved": False, "leader_okay": True})
            .execute()
        )
        team_ids = [team["team_id"] for team in response.data]
        team_members = []
        for team_id in team_ids:
            team_members.append(get_team_members(team_id))

        # add team members to response
        for i, team in enumerate(response.data):
            team["members"] = team_members[i]

        return response.data
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def approve_team(team_id):
    supabase = st.session_state.supabase
    try:
        response = (
            supabase.from_("teams")
            .update({"is_approved": True})
            .match({"team_id": team_id})
            .execute()
        )
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
