import streamlit as st
import pandas as pd
import plotly.express as px
from database_manager import create_database, get_latest_data,connect_to_database
import base64
def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href
                
def admin_login():
    ad_user = st.text_input("Username")
    ad_password = st.text_input("Password", type='password')

    if st.button('Login'):
        connection, cursor = connect_to_database()
        create_database(connection, cursor)
        if ad_user == 'roua' and ad_password == 'roua':
            st.success("Welcome {}".format(ad_user))
            
            # Display All Data
            cursor.execute('''SELECT * FROM user_data''')
            data_all = cursor.fetchall()
            st.header("**All User Data**")
            df_all = pd.DataFrame(data_all, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp',
                                                     'Predicted Field', 'Actual Skills', 'Recommended Skills'])
            st.dataframe(df_all)
            st.markdown(get_table_download_link(df_all, 'All_User_Data.csv', 'Download All Data Report'), unsafe_allow_html=True)

            # Admin Side Data
            query = 'SELECT * FROM user_data;'
            plot_data = pd.read_sql(query, connection)
        
            #     # Plot the count of users for each job category
            fig = px.bar(df_all, x='Predicted Field', title='Count of Users for Each Job Category')
            fig.update_layout(xaxis_title='Job Category', yaxis_title='Number of Users')
            st.plotly_chart(fig)
            # else:
            #     st.warning("No data available.")
            # Pie Chart for Resume Scores
            # st.subheader("Pie Chart for Resume Scores")
            # resume_score_chart = px.pie(plot_data, names='Resume Score', title='Resume Scores Distribution')
            # st.plotly_chart(resume_score_chart)

            # Line Chart for Resume Scores Over Time
            # st.subheader("Line Chart for Resume Scores Over Time")
            # resume_scores_over_time_chart = px.line(plot_data, x='Timestamp', y='Resume Score', labels={'Resume Score': 'Average Resume Score'},
            #                                         title='Average Resume Score Over Time')
            # st.plotly_chart(resume_scores_over_time_chart)

            # Bar Chart for Recommended Skills
            st.subheader("Bar Chart for Recommended Skills")
            skills = [skill for skills_list in plot_data['Recommended Skills'] for skill in skills_list]
            recommended_skills_chart = px.bar(pd.Series(skills).value_counts(), x=pd.Series(skills).unique(),
                                            y=pd.Series(skills).value_counts(), labels={'y': 'Frequency'},
                                            title='Recommended Skills Frequency')
            st.plotly_chart(recommended_skills_chart)

            # Bar Chart for Recommended Courses
            st.subheader("Bar Chart for Recommended Courses")
            recommended_courses_chart = px.bar(plot_data['Recommended Courses'].value_counts(),
                                                x=plot_data['Recommended Courses'].unique(),
                                                y=plot_data['Recommended Courses'].value_counts(),
                                                labels={'y': 'Popularity'}, title='Recommended Courses Popularity')
            st.plotly_chart(recommended_courses_chart)

            # Bar Chart for User Levels
            st.subheader("Bar Chart for User Levels")
            user_levels_chart = px.bar(plot_data['User Level'].value_counts(), x=plot_data['User Level'].unique(),
                                        y=plot_data['User Level'].value_counts(), labels={'y': 'Number of Users'},
                                        title='User Levels Distribution')
            st.plotly_chart(user_levels_chart)

            # Bar Chart for Predicted Fields
            st.subheader("Bar Chart for Predicted Fields")
            predicted_fields_chart = px.bar(plot_data['Predicted Field'].value_counts(), x=plot_data['Predicted Field'].unique(),
                                            y=plot_data['Predicted Field'].value_counts(),
                                            labels={'y': 'Number of Users'}, title='Predicted Fields Distribution')
            st.plotly_chart(predicted_fields_chart)

            # Scatter Plot for Resume Scores vs. Number of Pages
            st.subheader("Scatter Plot for Resume Scores vs. Number of Pages")
            scatter_chart = px.scatter(plot_data, x='Number of Pages', y='Resume Score', title='Resume Scores vs. Number of Pages')
            st.plotly_chart(scatter_chart)

            # Bar Chart for Total Pages in Resumes
            st.subheader("Bar Chart for Total Pages in Resumes")
            total_pages_chart = px.bar(plot_data['Number of Pages'].value_counts(), x=plot_data['Number of Pages'].unique(),
                                    y=plot_data['Number of Pages'].value_counts(), labels={'y': 'Number of Users'},
                                    title='Total Pages in Resumes Distribution')
            st.plotly_chart(total_pages_chart)

            # Bar Chart for User Engagement Over Time
            st.subheader("Bar Chart for User Engagement Over Time")
            user_engagement_chart = px.bar(plot_data.resample('D', on='Timestamp').size(),
                                            x=plot_data.resample('D', on='Timestamp').size().index,
                                            y=plot_data.resample('D', on='Timestamp').size(),
                                            labels={'y': 'Number of Users'}, title='User Engagement Over Time')
            st.plotly_chart(user_engagement_chart)

            # ... (Continue with other charts if needed)

            # Close the connection
            connection.close()
        else:
            st.error("Invalid username or password. Please try again.")
