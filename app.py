%%writefile app.py
import os
import streamlit as st
from backend import analyze_feedback_with_groq

# Streamlit app title and description
st.title('Customer Feedback Analysis with Real-Time Improvement Suggestions')
st.write('Enter customer feedback to analyze sentiment, receive a confidence score, and get improvement suggestions based on the feedback.')

# Feedback input area
feedback = st.text_input("Enter Feedback:")

if feedback:
    # Analyze feedback using the backend
    sentiment, confidence, rating, improvement = analyze_feedback_with_groq(feedback)
    
    # Display the results on the Streamlit UI
    st.write(f"**Feedback:** {feedback}")
    st.write(f"**Sentiment:** {sentiment}")
    st.write(f"**Confidence:** {confidence}")
    st.write(f"**Rating:** {rating}")
    st.write(f"**Improvement Suggestion:** {improvement}")
else:
    st.write("Please enter some feedback to analyze.")
