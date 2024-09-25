import streamlit as st
import time
from frontend.utils.browser import reload_page


def logout_button(cookies):
    if not cookies.ready():
        st.stop()

    if st.button("Logout"):
        st.info("Logging out...")
        st.session_state.clear()
        cookies.set("g_session", "")
        cookies.save()
        time.sleep(1)
        reload_page()
