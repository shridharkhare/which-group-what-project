import streamlit as st


def get_student_status(roll, div):
    supabase = st.session_state.supabase
    if roll:
        try:
            student = (
                supabase.table("students")
                .select("name", "team_id")
                .match({"roll_no": roll, "div": div})
                .execute()
            )
            status = [student.data[0]["name"], student.data[0]["team_id"]]
            return status
        except Exception as e:
            st.error(f"Failed to fetch student: {e}")
            return {}


def get_max_team_id(div):
    supabase = st.session_state.supabase
    try:
        response = supabase.table("teams").select("div", "team_no.max()").execute()
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


def update_student(student_id, team_id):
    supabase = st.session_state.supabase
    try:
        response = (
            supabase.table("students")
            .update({"team_id": team_id})
            .match({"student_id": student_id})
            .execute()
        )
        return response
    except Exception as e:
        print(e)
        return


def request_students(roll_calls, data):
    supabase = st.session_state.supabase
    for i in roll_calls:
        receiver_id = "CE" + data["div"] + "3" + str(i).zfill(2)
        try:
            response = (
                supabase.table("team_req")
                .insert({"sender_id": data["leader_id"], "receiver_id": receiver_id})
                .execute()
            )
            print(response)
            return response
        except Exception as e:
            print(e)
            return


def add_team(data):
    supabase = st.session_state.supabase

    team_no = get_max_team_id(data["div"])
    data["team_no"] = team_no

    no_of_students = len(data["roll_calls"])
    data["no_mem"] = no_of_students

    roll_calls = data["roll_calls"]
    del data["roll_calls"]

    team_id = "T" + data["div"] + str(team_no)
    data["team_id"] = team_id

    try:
        response = supabase.table("teams").insert(data).execute()
        update_student(data["leader_id"], team_id)
        request_students(roll_calls, data)
    except Exception as e:
        print(e)


def get_my_team_id(student_id):
    supabase = st.session_state.supabase
    try:
        response = (
            supabase.table("students")
            .select("team_id")
            .match({"student_id": student_id})
            .execute()
        )
        return response.data[0]["team_id"]
    except Exception as e:
        st.error(f"Failed to fetch team id: {e}")
        return


def get_team_topic(team_id):
    supabase = st.session_state.supabase
    try:
        response = (
            supabase.table("teams").select("*").match({"team_id": team_id}).execute()
        )
        return response.data[0]
    except Exception as e:
        st.error(f"Failed to fetch team: {e}")
        return


def get_team_members(team_id):
    supabase = st.session_state.supabase
    try:
        response = (
            supabase.table("students")
            .select("student_id", "name", "roll_no")
            .match({"team_id": team_id})
            .execute()
        )
        return response.data
    except Exception as e:
        st.error(f"Failed to fetch team members: {e}")
        return


def get_my_team(student_id):
    team_id = get_my_team_id(student_id)
    if not team_id:
        return {}, []
    team_details = get_team_topic(team_id)
    team_members = get_team_members(team_id)
    return team_details, team_members


def send_team_for_approval(team_id):
    supabase = st.session_state.supabase
    try:
        current_user = st.session_state.user["student_id"]
        response = (
            supabase.table("teams")
            .update({"leader_okay": True})
            .match({"team_id": team_id, "leader_id": current_user})
            .execute()
        )
        return response
    except Exception as e:
        st.error(f"Failed to send team for approval: {e}")
        return
