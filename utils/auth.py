import streamlit as st

def get_student_name():
    if "student_name" not in st.session_state:
        st.session_state.student_name = ""
    name = st.text_input("👤 Student name (optional)", value=st.session_state.student_name)
    st.session_state.student_name = name
    return name or "Student"
