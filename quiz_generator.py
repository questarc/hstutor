import streamlit as st
from utils.nvidia_client import complete

def build_quiz_system_prompt(subject: str, step_by_step: bool):
    base = (
        "You are a high school quiz generator. Create clear multiple-choice questions. "
        "Use markdown:\n"
        "- Each question starts with 'Q1:', 'Q2:', etc.\n"
        "- Options labeled A), B), C), D).\n"
        "- Include 'Correct answer:' and a brief explanation."
    )
    if subject != "General":
        base += f" Focus on {subject} topics."
    return {"role": "system", "content": base}

def render_quiz(subject: str, step_by_step: bool):
    st.subheader("📝 Quiz Generator")
    st.write("Generate practice quizzes with clear answers and explanations.")

    topic = st.text_input("📚 Topic (e.g., 'quadratic equations', 'cell division')")
    num_questions = st.slider("Number of questions", 3, 15, 5)

    if st.button("Generate Quiz"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            system_prompt = build_quiz_system_prompt(subject, step_by_step)
            user_prompt = (
                f"Create a {num_questions}-question multiple-choice quiz on: {topic}. "
                "Use the markdown format described."
            )
            messages = [system_prompt, {"role": "user", "content": user_prompt}]
            with st.spinner("Generating quiz..."):
                quiz_text = complete(messages)
            st.markdown(quiz_text)
            st.session_state["quizzes_generated"] = st.session_state.get("quizzes_generated", 0) + 1
