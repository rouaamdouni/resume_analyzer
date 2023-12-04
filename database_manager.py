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
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)


def insert_data(cursor, name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills,
                recommended_skills, courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (
        name, email, str(res_score), timestamp, str(
            no_of_pages), reco_field, cand_level, skills, recommended_skills,
        courses)
    cursor.execute(insert_sql, rec_values)

# Add other functions if needed
