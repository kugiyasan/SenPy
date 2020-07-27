import discord
from discord.ext import commands

from cogs.utils.dbms import conn, cursor


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(aliases=["settings"])
    # async def config(self, ctx: commands.Context):
    #     """Regroup all the settings in one command"""
    #     pass

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["welcome", "welcomechannel"])
    async def welcomeChannel(self, ctx, channelID: int = 0):
        """View the current welcoming channel and change it to your preference"""
        if channelID == 0:
            with conn:
                cursor.execute(
                    "SELECT welcomebye FROM guilds WHERE id=%s", (ctx.guild.id,))
                channel = cursor.fetchone()[0]

                await ctx.send(f"Welcome messages are sent in the {self.bot.get_channel(channel)} channel (id: {channel})\n"
                               + "to change the channel, type 'xd welcome 1234567890' and replace the number with the channel id")

                return

        channel = self.bot.get_channel(channelID)
        if channel == None:
            await ctx.send("Unknown channel, be sure to give me the right channel id!")
            return
        if channel.guild.id != ctx.guild.id:
            await ctx.send("You can't use the channel of another server to welcome people!")
            return

        await channel.send("Welcoming will now be sent in this channel!\nThis message will deleted automatically in 30 seconds", delete_after=30.0)

        with conn:
            cursor.execute("""INSERT INTO guilds (id, welcomebye)
                            VALUES(%s, %s) 
                            ON CONFLICT(id) 
                            DO UPDATE SET welcomebye = %s""", (ctx.guild.id, channelID, channelID))
        
        await ctx.send("Setting saved!")


def setup(bot):
    bot.add_cog(Settings(bot))
