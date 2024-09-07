import streamlit as st
from streamlit_extras.switch_page_button import switch_page


def logout_button():
    if st.button("Logout"):
        st.info("Logging out...")
        st.session_state.clear()
        switch_page("streamlit_app")
        st.rerun()
