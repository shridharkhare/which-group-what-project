from supabase import create_client, Client
import streamlit as st


def create_supabase_client():
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)

    st.session_state.supabase = supabase
