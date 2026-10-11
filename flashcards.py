import streamlit as st
from utils.nvidia_client import complete
from utils.export import flashcards_to_csv_bytes, flashcards_to_pdf_bytes

def build_flashcard_system_prompt(subject: str):
    base = (
        "You are a high school flashcard generator. "
        "Generate flashcards in 'Term: ... – Definition: ...' or 'Question: ... – Answer: ...' format. "
        "One flashcard per line."
    )
    if subject != "General":
        base += f" Focus on {subject} topics."
    return {"role": "system", "content": base}

def render_flashcards(raw_text: str):
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    for line in lines:
        if "Term:" in line or "Question:" in line:
            st.markdown(
                f"""
<div style="
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 8px;
    background-color: #f0f9ff;
    border: 1px solid #90cdf4;
    font-size: 0.95rem;
">
{line}
</div>
""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(line)

def render_flashcard_page(subject: str):
    st.subheader("📚 Flashcard Generator")
    st.write("Generate colorful flashcards and download them as CSV or PDF.")

    topic = st.text_input("📘 Topic (e.g., 'geometry formulas', 'cell organelles')")
    num_cards = st.slider("Number of flashcards", 5, 30, 10)

    if st.button("Generate Flashcards"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            system_prompt = build_flashcard_system_prompt(subject)
            user_prompt = (
                f"Create {num_cards} flashcards for the topic: {topic}. "
                "Use one flashcard per line in 'Term: ... – Definition: ...' format."
            )
            messages = [system_prompt, {"role": "user", "content": user_prompt}]
            with st.spinner("Generating flashcards..."):
                cards_text = complete(messages)

            render_flashcards(cards_text)

            csv_bytes = flashcards_to_csv_bytes(cards_text)
            pdf_bytes = flashcards_to_pdf_bytes(cards_text, title=f"Flashcards – {topic}")

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download CSV",
                    data=csv_bytes,
                    file_name=f"flashcards_{topic.replace(' ', '_')}.csv",
                    mime="text/csv",
                )
            with col2:
                st.download_button(
                    "📥 Download PDF",
                    data=pdf_bytes,
                    file_name=f"flashcards_{topic.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                )

            st.session_state["flashcards_generated"] = st.session_state.get("flashcards_generated", 0) + 1
