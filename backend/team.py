import streamlit as st


def get_student_status(roll, div):
    supabase = st.session_state.supabase
    if roll:
        try:
            student = (
                supabase.table("students")
                .select("team_id", "name")
                .eq("div", div)
                .eq("roll_no", roll)
                .execute()
            )
            status = [student.data[0]["name"], student.data[0]["team_id"]]
            # st.write(status)
            return status
        except Exception as e:
            st.error(f"Failed to fetch student: {e}")
            return {}


def get_max_team_id(div):
    supabase = st.session_state.supabase
    try:
        response = supabase.table("teams").select("div", "team_no.max()").execute()
        # print(response)
        if response.data == []:
            return 1
        elif len(response.data) == 1:
            if response.data[0]["div"] == div:
                return response.data[0]["max"] + 1
            else:
                return 1
        else:
            for item in response.data:
                if item["div"] == div:
                    return item["max"] + 1

    except Exception as e:
        print(e)
        return 0


def update_student(roll_calls, team_id):
    supabase = st.session_state.supabase
    for i in roll_calls:
        try:
            response = (
                supabase.table("students")
                .eq("roll_no", i)
                .update({"team_id": team_id})
                .execute()
            )
            print(response)
        except Exception as e:
            print(e)
            return


def add_team(data):
    supabase = st.session_state.supabase
    team_no = get_max_team_id(data["div"])
    data["team_no"] = team_no
    roll_calls = data["roll_calls"]
    del data["roll_calls"]
    try:
        response = supabase.table("teams").insert(data).execute()
        print(response)
        id = response.data[0]["id"]
        # update_student(supabase, roll_calls, id)
    except Exception as e:
        print(e)
