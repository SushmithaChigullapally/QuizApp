import streamlit as st
from .quiz_navigation import initialize_quiz_state, next_question, prev_question

def display_question(question, question_num, total_questions):
    """Display a single question with navigation controls"""
    # Create three columns for better layout
    col1, col2, col3 = st.columns([1, 10, 1])
    
    with col2:
        # Progress bar and question counter
        st.progress((question_num) / total_questions)
        st.write(f"Question {question_num + 1} of {total_questions}")
        
        # Question display
        st.write(question['question'])
        
        options = {
            'A': question['options'][0],
            'B': question['options'][1],
            'C': question['options'][2],
            'D': question['options'][3]
        }
        
        answer = st.radio(
            "Select your answer:",
            options.keys(),
            format_func=lambda x: f"{x}) {options[x]}",
            key=f"q_{question_num}"
        )
        
        st.session_state.answers[question_num] = {
            'selected': answer,
            'correct': question['correct'],
            'question': question['question'],
            'options': options
        }
        
        # Navigation buttons
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            if question_num > 0:
                st.button("← Previous", on_click=prev_question, use_container_width=True)
        
        with button_col2:
            if question_num < total_questions - 1:
                st.button("Next →", on_click=next_question, use_container_width=True)
            else:
                st.button("Submit Quiz", on_click=lambda: setattr(st.session_state, 'submitted', True), 
                         type="primary", use_container_width=True)

def display_quiz_form(questions):
    """Display the quiz with navigation"""
    initialize_quiz_state()
    
    if not st.session_state.submitted:
        display_question(
            questions[st.session_state.current_question],
            st.session_state.current_question,
            len(questions)
        )
        return False
    
    return True



