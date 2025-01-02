
import streamlit as st
from transformers import pipeline

# Load sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Streamlit app title and description
st.title('Customer Feedback Sentiment Analysis')
st.write('Enter customer feedback to analyze sentiment, confidence score, and receive a rating.')

# Feedback input area
feedback = st.text_input("Enter Feedback:")

# Process the feedback after pressing Enter
if feedback:
    # Get sentiment analysis result
    result = sentiment_pipeline(feedback)
    sentiment = result[0]['label']
    confidence = round(result[0]['score'], 2)

    # Assign rating based on sentiment
    if sentiment == "POSITIVE":
        rating = "5/5"
    elif sentiment == "NEGATIVE":
        rating = "2/5"
    else:
        rating = "3/5"

    # Display the results: sentiment, confidence, and rating
    st.write(f"**Feedback:** {feedback}")
    st.write(f"**Sentiment:** {sentiment}")
    st.write(f"**Confidence:** {confidence}")
    st.write(f"**Rating:** {rating}")
