import discord
from discord.ext import commands

import itertools
from typing import Tuple


class MyHelpCommand(commands.HelpCommand):
    def divideInTwoColumns(self, text: str) -> Tuple[str, str]:
        half = text.index("\n\n", len(text) // 2)
        return text[:half], text[half:]

    # This function triggers when somone type `<prefix>help`
    async def send_bot_help(self, mapping) -> None:
        ctx = self.context
        text = ""

        def get_category(command):
            cog = command.cog
            return cog.qualified_name if cog is not None else "No Category"

        filtered = await self.filter_commands(
            ctx.bot.commands, sort=True, key=get_category
        )
        to_iterate = itertools.groupby(filtered, key=get_category)

        for category, commands_obj in to_iterate:
            if category == "Help":
                continue

            commands_obj = sorted(commands_obj, key=lambda c: c.name)
            commands_name = "\n".join(str(command) for command in commands_obj)
            text += f"\n\n**{category}:**\n" + commands_name

        column1, column2 = self.divideInTwoColumns(text)

        embed = discord.Embed(
            title=f"Here are all the available command for {ctx.bot.user.name}!",
            color=discord.Color(0xFF5BAE),
        )
        embed.set_thumbnail(url=ctx.me.avatar.url)

        embed.add_field(name="_ _", value=column1)
        embed.add_field(name="_ _", value=column2)

        await ctx.send(embed=embed)

    # This function triggers when someone type `<prefix>help <cog>`
    async def send_cog_help(self, cog: commands.Cog):
        ctx = self.context
        print(cog.qualified_name)

        def get_category(command):
            cmdCog = command.cog
            return cmdCog.qualified_name if cmdCog is not None else "No Category"

        filtered = await self.filter_commands(
            ctx.bot.commands, sort=True, key=get_category
        )
        to_iterate = itertools.groupby(filtered, key=get_category)

        commands_obj = None
        for category, commands_obj in to_iterate:
            print(category, cog)
            if category != cog:
                continue

            commands_obj = sorted(commands_obj, key=lambda c: c.name)

        embed = discord.Embed(title="Commands:", color=discord.Color(0xFF5BAE))
        embed.set_thumbnail(url=ctx.me.avatar_url)

        for command in commands_obj:
            embed.add_field(
                name=" / ".join((command.name, *command.aliases)),
                value=command.short_doc or "No description",
                inline=False,
            )

        await ctx.send(embed=embed)

    # TODO make this an nice looking embed
    # This function triggers when someone type `<prefix>help <command>`
    async def send_command_help(self, command):
        ctx = self.context
        text = self.get_command_signature(command) + "\n\n"

        if command.help:
            text += command.help + "\n\n"

        await ctx.send(f"```{text}```")

    # TODO create a group command and complete this coroutine
    # This function triggers when someone type `<prefix>help <group>`
    async def send_group_help(self, group):
        # ctx = self.context
        raise NotImplementedError


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Storing main help command in a variable
        self.bot._original_help_command = bot.help_command

        # Assiginig new help command to bot help command
        bot.help_command = MyHelpCommand()

        # Setting this cog as help command cog
        bot.help_command.cog = self

    def cog_unload(self):
        # Setting help command to the previous help command
        # so if this cog unloads the help command restores to previous
        self.bot.help_command = self.bot._original_help_command


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))


# Useful variables for help command
# =============================

# self.clean_prefix  # Current prefix
# ctx.bot  # The bot
# ctx.bot.cogs  # Returns a dict of loaded cogs
# # Returns a list of commands a cog have. Including both hidden and disabled
# cog.get_commands()
# cog.description  # Cogs description. Returns a empty string if there is nothing
# command.qualified_name
# # A commands qualified name.
# # Returns function name if the name kwarg is not passed while creating the command.
# # It works for Cog and group too
# # A commands help. Returns an empty string if there is nothing. Works for group too.
# command.help
# # Command signature. Return an empty string if there is nothing. Works for group too
# command.signature
