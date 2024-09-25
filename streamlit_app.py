import streamlit as st
import json

# Local imports
from frontend.utils.sidebar import set_sidebar
from frontend.utils.login_button import login_button
from backend.auth_flow import authenticate_user
from backend import create_supabase_client
from frontend.cookies.cookies import create_cookie_manager

cookies = create_cookie_manager()
if not cookies.ready():
    st.stop()


# Main program after login
def main():
    if "user" not in st.session_state:
        st.title("Streamlit Supabase Auth")
        with st.spinner("Authenticating user..."):

            if "g_session" in cookies.keys() and str(cookies["g_session"]):
                g_session = json.loads(cookies.get("g_session"))

                user: object = authenticate_user(g_session)
                if user is not None:
                    st.session_state.user = dict(user)["user_metadata"]
                    st.rerun()

            else:
                login_button()
    else:
        set_sidebar(st.session_state.user, cookies)
        st.title("My Dashboard")
        st.subheader("Pending Requests")
        st.write("You currently have no pending requests.")


create_supabase_client()
main()
