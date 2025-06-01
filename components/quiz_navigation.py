import streamlit as st

def initialize_quiz_state():
    """Initialize quiz session state variables"""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'explanations' not in st.session_state:
        st.session_state.explanations = {}

def next_question():
    """Navigate to next question"""
    st.session_state.current_question += 1

def prev_question():
    """Navigate to previous question"""
    st.session_state.current_question -= 1