import discord
from discord.ext import commands

from .utils.dbms import db


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(aliases=["settings"])
    # async def config(self, ctx: commands.Context):
    #     """Regroup all the settings in one command"""
    #     pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: commands.Context, newPrefix=None):
        """change the command prefix for this server"""
        if newPrefix == "xd":
            newPrefix = None

        if not ctx.guild:
            await ctx.send("Failed to retrieve the guild id, please try again")
            return

        db.set_data(
            """INSERT INTO guilds (id, command_prefix)
                VALUES(%s, %s)
                ON CONFLICT(id)
                DO UPDATE SET command_prefix = %s""",
            (ctx.guild.id, newPrefix, newPrefix),
        )

        if not newPrefix:
            await ctx.send("The command prefix has been reset to xd!")
            return

        await ctx.send(f'The new command prefix for this server is "{newPrefix}"')

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["welcome", "welcomechannel"])
    async def welcomeChannel(
        self, ctx, channel_converter: commands.TextChannelConverter = None
    ):
        """View the current welcoming channel and change it to your preference"""
        if not channel_converter:
            result = db.get_data(
                "SELECT welcomebye FROM guilds WHERE id=%s", (ctx.guild.id,)
            )

            text = ""
            if len(result[0]) < 1:
                text += "No welcome channel is set on this server\n"
            else:
                ch = result[0][0]
                mention = self.bot.get_channel(ch).mention
                text += f"Welcome messages are sent in {mention} (id: {ch})\n"

            text += (
                'to change the channel, type "xd welcome #welcome"'
                "and put the actual channel name"
            )
            await ctx.send(text)
            return

        channel: discord.TextChannel = channel_converter

        if channel.guild.id != ctx.guild.id:
            await ctx.send(
                "You can't use the channel of another server to welcome people!"
            )
            return

        try:
            await channel.send(
                "Welcoming will now be sent in this channel!\n"
                "This message will be deleted automatically in 30 seconds",
                delete_after=30.0,
            )
        except discord.errors.Forbidden:
            await ctx.send("I don't have Permissions to write in that channel!")
            return

        await ctx.send(f"A test have been sent into the {channel.mention} channel!")

        db.set_data(
            """INSERT INTO guilds (id, welcomebye)
                VALUES(%s, %s)
                ON CONFLICT(id)
                DO UPDATE SET welcomebye = %s""",
            (ctx.guild.id, channel.id, channel.id),
        )

        await ctx.send("Setting saved!")


def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))
