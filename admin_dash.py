import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from database_manager import create_database, get_all_data_sorted, get_latest_data,connect_to_database
import base64
def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href
                


def admin_login():
    admin_emails = ['rouaamdouni0@gmail.com', 'alimekni5@gmail.com']
    ad_password = 'rouaroua'
    ad_user = st.text_input("Username")
    ad_password = st.text_input("Password", type='password')

    if st.button('Login'):
        connection, cursor = connect_to_database()
        create_database(connection, cursor)
        if ad_user in admin_emails and ad_password == ad_password:
            if ad_user == 'rouaamdouni0@gmail.com':
                st.success("Welcome Roua")
            else:
                st.success("Welcome Ali")
            # st.success("Welcome {}".format(ad_user))
            
            # Display All Data
            all_data = get_all_data_sorted(cursor)
            columns = ['ID', 'Name', 'Email_ID', 'Resume score', 'Timestamp', 'Predicted Field', 'Actual Skills', 'Recommended Skills']
            df_all = pd.DataFrame(all_data, columns=columns)
            df_all['Resume score'] = df_all['Resume score'].astype(float)  # Convert 'resume_score' to float for sorting

            # Sort the DataFrame by 'resume_score' in descending order
            df_all = df_all.sort_values(by='Resume score', ascending=False)
            st.dataframe(df_all)
            st.markdown(get_table_download_link(df_all, 'All_User_Data.csv', 'Download All Data Report'), unsafe_allow_html=True)

            # Admin Side Data
            query = 'SELECT * FROM user_data;'
            plot_data = pd.read_sql(query, connection)
        
            #     # Plot the count of users for each job category
            fig = px.bar(df_all, x='Predicted Field', title='Count of Users for Each Job Category')
            fig.update_layout(xaxis_title='Job Category', yaxis_title='Number of Users')
            st.plotly_chart(fig)


            #Histogram or box plot showing the distribution of resume scores.
            fig = px.histogram(df_all, x='Resume score', title='Distribution of Resume Scores')
            fig.update_layout(xaxis_title='Resume Score', yaxis_title='Count')
            st.plotly_chart(fig)

            ## ...

            #Line chart showing the number of user registrations over time.
            df_all['Timestamp'] = pd.to_datetime(df_all['Timestamp'], format="%Y-%m-%d_%H:%M:%S")
            df_all = df_all.sort_values(by='Timestamp')  # Sort by Timestamp in ascending order
            fig_user_activity = px.line(df_all, x='Timestamp', title='User Activity Over Time')
            fig_user_activity.update_layout(xaxis_title='Timestamp', yaxis_title='Number of Users')
            st.plotly_chart(fig_user_activity)

            # ...


            #Pie chart or bar chart showing the distribution of predicted fields for all users.
            fig_predicted_field = px.pie(df_all, names='Predicted Field', title='Distribution of Predicted Fields')
            st.plotly_chart(fig_predicted_field)
            
            #Word cloud or bar chart showing the most frequently mentioned skills in the "Actual Skills" and "Recommended Skills" columns.

            # Generate word cloud for Actual Skills
            wordcloud_actual = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df_all['Actual Skills']))
            st.image(wordcloud_actual.to_image(), caption='Word Cloud for Actual Skills')

            # Generate word cloud for Recommended Skills
            wordcloud_recommended = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df_all['Recommended Skills']))
            st.image(wordcloud_recommended.to_image(), caption='Word Cloud for Recommended Skills')

                       # Close the connection
            connection.close()
        else:
            st.error("Invalid username or password. Please try again.")
