print('Starting up...')
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
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.PlayerDataHandler import *
from util.GuildDataHandler import *
from util.SLHandle import load
from util.TextFormat import *
from util.ColorUtil import *
from util.ToolsUtil import calculatorFunct as calc
from util.cmdutil import cmdutil
text = cmdutil()

dpv = discordpyVersion = discord.version_info
text.log(f"Running DiscordPy v{dpv[0]}.{dpv[1]}.{dpv[2]} {dpv[3]}-{dpv[4]}")

text.log("Importing commands from file...")

dataFile = os.path.dirname(os.path.abspath(__file__))

text.log("Constructing bot instance...")
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)
bot = commands.Bot(command_prefix="z/", description="Beta branch of Zako!", intents=intents)

text.log('Finding server...')
@bot.event
async def on_ready():  # Bot boot-up. Below text appears if it successfully boots.
    text.log('Logged in as ' + bot.user.name + ' with ID <' + str(bot.user.id) + '>')
    text.log("Logged into {0} guilds.".format(len(bot.guilds)))
    text.log('------')
        
## ----- Commands ----- ##
text.log('Loading commands...')

_cmdl_ = []
catdesc = {}
cmddesc = {}
working_import = None
for root, dirs, files in os.walk("cmds"):
    for file in files:
        try:
            if "cpython-38.pyc" in file:
                continue
            file = file[:-3]
            text.log(f"> Loading commands from *\\cmds\\{file}.py...")
            empty = {}
            try:
                exec(f"from cmds import {file} as {file}; workingImport = {file}._cmdl_()")
                if len(workingImport) == 0:
                    text.warn(f"Category {file} has no listed commands. Skipping...")
                    continue
                else:
                    exec(f"catdesc['{file}'] = {file}._catdesc_(); cmddesc[{'file'}] = workingImport")
            except Exception as e:
                text.warn(f"Module {file} is broken: {e}. Skipping...")
                continue
            for cmd in workingImport:
                try:
                    exec(f"_cmdl_.append(file+'.'+cmd);")
                    #text.log(f">> Found z/{cmd}.")
                except Exception as e: #command is broken for some reason
                    text.warn(f"Command {cmd} is broken: {e}. Skipping...")
                    continue
        except Exception as e: #category is broken for some reason
            text.warn(f"Category {file} is broken: {e}. Skipping...")
            continue
text.log("Implementing commands...")
for cmd in _cmdl_:
    try:
        #text.log(f"> Implementing {cmd}...")
        exec(f"bot.add_command({cmd})")
    except Exception as e:
        text.warn(f"Command {cmd} is broken: {e}. Skipping...")
        continue
        

#these commands are too important to leave anywhere else.
@bot.command(aliases=['reset', 'reboot', 'reload'])
async def restart(ctx): #Runs z/debug restart
    """Dev Command. Restarts Zako. Doesn't work in the developer build!"""
    if str(ctx.author.id) == '248641004993773569':
        mess = 'Zakobot is restarting!'
        await ctx.send(mess)
        text.log(mess)
        sys.exit(99999)
    else:
        out = 'You do not have permission to perform this action.'
        await ctx.send(out)
    return

@bot.command(aliases=['cmds', 'command', 'commands'])
async def cmd(ctx, *category):
    """Shows a list of Zako's commands and categories. Doesn't replace z/help."""
    returnText = "```Zako3 Commands"
    if category == (): returnText += "\n==================================\n\n"
    for root, dirs, files in os.walk("cmds"):
        for file in files:
            if "cpython-38.pyc" in file:
                continue
            if file[:-3] not in list(catdesc.keys()):
                continue
            file = file[:-3]
            if category == (): returnText += file[4:] + " - " + catdesc[file] + "\n"
            elif file[4:] == category[0]:
                returnText += " - Category: " + category[0].title() + "\n==================================\n\n"
                clist = cmddesc[file]
                for cmd in clist:
                    try: #get the command description
                        returnText += cmd + " - " + bot.get_command(cmd).help.split("\n")[0] + "\n"
                    except Exception: #no description provided!
                        returnText += cmd + " - No description provided.\n"
    if category != ():
        if "cmd_"+category[0] not in list(cmddesc.keys()): returnText += " - Category: INVALID\n==================================\n\nNo such category exists. Please do z/cmd to list all categories."
        else: returnText += "\nDo z/help <command> for more info."
    if category == (): returnText += "\nDo z/cmd <category> for a list of commands."
                
    await ctx.send(returnText + "```")
    return
        
restarted = True

@bot.event
async def on_message(message):
    try:
        global restarted
        author = message.author
        guild = message.guild
        ts = datetime.timestamp(datetime.now())
        ctx = await bot.get_context(message)
        
        preloadGuilddata(guild)

        ### Check if a message should be processed.

        #Check if a bot said smth
        if author.bot:
            if author.id not in [405968021337669632, 807593322033971231]:
                text.log(f"{author.name} said something in {guild.name}, but they're a bot.")
            return

        #Check if a banned person is using Zako.
        if not exists(f".\\data\\zakoBlacklist.json"):
            blacklist = []
            text.log("File .\\data\\zakoBlacklist.json not found.")
        else: blacklist = loadJSON("zakoBlacklist.json", "data")
        if author.id in blacklist:
            text.log(f"{author.name} said something in {guild.name}, but they're banned from using me.")
            return

        #Check for any banned words.
        for word in GuilddataGetFile(guild, "curses.json"):
            if not author.guild_permissions.manage_messages:
                if word in str.lower(message.content):
                    await message.channel.send(f"You can't say that, <@{message.author.id}>!")
                    await message.delete()
                    text.log(f"{author.name} said something in {guild.name}, but they said something that wasn't allowed on that guild.")
                    return

        #Check for any moderation rules.
        #Censorship
        admin = GuilddataGetFile(guild, "admin.json")
        if str(author.id) in admin["Censored Users"]:
            if not author.guild_permissions.manage_messages:
                await message.delete()
                text.log(f"{author.name} said something in {guild.name}, but they are being censored.")
                return

        #Images in an image blocked channel
        if str(message.channel.id) in admin["Image Blocked Channels"]:
            if not author.guild_permissions.manage_messages:
                for ext in [".jpg", ".png", ".jpeg", ".gif"]: 
                    if message.content.endswith(ext): #Image links
                        await message.delete()
                        text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                        return
                    else: #Attached image
                        for attachment in message.attachments:
                            if attachment.url.endswith(ext):
                                await message.delete()
                                text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                                return
                if "https://tenor.com/view/" in message.content: #tenor
                    await message.delete()
                    text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                    return

        #Links in a link blocked channel
        if str(message.channel.id) in admin["Link Blocked Channels"]:
            if not author.guild_permissions.manage_messages:
                for hyper in ["http://", "https://"]:
                    if hyper in message.content:
                        await message.delete()
                        text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                        return
                    else:
                        for attachment in message.attachments:
                            if hyper in attachment.url:
                                await message.delete()
                                text.log(f"{author.name} said something in {guild.name}, but it contained blocked content.")
                                return

        # Seems good.
        text.log(f"{author.name} said something in {guild.name}.")


        ### Construct and update player and guild data.

        preloadPlayerdata(author)
        
        userStats = PlayerdataGetFile(author, "stats.json")
        userStats["Messages Sent"] += 1
        userStats = updateStats(userStats)
        userStats["Activity Board"][-1] += 1
        PlayerdataSetFile(author, "stats.json", userStats)
        
        guildStats = GuilddataGetFile(guild, "stats.json")
        guildStats["Messages Sent"] += 1
        guildStats = updateStats(guildStats)
        guildStats["Activity Board"][-1] += 1
        GuilddataSetFile(guild, "stats.json", guildStats)
        
        guildSettings = GuilddataGetFile(guild, "settings.json")
        guildStats = GuilddataGetFile(guild, "stats.json")
        guildOnMessageIsEvent = GuilddataGetFile(guild, "scripts\\onMessageIs.json")
        guildOnMessageHasEvent = GuilddataGetFile(guild, "scripts\\onMessageHas.json")

        guildStats["Members"], guildStats["Users"], guildStats["Bots"] = realUsers(guild)

        #Save playername to file
        if not exists(f".\\data\\playerNameDB.json"):
            playerNameDict = {}
            text.log("File .\\data\\playerNameDB.json not found.")
        else: playerNameDict = loadJSON("playerNameDB.json", "data")
        
        if str(author.id) not in list(playerNameDict.keys()):
            playerNameDict[author.id] = author.name
            saveJSON(playerNameDict, "playerNameDB.json", "data")
            text.log(f"Added {author.name} to user table.")
        elif playerNameDict[str(author.id)] != author.name:
            text.log(f"{playerNameDict[str(author.id)]} changed their name to {author.name}.")
            playerNameDict[author.id] = author.name
            saveJSON(playerNameDict, "playerNameDB.json", "data")
            PlayerdataSetFileIndex(author, "profile.json", "Name", author.name)
        PlayerdataSetFileIndex(author, "profile.json", "Name", author.name)
        
        #Add experience
        if guildSettings["Levels"] and PlayerdataGetFileIndex(author, "timers.json", "EXPTimer") < ts-5:
            def incrementXP(userLevelFile, coins=True):
                userLevelFile["Experience"] += random.randrange(5,10)
                if userLevelFile["Level"] < 200:
                    if userLevelFile["Experience"] >= 20+(userLevelFile["Level"]**2*20):
                        userLevelFile["Experience"] -= 20+(userLevelFile["Level"]**2*20)
                        userLevelFile["Level"] += 1
                        text.log(f"{author.name} is now level {userLevelFile['Level']}.")

                        if coins:
                            userSilver = PlayerdataGetFileIndex(author, "wallet.json", "Args")
                            userSilver += 10*userLevelFile["Level"]
                            PlayerdataSetFileIndex(author, "wallet.json", "Args", userSilver)
                        return userLevelFile, True
                    else: return userLevelFile, False

            async def reactToLvUp(integer):
                thirdNumSet = ["<:zero:962696895682199593>", "<:one2:996450500167872612>",
                                "<:two:962696895988396062>"]
                secondNumSet = ["<:zero:962696895682199593>", "<:one:962696895925481482>",
                                "<:two:962696895988396062>", "<:three:962696895917080666>",
                                "<:four:962696895514431529>", "<:five:962696895996780594>",
                                "<:six:962696896072257626>", "<:seven:962696895980011630>",
                                "<:eight:962696895422165003>", "<:nine:962696895921274910>"]
                if PlayerdataGetFileIndex(author, "settings.json", "LvUpReacts") and guildSettings["LvUpReacts"]:
                    await message.add_reaction(u"\U0001F1F1")
                    await message.add_reaction(u"\U0001F1FB")
                    await message.add_reaction(u"\u2B06")
                    await message.add_reaction(str(integer)[0]+"\u20e3")
                    if integer >= 10: await message.add_reaction(secondNumSet[int(str(integer)[1])])
                    if integer >= 100: await message.add_reaction(thirdNumSet[int(str(integer)[2])])
                            
            userGlobalLevel = PlayerdataGetFile(author, "level.json")
            userGuildLevel = {"Experience": 0, "Level": 0}
            levelFile = GuilddataGetFile(guild, "levels.json")
            if str(author.id) in levelFile: userGuildLevel = levelFile[str(author.id)]

            userGlobalLevel = incrementXP(userGlobalLevel)
            userGuildLevel = incrementXP(userGuildLevel, False)
            PlayerdataSetFile(author, "level.json", userGlobalLevel[0])
            levelFile[str(author.id)] = userGuildLevel[0]
            GuilddataSetFile(guild, "levels.json", levelFile)

            if guildSettings["GlobalLevel"] and userGlobalLevel[1]: await reactToLvUp(userGlobalLevel[0]["Level"])
            if not guildSettings["GlobalLevel"] and userGuildLevel[1]: await reactToLvUp(userGuildLevel[0]["Level"])
            
            PlayerdataSetFileIndex(author, "timers.json", "EXPTimer", ts)
        
        #update timestamp
        userTimestamp = PlayerdataGetFileIndex(author, "timers.json", "Timestamp")
        ts = datetime.timestamp(datetime.now())
        if ts >= userTimestamp+900:
            PlayerdataSetFileIndex(author, "timers.json", "Timestamp", ts)
        UpdateTimers(author)


        ### Check for announcement
        if guild.id == 620840204495880192 and message.channel.id == 994649780955389952:
            if str.lower(message.content) == "changelog":
                changelog = loadJSON("changelog.txt", ".\\data\\")
                announce = changelog[list(changelog.keys())[-1]]
                source = "self"
            else:
                announce = message.content
                source = "author"
            for server in bot.guilds:
                if exists(f".\\guilddata\\{server.id}\\admin.json"):
                    announceChannel = GuilddataGetFileIndex(server, "admin.json", "Update Channel")
                    if announceChannel != None:
                        channel = server.get_channel(int(announceChannel))
                        text.log(f"Announcement from {source} sent to {server.name}-{channel.name} ({server.id}-{channel.id}):\n{announce}")
                        if source == "self": #send message as Zako
                            await channel.send(announce)
                        elif source == "author": #send message as whom'st've posted it
                            webhooks = await channel.webhooks()
                            hook = None
                            for webhook in webhooks:
                                if webhook.name == "Zako":
                                    hook = webhook
                            if hook == None:
                                hook = await channel.create_webhook(name="Zako")
                            hookmsg = await hook.send(announce, username=author.display_name, avatar_url=author.avatar_url)
                    

        ### Load global data

        if restarted:
            ## ----- Emojis ----- ##
            text.log('Gathering custom emojis...')

            emojis = {}
            for guild in bot.guilds:
                for emote in guild.emojis:
                    if not emote.animated:
                        if emote.name not in list(emojis.keys()):
                            emojis[emote.name] = f"<:{emote.name}:{emote.id}>"
                        else:
                            number = 0
                            while emote.name + "~" + str(number) in emojis: number += 1
                            emojis[emote.name + "~" + str(number)] = f"<a:{emote.name}:{emote.id}>"
                    else:
                        if emote.name not in list(emojis.keys()):
                            emojis[emote.name] = f"<a:{emote.name}:{emote.id}>"
                        else:
                            number = 0
                            while emote.name + "~" + str(number) in emojis: number += 1
                            emojis[emote.name + "~" + str(number)] = f"<a:{emote.name}:{emote.id}>"
                text.log(f"Gathered {len(guild.emojis)} from {guild.name}!")
            saveJSON(emojis, "emojis.json", "data")

            restarted = False


        ### Translate emotes

        emojis = loadJSON("emojis.json", "data")
        string = message.content
        for emoji in list(emojis.keys()):
            if f":{emoji}:" in string:
                if f"<:{emoji}:" not in string and f"<a:{emoji}:" not in string:
                    text.debug(emojis[emoji])
                    text.debug(string)
                    string = string.replace(f":{emoji}:", emojis[emoji])
                else:
                    pass #Nitro scum smh
                    
        if string != message.content:
            webhooks = await message.channel.webhooks()
            hook = None
            for webhook in webhooks:
                if webhook.name == "Zako":
                    hook = webhook
            if hook == None:
                hook = await message.channel.create_webhook(name="Zako")
            await discord.Message.delete(message)
            hookmsg = await hook.send(string, username=author.display_name, avatar_url=author.avatar_url, wait=True)
            if message.reference != None:
                converter = commands.MessageConverter()
                ref = await converter.convert(ctx, f"{message.reference.channel_id}-{message.reference.message_id}")
                
                link = f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ref.id}"
                color = rectColor(PlayerdataGetFileIndex(author, "settings.json", "Color"))
                embed = discord.Embed(title="Reply to: ", description=ref.content, color=color, url=link)
                embed.set_author(name=ref.author.display_name, url=link, icon_url=ref.author.avatar_url)
                await hook.send(embed=embed, username=author.display_name, avatar_url=author.avatar_url)
            return #the message is gone, no point in continuing
                    

        ### Process commands and events

        await bot.process_commands(message)

        async def parseEventCommand(inp, event):
            recurses = 0
            offset = 0
            actionNo = 1
            loop = True
            userInfo = realUsers(guild)
            variables = {"serverName": guild.name, "memberCount": userInfo[0], "userCount": userInfo[1],
                         "botCount": userInfo[2], "serverID": guild.id, "userName": author.name,
                         "userID": author.id, "userNick": author.display_name, "userPing": f"<@{author.id}>",
                         "message": message.content.replace(inp, "")}
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
                            await message.channel.send(" ".join(sendBuffer).replace("\n ", "\n"))
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
                                await message.channel.send(f"Script '{inp}' has encountered an exception in action {actionNo} '{action}'.\n  Too many functions have been called.")
                                return
                            event = [*GuilddataGetFile(guild, "scripts\\function.json")[action[4+offset:]], *event[actionNo:]]
                            recurses += 1
                            loop = True
                            break
                        actionNo += 1
                    except Exception as e:
                        await message.channel.send(f"Script '{inp}' has encountered an exception in action {actionNo} '{action}'.\n  {e}")
                    

        for event in list(guildOnMessageIsEvent.keys()):
            if str.lower(message.content) == str.lower(event):
                await parseEventCommand(event, guildOnMessageIsEvent[event])

        for event in list(guildOnMessageHasEvent.keys()):
            if str.lower(event) in str.lower(message.content):
                await parseEventCommand(event, guildOnMessageHasEvent[event])

    except Exception as e:
        text.error(e)

    text.num = [0]

            

text.log("Loading error handler...")

@bot.event
async def on_command_error(ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Not a command. Do z/help for a list of commands.')
        return

    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'I lack the **{}** permission(s) needed to run this command.'.format(fmt)
        await ctx.send(_message)
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send('This command has been disabled.')
        return

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after)))
        return

    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
        await ctx.send(_message)
        return

    if isinstance(error, commands.UserInputError):
        await ctx.send("Args are either too short or otherwise wrong for this command. Check z/help <command> and try again.")
        return

    if isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send('This command cannot be used in direct messages.')
        except discord.Forbidden:
            pass
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
        return

    # ignore all other exception types, but print them to stderr
    await ctx.send(f'Ignoring exception in command {ctx.command}: {error}')
    text.error(error)

    #traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# ----- Bot Load Finalization ----- #
text.log('Inserting key...')
bot.run(load("key.txt"))
text.log('Running!')
