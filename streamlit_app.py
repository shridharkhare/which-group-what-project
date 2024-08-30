import streamlit as st

# Local imports
from frontend.utils.sidebar import set_sidebar
from backend import create_supabase_client


# Main program on the dashboard
def main():
    set_sidebar(
        user={
            "full_name": "John Doe",
            "avatar_url": "https://avatars.githubusercontent.com/u/832385?s=200&v=4",
        }
    )
    st.title("My Dashboard")
    st.subheader("Pending Requests")
    st.write("You currently have no pending requests.")


create_supabase_client()
main()
