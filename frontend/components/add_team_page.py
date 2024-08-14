import pandas as pd
import streamlit as st
from supabase import Client, create_client


# Set up caching
@st.cache_resource
def connect_to_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
    return supabase

def get_max_team_id(supabase, div):
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

def update_student(supabase, roll_calls, team_id):
    for i in roll_calls:
        try:
            response = supabase.table("students").eq("roll_no", i).update({"team_id": team_id}).execute()
            print(response)
        except Exception as e:
            print(e)
            return

def add_team(supabase, data):
    team_no = get_max_team_id(supabase, data["div"])
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

def read_data(supabase):

    st.title("Welcome to the Which_Group_What_Project")
    st.header("Add a team")

    st.subheader("Select the number of students in the team", divider=True)
    num_students = st.radio("Number of students", [1, 2, 3, 4], horizontal=True, label_visibility="collapsed")
    
    st.subheader("Select the division of the team", divider=True)
    div = st.radio("Division", ["A", "B"], horizontal=True, label_visibility="collapsed")

    
    st.subheader(f"Enter roll-no of team members", divider=True)
    roll_calls = []
    
    for i in range(num_students):
        roll = st.number_input(f"Roll No of member {i+1}", value = None, placeholder = f"eg. {21+i}", min_value = 1, format = "%d")
        student_in_grp(supabase, roll, div)
        roll_calls.append(roll) #Remember to clear this on update or clear button

    st.subheader("Enter the topic name")
    topic = st.text_input(label="Topic name", label_visibility = "collapsed", placeholder="eg. Project 2232" )

    st.subheader("Enter roll no of the leader")
    leader_id = st.number_input("eg. 21", value = None, placeholder="eg. 21", min_value = 1,  format = "%d")
    
    data = {
        "div": div,
        "leader_id": leader_id,
        "topic": topic,
        "roll_calls": roll_calls
    }
    
    # st.write(data)
     
    if st.button("Submit"):
        submit_data(supabase, data, leader_id, roll_calls)     
    else: 
        pass
        
    if st.button("Clear"):
        data = {}
        st.write("Cleared")
        st.write(data)
        st.rerun()
        
def student_in_grp(supabase, roll, div):
    if roll:
            student = supabase.table("students").select("team_id", "name").eq("div", div).eq("roll_no", roll).execute()
            st.write(student.data[0]["name"])
            
            if student.data[0]["team_id"] is not None:
                st.warning("Student already in a team")
        
def submit_data(supabase, data, leader_id, roll_calls):
    # If any roll number is NULL
    if None in roll_calls:  
        st.warning("Please enter roll numbers for all students")
        return 
    
    #If project name is NULL: 
    if data["topic"] == "":
        st.warning("Please enter a project name")
        return
    
    #If roll number is not unique
    if len(roll_calls) != len(set(roll_calls)):
        st.warning("Roll numbers should be unique")
        return
    
    #If leader is not part of the team
    if leader_id not in roll_calls:
        st.warning("Leader should be part of the team")
        return
    
    add_team(supabase, data)
    st.success("Team added successfully")

def main ():
    # st.title("Welcome to the Which-Group-What-Project")
    # st.header("Please select student and enter project name")

    supabase = connect_to_supabase()
    # data = read_data()

    data = {
        "div": "A",
        "leader_id": 4,
        "topic": "Project 2232",
        "num_members" : 4,
        "members": [1, 2, 3, 4]
    }
    add_team(supabase, data)


if __name__ == "__main__":
    supabase = connect_to_supabase()
    read_data(supabase)
    
    