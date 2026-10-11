from gtts import gTTS
import streamlit as st
from tutor_chat import render_tutor_chat
from quiz_generator import render_quiz
from flashcards import render_flashcard_page
from dashboard import render_dashboard
from utils.auth import get_student_name

def voice_tutor(last_answer: str):
    st.subheader("🔊 Voice Tutor (beta)")
    if not last_answer:
        st.info("Ask a question in Tutor Chat or Homework Solver first to generate audio.")
        return
    if st.button("Generate audio for last answer"):
        tts = gTTS(text=last_answer, lang="en")
        audio_bytes = tts_to_bytes(tts)
        st.audio(audio_bytes, format="audio/mp3")

def tts_to_bytes(tts_obj):
    import io
    buf = io.BytesIO()
    tts_obj.write_to_fp(buf)
    buf.seek(0)
    return buf.getvalue()

def main():
    subject = st.sidebar.selectbox(
        "📚 Subject",
        [
            "General",
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "English",
            "History",
            "Economics",
            "Computer Science"
        ]
    )
    step_by_step = st.sidebar.checkbox("✅ Step-by-step explanations", value=True)
    student_name = get_student_name()

    mode = st.sidebar.radio(
        "🧭 Mode",
        ["Tutor Chat", "Homework Solver", "Quiz Generator", "Flashcard Generator", "Dashboard", "Voice Tutor (beta)"]
    )

    if mode in ["Tutor Chat", "Homework Solver"]:
        render_tutor_chat(subject, step_by_step, mode, student_name)
    elif mode == "Quiz Generator":
        render_quiz(subject, step_by_step)
    elif mode == "Flashcard Generator":
        render_flashcard_page(subject)
    elif mode == "Dashboard":
        render_dashboard(student_name)
    elif mode == "Voice Tutor (beta)":
        # Use last assistant answer from Tutor Chat / Homework Solver
        last_answer = None
        for key in st.session_state:
            if key.startswith("chat_history_"):
                history = st.session_state[key]
                for msg in reversed(history):
                    if msg["role"] == "assistant":
                        last_answer = msg["content"]
                        break
        voice_tutor(last_answer)

if __name__ == "__main__":
    main()
