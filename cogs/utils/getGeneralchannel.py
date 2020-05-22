import re

async def getGeneralchannel(guild):
    channel = guild.system_channel
    if channel is not None:
        return channel

    for channel in guild.channels:
        if re.search('g[eé]n[eé]ral', channel.name):
            return channel
    
    raise NoChannelError

async def permissiontoWrite(member, channel):
    channel.permissions_for(member)

class NoChannelError(Exception):
    pass
