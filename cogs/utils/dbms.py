import discord
from discord.ext import commands
import sqlite3


# class Database(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.conn = sqlite3.connect("users_settings.sqlite")
#         self.c = self.conn.cursor()

#     # def __del__(self):
#     #     self.conn.close()

#     def cog_unload(self):
#         self.conn.close()

#     async def delete_user(self, userid: int):
#         with self.conn:
#             self.c.execute("DELETE from users WHERE id = ?", (userid,))

# async def updateValue(self, table, value):
#     pass
#     # c.execute("INSERT INTO Users VALUES (434437407023169547, 0, 0, 0)")

# async def getValue(self, table, objectID, column, default=None):
#     with self.conn:
#         if table == "users":
#             self.c.execute("SELECT DISTINCT * FROM users WHERE id=?", (objectID,))

#             headers = {
#                 "id": 0,
#                 "numberOfEmbedRequests": 1,
#                 "mofupoints": 2,
#                 "easterEggClaimed": 3
#             }

#         elif table == "guilds":
#             self.c.execute("SELECT DISTINCT * FROM guilds WHERE id=?", (objectID,))

#             headers = {
#                 "id": 0,
#                 "command_prefix": 1,
#                 "welcomeBye": 2,
#                 "rektDab": 3,
#                 "reactions": 4
#             }

#         else:
#             raise UnknownTableName(f"{table} isn't a table name!")
        
#         output = self.c.fetchone()
        
#         if not output:
#             return default
#         else:
#             output = output[headers[column]]

#         return output

# class UnknownTableName(Exception):
#     pass

# def setup(bot):
#     bot.add_cog(Database(bot))

conn = sqlite3.connect("users_settings.sqlite")