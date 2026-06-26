# app/database/db_config.py
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
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
