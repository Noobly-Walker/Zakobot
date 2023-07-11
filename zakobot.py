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
import importlib
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.PlayerDataHandler import *
from util.GuildDataHandler import *
from util.SLHandle import load
from util.TextFormat import *
from util.ColorUtil import *
from util.ToolsUtil import calculatorFunct as calc
from util.cmdutil import cmdutil
from util.ListenerReactor import *
text = cmdutil()
local = loadJSON('.\\locals\\locals.json')
PATH = load(".\\locals\\%PATH%")

dpv = discordpyVersion = discord.version_info
text.log(f"Running DiscordPy v{dpv[0]}.{dpv[1]}.{dpv[2]} {dpv[3]}-{dpv[4]}")

text.log("Importing commands from file...")

dataFile = os.path.dirname(os.path.abspath(__file__))
    
text.log("Constructing bot instance...")
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)
bot = commands.Bot(command_prefix=local["prefix"], description=f"{local['branch']} branch of Zako!", intents=intents)
        
## ----- Commands ----- ##
text.log('Loading commands...')

categoryDescriptions = {}
categoryCommands = {}
# loop through modules and import them
for root, dirs, files in os.walk("cmds"):
    for file in files:
        if file.endswith(".py") and not file.startswith("_"):
            categoryName = file[:-3] # remove ".py" extension
            try:
                categoryPath = f"cmds.{categoryName}"
                categoryImport = importlib.import_module(categoryPath)
                categoryDescriptions[categoryName] = categoryImport.categoryDescription()
            except ImportError as e:
                text.warn(f"Category {categoryName} is broken: {e}. Skipping...")
                continue
            # add commands to bot object and to categoryCommands
            for cmd in categoryImport.commandList():
                try:
                    bot.add_command(cmd)
                    # add command to the list of commands for this category
                    if categoryName not in categoryCommands:
                        categoryCommands[categoryName] = [cmd.name]
                    else:
                        categoryCommands[categoryName].append(cmd.name)
                except Exception as e:
                    try: text.warn(f"Command {cmd.name} is broken: {e}. Skipping...")
                    except Exception: text.warn(f"Command {cmd} is broken: {e}. Skipping...")
                    continue

#these commands are too important to leave anywhere else.
@bot.command()
async def restart(ctx): #Runs z!debug restart
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

@bot.command()
async def reload(ctx): #Runs like on_ready()
    """Dev Command. Reloads some Zako things."""
    if str(ctx.author.id) == '248641004993773569':
        await ctx.send("Reloading...")
        emojict = reloadEmojis(bot)
        await ctx.send(f"Loaded {emojict} custom emojis!")
        await ctx.send("Done!")
        text.log("Reloaded successfully, I hope.")
    else:
        out = 'You do not have permission to perform this action.'
        await ctx.send(out)
    return

bot.remove_command('help')

@bot.command(aliases=['cmd', 'cmds', 'command', 'commands', '?'])
async def help(ctx, *category_or_command):
    """Shows a list of Zako's commands and categories, and gives information on commands.
Did you seriously do '[prefix]help help'? You must be new to Discord bots, huh...
[prefix]help (category) - Lists categories.
[prefix]help (command) - Displays information on a command."""
    returnText = f"Zako Zaun {local['branch']} Commands"
    if category_or_command == (): returnText += "\n==================================\n\n"
    wasCategory = False
    for root, dirs, files in os.walk("cmds"): # look for the category
        for file in files:
            if "cpython-38.pyc" in file: continue
            if file[:-3] not in list(categoryDescriptions.keys()): continue
            file = file[:-3]
            if category_or_command == (): returnText += file[4:] + " - " + categoryDescriptions[file] + "\n"
            elif file[4:] == category_or_command[0]:
                returnText += " - Category: " + category_or_command[0].title() + "\n==================================\n\n"
                clist = categoryCommands[file]
                wasCategory = True
                for cmd in clist:
                    try: #get the command description
                        returnText += cmd + " - " + bot.get_command(cmd).help.split("\n")[0] + "\n"
                    except Exception: #no description provided!
                        returnText += cmd + " - No description provided.\n"
    if category_or_command != (): # if there was a category being searched
        command = bot.get_command(category_or_command[0])
        if command:
            # Show help for the command
            if wasCategory:
                returnText += f"```\n```Zako Zaun {local['branch']} Commands"
            returnText += f" - Command: {category_or_command[0].title()}\n==================================\n{bot.command_prefix}{category_or_command[0]} "
            for param in command.clean_params:
                returnText += f"<{param}> "
            returnText += f"\n\n{command.help}".replace('[PREFIX]', bot.command_prefix)
        elif "cmd_"+category_or_command[0] not in list(categoryDescriptions.keys()): # it's not a command or a category
            returnText += f" - NO RESULTS\n==================================\n\n\
No such category or command exists. Please do {bot.command_prefix}help to list all categories."
        else: returnText += f"\nDo {bot.command_prefix}help <command> for more info." # wut
    if category_or_command == (): returnText += f"\nDo {bot.command_prefix}help <category> for a list of commands." # Nothing was being searched
    for i in ["\n".join(str(returnText).split('\n')[start:start+15]) for start in range(0, len(str("```" + returnText).split('\n')), 15)]:
        await ctx.send("```"+i+"```")
    return


@bot.event
async def on_ready():  # Bot boot-up. Below text appears if it successfully boots.
    text.log('Logged in as ' + bot.user.name + ' with ID <' + str(bot.user.id) + '>')
    text.log("Logged into {0} guilds.".format(len(bot.guilds)))
    reloadEmojis(bot)
    text.log('------')

@bot.event
async def on_member_join(member):
    try:
        guild = member.guild
        updateMemberCount(guild)
        
        text.log(f"{global_name(member)} ({member.id}) has joined {guild.name}")
        
        guildOnMemberJoinEvent = GuilddataGetFile(guild, "scripts\\onMemberJoin.json")
        
        for event in list(guildOnMemberJoinEvent.keys()):
            await parseEventCommand(member, event, guildOnMemberJoinEvent[event])

        guildSettings = GuilddataGetFile(guild, "settings.json")
        if guildSettings["NewUserRoleID"] != "None":
            roleID = int(guildSettings["NewUserRoleID"])
            role = discord.utils.get(guild.roles, id=roleID)
            if role is not None: await member.add_roles(role)
            
    except Exception as e:
        text.error(e)

@bot.event
async def on_member_remove(member):
    try:
        guild = member.guild
        updateMemberCount(guild)
        
        text.log(f"{global_name(member)} ({member.id}) has left {guild.name}")
        
        guildOnMemberLeaveEvent = GuilddataGetFile(guild, "scripts\\onMemberLeave.json")
        for event in list(guildOnMemberLeaveEvent.keys()):
            await parseEventCommand(member, event, guildOnMemberLeaveEvent[event])
    except Exception as e:
        text.error(e)

@bot.event
async def on_guild_join(guild):
    reloadEmojis()

@bot.event
async def on_guild_remove(guild):
    reloadEmojis()

@bot.event
async def on_guild_emojis_update(guild):
    reloadEmojis()

@bot.event
async def on_message(message):
    try:
        global restarted
        author = message.author
        guild = message.guild
        ts = datetime.timestamp(datetime.now())
        ctx = await bot.get_context(message)
        
        preloadGuilddata(guild)
        if not await preprocessMessage(ctx): return
        preloadPlayerdata(author)

        ### Construct and update player and guild data.
        
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
        bot.command_prefix = guildSettings["Prefix"]

        #Save playername to file
        if not exists(f"{PATH}\\playerNameDB.json"):
            playerNameDict = {}
            text.log(f"File {PATH}\\playerNameDB.json not found.")
        else: playerNameDict = loadJSON("playerNameDB.json", PATH)
        
        if str(author.id) not in list(playerNameDict.keys()):
            playerNameDict[author.id] = global_name(author)
            saveJSON(playerNameDict, "playerNameDB.json", PATH)
            text.log(f"Added {global_name(author)} to user table.")
        elif playerNameDict[str(author.id)] != global_name(author):
            text.log(f"{playerNameDict[str(author.id)]} changed their name to {global_name(author)}.")
            playerNameDict[author.id] = global_name(author)
            saveJSON(playerNameDict, "playerNameDB.json", PATH)
            PlayerdataSetFileIndex(author, "profile.json", "Name", global_name(author))
        PlayerdataSetFileIndex(author, "profile.json", "Name", global_name(author))
        
        #Add experience
        if guildSettings["Levels"] and PlayerdataGetFileIndex(author, "timers.json", "EXPTimer") < ts-5:
            userGlobalLevel = PlayerdataGetFile(author, "level.json")
            userGuildLevel = {"Experience": 0, "Level": 0}
            levelFile = GuilddataGetFile(guild, "levels.json")
            if str(author.id) in levelFile: userGuildLevel = levelFile[str(author.id)]

            expGain = random.randrange(5,10)
            userGlobalLevel = incrementXP(ctx, userGlobalLevel, expGain)
            userGuildLevel = incrementXP(ctx, userGuildLevel, expGain, False)
            PlayerdataSetFile(author, "level.json", userGlobalLevel[0])
            levelFile[str(author.id)] = userGuildLevel[0]
            GuilddataSetFile(guild, "levels.json", levelFile)

            if guildSettings["GlobalLevel"] and userGlobalLevel[1]: await reactToLvUp(ctx, userGlobalLevel[0]["Level"])
            if not guildSettings["GlobalLevel"] and userGuildLevel[1]: await reactToLvUp(ctx, userGuildLevel[0]["Level"])
            
            PlayerdataSetFileIndex(author, "timers.json", "EXPTimer", ts)
        
        #update timestamp
        userTimestamp = PlayerdataGetFileIndex(author, "timers.json", "Timestamp")
        ts = datetime.timestamp(datetime.now())
        if ts >= userTimestamp+900:
            PlayerdataSetFileIndex(author, "timers.json", "Timestamp", ts)
        UpdateTimers(author)

        try:
            converter = commands.MemberConverter()
            zakostable = await converter.convert(ctx, "Zako Zaun#9904")
        except Exception:
            zakostable = False

        ### Check for announcement
        if guild.id == 620840204495880192 and message.channel.id == 994649780955389952:
            if str.lower(message.content) == "changelog":
                changelog = loadJSON(f"changelog.txt", PATH)
                announce = changelog[list(changelog.keys())[-1]]
                source = "self"
            else:
                announce = message.content
                source = "author"
            for server in bot.guilds:
                preloadGuilddata(server)
                announceChannel = GuilddataGetFileIndex(server, "admin.json", "Update Channel")
                isGetUpdates = GuilddataGetFileIndex(server, "settings.json", "GetUpdates")
                if announceChannel != None and isGetUpdates and ((local['branch'] == "Developer" and zakostable not in guild.members) or local['branch'] == "Main"):
                    channel = server.get_channel(int(announceChannel))
                    text.log(f"Announcement from {source} sent to {server.name}-{channel.name} ({server.id}-{channel.id}):\n{announce}")
                    if source == "self": #send message as Zako
                        for i in ["\n".join(str("# " + announce).split('\n')[start:start+15]) for start in range(0, len(str("# " + announce).split('\n')), 15)]:
                            await channel.send(i)
                    elif source == "author": #send message as whom'st've posted it
                        webhooks = await channel.webhooks()
                        hook = None
                        for webhook in webhooks:
                            if webhook.name == "Zako": await hook.delete()
                            if webhook.name == f"Zako{local['branch']}": hook = webhook
                        if hook == None: hook = await channel.create_webhook(name=f"Zako{local['branch']}")
                        hookmsg = await hook.send(announce, username=global_name(author), avatar_url=author.avatar_url)


        ### Translate emotes and @someone

        emojis = loadJSON("emojis.json", "data")
        string = message.content
        react = ""
        if (local['branch'] == "Developer" and zakostable not in guild.members) or local['branch'] == "Main":
            for emoji in list(emojis.keys()):
                if f":{emoji}:" in string:
                    if f"<:{emoji}:" not in string and f"<a:{emoji}:" not in string:
                        string = string.replace(f":{emoji}:", emojis[emoji])
                    else:
                        pass #Nitro scum smh
                    if string == f"++{emojis[emoji]}":
                        react = emojis[emoji]
                        string = ""
                    if string == f"+++{emojis[emoji]}":
                        converter = commands.EmojiConverter()
                        sticker = await converter.convert(ctx, emojis[emoji])
                        string = str(sticker.url)
                    
            if (string != message.content or f"{bot.command_prefix}webhook" in message.content):
                webhooks = await message.channel.webhooks()
                hook = None
                for webhook in webhooks:
                    if webhook.name == "Zako": await hook.delete()
                    if webhook.name == f"Zako{local['branch']}": hook = webhook
                if hook == None:
                    hook = await message.channel.create_webhook(name=f"Zako{local['branch']}")
                await discord.Message.delete(message)
                if f"{bot.command_prefix}webhook" in string:
                    string = string.replace(f"{bot.command_prefix}webhook", "")
                    string = formatText(string)
                if string not in ["", " "]:
                    hookmsg = await hook.send(string, username=global_name(author), avatar_url=author.avatar_url, wait=True)
                if message.reference != None:
                    converter = commands.MessageConverter()
                    ref = await converter.convert(ctx, f"{message.reference.channel_id}-{message.reference.message_id}")
                    if string not in ["", " "]:
                        link = f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ref.id}"
                        color = rectColor(PlayerdataGetFileIndex(author, "settings.json", "Color"))
                        embed = discord.Embed(title="Reply to: ", description=ref.content, color=color, url=link)
                        embed.set_author(name=ref.global_name(author), url=link, icon_url=ref.author.avatar_url)
                        await hook.send(embed=embed, username=global_name(author), avatar_url=author.avatar_url)
                    if react != "":
                        await ref.add_reaction(react)
                elif react != "":
                    targetMessage = [m async for m in message.channel.history(limit=1)][0]
                    await targetMessage.add_reaction(react)
                return #the message is gone, no point in continuing

            if "@someone" in string and guildSettings["SomeonePing"]: #ping random person!
                while True:
                    randomUser = random.choice(guild.members)
                    if not randomUser.bot: break
                await ctx.send(f"<@{randomUser.id}>")

        ### Process commands and events
        
        await bot.process_commands(message)

        for event in list(guildOnMessageIsEvent.keys()):
            if str.lower(message.content) == str.lower(event):
                await parseEventCommand(ctx, event, guildOnMessageIsEvent[event])

        for event in list(guildOnMessageHasEvent.keys()):
            if str.lower(event) in str.lower(message.content):
                await parseEventCommand(ctx, event, guildOnMessageHasEvent[event])

    except Exception as e:
        text.error(e)

    text.num = [0]
    bot.command_prefix = local["prefix"]

            

text.log("Loading error handler...")

@bot.event
async def on_command_error(ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        command = ctx.message.content
        guild = ctx.guild
        guildOnMessageIsEvent = GuilddataGetFile(guild, "scripts\\onMessageIs.json")
        guildOnMessageHasEvent = GuilddataGetFile(guild, "scripts\\onMessageHas.json")
        isEvent = False
        for event in list(guildOnMessageIsEvent.keys()):
            if str.lower(command) == str.lower(event):
                isEvent = True
                break
        for event in list(guildOnMessageHasEvent.keys()):
            if str.lower(event) in str.lower(command):
                isEvent = True
                break
        if not isEvent:
            await ctx.send(f'Not a command. Do {bot.command_prefix}help for a list of commands.')
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

    #if isinstance(error, commands.UserInputError):
    #    await ctx.send(f"Args are either too short or otherwise wrong for this command. Check {bot.command_prefix} <command> and try again.")
    #    return

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
bot.run(loadJSON(".\\locals\\keys.json")["discord"])
text.log('Running!')
