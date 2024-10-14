import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import json

st.set_page_config(page_title="Which-Group-What-Project")

# Local imports
from frontend.utils.login_button import login_button
from frontend.utils.logout_button import logout_action
from backend.auth_flow import authenticate_user
from backend.auth_flow import assign_user_role
from backend import create_supabase_client
from frontend.cookies.cookies import create_cookie_manager


cookies = create_cookie_manager()
st.session_state.cookies = cookies
if not cookies.ready():
    st.stop()


# Main program after login
def main():
    # Checks if a user is present in the session state
    if "user" not in st.session_state:
        st.title("Streamlit Supabase Auth")
        with st.spinner("Authenticating user..."):

            if "g_session" in cookies.keys() and str(cookies["g_session"]):
                g_session = json.loads(cookies.get("g_session"))

                user: object = authenticate_user(g_session, cookies)

                if user is not None:
                    if "user_type" in dict(user)["user_metadata"]:
                        st.session_state.user = dict(user)["user_metadata"]
                        st.rerun()

                    email = dict(user)["email"]

                    email_role_map = {
                        "@student.mes.ac.in": "student",
                        "@mes.ac.in": "faculty",
                        "kshreedhar01622@gmail.com": "admin",
                        "thebrahmnicboy@gmail.com": "admin",
                    }

                    role_assigned = False

                    for key, role in email_role_map.items():
                        if email.endswith(key) or email == key:
                            response = assign_user_role(role, email)
                            st.session_state.user = dict(response)["user_metadata"]
                            st.rerun()
                            role_assigned = True
                            break

                    if not role_assigned:
                        st.write("You are not allowed to access this app.")
                        logout_action(cookies)
            else:
                login_button()
    else:
        switch_page("dashboard")


create_supabase_client()
main()
