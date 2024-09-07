import streamlit as st

# Local imports
from frontend.utils.sidebar import set_sidebar
from frontend.utils.login_button import login_button
from backend.auth_flow import authenticate_user
from backend import create_supabase_client


# Main program after login
def main():
    if "user" not in st.session_state:
        st.title("Streamlit Supabase Auth")
        with st.spinner("Authenticating user..."):
            if "g_session" not in st.session_state:
                login_button()
            else:
                g_session = st.session_state.g_session
                user: object = authenticate_user(g_session)
                if user is not None:
                    st.session_state.user = dict(user)["user_metadata"]
                    st.rerun()
    else:
        set_sidebar(st.session_state.user)
        st.title("My Dashboard")
        st.subheader("Pending Requests")
        st.write("You currently have no pending requests.")


create_supabase_client()
main()
