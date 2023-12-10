from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber


def calculate_similarity(resume_skills, recommended_skills):
    all_skills = ' '.join(resume_skills + recommended_skills)
    vectorizer = CountVectorizer().fit_transform([all_skills, ' '.join(recommended_skills)])
    similarity_matrix = cosine_similarity(vectorizer)
    similarity_score = similarity_matrix[0, 1]
    return similarity_score


def calculate_completeness(resume_sections):
    required_sections = ['education', 'work_experience', 'skills', 'projects']
    missing_sections = [section for section in required_sections if section not in resume_sections]
    completeness_score = 1.0 - len(missing_sections) / len(required_sections)
    return max(completeness_score, 0.0)


def calculate_formatting(resume_path):
    try:
        with pdfplumber.open(resume_path) as pdf:
            num_pages = len(pdf.pages)
            # You can add more criteria based on the PDF content or layout
    except Exception as e:
        # Handle exceptions (e.g., file not found, not a PDF, etc.)
        print(f"Error reading PDF: {e}")
        num_pages = 0

    # Assuming you want to give a higher score for shorter resumes (less than 2 pages)
    return max(2.0 - num_pages, 0.0)


def calculate_keywords(resume_text, job_keywords):
    # Check if keywords from job description are present in the resume
    resume_keywords = set(resume_text.lower().split())
    matching_keywords = set(job_keywords.lower().split()) & resume_keywords
    keyword_score = len(matching_keywords) / len(job_keywords)
    return keyword_score


def calculate_experience_achievements(experience_years, achievements):
    # Add your own criteria for evaluating experience and achievements
    # This is a placeholder, you may need to define what constitutes good experience and achievements
    # Here, I'm assuming a higher score for more experience (up to 10 years) and more achievements
    experience_score = min(experience_years / 10, 1.0)
    achievements_score = min(len(achievements) / 5, 1.0)
    return (experience_score + achievements_score) / 2


def calculate_education(education_degree):
    # Add your own criteria for evaluating education
    # This is a placeholder, you may need to define what constitutes good education
    # Here, I'm assuming a higher score for a higher level of education
    education_score = 0.2 if 'bachelor' in education_degree.lower() else 0.4
    return education_score


def calculate_resume_score(resume_data, job_category, recommended_skills):
    # Extract relevant information from the resume data
    resume_skills = resume_data.get('skills', [])
    resume_sections = resume_data.get('sections', [])
    resume_text = resume_data.get('text', '')
    experience_years = resume_data.get('experience_years', 0)
    achievements = resume_data.get('achievements', [])
    education_degree = resume_data.get('education_degree', '')

    # Calculate individual scores
    similarity_score = calculate_similarity(resume_data['skills'], recommended_skills)
    completeness_score = calculate_completeness(resume_sections)
    formatting_score = calculate_formatting(resume_text)
    keywords_score = calculate_keywords(resume_text, job_category)
    experience_achievements_score = calculate_experience_achievements(experience_years, achievements)
    education_score = calculate_education(education_degree)

    # Define weights for each criterion
    weights = {
        'similarity': 0.3,
        'completeness': 0.2,
        'formatting': 0.1,
        'keywords': 0.1,
        'experience_achievements': 0.1,
        'education': 0.1,
        'language_grammar': 0.1,
    }

    # Calculate the overall score
    overall_score = (
            similarity_score * weights['similarity'] +
            completeness_score * weights['completeness'] +
            formatting_score * weights['formatting'] +
            keywords_score * weights['keywords'] +
            experience_achievements_score * weights['experience_achievements'] +
            education_score * weights['education']

    )

    return overall_score
