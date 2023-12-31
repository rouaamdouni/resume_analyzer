import pymysql

def connect_to_database():
    connection = pymysql.connect(host='localhost', user='root', password='')
    cursor = connection.cursor()
    return connection, cursor

def create_database(connection, cursor):
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)
    connection.select_db("sra")

def create_user_data_table(cursor):
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,  -- Added comma here
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)

def insert_data(cursor, name, email, res_score, timestamp, reco_field, skills, recommended_skills):
    DB_table_name = 'user_data'
    insert_sql = f"INSERT INTO {DB_table_name} (Name, Email_ID, resume_score, Timestamp, Predicted_Field, Actual_skills, Recommended_skills) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    rec_values = (
        name, email, str(res_score), timestamp, reco_field, skills, recommended_skills
    )
    cursor.execute(insert_sql, rec_values)



def get_latest_data(cursor):
    DB_table_name = 'user_data'
    query = f"SELECT * FROM {DB_table_name} ORDER BY Timestamp DESC LIMIT 1"
    cursor.execute(query)
    latest_data = cursor.fetchone()
    return latest_data

def get_all_data_sorted(cursor):
    DB_table_name = 'user_data'
    query = f"SELECT * FROM {DB_table_name} ORDER BY CAST(resume_score AS SIGNED) DESC" 
    cursor.execute(query)
    all_data = cursor.fetchall()
    return all_data