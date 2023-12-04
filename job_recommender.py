import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np
import re

# Load your job posting dataset
job_data = pd.read_csv('job_postings.csv')

# Combine relevant text columns into one for job descriptions
job_data['text_data'] = job_data['description'] + ' ' + job_data['skills_desc']

# Preprocess the text data
job_data['text_data'] = job_data['text_data'].apply(lambda x: re.sub('[^a-zA-Z0-9\.]', ' ', str(x)).lower())

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=1000)

# Fit and transform the TF-IDF vectorizer on the job descriptions
tfidf_matrix = vectorizer.fit_transform(job_data['text_data'])

# Build a NearestNeighbors model
nn_model = NearestNeighbors(n_neighbors=10, algorithm='brute', metric='cosine')
nn_model.fit(tfidf_matrix)

# Now, use this model for user input as shown in the previous example
# Get user input and process it
user_input = st.text_area("Enter your skills and job description", '')
user_input = re.sub('[^a-zA-Z0-9\.]', ' ', user_input).lower()

# Transform the user input to a TF-IDF vector
user_tfidf = vectorizer.transform([user_input])

# Find the nearest neighbors based on cosine similarity
_, job_indices = nn_model.kneighbors(user_tfidf)

# Display top job recommendations
st.title('Top Job Recommendations (Content-Based)')
top_jobs = job_data.iloc[job_indices[0]][['title', 'description', 'max_salary', 'location']]
st.table(top_jobs)
