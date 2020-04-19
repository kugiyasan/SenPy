import discord
from discord.ext import commands

@bot.command()
async def insult(ctx):
    """random compliment directly from the web"""
    webpage = requests.get(
        'http://www.robietherobot.com/insult-generator.htm')  # .readlines()[115].decode('utf-8')
    if(webpage.status_code == 200):
        print(webpage.text)
        await ctx.send("You're a " + webpage.text[115][12:webpage.index('<')])
    else:
        print('Error not the good status code 200 !=', webpage.status_code)

# class Slapper(commands.Converter):
#     async def convert(self, ctx, argument):
#         to_slap = random.choice(ctx.guild.members)
#         return '{0.author} slapped {1} because *{2}*'.format(ctx, to_slap, argument)

# @bot.command()
# async def slap(ctx, *, reason: Slapper):
#     """SLAP LIKE NOW"""
#     await ctx.send(reason)


@bot.command()
async def joined(ctx, *, member: discord.Member = None):
    """tells the time that a member joined this server"""
    if not member:
        member = ctx.author
    await ctx.send('{0} joined on {0.joined_at}'.format(member))


@bot.command()
async def stalk(ctx):
    """get status of all online members"""
    members = ctx.guild.members
    output = []
    for member in members:
        if member.bot:
            continue
        if not member.activities:
            if member.status != discord.Status.offline:
                output.append(f'{member.name} is {member.status}')
            continue
        verb = str(member.activities[0].type)
        verb = verb[verb.index('.')+1:]
        if verb == 'custom':
            verb = 'saying'
        output.append(f'{member.name} is {verb} {member.activities[0].name}')
    await ctx.send('\n'.join(output))
