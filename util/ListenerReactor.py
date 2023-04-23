import discord
from discord.ext import commands
import random
import os
from os import walk
import typing
from datetime import *
import sys
from discord.ext.commands import BadArgument
import math
import traceback
import shutil
import asyncio
from datetime import datetime
from emoji import emojize
import re
import requests
import json
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.PlayerDataHandler import *
from util.GuildDataHandler import *
from util.SLHandle import load, loadJSON, saveJSON
from util.TextFormat import *
from util.ColorUtil import *
from util.ToolsUtil import calculatorFunct as calc
from util.cmdutil import cmdutil
text = cmdutil()
local = loadJSON('.\\locals\\locals.json')
PATH = load(".\\locals\\%PATH%")


def reloadEmojis(bot):
    defaultEmojis = getDefaultEmojis()
    text.log('Gathering custom emojis...')
    emojis = {}
    for guild in bot.guilds:
        for emote in guild.emojis:
            if emote.animated: a = "a"
            else: a = ""
            if emote.name not in emojis.keys() and emote.name not in defaultEmojis:
                emojis[emote.name] = f"<{a}:{emote.name}:{emote.id}>"
            elif emote.name in emojis.keys():
                emojis[emote.name + "~0"] = emojis[emote.name]
                del emojis[emote.name]
                number = 1
                while emote.name + "~" + str(number) in emojis: number += 1
                emojis[emote.name + "~" + str(number)] = f"<{a}:{emote.name}:{emote.id}>"
            elif emote.name in defaultEmojis:
                emojis[emote.name + "~0"] = f"<{a}:{emote.name}:{emote.id}>"
                
        text.log(f"[EMJLOADER] Gathered {len(guild.emojis)} from {guild.name}!")
    saveJSON(emojis, "emojis.json", "data")
    return len(emojis.keys())

def getDefaultEmojis():
    defaultEmojilist = []
    if not exists(f"{PATH}\\defaultEmojis.json"):
        text.log('Gathering default emojis...')
        r = requests.get("https://emzi0767.gl-pages.emzi0767.dev/discord-emoji/discordEmojiMap-canary.json")
        emojiDB = json.loads(r.content)["emojiDefinitions"]
        for emoji in emojiDB:
            defaultEmojilist = [*defaultEmojilist, *emoji["names"]]
        saveJSON(defaultEmojilist, "defaultEmojis.json", PATH)
    else:
        defaultEmojilist = loadJSON("defaultEmojis.json", PATH)
    return defaultEmojilist
    
async def preprocessMessage(ctx):
    message = ctx.message
    author = message.author
    guild = message.guild
    
    #Check if a bot said smth
    if author.bot:
        if author.id not in [405968021337669632, 807593322033971231]:
            text.log(f"{author.name} said something in {guild.name}, but they're a bot.")
        return False

    #Check if a banned person is using Zako.
    if not exists(f"{PATH}\\zakoBlacklist.json"):
        blacklist = []
        text.log(f"File {PATH}\\zakoBlacklist.json not found.")
    else: blacklist = loadJSON("zakoBlacklist.json", PATH)
    if author.id in blacklist:
        text.log(f"{author.name} said something in {guild.name}, but they're banned from using me.")
        return False

    #Check for any moderation rules.
    #Censorship
    admin = GuilddataGetFile(guild, "admin.json")
    guildSettings = GuilddataGetFile(guild, "settings.json")
    if admin["Admin Channel"] is not None:
        converter = commands.TextChannelConverter()
        adminChannel = await converter.convert(ctx, admin["Admin Channel"])
    else: adminChannel = None

    #Check if Zako is ignoring this channel.
    if str(message.channel.id) in admin["Zako Ignored Channels"]:
        if not author.guild_permissions.manage_messages:
            text.log(f"{author.name} said something in {guild.name}, but I'm ignoring the channel.")
            return False

    #Check for artificial character limit
    if not author.guild_permissions.manage_messages:
        if len(message.content) > guildSettings["CharacterLimit"]:
            await message.delete()
            await message.channel.send(f"Your message is too long... You've hit the {guildSettings['CharacterLimit']} character count limit.")
            if adminChannel is not None:
                await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that exceeded the character limit:")
                for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                    await adminChannel.send(i)
            text.log(f"{author.name} said something in {guild.name}, but it exceeded the character limit.")
            return False

    #Check for any banned words.
    for word in GuilddataGetFile(guild, "curses.json"):
        if not author.guild_permissions.manage_messages:
            if word in str.lower(message.content):
                await message.channel.send(f"You can't say that, <@{message.author.id}>!")
                await message.delete()
                text.log(f"{author.name} said something in {guild.name}, but they said something that wasn't allowed on that guild.")
                if adminChannel is not None:
                    await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that contained a word that wasn't allowed:")
                    for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                        await adminChannel.send(i)
                return False
    
    if str(author.id) in admin["Censored Users"]:
        if not author.guild_permissions.manage_messages:
            await message.delete()
            text.log(f"{author.name} said something in {guild.name}, but they are being censored.")
            if adminChannel is not None:
                await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that was censored:")
                for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                    await adminChannel.send(i)
            return False

    #Images in an image blocked channel
    if str(message.channel.id) in admin["Image Blocked Channels"]:
        if not author.guild_permissions.manage_messages:
            for ext in [".jpg", ".png", ".jpeg", ".gif"]: 
                if message.content.endswith(ext): #Image links
                    await message.delete()
                    text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                    if adminChannel is not None:
                        await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that contained an image:")
                        for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                            await adminChannel.send(i)
                    return False
                else: #Attached image
                    for attachment in message.attachments:
                        if attachment.url.endswith(ext):
                            await message.delete()
                            text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                            if adminChannel is not None:
                                await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that contained an image:")
                                for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                                    await adminChannel.send(i)
                                await adminChannel.send(attachment.url)
                            return False
            if "https://tenor.com/view/" in message.content: #tenor
                await message.delete()
                text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                if adminChannel is not None:
                    await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that contained an image:")
                    for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                        await adminChannel.send(i)
                return False

    #Links in a link blocked channel
    if str(message.channel.id) in admin["Link Blocked Channels"]:
        if not author.guild_permissions.manage_messages:
            for hyper in ["http://", "https://"]:
                if hyper in message.content:
                    for ext in [".jpg", ".png", ".jpeg", ".gif"]: 
                        if not message.content.endswith(ext): #Filter out image links
                            await message.delete()
                            text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                            if adminChannel is not None:
                                await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that contained a link:")
                                for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                                    await adminChannel.send(i)
                            return False
                else:
                    for attachment in message.attachments:
                        if hyper in attachment.url:
                            for ext in [".jpg", ".png", ".jpeg", ".gif"]: 
                                if not message.content.endswith(ext): #Filter out image links
                                    await message.delete()
                                    text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                                    if adminChannel is not None:
                                        await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that contained a link:")
                                        for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                                            await adminChannel.send(i)
                                    return False

    #Emojis in an emoji blocked channel
    if str(message.channel.id) in admin["Emoji Blocked Channels"]:
        if not author.guild_permissions.manage_messages:
            emojimap = loadJSON("emoji_map.json", PATH)
            for emoji in emojimap:
                if emojimap[emoji] in message.content:
                    await message.delete()
                    text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                    await message.channel.send("This emoji doesn't work here because emojis are disabled in this channel.")
                    if adminChannel is not None:
                        await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that likely contained an emoji:")
                        for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                            await adminChannel.send(i)
                    return False
            if re.search("^<:.*>$", message.content) != None or re.search("^<a:.*>$", message.content) != None:
                await message.delete()
                text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                await message.channel.send("This emoji doesn't work here because emojis are disabled in this channel.")
                if adminChannel is not None:
                    await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that likely contained an emoji:")
                    for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                        await adminChannel.send(i)
                return False
            eml = loadJSON("emojis.json", "data")
            for emoji in eml:
                if f":{emoji}:" in message.content:
                    await message.delete()
                    text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                    await message.channel.send("This emoji doesn't work here because emojis are disabled in this channel.")
                    if adminChannel is not None:
                        await adminChannel.send(f"{author.name} ({author.id}) sent a message in <#{message.channel.id}> that likely contained an emoji:")
                        for i in [message.content[start:start+2000] for start in range(0, len(message.content), 2000)]:
                            await adminChannel.send(i)
                    return False 
            

    # Seems good.
    text.log(f"{author.name} said something in {guild.name}.")
    return True

async def parseEventCommand(ctx, inp, event):
    if type(ctx) is discord.ext.commands.context.Context:
        message = ctx.message
        author = message.author
        guild = message.guild
        channel = message.channel
        
        userInfo = realUsers(guild)
        variables = {"serverName": guild.name, "memberCount": userInfo[0], "userCount": userInfo[1],
                     "botCount": userInfo[2], "serverID": guild.id, "userName": author.name,
                     "userID": author.id, "userNick": author.display_name, "userPing": f"<@{author.id}>",
                     "message": message.content.replace(inp, ""), "channelName": channel.name,
                     "channelID": channel.id, "printChannel": channel.id}
    elif type(ctx) is discord.member.Member:
        message = None
        author = ctx
        guild = ctx.guild
        channel = None
        
        userInfo = realUsers(guild)
        variables = {"serverName": guild.name, "memberCount": userInfo[0], "userCount": userInfo[1],
                     "botCount": userInfo[2], "serverID": guild.id, "userName": author.name,
                     "userID": author.id, "userNick": author.display_name, "userPing": f"<@{author.id}>",
                     "message": "None", "channelName": "None", "channelID": 0, "printChannel": 0}
    
    recurses = 0
    offset = 0
    actionNo = 1
    loop = True
    
    sendBuffer = []
    while loop:
        loop = False
        for action in event:
            try:
                if action[offset:6+offset] == "react ":
                    try:
                        await message.add_reaction(formatText(action[6+offset:]))
                    except discord.errors.HTTPException:
                        await message.add_reaction(emojize(action[6+offset:]))
                elif action[offset:5+offset] == "send ":
                    sendBuffer.append(formatText(action[5+offset:]))
                elif action[offset:4+offset] == "var ":
                    vari = action[4+offset:].split("=")
                    for part in range(len(vari)): vari[part] = vari[part].strip()
                    variables[vari[0]] = eval(vari[1])
                    if vari[0] == "printChannel": #if the programmer has manually set this variable, we need to change the channel!
                        for ch in guild.text_channels:
                            if variables[vari[0]] == ch.id: channel = ch
                elif action[offset:7+offset] == "return ":
                    sendBuffer.append(str(variables[action[7+offset:]]))
                elif action[offset:3+offset] == "br ":
                    br = ""
                    for i in range(int(action[3+offset:])):
                        br += "\n"
                    sendBuffer.append(br)
                elif action[offset:2+offset] == "br":
                    sendBuffer.append("\n")
                elif action[offset:5+offset] == "pull ":
                    variables[action[5+offset:]] = " ".join(sendBuffer).replace("\n ", "\n")
                    sendBuffer = []
                elif action[offset:5+offset] == "print":
                    await channel.send(" ".join(sendBuffer).replace("\n ", "\n"))
                    sendBuffer = []
                elif action[offset:5+offset] == "save ":
                    save(str(variables[action[5+offset:]]), action[5+offset:] + ".txt", f".\\guilddata\\{guild.id}\\data\\")
                elif action[offset:5+offset] == "load ":
                    data = load(action[5+offset:] + ".txt", f".\\guilddata\\{guild.id}\\data\\")
                    try:
                        variables[action[5+offset:]] = eval(data)
                    except (SyntaxError,TypeError):
                        #just return it as string smh
                        variables[action[5:]] = data
                elif action[offset:5+offset] == "calc ":
                    vari = action[5+offset:].split(",")
                    for part in range(len(vari)): vari[part] = vari[part].strip()
                    for variable in list(variables.keys()):
                        if variable in vari[1]: vari[1] = vari[1].replace(variable, str(variables[variable]))
                    variables[vari[0]] = calc(author, vari[1])
                elif action[offset:5+offset] == "eval ":
                    vari = action[5+offset:].split(",")
                    for part in range(len(vari)): vari[part] = vari[part].strip()
                    for variable in list(variables.keys()):
                        if variable in vari[1]:
                            if type(variables[variable]) != str:
                                vari[1] = vari[1].replace(variable, str(variables[variable]))
                            else:
                                vari[1] = vari[1].replace(variable, '"' + variables[variable].strip() + '"')
                    variables[vari[0]] = eval(vari[1])
                elif action[offset:3+offset] == "if ":
                    vari = action[3+offset:]
                    for variable in list(variables.keys()):
                        if variable in vari: 
                            if type(variables[variable]) != str:
                                vari = vari.replace(variable, str(variables[variable]))
                            else:
                                vari = vari.replace(variable, '"' + variables[variable].strip() + '"')
                    if eval(vari):
                        offset += 2
                elif action[offset:4+offset] == "back":
                    offset -= 2
                elif action[offset:4+offset] == "run ":
                    if recurses == 20:
                        await channel.send(f"Script '{inp}' has encountered an exception in action {actionNo} '{action}'.\n  Too many functions have been called.")
                        return
                    event = [*GuilddataGetFile(guild, "scripts\\function.json")[action[4+offset:]], *event[actionNo:]]
                    recurses += 1
                    loop = True
                    break
                actionNo += 1
            except Exception as e:
                await channel.send(f"Script '{inp}' has encountered an exception in action {actionNo} '{action}'.\n  {e}")
                text.warn(f"[SCRIPTERROR] Script '{inp}' from {guild.name} has encountered an exception in action {actionNo} '{action}'.\n  {e}")
