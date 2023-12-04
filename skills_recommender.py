import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_job_categories_from_csv(file_path):
    job_categories = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row['Job Category']
            skills = row['Skills'].split(', ')
            job_categories[category] = skills
    return job_categories


def calculate_similarity(resume_skills, recommended_skills):
    all_skills = ' '.join(resume_skills + recommended_skills)
    vectorizer = CountVectorizer().fit_transform([all_skills, ' '.join(recommended_skills)])
    similarity_matrix = cosine_similarity(vectorizer)
    similarity_score = similarity_matrix[0, 1]
    return similarity_score



def recommend_skills(resume_skills, csv_file_path):
    job_categories = read_job_categories_from_csv(csv_file_path)

    max_similarity = 0
    recommended_category = ''
    for category, recommended_skills in job_categories.items():
        similarity_score = calculate_similarity(resume_skills, recommended_skills)
        if similarity_score > max_similarity:
            max_similarity = similarity_score
            recommended_category = category

    return recommended_category, job_categories[recommended_category]
