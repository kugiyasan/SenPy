import discord
import json


async def updateValueJson(value, *keys, appendList=False):
    with open('config.json', 'r') as configFile:
        data = json.load(configFile)

    cursor = data
    for key in keys[:-1]:
        try:
            cursor = cursor[key]
        except:
            cursor[key] = {}
            cursor = cursor[key]
    
    if appendList:
        cursor[keys[-1]].append(value)
    else:
        cursor[keys[-1]] = value

    with open('config.json', 'w+') as configFile:
        json.dump(data, configFile)

async def updateWordStory(value, guild, attribute, appendList=False):
    await updateValueJson(value, 'guilds', guild, 'word-story', attribute, appendList=appendList)

async def getValueJson(*keys, default=None):
    with open('config.json', 'r') as configFile:
        data = json.load(configFile)

    for key in keys:
        try:
            data = data[key]
        except:
            return default
    
    return data

