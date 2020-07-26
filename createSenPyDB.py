import os
import psycopg2

try:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
except:
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL)

cur = conn.cursor()

# cur.execute("""CREATE TABLE guilds (
#     id BIGINT PRIMARY KEY,
#     command_prefix VARCHAR(255),
#     welcomeBye BIGINT,
#     rolesToGive BIGINT []
# )""")
# cur.execute("""CREATE TABLE users(
#     id BIGINT PRIMARY KEY,
#     numberOfEmbedRequests INT DEFAULT 0,
#     mofupoints INT DEFAULT 0,
#     easterEggClaimed BOOL DEFAULT FALSE
# )""")

cur.execute("SELECT * FROM guilds")
print(cur.fetchall())

# conn.commit()
cur.close()
conn.close()
