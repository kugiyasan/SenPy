import os
import psycopg2

# TODO auto reconnect function
# https://stackoverflow.com/questions/42385391/auto-reconnect-postgresq-database

try:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
except:
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL)

cursor = conn.cursor()