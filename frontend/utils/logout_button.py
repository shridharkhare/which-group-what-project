import streamlit as st
import time


def logout_button(cookies):
    if st.button(" :material/logout: Logout", type="primary"):
        logout_action(cookies)


def logout_action(cookies):
    if not cookies.ready():
        return

    st.info("Logging out...")
    cookies.set("g_session", "")
    cookies.save()
    time.sleep(0.5)
    st.session_state.clear()
    st.rerun()
