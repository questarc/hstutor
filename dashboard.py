import streamlit as st

def render_dashboard(student_name: str):
    st.subheader("📊 Teacher & Student Dashboard")

    questions = st.session_state.get("questions_answered", 0)
    quizzes = st.session_state.get("quizzes_generated", 0)
    flashcards = st.session_state.get("flashcards_generated", 0)

    st.markdown(f"**👤 Student:** {student_name}")
    st.markdown(f"- 💬 Questions answered: **{questions}**")
    st.markdown(f"- 📝 Quizzes generated: **{quizzes}**")
    st.markdown(f"- 📚 Flashcard sets generated: **{flashcards}**")

    st.write("Use this dashboard to track engagement and activity over time.")
