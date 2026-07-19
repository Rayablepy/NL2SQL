import asyncio
import os
import streamlit as st
from loader import save_data
from main import getresponse

SAMPLE_DIR = "sample_data"
os.makedirs(SAMPLE_DIR, exist_ok=True)

with st.sidebar:
    st.header("Upload Data")
    uploaded_files = st.file_uploader(
        "Upload files to sample_data",
        type=["pdf", "csv", "txt", "docx", "xlsx"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        for f in uploaded_files:
            dest = os.path.join(SAMPLE_DIR, f.name)
            save_data(f.name)
            with open(dest, "wb") as out:
                out.write(f.getbuffer())
        st.success(f"Saved {len(uploaded_files)} file(s) to {SAMPLE_DIR}")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Your input here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(getresponse(prompt))
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
