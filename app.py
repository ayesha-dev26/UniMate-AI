import streamlit as st
import os
from groq import Groq

st.set_page_config(
    page_title="UniMate AI",
    page_icon="🎓"
)

st.title("🎓 UniMate AI")
st.write("Your AI-powered University Assistant")

api_key = st.secrets["GROQ_API_KEY"]
st.write("API key loaded:", api_key.startswith("gsk_"))
st.write("API key length:", len(api_key))
st.write("API key preview:", api_key[:4])
st.write("Secret names:", list(st.secrets.keys()))

if not api_key:
    st.error("Groq API key not found. Check Codespaces Secrets.")
    st.stop()

client = Groq(api_key=api_key)

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
                            "content": "You are UniMate AI, a helpful university study assistant."
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
                st.error(f"Erroe:{e}")
