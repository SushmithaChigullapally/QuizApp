import streamlit as st
import plotly.graph_objects as go
from utils.gemini_helper import generate_explanation

def create_score_chart(score, total):
    """Create a gauge chart for the quiz score"""
    score_percentage = (score / total) * 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score_percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Quiz Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "lightblue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    return fig

def display_results(questions):
    """Display quiz results with visualizations and explanations"""
    st.session_state.score = sum(
        1 for q in st.session_state.answers.values()
        if q['selected'] == q['correct']
    )
    
    st.subheader("Quiz Results")
    
    # Display score gauge
    fig = create_score_chart(st.session_state.score, len(questions))
    st.plotly_chart(fig)
    
    # Display detailed feedback
    for i, q in st.session_state.answers.items():
        with st.expander(f"Question {i + 1} Details"):
            st.write(q['question'])
            selected = q['selected']
            correct = q['correct']
            
            if selected == correct:
                st.success(f"✅ Correct! You selected {selected}) {q['options'][selected]}")
            else:
                st.error(f"❌ Wrong! You selected {selected}) {q['options'][selected]}")
                st.write(f"The correct answer was {correct}) {q['options'][correct]}")

            # Get explanation if not already generated
            if i not in st.session_state.explanations:
                with st.spinner("Generating explanation..."):
                    explanation = generate_explanation(q['question'], q['options'][correct])
                    st.session_state.explanations[i] = explanation
            
            if st.button("Show Explanation", key=f"exp_{i}"):
                st.info(st.session_state.explanations[i])
