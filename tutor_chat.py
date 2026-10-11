import streamlit as st
from utils.nvidia_client import complete

def build_system_prompt(subject: str, step_by_step: bool, mode: str):
    base = (
        "You are a friendly high school tutor. Explain concepts clearly and simply. "
        "Use markdown: headings, bullet points, bold key terms, and LaTeX for formulas."
    )
    if subject != "General":
        base += f" Focus on {subject} topics."
    if step_by_step:
        base += " Always explain in numbered, step-by-step format."
    if mode == "Homework Solver":
        base += " Help the student understand and solve homework problems, but show steps, not just final answers."
    return {"role": "system", "content": base}

def render_tutor_chat(subject: str, step_by_step: bool, mode: str, student_name: str):
    icon = "💬" if mode == "Tutor Chat" else "🧮"
    st.subheader(f"{icon} {mode}")

    key = "chat_history_" + mode.replace(" ", "_")
    if key not in st.session_state:
        st.session_state[key] = [build_system_prompt(subject, step_by_step, mode)]

    # Show history
    for msg in st.session_state[key]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    prompt_label = "Ask your question..." if mode == "Tutor Chat" else "Paste your homework problem..."
    user_input = st.chat_input(prompt_label)

    if user_input:
        if step_by_step:
            user_input = f"Explain this step-by-step for a high school student named {student_name}:\n\n" + user_input

        st.session_state[key].append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = complete(st.session_state[key])
            st.markdown(answer)
            st.session_state[key].append({"role": "assistant", "content": answer})

        # Progress tracking
        st.session_state["questions_answered"] = st.session_state.get("questions_answered", 0) + 1
