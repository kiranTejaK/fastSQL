# app/database/db_config.py
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# def get_local_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="password123",
#             database="dev-heitage-api"
#         )
#         connection.autocommit = True
#         return connection
#     except Error as e:
#         print("Error while connecting to MySQL", e)
#         raise

# # 0004cd6e7815454bf411bde3b25109d4f6d6a639e22de1ad754e410e65343eb0bd0b3b2470a72fe6a7da96e352c1d65808cb1242e462bbecff110c106492f266

# def get_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host="mysql-illusiontech.alwaysdata.net",
#             user="392240_admin",
#             password="angelnumbers138",
#             database="illusiontech_fastsql"
#         )
#         connection.autocommit = True
#         return connection
#     except Error as e:
#         print("Error while connecting to MySQL", e)
#         raise
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASS"),
            database = os.getenv("DB_DATABASE"),
        )
        connection.autocommit = True
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        raise

# import mysql.connector
# from mysql.connector import errorcode

# try:
#     connection = mysql.connector.connect(
#         host="illusiontech.alwaysdata.net",
#         user="392240_admin",
#         password="angelnumbers138",
#         database="illusiontech_fastsql"
#     )
#     print("Connection successful!")
# except mysql.connector.Error as err:
#     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#         print("Invalid credentials")
#     elif err.errno == errorcode.ER_BAD_DB_ERROR:
#         print("Database does not exist")
#     else:
#         print(f"Error: {err}")
