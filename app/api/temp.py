import os

import mysql.connector
from dotenv import load_dotenv

# loading variables from .env file
load_dotenv()

# Establish database connection
def connect_to_database():
    return mysql.connector.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"),
                              host='127.0.0.1',
                              database='muji')

if __name__ == "__main__":
    conn = connect_to_database()
    print(conn)