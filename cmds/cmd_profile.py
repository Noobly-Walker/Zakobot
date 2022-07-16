import asyncio
import discord
from discord import Client
from discord.ext import commands
import traceback
from os import walk
from os.path import isdir,exists
from datetime import *
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import expol
from util.TimeUtil import *
from util.SLHandle import *
from util.PlayerDataHandler import *
from util.GuildDataHandler import *
from util.ColorUtil import rectColor
from util.TextFormat import *
from util.DataHandlerUtil import *
from util.cmdutil import cmdutil
text = cmdutil()

def _cmdl_():
    return ["profile", "leaderboard", "settings", "statistics"]

def _catdesc_():
    return "Commands involving individual users."


@commands.command(aliases=['pf', 'lv', 'level'])
async def profile(ctx, *userIn):
    """Shows user information."""
    user = ctx.author
    if len(userIn) == 1:
        converter = commands.MemberConverter()
        user = await converter.convert(ctx, userIn[0])
    try:
        userProfile = PlayerdataGetFile(user, "profile.json")
        userLevelFile = PlayerdataGetFile(user, "level.json")
        userWalletFile = PlayerdataGetFile(user, "wallet.json")
        expCap = 20+(userLevelFile['Level']**2*20)
        percentage = userLevelFile['Experience']/expCap*20
        bar = "["
        for i in range(min(int(percentage), 20)): bar += "\u2588"
        for i in range(20-int(percentage)): bar += "\u2500"
        bar += "]"
        try:
            guildLevelFile = GuilddataGetFile(ctx.guild, "levels.json")[str(userProfile["ID"])]
            gExpCap = 20+(guildLevelFile['Level']**2*20)
            gPercentage = guildLevelFile['Experience']/gExpCap*20
            gBar = "["
            for i in range(min(int(gPercentage), 20)): gBar += "\u2588"
            for i in range(20-int(gPercentage)): gBar += "\u2500"
            gBar += "]"
        except Exception: # player may not exist here
            pass
        embed = discord.Embed(title=f"**{userProfile['Name']}** *({userProfile['ID']})*", color=rectColor(PlayerdataGetFileIndex(user, "settings.json", "Color")))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name=f"Global - Level {userLevelFile['Level']}\n{bar}",
                        value=f"{userLevelFile['Experience']}/{expCap} Exp to Lv{userLevelFile['Level']+1} ({userLevelFile['Experience']/expCap*100:.1f}%)", inline=False)
        try:
            embed.add_field(name=f"{ctx.guild.name} - Level {guildLevelFile['Level']}\n{gBar}",
                        value=f"{guildLevelFile['Experience']}/{gExpCap} Exp to Lv{guildLevelFile['Level']+1} ({guildLevelFile['Experience']/gExpCap*100:.1f}%)", inline=False)
        except Exception: # player may not exist here
            pass
        embed.add_field(name=f"Wallet", value=f"{userWalletFile['Aurus']}GP {userWalletFile['Args']}SP {userWalletFile['Kups']}CP", inline=False)
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send("The requested user does not have a profile set up yet, or does not exist. Or something's broken.")

@commands.command(aliases=['stats'])
async def statistics(ctx, *userIn):
    """View some recorded metrics!"""
    user = ctx.author
    if len(userIn) == 1:
        converter = commands.MemberConverter()
        user = await converter.convert(ctx, userIn[0])
    try:
        ts = datetime.timestamp(datetime.now())
        userStats = PlayerdataGetFile(user, "stats.json")
        userProfile = PlayerdataGetFile(user, "profile.json")
        userLevel = PlayerdataGetFile(user, "level.json")
        embed = discord.Embed(title=f"{userProfile['Name']}'s Statistics", color=rectColor(PlayerdataGetFileIndex(user, "settings.json", "Color")))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name=f"Stats", value=f"\
Global Messages Sent:\n\
Average Msgs/dy (60d):\n\
Average Msgs/dy (all time):\n\
Account Creation:\n\
Dailys Claimed:\n\
Personal Counting Done:\n\
Global Experience Gained:")
        embed.add_field(name=f"Values", value=f"\
{userStats['Messages Sent']}\n\
{get60DayActivity(userStats):.3f}\n\
{getActivity(userStats):.3f}\n\
{getAcctAgeYMDAsStr(userStats)} ago\n\
{userStats['Dailys Claimed']}\n\
{expol(userStats['Counting Done']):{GetNotationCode(ctx.author)}}\n\
{expol(levelToExp(userLevel['Level'])+userLevel['Experience']):{GetNotationCode(ctx.author)}}")
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send("The requested user does not have a profile set up yet, or does not exist. Or something's broken.")

@commands.command(aliases=['set', 'setting'])
async def settings(ctx, setting="", newValue=None):
    """Change how Zako interacts with you!
Booleans (that is, settings with true/false values) can be toggled without a newValue set

Color can be named using the table of color names below, or darkBaseColor/lightBaseColor
Color can be defined as three numbers in the format RRR,GGG,BBB, where RGB is decimal
Color can be defined as three numbers in the format 0xxRR,0xGG,0xBB, where RGB is hexadecimal

Base colors (Max sat, min lum):
  gray/grey, red, vermillion, orange, amber, yellow, chartreuse, green, cyan, cornflower, blue, violet, purple, magenta
  black, white (these base colors don't have dark or light variants, for what i hope to be obvious reasons)

All accepted color names (not including darkBaseColor/lightBaseColor if another name exists, eg. lightRed is accepted):
  black, darkGray/darkGrey, gray/grey, silver, white
  maroon, red, pink
  brick/copper, vermillion, peach
  brown, orange, lightOrange
  brass, amber, lightAmber
  gold, yellow, lemon
  swamp, chartreuse, avocado
  forest, green, lime
  teal, cyan, sky
  darkCornflower, cornflower, lightCornflower
  navy, blue, slate
  midnight, indigo, lightIndigo
  plum, purple, lavender
  eggplant, magenta, rose"""
    userSettings = PlayerdataGetFile(ctx.author, "settings.json")
    if setting == "":
        out = ""
        for setn in list(userSettings.keys()):
            out += setn.ljust(10) + " = " + str(userSettings[setn]) + "\n"
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"**{ctx.author.name}'s Settings**", value=out)
        await ctx.send(embed=embed)
    else:
        if setting not in userSettings: await ctx.send("Setting doesn't exist. Do z/settings to get a list of settings.")
        if type(userSettings[setting]) is bool:
            if newValue == None: userSettings[setting] = not userSettings[setting]
            else: userSettings[setting] = bool(newValue)
            await ctx.send("Updated. :thumbsup:")
        else:
            if newValue == None: await ctx.send("Please redo this command with a new value for this."); return
            if setting == "Color":
                try: newValue = rectColor(newValue)
                except Exception: await ctx.send(f"'{newValue}' isn't a valid color."); return
            try:
                newValue = type(userSettings[setting])(newValue)
            except Exception as e: await ctx.send(e); return
            userSettings[setting] = newValue
            await ctx.send("Updated. :thumbsup:")
        PlayerdataSetFile(ctx.author, "settings.json", userSettings)

@commands.command(aliases=['top', 'leader', 'lb', 'rank', 'ranks'])
async def leaderboard(ctx, *, args=""):
    """See how you rank!
Global compares with all Zako users.
Boards:
  level         - Ranks people by level. Local/global, user only.
  value         - Ranks people by net worth. Local/global, user only.
  activity      - Ranks by avg messages per day. Local/global, user/server.
  msgs/messages - Ranks by messages sent. Local/global, user/server.
  count         - Ranks by amount added to count. Local/global, user/server.
  members       - Ranks by number of total members. Global only, server only.
  users         - Ranks by number of users. Global only, server only.
  user%         - Ranks by percentage of users to total members. Global only, server only.

Scopes:
  local         - Stats in this server.
  global        - Global stats.

Sources:
  user          - User stats.
  server/guild  - Server stats."""
    
    board = ""
    globalboard = False
    source = ""
    args = str.lower(args)

    # Check arguments and set them based on context
    if "level" in args: board = "level"
    elif "value" in args: board = "value"
    elif "activity" in args: board = "activity"
    elif "msgs" in args: board = "msgs"
    elif "messages" in args: board = "msgs"
    elif "count" in args: board = "count"
    elif "members" in args: board = "members"
    elif "users" in args: board = "users"
    elif "user%" in args: board = "user%"
    else:
        if "guild" in args: board = "members"
        elif "server" in args: board = "members"
        else: board = "level"
    
    if "local" in args: globalboard = False
    elif "global" in args: globalboard = True
    else:
        if board in ["members", "users", "user%"]: globalboard = True
        elif "guild" in args: globalboard = True
        elif "server" in args: globalboard = True
        else: globalboard = False
    
    if "user" in args and "users" not in args: source = "player"
    elif "user" in args and "users" in args: source = "guild"
    elif "guild" in args: source = "guild"
    elif "server" in args: source = "guild"
    else: source = "player"

    #Block incorrect argument combinations
    if [board, source] in [["level", "guild"], ["value", "guild"], ["members", "player"],
                           ["users", "player"], ["user%", "player"]]:
        await ctx.send("Error: Source does not have that board!"); return
    if [board, globalboard] in [["members", False], ["users", False], ["user%", False]]:
        await ctx.send("Error: Board cannot be viewed in this scope!"); return
    guild = ctx.message.guild
    leaderboard = {}
    memberPool = []

    if source == "player":
        guildMembers = []
        botMembers = []

        #populate guild members
        async for member in guild.fetch_members():
            guildMembers.append(member.id)

        #populate bot members
        for root, dirs, files in walk("playerdata"):
            if root == "playerdata": continue
            botMembers.append(root.replace("playerdata\\",''))

        #find all IDs in both guild and bot, if not global
        if not globalboard:
            memberPool = [str(ID) for ID in guildMembers if str(ID) in botMembers]
        else:
            memberPool = botMembers
    if source == "guild":
        #populate guilds
        for root, dirs, files in walk("guilddata"):
            if root == "guilddata": continue
            if "\\data" in root or "\\scripts" in root: continue
            memberPool.append(root.replace("guilddata\\",''))
    
    #get data for leaderboard
    for member in memberPool:
        path = f".\\{source}data\\{member}\\"
        try:
            if board == 'level':
                if not GuilddataGetFileIndex(ctx.guild, "settings.json", "GlobalLevel") and not globalboard:
                    LvData = loadJSON("levels.json", f".\\guilddata\\{ctx.guild.id}\\")[member]
                else:
                    LvData = loadJSON("level.json", path)
                value = [LvData["Level"],LvData["Experience"]]
            elif board == 'value':
                WalletData = loadJSON("wallet.json", path)
                value = [GSCToInt(WalletData["BankAurus"]+WalletData["Aurus"],
                                 WalletData["BankArgs"]+WalletData["Args"],
                                 WalletData["BankKups"]+WalletData["Kups"])]
            elif board in ["activity", "msgs", "count", "members", "users", "user%"]:
                StatData = loadJSON("stats.json", path)
                ts = datetime.timestamp(datetime.now())
                if board == "activity":
                    value = [getActivity(StatData)]
                    if source == "guild":
                        converter = commands.GuildConverter()
                        guildCTX = await converter.convert(ctx, str(loadJSON("profile.json", path)["ID"]))
                        value.append(getActivityRating(guildCTX))
                if board == "msgs": value = [StatData['Messages Sent']]
                if board == "count": value = [f"{expol(StatData['Counting Done']):{GetNotationCode(ctx.author)}}"]
                if board == "members": value = [StatData['Members']]
                if board == "users": value = [StatData['Users']]
                if board == "user%": value = [StatData['Users']/StatData['Members']*100]
            else:
                await ctx.send("Invalid board."); return
            leaderboard[loadJSON("profile.json", path)["Name"]] = value
        except (TypeError, KeyError) as e:
            #data returned None => TypeError: 'NoneType' object is not subscriptable
            #data not updated => KeyError: variable
            continue
    
    #sort list
    marklist=list(leaderboard.items())
    def sortKey(key):
        return key[1]
    marklist.sort(key=sortKey, reverse=True)
    leaderboard=dict(marklist)

    indexList = ""
    valueList = ""
    index = 1
    foundAuthor = False
    auth = ""
    if source == "player": auth = ctx.author.name
    if source == "guild": auth = ctx.guild.name
    for x in list(leaderboard)[0:20]:
        indexList += f"#{index}: {x}\n"
        if board == "level":
            valueList += f"Lv{leaderboard[x][0]}, {leaderboard[x][1]}Exp\n"
        elif board == "value":
            gold, silver, copper = IntToGSC(leaderboard[x][0])
            valueList += f"{gold}GP {silver}SP {copper}CP\n"
        elif board in ["user%", "activity"]:
            if source == "guild": valueList += f"{leaderboard[x][0]:.3f} ({leaderboard[x][1]})\n"
            else: valueList += f"{leaderboard[x][0]:.3f}\n"
        elif board in ["msgs", "members", "users", "count"]:
            valueList += f"{leaderboard[x][0]}\n"
        if x == auth: foundAuthor = True
        index += 1
    index = 1
    authorRank = ""
    if not foundAuthor: #the person or guild who asked is not in the top 20, so find them
        for x in list(leaderboard):
            if x == auth:
                if board == "level":
                    authorRank += f"#{index}: {x} - Lv{leaderboard[x][0]}, {leaderboard[x][1]}Exp"
                elif board == "value":
                    gold, silver, copper = IntToGSC(leaderboard[x][0])
                    authorRank += f"#{index}: {x} - {gold}GP {silver}SP {copper}CP"
                elif board in ["user%", "activity"]:
                    authorRank += f"#{index}: {x} - {leaderboard[x][0]:.3f}"
                elif board in ["msgs", "members", "users", "count"]:
                    authorRank += f"#{index}: {x} - {leaderboard[x][0]}"
                foundAuthor = True
                break
            index += 1
        if not foundAuthor: #the person or guild who asked isn't on this leaderboard
            authorRank += f"Unlisted - Not on {board} leaderboard"
            
    if indexList == "" or valueList == "": string = "Couldn't find any profiles. If you believe this is in error, report it using z/file."
    embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
    title = "Leaderboard"
    if globalboard: title = "**Global Leaderboard**"
    else: title = f"**{guild.name}'s Leaderboard**"
    embed.add_field(name=title, value=indexList[0:-1])
    embed.add_field(name=f"**{board.title()}**", value=valueList[0:-1])
    if authorRank != "":
        if source == "player": embed.add_field(name=f"**Your Rank - {board.title()}**", value=authorRank, inline=False)
        if source == "guild": embed.add_field(name=f"**{auth}'s Rank - {board.title()}**", value=authorRank, inline=False)
    await ctx.send(embed=embed)
