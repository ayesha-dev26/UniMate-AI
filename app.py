import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="UniMate AI",
    page_icon="🎓"
)

st.title("🎓 UniMate AI")
st.write("Your AI-powered University Assistant")

api_key = st.secrets.get("GROQ_API_KEY", "")
st.write("API key length:", len(api_key))

if not api_key:
    st.error("Groq API key not found.")
    st.stop()

client = Groq(api_key=api_key)

st.subheader("Ask UniMate AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask your university question...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": """You are UniMate AI, an expert academic assistant for university students.

Answer academic questions accurately and clearly.
Use simple English.
Explain concepts step by step.
Give relevant examples.
For programming, explain code and logic.
For mathematics, show calculations step by step.
For computer science topics, provide correct technical explanations.
Do not invent facts.
If you are unsure, say so honestly.
Stay focused on the student's question."""
                        },
                        *st.session_state.messages
                    ]
                )

                answer = response.choices[0].message.content

                st.write(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

st.subheader("About UniMate AI")

st.write(
    "UniMate AI helps university students with "
    "their academic questions and learning."
)

st.caption("© 2026 UniMate AI | Your Smart University Assistant")
