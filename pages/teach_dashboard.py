import streamlit as st

from frontend.sidebar.sidebar import set_sidebar
from backend.teach_dash import get_teams, approve_team
from frontend.utils.utils import convert_timestamp


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    st.subheader("Pending Approvals", anchor=None)
    appr_reqs = get_teams(False)

    req_count = len(appr_reqs)

    st.write(f"You currently have {req_count} pending approvals requests.")

    with st.container(border=True, height=530):
        for req in appr_reqs:
            with st.expander(
                f"Team: {req['team_id'][1:2:]} - {req['team_id'][2::]}",
                expanded=False,
            ):
                st.write(f"- **Leader:** {req['students']['name']}")

                st.write(f"- **Topic:** {req['topic']}")

                st.write(f"- **Number of members:** {req['no_mem']}")

                req_time = req["leader_okay_time"]
                converted_time = convert_timestamp(req_time)

                st.write(f"- **Requested at:** {converted_time}")

                for student in req["members"]:
                    st.write(f"*{student['student_id']}* - {student['name']}")

                if st.button("Approve"):
                    approve_team(req["team_id"])
                    st.rerun()


# Page starts here
st.set_page_config(
    page_title="Which-Group-What-Project",
    layout="wide",
    page_icon=":material/dashboard:",
)

set_sidebar()
st.title(":material/dashboard: Teacher Dashboard")

local_css("style.css")
main()
