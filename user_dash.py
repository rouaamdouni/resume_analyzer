import io
import datetime
import time
from course_recommendation import recommendCourse
from database_manager import connect_to_database, create_database, create_user_data_table, insert_data
from job_recommender import recommendJob
from score_calculating import calculate_resume_score
from skills_recommender import recommend_skills
import plotly.express as px
from PIL import Image
from streamlit_tags import st_tags
from pdfminer3.converter import TextConverter
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfpage import PDFPage

from pdfminer3.layout import LAParams
from pyresparser import ResumeParser
import pandas as pd
import nltk
import spacy
import streamlit as st
import base64


nltk.download('stopwords')
spacy.load('en_core_web_sm')

##reading and parsing the pdf file
def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(
        resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

##displaying the pdf
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


##setting the page config title and icon
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon='./Logo/SRA_Logo.ico',
)

def user_login():
    csv_file_path = './datasets/job_skills_extended.csv'
    connection, cursor = connect_to_database()

    create_database(connection, cursor)
    st.markdown(
                '''<h4 style='text-align: left; color: #d73b5c;'> Upload your resume, and get smart recommendation based on it </h4>''',
                unsafe_allow_html=True)
    pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
    if pdf_file is not None:
                save_image_path = './Uploaded_Resumes/' + pdf_file.name

                with open(save_image_path, "wb") as f:
                    f.write(pdf_file.getbuffer())

                show_pdf(save_image_path)

                resume_data = ResumeParser(save_image_path).get_extracted_data()

                if resume_data:
                    # Get the whole resume data
                    resume_text = pdf_reader(save_image_path)

                    st.header("**Resume Analysis**")
                    st.success("Hello " + resume_data['name'])
                    st.subheader("**Your Basic info**")
                    try:
                        st.text('Name: ' + resume_data['name'])
                        st.text('Email: ' + resume_data['email'])
                        st.text('Contact: ' + resume_data['mobile_number'])
                        st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                    except:
                        pass

                    st.subheader("**Skills Recommendation💡**")
                    # Skill shows
                    keywords = st_tags(label='### Skills that you have',
                                    text='See our skills recommendation',
                                    value=resume_data['skills'], key='1')

                    resume_skills = resume_data['skills']

                    # Specify the path to your CSV file
                    

                    # Use the recommend_job_category function
                    recommended_category, recommended_skills = recommend_skills(
                        resume_skills, csv_file_path)

                    # Print or use the recommended job category and skills as needed
                    print("Recommended Job Category:", recommended_category)
                    print("Recommended Skills:", recommended_skills)
                    st.success("** Our analysis says you are looking  " +
                            recommended_category + "  Jobs.**")

                    recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                text='Recommended skills generated from System',
                                                value=recommended_skills, key='2')
                    st.markdown(
                        '''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',
                        unsafe_allow_html=True)

                    # Insert into table
                    ts = time.time()
                    cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    timestamp = str(cur_date + '_' + cur_time)

                    # Resume writing recommendation
                    st.subheader("**Resume Tips & Ideas💡**")
                    st.subheader("**Resume Score📝**")
                    st.markdown(
                        """
                        <style>
                            .stProgress > div > div > div > div {
                                background-color: #d73b5c;
                            }
                        </style>""",
                        unsafe_allow_html=True,
                    )
                    # Calculate the resume score
                    resume_score = calculate_resume_score(resume_data, recommended_category, recommended_skills)

                    # Display a progress bar
                    my_bar = st.progress(0)
                    score = 0

                    # Simulate the progress and update the progress bar
                    for percent_complete in range(int(resume_score * 100)):
                        score += 1
                        time.sleep(0.1)
                        my_bar.progress(percent_complete + 1)

                    st.success('** Your Resume Writing Score: ' + str(score) + '**')
                    st.warning(
                        "** Note: This score is calculated based on the content that you have added in your Resume. **")

                    # Display the final score
                    st.success('** Your Resume Writing Score: ' + str(score) + '**')
                    st.warning(
                        "** Note: This score is calculated based on the content that you have added in your Resume. **")

                    recommendCourse(recommended_skills, recommended_category)
                    create_user_data_table(cursor)
                    print(resume_data['name'], resume_data['email'], resume_score, timestamp, recommended_category, resume_data['skills'], recommended_skills)
                    insert_data(cursor, resume_data['name'], resume_data['email'], str(resume_score), timestamp,
                    recommended_category, str(resume_data['skills']) ,str(recommended_skills))

                    
                    recommendJob(resume_skills, recommended_category)

                    connection.commit()
                    st.error('Something went wrong..')        
            
            