# Import libraries
import pandas as pd
from transformers import pipeline

# Load a pre-trained sentiment analysis pipeline from Hugging Face
sentiment_pipeline = pipeline("sentiment-analysis")

# Upload and load the feedback CSV file
from google.colab import files
uploaded = files.upload()
feedback_file = list(uploaded.keys())[0]  # Get the uploaded file name
feedback_data = pd.read_csv(feedback_file)

# Function to analyze sentiment with suggestions using prompt techniques
def analyze_sentiment_with_suggestions(feedback):
    try:
        # Define the prompt asking for sentiment analysis and improvement suggestions
        prompt = f"Please analyze the sentiment of the following feedback and provide suggestions for improvements based on the sentiment. Respond with a JSON object containing the sentiment and a brief suggestion for improvement.\n\nFeedback: {feedback}"
        
        # Send the feedback to the sentiment analysis pipeline with the custom prompt
        result = sentiment_pipeline(prompt[:512])  # Truncate to first 512 tokens for compatibility
        
        sentiment = result[0]['label']
        score = result[0]['score']
        
        # Suggestions for improvement based on the sentiment
        if sentiment == "NEGATIVE":
            suggestion = "Consider improving customer service and addressing the issues mentioned."
        elif sentiment == "POSITIVE":
            suggestion = "Continue maintaining the high quality of service and address any minor concerns."
        else:
            suggestion = "Maintain consistency in your service and try to enhance areas that received neutral feedback."

        # Return the sentiment and the suggestion for improvement in a structured JSON format
        sentiment_analysis_result = {
            "sentiment": sentiment,
            "confidence": round(score, 2),
            "suggestion": suggestion
        }
        return sentiment_analysis_result

    except Exception as e:
        return {"error": f"Error analyzing feedback: {e}"}

# Apply sentiment analysis to each feedback entry
feedback_data['Sentiment and Suggestion'] = feedback_data['Feedback'].apply(analyze_sentiment_with_suggestions)

# Trigger alerts for negative sentiment
alerts = feedback_data[feedback_data['Sentiment and Suggestion'].apply(lambda x: "NEGATIVE" in str(x['sentiment']).upper())]
if not alerts.empty:
    print("Alert: Negative sentiment detected in feedback!\n")
    print(alerts)

# Save results to a new JSON file
output_file = "feedback_analysis_results_with_suggestions.json"
feedback_data.to_json(output_file, orient="records", lines=True)
print(f"Sentiment analysis complete. Results saved to {output_file}.")
