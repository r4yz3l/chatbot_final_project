import streamlit as st
from components.sidebar import render_sidebar
from components.chat_interface import render_chat

st.set_page_config(
    page_title="AI Productivity Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "style" not in st.session_state:
    st.session_state.style = "Santai"
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "goals" not in st.session_state:
    st.session_state.goals = []
if "notes" not in st.session_state:
    st.session_state.notes = []

render_sidebar()
render_chat()