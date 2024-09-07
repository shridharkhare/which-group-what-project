import streamlit as st


# Function to return the Google login link
def return_google_login_link():
    supabase = st.session_state.supabase
    try:
        data = supabase.auth.sign_in_with_oauth(
            {
                "provider": "google",
                "options": {"redirect_to": st.secrets["REDIRECT_URL"]},
            }
        )
        return data.url
    except Exception as e:
        st.write(e)


# Function to authenticate the user
def authenticate_user(g_session: dict):
    supabase = st.session_state.supabase
    if g_session is not None:
        access_token = g_session["access_token"]
        refresh_token = g_session["refresh_token"]
        try:
            response = supabase.auth.set_session(
                access_token=access_token, refresh_token=refresh_token
            )
            return response.user
        except Exception as e:
            if type(e).__name__ == "AuthApiError":
                if e.message == "Invalid Refresh Token: Already Used":
                    st.error("The refresh token was already used. Please login again.")
                elif e.message == "User from sub claim in JWT does not exist":
                    st.error("The access token was messed with. Please login again.")
                else:
                    st.error("Error:", e)
                st.info("Logging out...")
                st.session_state.clear()
            else:
                st.write("Error:", e)
            return None
