import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()

def create_database_if_not_exists(cursor, db_name: str):
    cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
    result = cursor.fetchone()
    
    if not result:
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Base de datos {db_name} creada satisfactoriamente.")
    else:
        print(f"Base de datos {db_name} ya existe.")
        
def execute_sql_script(cursor, script_path: str):
    try:
        with open(script_path, 'r') as file:
            
            sql_script_content = file.read()
            for statement in sql_script_content.split(";"):
                if statement.strip():
                    cursor.execute(statement)
            print(f"Script SQL {script_path} ejecutado satisfactoriamente.")
            
    except Error as err:
        print(f"Error al intentar ejecutar el script SQL: {err}")

def initialize_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        
        if connection.is_connected():  
            
            cursor = connection.cursor()
            
            create_database_if_not_exists(cursor, os.getenv("DB_NAME"))
            cursor.execute(f"USE {os.getenv('DB_NAME')}")
            execute_sql_script(cursor, "src/data/schema.sql")
            
            connection.commit()
            print("Base de datos configurada correctamente.")
           
        else:
            print("Error al intentar conectar a la base de datos.")
    

    except Error as e:
        print(f"Error al intentar crear la base de datos y ejecutar el script SQL: {e}")
    
    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()

initialize_database()
