
import pandas as pd
import streamlit as st

from sklearn.feature_extraction.text import CountVectorizer
import nltk  # for stemming process
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

ps = PorterStemmer()
dataset_path = './datasets/Coursera.csv'
data = pd.read_csv(dataset_path)
data = data[['Course Name', 'Difficulty Level', 'Course Description', 'Skills', 'Course URL']]
# print(data.head(5))

## Data Pre-Processing
# Removing spaces between the words (Lambda funtions can be used as well)
# Define a lambda function to replace characters
replace_characters = lambda x: x.replace(' ', ',').replace(',,', ',').replace(':', '').replace('_', '').replace('(',
                                                                                                                '').replace(
    ')', '')
# Apply the lambda function to the specified columns
columns_to_replace = ['Course Name', 'Course Description', 'Skills']
data[columns_to_replace] = data[columns_to_replace].applymap(replace_characters)

# print(data.head(5))
data['tags'] = data['Course Name'] + data['Difficulty Level'] + data['Course Description'] + data['Skills'] + data[
    'Course URL']
data['tags'].iloc[1]
# print(data.head(5))
##Dataframe to be used
new_df = data[['Course Name', 'tags']]
new_df['tags'] = data['tags'].str.replace(',', ' ')
new_df['Course Name'] = data['Course Name'].str.replace(',', ' ')
new_df.rename(columns={'Course Name': 'course_name'}, inplace=True)
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())  # lower casing the tags column


##Text Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()


##Stemming Process
# defining the stemming function
def stem(text):
    y = []

    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)


new_df['tags'] = new_df['tags'].apply(stem)  # applying stemming on the tags column


similarity = cosine_similarity(vectors)


def recommendCourse(user_skills, user_job_category):
    # Combine user input into a tag
    user_tags = f"{user_job_category} {user_skills}"

    # Stemming process
    user_tags = stem(replace_characters(user_tags.lower()))

    # Transform user input into vector
    user_vector = cv.transform([user_tags]).toarray()

    # Calculate cosine similarity between user input and all courses
    user_similarity = cosine_similarity(user_vector, vectors)

    # Find the course indices sorted by similarity
    course_indices = sorted(enumerate(user_similarity[0]), reverse=True, key=lambda x: x[1])[1:7]

    # Display recommended courses
   # Header
    st.title("Recommended Courses")

    # Display recommended courses
    st.subheader("Recommended Courses:")

    # Create two columns for course names and URLs
    col1, col2 = st.columns(2)

    for index, _ in course_indices:
        # Display course name in the first column
        with col1:
            st.write(f"**Course Name:** {new_df.iloc[index]['course_name']}")
        
        # Display course URL in the second column
        with col2:
            st.write(f"**Course URL:** {data.iloc[index]['Course URL']}")

