import streamlit as st
from groq import Groq
import pdfplumber


client = Groq(api_key="API_KEY")

st.title("Personal AI Assistant")


uploaded_file = st.file_uploader("Attach a file (optional)", type=["txt", "pdf", "py"])

file_content = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            file_content = "\n".join(page.extract_text() or "" for page in pdf.pages)
    else:
        file_content = uploaded_file.read().decode("utf-8")
    st.success(f" {uploaded_file.name} loaded!")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Clear"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    
    full_prompt = f"File content:\n{file_content}\n\nQuestion: {prompt}" if file_content else prompt

    st.session_state.messages.append({"role": "user", "content": full_prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = " Daily limit exceeded! Please try again tomorrow."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
