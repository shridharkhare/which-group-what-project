import streamlit as st
from frontend.cookies.encrypted_cookie_manager import EncryptedCookieManager


def create_cookie_manager():
    # This should be on top of your script
    cookies = EncryptedCookieManager(
        # This prefix will get added to all your cookie names.
        # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.
        prefix="evozone_which-grp-what-proj_",
        # You should really setup a long COOKIES_PASSWORD secret if you're running on Streamlit Cloud.
        password=str(st.secrets["COOKIES_PASSWORD"]),
    )

    return cookies
