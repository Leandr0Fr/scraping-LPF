from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

except psycopg2.OperationalError as e:
    print(f"Error en la conexión: {e}")
