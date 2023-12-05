import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

ps = PorterStemmer()

# Read the job dataset
dataset_path = './datasets/job_postings.csv'
data = pd.read_csv(dataset_path)

# Replace characters only in specific columns
def replace_characters(x):
    return str(x).replace(' ', ',').replace(',,', ',').replace(':', '').replace('_', '').replace('(', '').replace(')', '') if pd.notna(x) else x

columns_to_replace = ['title', 'description', 'skills_desc']

for col in columns_to_replace:
    data[col] = data[col].apply(replace_characters)

# Combine relevant columns into 'tags'
data['tags'] = data['title'] + data['description'] + data['skills_desc'] + data['job_posting_url']

# Dataframe to be used
new_df = data[['title', 'tags']]
new_df['tags'] = data['tags'].str.replace(',', ' ')
new_df['title'] = data['title'].str.replace(',', ' ')
new_df.rename(columns={'title': 'job_title'}, inplace=True)
new_df['tags'] = new_df['tags'].apply(lambda x: str(x).lower() if pd.notna(x) else '')

# Text Vectorization
cv = CountVectorizer(max_features=500, stop_words='english')
vectors = csr_matrix(cv.fit_transform(new_df['tags']))

# Use TruncatedSVD for dimensionality reduction
n_components = 300  # Adjust the number of components as needed
svd = TruncatedSVD(n_components=n_components)
vectors = svd.fit_transform(vectors)

# Stemming Process
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

similarity = cosine_similarity(vectors)

def recommendJob(user_skills, user_job_category):
    # Combine user input into a tag
    user_tags = f"{user_job_category} {user_skills}"

    # Stemming process
    user_tags = stem(replace_characters(user_tags.lower()))

    # Transform user input into vector
    user_vector = cv.transform([user_tags]).toarray()
    user_vector = svd.transform(user_vector)  # Transform the user vector using TruncatedSVD

    # Calculate cosine similarity between user input and all jobs
    user_similarity = cosine_similarity(user_vector, vectors)

    # Find the job indices sorted by similarity
    job_indices = sorted(enumerate(user_similarity[0]), reverse=True, key=lambda x: x[1])[1:6]

    # Display recommended jobs
    st.subheader("Recommended Jobs:")
    for index, _ in job_indices:
        st.write(f"Job Title: {new_df.iloc[index].job_title}")
        st.write(f"Job Description: {data.iloc[index]['description']}")
        st.write(f"Job URL: {data.iloc[index]['job_posting_url']}")
        st.write("-" * 50)  # Separator for better readability
