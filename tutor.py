import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

# ---------------------------
# Load API Key
# ---------------------------
load_dotenv()
API_KEY = os.getenv("NVIDIA_API_KEY")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=API_KEY
)

# ---------------------------
# Streamlit Setup
# ---------------------------
st.set_page_config(page_title="High School Tutor", layout="wide")
st.title("🎓 High School Tutor – NVIDIA‑Powered Learning Assistant")
st.write("A school-ready app for tutoring, quizzes, and flashcards across high school subjects.")

# ---------------------------
# Sidebar Controls
# ---------------------------
st.sidebar.header("Settings")

subject = st.sidebar.selectbox(
    "Subject",
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

step_by_step = st.sidebar.checkbox("Step-by-step explanations", value=True)

mode = st.sidebar.radio(
    "Mode",
    ["Tutor Chat", "Quiz Generator", "Flashcard Generator"]
)

# ---------------------------
# Build System Prompt
# ---------------------------
def build_system_prompt():
    prompt = "You are a friendly high school tutor. Explain concepts clearly and simply."

    if subject != "General":
        prompt += f" Focus on {subject}."

    if step_by_step:
        prompt += " Use step-by-step explanations."

    if mode == "Quiz Generator":
        prompt += " Generate multiple-choice quizzes with correct answers and explanations."

    if mode == "Flashcard Generator":
        prompt += " Generate flashcards in Term–Definition or Question–Answer format."

    return {"role": "system", "content": prompt}


# ---------------------------
# Streaming Helper (FIXED)
# ---------------------------
def stream_nvidia_response(messages):
    """
    FIXED streaming function:
    - Handles empty chunks
    - Handles missing choices
    - Streams reliably
    """
    response_text = ""

    completion = client.chat.completions.create(
        model="nvidia/nemotron-3.5-lightning-30b-a3b",
        messages=messages,
        temperature=0.6,
        top_p=0.9,
        max_tokens=2048,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        stream=True
    )

    for chunk in completion:
        if not hasattr(chunk, "choices"):
            continue
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        if not delta:
            continue

        content_piece = delta.content
        if content_piece:
            response_text += content_piece
            yield response_text


# ---------------------------
# Tutor Chat Mode
# ---------------------------
if mode == "Tutor Chat":
    st.subheader("Tutor Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [build_system_prompt()]

    # Display history
    for msg in st.session_state.chat_history:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    user_input = st.chat_input("Ask your question...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""

            for partial in stream_nvidia_response(st.session_state.chat_history):
                full = partial
                placeholder.write(full)

            st.session_state.chat_history.append({"role": "assistant", "content": full})


# ---------------------------
# Quiz Generator Mode
# ---------------------------
elif mode == "Quiz Generator":
    st.subheader("Quiz Generator")

    topic = st.text_input("Topic")
    num_questions = st.slider("Number of questions", 3, 15, 5)

    if st.button("Generate Quiz"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            messages = [
                build_system_prompt(),
                {
                    "role": "user",
                    "content": (
                        f"Create a {num_questions}-question multiple-choice quiz "
                        f"on: {topic}. Include correct answers and explanations."
                    )
                }
            ]

            with st.spinner("Generating quiz..."):
                full = ""
                for partial in stream_nvidia_response(messages):
                    full = partial
                    st.markdown(full)


# ---------------------------
# Flashcard Generator Mode
# ---------------------------
elif mode == "Flashcard Generator":
    st.subheader("Flashcard Generator")

    topic = st.text_input("Topic")
    num_cards = st.slider("Number of flashcards", 5, 30, 10)

    if st.button("Generate Flashcards"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            messages = [
                build_system_prompt(),
                {
                    "role": "user",
                    "content": (
                        f"Create {num_cards} flashcards for: {topic}. "
                        "Use Term–Definition or Question–Answer format."
                    )
                }
            ]

            with st.spinner("Generating flashcards..."):
                full = ""
                for partial in stream_nvidia_response(messages):
                    full = partial
                    st.markdown(full)
