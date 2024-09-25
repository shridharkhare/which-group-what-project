import streamlit as st
from backend.students import get_students
from frontend.utils.sidebar import set_sidebar
from backend.students import get_students

set_sidebar()
st.title("Students in PCE Comp Engg")


def show_students():
    students: dict = get_students()
    st.dataframe(students, width=1000, height=500)


def main():
    show_students()


main()
