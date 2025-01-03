from pyngrok import ngrok
import os
import requests
import streamlit as st

# Set your ngrok authtoken (replace with your own token)
ngrok.set_auth_token("2r4rR7EB6fEySe2d1AbZ7mWQxoA_76AgXFS9gYYAK3vyEScZq")

# Open a tunnel on port 8501 for Streamlit
public_url = ngrok.connect(8501)

print(f"Streamlit app is available at {public_url}")

# Replace with your Groq API key
GROQ_API_KEY = "YOUR_API_KEY"
GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# Function to generate improvement suggestions based on feedback
def generate_improvement_suggestion(prompt):
    # One-line real-time response based on feedback content
    if "food" in prompt.lower():
        if "cold" in prompt.lower():
            return "Ensure food is served at the appropriate temperature and improve service efficiency."
        else:
            return "Consider diversifying the menu and ensuring fresh ingredients."
    
    elif "room" in prompt.lower() or "bed" in prompt.lower():
        if "spotless" in prompt.lower():
            return "Maintain high cleanliness standards and prioritize comfort."
        elif "uncomfortable" in prompt.lower():
            return "Upgrade bed mattresses and improve room maintenance."
        else:
            return "Ensure consistency in room cleanliness and comfort."
    
    elif "staff" in prompt.lower():
        if "accommodating" in prompt.lower():
            return "Ensure all staff maintain positive attitudes and are well-trained."
        elif "unhelpful" in prompt.lower():
            return "Provide additional training to improve staff responsiveness."
    
    elif "wifi" in prompt.lower():
        return "Upgrade the Wi-Fi infrastructure for better reliability and speed."
    
    elif "noise" in prompt.lower():
        return "Improve soundproofing and manage noise levels effectively."
    
    elif "check-out" in prompt.lower():
        return "Simplify the check-out process and improve staff efficiency."
    
    else:
        return "Review feedback in specific areas for further improvements."

# Function to analyze feedback using the Groq API
def analyze_feedback_with_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"Analyze this feedback: {prompt}"}]
    }
    try:
        response = requests.post(GROQ_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        # Extract response content (analysis)
        response_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Sentiment analysis (simple approach based on response content)
        if "positive" in response_content.lower():
            sentiment = "POSITIVE"
            confidence = 0.9
        elif "negative" in response_content.lower():
            sentiment = "NEGATIVE"
            confidence = 0.9
        else:
            sentiment = "NEUTRAL"
            confidence = 0.5
        
        # Rating based on sentiment
        if sentiment == "POSITIVE":
            rating = "5/5"
        elif sentiment == "NEGATIVE":
            rating = "2/5"
        else:
            rating = "3/5"

        # Improvement suggestion based on feedback
        improvement = generate_improvement_suggestion(prompt)

        return sentiment, confidence, rating, improvement

    except requests.exceptions.RequestException as e:
        return "Error in API request", 0, "N/A", "Unable to analyze feedback due to an error."

# Define the Streamlit app script
streamlit_code = """
import streamlit as st
import requests

# Replace with your Groq API key
GROQ_API_KEY = "YOUR_API_KEY"
GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# Function to generate improvement suggestions based on feedback
def generate_improvement_suggestion(prompt):
    if "food" in prompt.lower():
        if "cold" in prompt.lower():
            return "Ensure food is served at the appropriate temperature and improve service efficiency."
        else:
            return "Consider diversifying the menu and ensuring fresh ingredients."
    
    elif "room" in prompt.lower() or "bed" in prompt.lower():
        if "spotless" in prompt.lower():
            return "Maintain high cleanliness standards and prioritize comfort."
        elif "uncomfortable" in prompt.lower():
            return "Upgrade bed mattresses and improve room maintenance."
        else:
            return "Ensure consistency in room cleanliness and comfort."
    
    elif "staff" in prompt.lower():
        if "accommodating" in prompt.lower():
            return "Ensure all staff maintain positive attitudes and are well-trained."
        elif "unhelpful" in prompt.lower():
            return "Provide additional training to improve staff responsiveness."
    
    elif "wifi" in prompt.lower():
        return "Upgrade the Wi-Fi infrastructure for better reliability and speed."
    
    elif "noise" in prompt.lower():
        return "Improve soundproofing and manage noise levels effectively."
    
    elif "check-out" in prompt.lower():
        return "Simplify the check-out process and improve staff efficiency."
    
    else:
        return "Review feedback in specific areas for further improvements."

# Function to analyze feedback using the Groq API
def analyze_feedback_with_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": f"Analyze this feedback: {prompt}"}]
    }
    try:
        response = requests.post(GROQ_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        response_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if "positive" in response_content.lower():
            sentiment = "POSITIVE"
            confidence = 0.9
        elif "negative" in response_content.lower():
            sentiment = "NEGATIVE"
            confidence = 0.9
        else:
            sentiment = "NEUTRAL"
            confidence = 0.5
        
        if sentiment == "POSITIVE":
            rating = "5/5"
        elif sentiment == "NEGATIVE":
            rating = "2/5"
        else:
            rating = "3/5"

        improvement = generate_improvement_suggestion(prompt)

        return sentiment, confidence, rating, improvement

    except requests.exceptions.RequestException as e:
        return "Error in API request", 0, "N/A", "Unable to analyze feedback due to an error."

# Streamlit app title and description
st.title('Customer Feedback Analysis with Real-Time Improvement Suggestions')
st.write('Enter customer feedback to analyze sentiment, receive a confidence score, and get improvement suggestions based on the feedback.')

# Feedback input area
feedback = st.text_input("Enter Feedback:")

if feedback:
    sentiment, confidence, rating, improvement = analyze_feedback_with_groq(feedback)
    
    st.write(f"**Feedback:** {feedback}")
    st.write(f"**Sentiment:** {sentiment}")
    st.write(f"**Confidence:** {confidence}")
    st.write(f"**Rating:** {rating}")
    st.write(f"**Improvement Suggestion:** {improvement}")
else:
    st.write("Please enter some feedback to analyze.")
"""

# Save the Streamlit script to a file
with open("app.py", "w") as file:
    file.write(streamlit_code)

# Run the Streamlit app in the background
os.system("streamlit run app.py")
