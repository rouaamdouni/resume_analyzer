#  else:
#         ## Admin Side
#         st.success('Welcome to Admin Side')
#         # st.sidebar.subheader('**ID / Password Required!**')

#         ad_user = st.text_input("Username")
#         ad_password = st.text_input("Password", type='password')
#         if st.button('Login'):
#             if ad_user == 'machine_learning_hub' and ad_password == 'mlhub123':
#                 st.success("Welcome Kushal")
#                 # Display Data
#                 cursor.execute('''SELECT*FROM user_data''')
#                 data = cursor.fetchall()
#                 st.header("**User's👨‍💻 Data**")
#                 df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
#                                                  'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
#                                                  'Recommended Course'])
#                 st.dataframe(df)
#                 st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
#                 ## Admin Side Data
#                 query = 'select * from user_data;'
#                 plot_data = pd.read_sql(query, connection)

#                 ## Pie chart for predicted field recommendations
#                 labels = plot_data.Predicted_Field.unique()
#                 print(labels)
#                 values = plot_data.Predicted_Field.value_counts()
#                 print(values)
#                 st.subheader("📈 **Pie-Chart for Predicted Field Recommendations**")
#                 fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
#                 st.plotly_chart(fig)

#                 ### Pie chart for User's👨‍💻 Experienced Level
#                 labels = plot_data.User_level.unique()
#                 values = plot_data.User_level.value_counts()
#                 st.subheader("📈 ** Pie-Chart for User's👨‍💻 Experienced Level**")
#                 fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
#                 st.plotly_chart(fig)


#             else:
#                 st.error("Wrong ID & Password Provided")