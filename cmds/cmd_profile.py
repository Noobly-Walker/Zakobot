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
from util.CardUtil import *
text = cmdutil()
local = loadJSON('.\\locals\\locals.json')
PATH = load(".\\locals\\%PATH%")

def commandList():
    return [profile, leaderboard, settings, statistics, backpack]

def categoryDescription():
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

@commands.command(aliases=['inventory', 'inv', 'bp'])
async def backpack(ctx, category=None, *args):
    """View your belongings!

backpack cards page|view (number)"""
    pack = PlayerdataGetFile(ctx.author, "backpack.json")
    if category == None:
        cats = []
        for cat in pack.keys():
            cats.append(cat)
        await ctx.send("Available Categories:\n> " + "\n> ".join(cats))
    if category == "cards":
        deck = pack["cards"]
        num = None
        if len(args) == 0:
            mode = "page"; num = 1
        elif args[0] in ["page", "view"]:
            if len(args) == 1: mode = args[0]; num = 1
            else: mode = args[0]; num = int(args[1])
        else:
            await ctx.send("Invalid arguments."); return
            
        if mode == "page":
            maximumCards = 25
            def sortInt(key):
                return int(key)
            keys = list(deck.keys())
            keys.sort(key=sortInt)
            cards = []
            for i in keys[ maximumCards*(num-1) : (maximumCards*num) ]:
                card = deck[i]
                if card[2] > 0: cards.append(["cardbase-shiny", card[0], int(i)])
                else: cards.append(["cardbase", card[0], int(i)])
            if len(cards) == 0:
                await ctx.send("You don't have any cards to show on this page.")
            else:
                getPack(cards)
                await ctx.send(f"Your cards (pg{num}):", file=discord.File(".\\temp\\pack.png"))
                
        elif mode == "view":
            if num == None: await ctx.send(f"Which card do you want to look at? {local['prefix']}backpack cards view (card ID)"); return
            if str(num) not in deck: await ctx.send("You don't have that card."); return
            
            card = deck[str(num)]
            if card[2] > 0: getCard(["cardbase-shiny", card[0], num])
            else: getCard(["cardbase", card[0], num])
            await ctx.send(f"You have {card[1]+card[2]} card(s), {card[2]} of them are foil.", file=discord.File(".\\temp\\card.png"))
            

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
        userMultis = PlayerdataGetFile(user, "multis.json")
        userGuildLevel = GuilddataGetFile(ctx.guild, "levels.json")[str(user.id)]["Level"]
        globalCount = expol(load(f"{PATH}\\counting.txt"))
        embed = discord.Embed(title=f"{userProfile['Name']}'s Statistics", color=rectColor(PlayerdataGetFileIndex(user, "settings.json", "Color")))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name=f"Stats", value=f"\
Global Messages Sent:\n\
Average Msgs/dy (60d):\n\
Average Msgs/dy (all time):\n\
Account Creation:\n\
Dailys Claimed:\n\
Personal Counting Done:\n\
Global Experience Gained:\n\
Global Counting Multiplier:\n\
Guild Counting Multiplier:")
        embed.add_field(name=f"Values", value=f"\
{userStats['Messages Sent']}\n\
{get60DayActivity(userStats):.3f}\n\
{getActivity(userStats):.3f}\n\
{getAcctAgeYMDAsStr(userStats)} ago\n\
{userStats['Dailys Claimed']}\n\
{expol(userStats['Counting Done']):{GetNotationCode(ctx.author)}}\n\
{expol(levelToExp(userLevel['Level'])+userLevel['Experience']):{GetNotationCode(ctx.author)}}\n\
{expol(2)**expol(globalCount.exponent)*(1+(userLevel['Level']/4))*(expol(userMultis['ShopCountingMulti']).log10()+1):{GetNotationCode(ctx.author)}}\n\
{expol(2)**expol(globalCount.exponent)*(1+(userGuildLevel/4))*(expol(userMultis['ShopCountingMulti']).log10()+1):{GetNotationCode(ctx.author)}}")
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send("The requested user does not have a profile set up yet, or does not exist. Or something's broken.")

@commands.command(aliases=['set', 'setting'])
async def settings(ctx, setting="", newValue=None):
    """Change how Zako interacts with you!
Booleans (that is, settings with true/false values) can be toggled without a newValue set

Color can be defined as three numbers in the format RRR,GGG,BBB, where RGB is decimal
Color can be defined as three numbers in the format 0xxRR,0xGG,0xBB, where RGB is hexadecimal
Color can also be named using the table found using this command.
  z!file read colors

Notation can be defined using the table found using this command.
  z!file read notations"""
    userSettings = PlayerdataGetFile(ctx.author, "settings.json")
    if setting == "":
        out = ""
        for setn in list(userSettings.keys()):
            out += setn.ljust(10) + " = " + str(userSettings[setn]) + "\n"
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"**{ctx.author.name}'s Settings**", value=out)
        await ctx.send(embed=embed)
    else:
        if setting not in userSettings: await ctx.send(f"Setting doesn't exist. Do {local['prefix']}settings to get a list of settings.")
        if type(userSettings[setting]) is bool:
            if newValue == None: userSettings[setting] = not userSettings[setting]
            else:
                if str.lower(newValue) in ["yes", "on", "1", "true"]: newValue = True
                elif str.lower(newValue) in ["no", "off", "0", "false"]: newValue = False
                else: await ctx.send("Invalid boolean input."); return
                userSettings[setting] = newValue
            await ctx.send("Updated. :thumbsup:")
        else:
            if setting == "Notation" and newValue == None:
                await ctx.send("Notation can be defined using the table found using this command.\n  z!file read notations")
                return
            if newValue == None: await ctx.send("Please redo this command with a new value for this."); return
            if setting == "Color":
                try: test = rectColor(newValue)
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
  activity      - Ranks by avg messages per day. Global only, user/server.
  msgs/messages - Ranks by messages sent. Global only, user/server.
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
    guild = ctx.message.guild

    # Check arguments and set them based on context
    if "level" in args: board = "level"
    elif "value" in args: board = "value"
    elif "activity" in args: board = "activity"
    elif any(x in args for x in ["msgs", "messages"]): board = "msgs"
    elif "count" in args: board = "count"
    elif "members" in args: board = "members"
    elif "users" in args: board = "users"
    elif "user%" in args: board = "user%"
    else:
        if any(x in args for x in ["guild", "server"]): board = "members"
        else: board = "level"
    
    if "local" in args: globalboard = False
    elif "global" in args: globalboard = True
    else:
        if board in ["members", "users", "user%", "msgs", "activity"]: globalboard = True
        elif board == "level": globalboard = GuilddataGetFileIndex(ctx.guild, "settings.json", "GlobalLevel")
        elif "guild" in args or "server" in args: globalboard = True
        elif "server" in args: globalboard = True
        else: globalboard = False
    
    if "user" in args and not any(x in args for x in ["users", "user%"]): source = "player"
    elif any(x in args for x in ["users", "user%", "guild", "server"]): source = "guild"
    else: source = "player"
    #Block incorrect argument combinations
    if [globalboard, source] == [False, "guild"]:
        await ctx.send("Error: Guilds can only be ranked with global scope!"); return
    if [board, source] in [["level", "guild"], ["value", "guild"], ["members", "player"],
                           ["users", "player"], ["user%", "player"]]:
        await ctx.send("Error: Source does not have that board!"); return
    if [board, globalboard] in [["members", False], ["users", False], ["user%", False],
                                ["msgs", False], ["activity", False]]:
        await ctx.send("Error: Board cannot be viewed in this scope!"); return
        
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
                if not globalboard:
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
                if board == "count": value = [expol(StatData['Counting Done'])]
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
    print(leaderboard)
    for x in list(leaderboard)[0:20]:
        print(x)
        indexList += f"#{index}: {x}\n"
        if board == "level":
            valueList += f"Lv{leaderboard[x][0]}, {leaderboard[x][1]}Exp\n"
        elif board == "value":
            gold, silver, copper = IntToGSC(leaderboard[x][0])
            valueList += f"{gold}GP {silver}SP {copper}CP\n"
        elif board == "activity":
            if source == "guild": valueList += f"{leaderboard[x][0]:.3f} ({leaderboard[x][1]})\n"
            else: valueList += f"{leaderboard[x][0]:.3f}\n"
        elif board == "user%":
            valueList += f"{leaderboard[x][0]:.3f}\n"
        elif board == "count":
            valueList += f"{leaderboard[x][0]:{GetNotationCode(ctx.author)}}\n"
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
            
    if indexList == "" or valueList == "": string = f"Couldn't find any profiles. If you believe this is in error, report it using {local['prefix']}file."
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
