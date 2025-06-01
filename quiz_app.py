# import streamlit as st
# from utils.gemini_helper import generate_quiz_questions
# from components.quiz_form import display_quiz_form
# from components.quiz_results import display_results

# def main():
#     st.title("🎯 AI-Powered Quiz Generator")
    
#     # Initialize session state
#     if 'quiz_started' not in st.session_state:
#         st.session_state.quiz_started = False
    
#     # Show configuration only if quiz hasn't started
#     if not st.session_state.quiz_started:
#         st.write("Generate custom quizzes on any topic using Google's Gemini AI!")
        
#         with st.form("quiz_config"):
#             topic = st.text_input("Enter the quiz topic:", placeholder="e.g., World History")
#             num_questions = st.slider("Number of questions:", min_value=1, max_value=10, value=5)
#             difficulty = st.select_slider(
#                 "Select difficulty level:",
#                 options=["Easy", "Medium", "Hard"],
#                 value="Medium"
#             )
            
#             generate_button = st.form_submit_button("Start Quiz")

#         if generate_button:
#             if not topic:
#                 st.warning("Please enter a topic!")
#                 return

#             with st.spinner("Generating your quiz..."):
#                 questions = generate_quiz_questions(topic, num_questions, difficulty)

#             if questions:
#                 # Store questions in session state
#                 st.session_state.questions = questions
#                 # Reset quiz state
#                 st.session_state.current_question = 0
#                 st.session_state.submitted = False
#                 st.session_state.answers = {}
#                 st.session_state.explanations = {}
#                 st.session_state.quiz_started = True
#                 st.experimental_rerun()
    
#     # Display quiz if it's started
#     else:
#         if 'questions' in st.session_state:
#             # Add a restart button
#             if st.sidebar.button("Start New Quiz"):
#                 st.session_state.quiz_started = False
#                 st.session_state.questions = None
#                 st.experimental_rerun()
            
#             if display_quiz_form(st.session_state.questions):
#                 display_results(st.session_state.questions)

# if __name__ == "__main__":
#     main()


import google.generativeai as genai
import streamlit as st


genai.configure(api_key="AIzaSyCah6l-MWhyWsXPBWMjU0JCWt2l_psJsWY")

def generate_quiz_questions(topic, num_questions, difficulty):
    """Generate quiz questions using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""Create {num_questions} multiple-choice {difficulty}-level questions from the text "{topic}". 
Format each question exactly as follows:
Q: [Question]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct: [Correct Letter]

Make sure to separate each question with a newline."""
        
        response = model.generate_content(prompt)
        return parse_questions(response.text)
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return []

def generate_explanation(question, correct_answer):
    """Generate explanation for a question using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""Explain why this is the correct answer:
Question: {question}
Correct Answer: {correct_answer}

Provide a clear and concise explanation."""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Unable to generate explanation: {str(e)}"

def parse_questions(raw_questions):
    """Parse the raw question text into structured format"""
    questions = []
    current_question = {}

    for line in raw_questions.split('\n'):
        line = line.strip()
        if not line:
            if current_question:
                questions.append(current_question)
                current_question = {}
        elif line.startswith('Q:'):
            if current_question:
                questions.append(current_question)
            current_question = {'question': line[2:].strip(), 'options': []}
        elif line.startswith(('A)', 'B)', 'C)', 'D)')):
            current_question['options'].append(line[2:].strip())
        elif line.startswith('Correct:'):
            current_question['correct'] = line[8:].strip()

    if current_question:
        questions.append(current_question)

    return questions
