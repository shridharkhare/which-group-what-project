import streamlit as st
from frontend.utils.sidebar import set_sidebar

set_sidebar(
    user={
        "full_name": "John Doe",
        "avatar_url": "https://avatars.githubusercontent.com/u/832385?s=200&v=4",
    }
)


st.title("Update Team")


def get_team_id(supabase, div, roll_no):
    try:
        response = (
            supabase.table("students")
            .select("team_id")
            .eq("div", div)
            .eq("roll_no", roll_no)
            .execute()
        )
        return response.data[0]["team_id"]
    except Exception as e:
        print(e)
        return 0


def get_team_no(supabase, div, roll_no):
    team_id = get_team_id(supabase, div, roll_no)
    try:
        response = supabase.table("teams").select("team_no").eq("id", team_id).execute()
        return response.data[0]["team_no"]
    except Exception as e:
        print(e)
        return 0


st.subheader(f"You are in team div - team_no")


if __name__ == "__main__":
    st.write("Team number")
