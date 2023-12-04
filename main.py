import random
import io
import datetime
import time
from course_recommendation import recommend
from database_manager import connect_to_database, create_database, create_user_data_table
from score_calculating import calculate_resume_score
from skills_recommender import recommend_skills
import plotly.express as px
import pafy
import pymysql
from PIL import Image
from streamlit_tags import st_tags
from pdfminer3.converter import TextConverter
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfpage import PDFPage

from pdfminer3.layout import LAParams
from pyresparser import ResumeParser
import base64
import pandas as pd
import nltk
import spacy
import streamlit as st

nltk.download('stopwords')
spacy.load('en_core_web_sm')


def get_table_download_link(df, filename, text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


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


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000"
    # type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

connection, cursor = connect_to_database()
create_database(connection, cursor)
create_user_data_table(cursor)

# connection to database
#connection = pymysql.connect(host='localhost', user='root', password='')
#cursor = connection.cursor()


def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills,
                courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (
        name, email, str(res_score), timestamp, str(
            no_of_pages), reco_field, cand_level, skills, recommended_skills,
        courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()


st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon='./Logo/SRA_Logo.ico',
)


def run():
    st.title("Start analysing your resume")
    st.sidebar.markdown("# connect as")
    activities = ["Normal User", "Admin"]
    choice = st.sidebar.selectbox(
        "Choose among the given options:", activities)
    # link = '[©Developed by Spidy20](http://github.com/spidy20)'
    # st.sidebar.markdown(link, unsafe_allow_html=True)
    img = Image.open('./Logo/logo.jpeg')
    img = img.resize((550, 250))
    st.image(img)

    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)
    connection.select_db("sra")

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    if choice == 'Normal User':
        st.markdown(
            '''<h4 style='text-align: left; color: #d73b5c;'> Upload your resume, and get smart recommendation based on it </h4>''',
            unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            # with st.spinner('Uploading your Resume....'):
            #     time.sleep(4)
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
                csv_file_path = 'job_skills_extended.csv'

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

                recommend(recommended_skills, recommended_category)
                connection.commit()
                st.error('Something went wrong..')
    else:
        ## Admin Side
        st.success('Welcome to Admin Side')
        # st.sidebar.subheader('**ID / Password Required!**')

        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'machine_learning_hub' and ad_password == 'mlhub123':
                st.success("Welcome Kushal")
                # Display Data
                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's👨‍💻 Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                 'Recommended Course'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
                ## Admin Side Data
                query = 'select * from user_data;'
                plot_data = pd.read_sql(query, connection)

                ## Pie chart for predicted field recommendations
                labels = plot_data.Predicted_Field.unique()
                print(labels)
                values = plot_data.Predicted_Field.value_counts()
                print(values)
                st.subheader("📈 **Pie-Chart for Predicted Field Recommendations**")
                fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)

                ### Pie chart for User's👨‍💻 Experienced Level
                labels = plot_data.User_level.unique()
                values = plot_data.User_level.value_counts()
                st.subheader("📈 ** Pie-Chart for User's👨‍💻 Experienced Level**")
                fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
                st.plotly_chart(fig)


            else:
                st.error("Wrong ID & Password Provided")
run()