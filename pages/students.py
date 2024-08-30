from backend.students import get_students

set_sidebar(
    user={
        "full_name": "John Doe",
        "avatar_url": "https://avatars.githubusercontent.com/u/832385?s=200&v=4",
    }
)
st.title("Students in PCE Comp Engg")


def show_students():
    students = get_students()
    st.dataframe(students, width=1000, height=500)


def main():
    show_students()


main()
