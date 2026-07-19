import asyncio
import os
from config import ACTUAL_FILE_PATH
import streamlit as st
from loader import save_data
from main import getresponse

DIR = ACTUAL_FILE_PATH
os.makedirs(DIR, exist_ok=True)

with st.sidebar:
    st.header("Upload Data")
    uploaded_files = st.file_uploader(
        "Upload files to sample_data",
        type=["pdf", "csv", "txt", "docx", "xlsx"],
        accept_multiple_files=True,
    )
    if uploaded_files:
        for f in uploaded_files:
            dest = os.path.join(DIR, f.name)
            with open(dest, "wb") as out:
                out.write(f.getbuffer())
                save_data(f.name)
        st.success(f"Saved {len(uploaded_files)} file(s) to {DIR}")

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
