"""Run with: streamlit run app.py"""
import streamlit as st
from llm import ask_llm
from rag import retrieve, build_context

st.set_page_config(page_title="Project VITAL — RAG Lab")
st.title("Project VITAL — Chatbot and RAG")
use_rag = st.sidebar.toggle("Enable RAG", value=False)
k = st.sidebar.slider("Retrieved documents", 1, 5, 2)
if "messages" not in st.session_state:
    st.session_state.messages = []
if st.sidebar.button("Clear conversation"):
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
question = st.chat_input("Ask about the fictional clinic policies")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    try:
        sources = []
        if use_rag:
            hits = retrieve(question, k)
            sources = [name for name, _, _ in hits]
            answer = ask_llm(question, build_context(hits))
        else:
            answer = ask_llm(question)
        if sources:
            answer += "\n\nRetrieved sources: " + ", ".join(sources)
    except Exception as exc:
        answer = f"Model unavailable: {exc}. Check that Ollama is running and the model is downloaded."
    with st.chat_message("assistant"):
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})