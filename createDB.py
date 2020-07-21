import os
import psycopg2
import sqlite3

connsqlite = sqlite3.connect("users_settings.sqlite")
guilds = connsqlite.execute("SELECT * FROM guilds").fetchall()
users = connsqlite.execute("SELECT * FROM users").fetchall()
connsqlite.close()

print(guilds, users)

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cur = conn.cursor()

cur.execute("""CREATE TABLE guilds (
    id BIGINT PRIMARY KEY,
    command_prefix VARCHAR(255),
    reactions BOOL DEFAULT FALSE,
    rektDab BOOL DEFAULT FALSE,
    welcomeBye BOOL DEFAULT FALSE,
    rolesToGive TEXT []
)""")
cur.execute("""CREATE TABLE users(
    id BIGINT PRIMARY KEY,
    numberOfEmbedRequests INT DEFAULT 0,
    mofupoints INT DEFAULT 0,
    easterEggClaimed BOOL DEFAULT FALSE
)""")


for guild in guilds:
    print(guild)
    cur.execute(
        "INSERT INTO guilds (id, command_prefix) VALUES (%s, %s)", guild[0:2])

for user in users:
    print(user)
    cur.execute("INSERT INTO users (id, numberOfEmbedRequests, mofupoints, easterEggClaimed) VALUES (%s, %s, %s, %s)",
                (*user[0:3], "TRUE" if user[3] else "FALSE"))


conn.commit()
cur.close()
conn.close()
