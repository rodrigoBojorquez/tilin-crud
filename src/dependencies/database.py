import os
import mysql.connector
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

async def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    
    cursor = connection.cursor(dictionary=True, buffered=True)
    
    try:
        yield connection, cursor
    finally:
        cursor.close()
        connection.close()