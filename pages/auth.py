# Pip packages
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
from streamlit_url_fragment import get_fragment
from frontend.utils.browser import get_session_from_fragment

with st.spinner("Authenticating user..."):
    # Get the current fragment
    current_fragment = get_fragment()
    # st.write(current_fragment)
    # time.sleep(0.5)

    # If not, check if the current fragment has a session
    if current_fragment is not None:
        g_session = get_session_from_fragment(current_fragment)
        # st.write(g_session)

        if "error" in g_session:
            st.error("Error:", g_session["error"])
            st.info("Redirecting to login page...")
            time.sleep(1)
            switch_page("streamlit_app")
        else:
            if g_session is not None:
                st.session_state.g_session = g_session
                switch_page("streamlit_app")
