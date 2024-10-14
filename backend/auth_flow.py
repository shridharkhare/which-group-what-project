import streamlit as st
from frontend.utils.logout_button import logout_action


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
def authenticate_user(g_session: dict, cookies):
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

                logout_action(cookies)
            else:
                st.write("Error:", e)
            return None


# Function to get the user ID from email
def get_student_id(email):
    supabase = st.session_state.supabase
    try:
        response = (
            supabase.table("students").select("student_id").eq("email", email).execute()
        )
        if response:
            st.write(response)
            student_id = response.data[0]["student_id"]
            return student_id
    except Exception as e:
        st.write("Error:", e)
        return None


# Function to assign user role to the user metadata
def assign_user_role(role, email):
    supabase = st.session_state.supabase
    try:
        if role == "student":
            student_id = get_student_id(email)
            response = supabase.auth.update_user(
                {"data": {"user_type": role, "student_id": student_id}}
            )
        else:
            response = supabase.auth.update_user({"data": {"user_type": role}})
        return response.user
    except Exception as e:
        st.write("Error:", e)
        return None
