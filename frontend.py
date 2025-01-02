
import streamlit as st
import pandas as pd

# Title
st.title("Sentiment Analysis for Hospitality Feedback")

# Load the results
data_file = "results.csv"
data = pd.read_csv(data_file)

# Display the results
st.write("### Sentiment Analysis Results")
st.dataframe(data)
