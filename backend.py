
import pandas as pd
from transformers import pipeline

# Load a pre-trained sentiment analysis pipeline from Hugging Face
sentiment_pipeline = pipeline("sentiment-analysis")

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

# Function to analyze sentiment and assign ratings
def analyze_sentiments_with_ratings(prompt_list):
    results = []
    for prompt in prompt_list:
        result = sentiment_pipeline(prompt)
        sentiment = result[0]['label']
        confidence = round(result[0]['score'], 2)

        # Assign ratings based on sentiment and confidence
        if sentiment == "POSITIVE":
            rating = 5 if confidence > 0.8 else 4
        elif sentiment == "NEGATIVE":
            rating = 1 if confidence > 0.8 else 2
        else:
            rating = 3  # Neutral or less confident outputs

        results.append({
            "text": prompt,
            "sentiment": sentiment,
            "confidence": confidence,
            "rating": rating
        })
    return results

# Analyze the prompts
analysis_results = analyze_sentiments_with_ratings(prompts)

# Save the results to a CSV file
df = pd.DataFrame(analysis_results)
df.to_csv("results.csv", index=False)
