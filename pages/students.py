import streamlit as st
from backend.students import get_all_students, get_student_by_batch
from frontend.sidebar.sidebar import set_sidebar

st.set_page_config(page_title="Students", layout="wide", page_icon=":material/people:")
set_sidebar()

st.title(":material/people: Students in SE Comp Engineering")

all, batch = st.tabs(["All Students", "Filter By Div/Batch"])


def show_students():
    students: dict = get_all_students()
    st.dataframe(students, width=1000, height=500)


def show_students_by_batch():
    st.subheader(" Select Division", divider=True)
    div = st.radio(
        "Select Division",
        ["A", "B"],
        key="batch_div",
        horizontal=True,
        label_visibility="collapsed",
    )

    st.subheader("Enter The Batch", divider=True)
    batch = st.radio(
        "Select Batch",
        ["Show all batches", "1", "2", "3"],
        horizontal=True,
        label_visibility="collapsed",
    )
    students: dict = get_student_by_batch(div, batch)
    st.dataframe(students, width=1000, height=500)


def main():

    with all:
        show_students()

    with batch:
        show_students_by_batch()


main()
