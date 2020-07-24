# import sqlite3

# connsqlite = sqlite3.connect("users_settings.sqlite")
# guilds = connsqlite.execute("SELECT * FROM guilds").fetchall()
# users = connsqlite.execute("SELECT * FROM users").fetchall()
# connsqlite.close()

# print(guilds, users)

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
#     reactions BOOL DEFAULT FALSE,
#     rektDab BOOL DEFAULT FALSE,
#     welcomeBye BOOL DEFAULT FALSE,
#     rolesToGive TEXT []
# )""")
cur.execute("""CREATE TABLE guilds (
    id BIGINT PRIMARY KEY,
    command_prefix VARCHAR(255),
    welcomeBye BIGINT,
    rolesToGive BIGINT []
)""")
# cur.execute("""CREATE TABLE users(
#     id BIGINT PRIMARY KEY,
#     numberOfEmbedRequests INT DEFAULT 0,
#     mofupoints INT DEFAULT 0,
#     easterEggClaimed BOOL DEFAULT FALSE
# )""")

cur.execute("INSERT INTO guilds (id, rolesToGive) VALUES (382248089450446848, Array [401135422211620865,391604044692455426,389050297168691220,555100574123687999,555100538589544449,555100546437087253,555093542796656643,555100538241417278,555100497137106974,391597731082141697,389060054927671299,391601620992917524,391601123842064404,391601091181281289,391601035673600012,391601547089281024,391601449945268225,391601519897870337,391601229060374529,391601175255842837,391601405275930624,391600996121313280,391600441034801152,391600624715694093,391600563571261441,391600943445311498,391600772846190594,391600877707722752,452580046142570497,391601266297405441,391601339400192011])")

# for guild in guilds:
#     print(guild)
#     cur.execute(
#         "INSERT INTO guilds (id, command_prefix) VALUES (%s, %s)", guild[0:2])

# for user in users:
#     print(user)
#     cur.execute("INSERT INTO users (id, numberOfEmbedRequests, mofupoints, easterEggClaimed) VALUES (%s, %s, %s, %s)",
#                 (*user[0:3], "TRUE" if user[3] else "FALSE"))


conn.commit()
cur.close()
conn.close()
