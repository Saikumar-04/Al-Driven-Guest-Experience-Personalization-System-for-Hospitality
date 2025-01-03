import json
import requests

# Replace with your Groq API key
GROQ_API_KEY = "YOUR_API_KEY"
GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# List of customer feedback prompts
prompts = [
    "The room was spotless, and the staff was incredibly accommodating.",
    "The food was cold, and the service took too long.",
    "We had a wonderful experience with the quick check-in and beautiful ambiance.",
    "The bed was uncomfortable, and the bathroom was not clean.",
    "The staff went out of their way to make our anniversary special.",
    "The Wi-Fi was unreliable, and it disrupted my work.",
    "The location is perfect, and the views are breathtaking.",
    "There was too much noise at night, and I couldn’t sleep.",
    "The breakfast spread was delightful, with plenty of healthy options.",
    "I found the check-out process confusing and the staff unhelpful."
]

# Function to generate improvement suggestions based on feedback
def generate_improvement_suggestion(prompt, response_content):
    # Real-time response based on feedback content
    if "food" in prompt.lower():
        if "cold" in prompt.lower():
            return "Ensure food is served at the appropriate temperature and improve service efficiency."
        else:
            return "Consider diversifying the menu and ensuring fresh ingredients."

    elif "room" in prompt.lower() or "bed" in prompt.lower():
        if "spotless" in prompt.lower():
            return "Maintain the high standards of cleanliness and ensure comfort is prioritized."
        elif "uncomfortable" in prompt.lower():
            return "Upgrade bed mattresses and improve room maintenance."
        else:
            return "Ensure consistency in room cleanliness and comfort."

    elif "staff" in prompt.lower():
        if "accommodating" in prompt.lower():
            return "Ensure all staff maintain a positive attitude and are well-trained in customer service."
        elif "unhelpful" in prompt.lower():
            return "Provide additional training to staff to improve responsiveness and guest interactions."

    elif "wifi" in prompt.lower():
        return "Upgrade the Wi-Fi infrastructure to offer stable and high-speed internet to guests."

    elif "noise" in prompt.lower():
        return "Address noise issues by improving soundproofing and managing noise levels in the facility."

    elif "check-out" in prompt.lower():
        return "Simplify the check-out process with clearer instructions and more efficient staff assistance."

    else:
        return "Review feedback in specific areas and identify further improvements."

# Function to analyze feedback using the Groq API
def analyze_feedback_with_groq(prompt_list):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    results = []
    for prompt in prompt_list:
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": f"Analyze this feedback: {prompt}"}]
        }
        try:
            response = requests.post(GROQ_API_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()

            # Extract the assistant's reply
            response_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

            # Generate an improvement suggestion based on response content and feedback
            improvement = generate_improvement_suggestion(prompt, response_content)

            results.append({
                "feedback": prompt,
                "response": response_content,
                "improvement_suggestion": improvement
            })

        except requests.exceptions.RequestException as e:
            results.append({
                "feedback": prompt,
                "error": str(e),
                "improvement_suggestion": "Unable to analyze feedback due to an error."
            })

    return results

# Analyze the prompts
analysis_results = analyze_feedback_with_groq(prompts)

# Print the results in JSON format
print(json.dumps(analysis_results, ensure_ascii=False, indent=4))

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the ngrok auth token from environment variables
ngrok_token = os.getenv("2r4rR7EB6fEySe2d1AbZ7mWQxoA_76AgXFS9gYYAK3vyEScZq")

# Print the token (for debugging, you can remove this later)
print(ngrok_token)
