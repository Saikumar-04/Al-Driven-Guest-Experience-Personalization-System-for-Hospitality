import requests
import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker()
# Function to Provide Sentiment
def provide_sentiment(feedback: str):
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        payload = {
            "messages": [
                {"role": "user", "content": f"Provide sentiment for the feedback: {feedback}"},
            ]
        }
        response = requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers)
        if response.status_code == 200:
            sentiment_response = response.json()["choices"][0]["message"]["content"]
            return sentiment_response.strip()
        else:
            print(f"API Error: {response.status_code}, {response.text}")
            return "Neutral"
    except Exception as e:
        print(f"Sentiment API failed: {e}")
        return "Neutral"

# Generate Main Dataset
def generate_main_dataset(num_rows=10000):
    main_data = []
    for _ in range(num_rows):
        feedback = fake.sentence()  # Generate random feedback
        sentiment = provide_sentiment(feedback)  # Get sentiment from the API
        row = {
            "Customer Name": fake.name(),
            "Customer Mail ID": fake.email(),
            "Feedback": feedback,
            "Sentiment": sentiment,
            "Date and Time": fake.date_time_this_year(),
            "Caretaker/Server Name": fake.name(),
            "Care Employee ID": random.randint(1000, 9999),
            "Customer Age": random.randint(18, 85),
            "Customer Contact": fake.phone_number(),
            "Department": random.choice(["Housekeeping", "Room Service", "Dining", "Wellness"]),
            "Customer Stay Duration": random.randint(1, 30),
            "Number of Visits": random.randint(1, 20),
            "Membership Status": random.choice(["Gold", "Silver", "Platinum", "None"]),
            "Amount to be Paid": round(random.uniform(50, 5000), 2),
            "NPS": random.randint(0, 10),
        }
        main_data.append(row)
    return pd.DataFrame(main_data)

# Generate Preferences Dataset
def generate_preferences_dataset(num_rows=10000):
    preferences_data = []
    for _ in range(num_rows):
        row = {
            "Customer ID": _ + 1,
            "Dining Preference": random.choice(["Vegetarian", "Vegan", "Non-Vegetarian"]),
            "Room Preference": random.choice(["Deluxe", "Suite", "Standard"]),
            "Sports Activities": random.choice(["Table Tennis", "Golf", "Swimming", "None"]),
            "Wellness": random.choice(["Gym", "Sauna", "Massage", "None"]),
            "Pricing Pattern": random.choice(["Frugal", "Luxury"]),
        }
        preferences_data.append(row)
    return pd.DataFrame(preferences_data)

# Save Datasets to CSV
def save_datasets():
    # Generate and Save Main Dataset
    main_dataset = generate_main_dataset(10000)
    main_dataset.to_csv("Customer-feedback.csv", index=False)
    print("Main dataset created: 'Customer-feedback.csv'")

    # Generate and Save Preferences Dataset
    preferences_dataset = Customer-preferences_dataset(10000)
    preferences_dataset.to_csv("hospitality_preferences.csv", index=False)
    print("Preferences dataset created: 'Customer-Preference.csv'")

# Main Execution
if __name__ == "__main__":
    save_datasets()
