import google.generativeai as genai
import streamlit as st


def generate_quiz_questions(topic, num_questions, difficulty):
    """Generate quiz questions using Gemini API"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""Create {num_questions} multiple-choice {difficulty}-level questions from the text {topic}. 
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



