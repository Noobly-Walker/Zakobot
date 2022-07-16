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
    return ["ping", "echo", "emoji", "joined", "now", "invite", 
            "echoformat", "changelog", "embed", "report"]

def _catdesc_():
    return "Important core commands."

@commands.command()
async def ping(ctx):
    """Kinda like poking me in the shoulder to see if I\'m awake."""
    await ctx.send('Yes? Hello.')

@commands.command()
async def echo(ctx, *, string):
    """I will repeat whatever text is put into this command!"""
    await ctx.send(string)

@commands.command(aliases=["echof"])
async def echoformat(ctx, *, string):
    """I will repeat whatever text is put into this command!
Accepts formatting! Slower.

e!emojiname - Replaces with emote."""
    await ctx.send(formatText(string))

@commands.command()
async def embed(ctx, color, title, *, string):
    """I will turn text into a custom embed!

Separate fields into <1024 character chunks using <field>.
Maximum 1024 characters per field, 6 fields per embed.

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
  eggplant, magenta, rose
"""
    embed = discord.Embed(title=title, color=rectColor(color))
    string = string.split("<field>")
    if len(string) > 6:
        await ctx.send("Error: Only six fields can be embedded."); return
    i = 1        
    for f in string:
        if len(f) > 1024:
            await ctx.send("Error: Field length is more than 24"); return
        embed.add_field(name=f"*{title} - field {i}*", value=f, inline=False)
        i += 1
    await ctx.send(embed=embed)

@commands.command(aliases=['em'])
async def emoji(ctx):
    """Returns a list of all emojis available to Zako."""
    eml = loadJSON("emojis.json", "data")
    out = ""
    for e in list(eml.keys()):
        name = e.replace('_', '\\_')
        if len(out + f"{name} = {eml[e]}, ") > 2000:
            await ctx.send(out)
            out = ""
        out += f"{name} = {eml[e]}, "
    await ctx.send(out[:-2])

@commands.command() # Bot returns the date a given user joined.
async def joined(ctx, member):
    """Returns the date when a user joined this server."""
    memberconverter = commands.MemberConverter()
    userobj = await memberconverter.convert(ctx, member)
    ttime = translate_time(userobj.joined_at)
    datejoined = "UNIX {} {} {}, {}:{}:{}.{}'{} UTC".format(ttime[0], ttime[1], ttime[2], ttime[3], ttime[4], ttime[5], ttime[6], ttime[7])
    out = f'{userobj.name} joined this server on {datejoined}.'
    await ctx.send(out)

@commands.command()
async def now(ctx):
    """Shows the current time anywhere on Earth."""
    DST = True
    DST_South = not DST
    out = f"**Anchorage Daylight Time**: {current_time(-9+DST)}\n\n\
**Pacific Daylight Time**: {current_time(-8+DST)}\n\n\
**Mountain Daylight Time**: {current_time(-7+DST)}\n\n\
**Central Daylight Time**: {current_time(-6+DST)}\n\n\
**Eastern Daylight Time**: {current_time(-5+DST)}\n\n\
**Atlantic Daylight Time**: {current_time(-4+DST)}\n\n\
**Brasília Time**: {current_time(-3)}\n\n\
**Universal Coordinated Time**: {current_time(0)}\n\n\
**British Summer Time**: {current_time(0+DST)}\n\n\
**Central European Summer Time**: {current_time(1+DST)}\n\n\
**Eastern European Summer Time**: {current_time(2+DST)}\n\n\
**Moscow Standard Time**: {current_time(3)}\n\n\
**China Standard Time**: {current_time(8)}\n\n\
**Singapore Time**: {current_time(8)}\n\n\
**Philipines Standard Time**: {current_time(8)}\n\n\
**Korea Standard Time**: {current_time(9)}\n\n\
**Japan Standard Time**: {current_time(9)}\n\n\
**Australia Eastern Standard Time**: {current_time(10+DST_South)}"
    await ctx.send(out)

@commands.command()
async def changelog(ctx, version=""):
    """View changes to Zako's code!"""
    changeFile = loadJSON("changelog.txt", ".\\data\\")
    versionList = list(changeFile.keys())
    if version == "":
        versionList1 = ""
        versionList2 = ""
        versionList3d = ""
        for v in versionList:
            if v[:2] == "1.": versionList1 += f"{v}, "
            if v[:2] == "2.": versionList2 += f"{v}, "
            if v[:4] == "3.0_": versionList3d += f"{v}, "
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")), title="Zako Zaun Changelog - Table of Contents")
        embed.add_field(name=f"1.X Releases (2018 Jan 25th ~ 2018 Mar 21st)", value=versionList1[:-2], inline=False)
        embed.add_field(name=f"2.X Releases (2020 Feb ?? ~ 2021 Apr 14th)", value=versionList2[:-2], inline=False)
        embed.add_field(name=f"3.0 Snapshots (2021 May 14 ~ present)", value=versionList3d[:-2], inline=False)
        await ctx.send(embed=embed)
    elif version in versionList: await ctx.send(changeFile[version])
    else: await ctx.send("Error: Version is either invalid or was never documented. Versions between α1.3.2 and α2.4.0 are undocumented.")

@commands.command(aliases=['inv'])
async def invite(ctx):
    """Invite the bot to your server!"""
    await ctx.send("Invite Zako 3.0 DEV to your server!\nhttps://discord.com/oauth2/authorize?client_id=807593322033971231&scope=bot&permissions=511")

@commands.command()
async def report(ctx, _type, mode, *, args:str):
    """Request features and report bugs!
Types:
  bug                                - Something's not working right, or at all.
  request/req/suggest/suggestion/sug - Something should be added or removed (please provide reason).

Modes:
  r/read/v/view/search               - Read report logs.
  s/send                             - Send report log.

Args:
  read (ID:int)                      - Returns a given report ID.
  read page (page:int=1)             - Returns a page of reports.
  read (status:str) (page:int=1)     - Returns all reports with that status, 20 at a time.
  send (message:str)                 - Sends a report.

Statuses:
  UNVIEWED               - A dev has not viewed the report. Bug or request.
  VIEWED                 - A dev has viewed the report, but has yet to do anything about it. Bug or request.
  WORKING                - A dev is looking into the issue, and trying to fix it. Bug or request.
  
  UNVERIFIED             - A dev has viewed the report, and may be looking into it. Bug only.
  UNREPLICABLE           - A dev has tried and failed to replicate this issue. Bug only.
  INVALID                - A dev has failed to find any issue. Bug only.
  WONTFIX                - A dev has decided that the report won't be fixable, for whatever reason. Bug only.
  FIXED                  - A dev has fixed the issue. Bug only.

  PLANNED                - A dev has viewed the report, and may be looking into it. Request only.
  WONTADD                - A dev has refused to add this feature. Request only.
  ADDED                  - A dev has taken action to add this feature. Request only.
"""
    
    _type = str.lower(_type)
    mode = str.lower(mode)
    statuses = ["UNVIEWED", "UNVERIFIED", "INVALID", "WORKING", "UNREPLICABLE",
                "WONTFIX", "FIXED", "PLANNED", "WONTADD", "ADD", "VIEWED"]
    
    if _type == "bug":
        if exists(".\\data\\bugs.json"): reports = loadJSON("bugs.json", "data")
        else: reports = []
    elif _type in ["request", "req", "suggestion", "suggest", "sug"]:
        if exists(".\\data\\requests.json"): reports = loadJSON("data\\requests.json")
        else: reports = []
    else: await ctx.send("Invalid type. Use z/help report for info, then try again."); return
    
    if mode in ["r", "read", "v", "view", "search"]:
        args = args.split()
        if args[0].isdigit():
            await ctx.send(f"[{int(args[0])}]({reports[int(args[0])][0]}) - {reports[int(args[0])][1]}")
            return
        else:
            filtered = []
            if args[0].upper() in statuses:
                for i in range(len(reports)):
                    if i[0] == str.upper(args[0]): filtered.append([i, *reports[i]])
            elif args[0].lower() == "page":
                for i in range(len(reports)):
                    filtered.append([i, *reports[i]])
            else: await ctx.send("No args provided. Used z/help reports for info, then try again.")
            page = 0
            if len(args) == 2:
                if args[1].isdigit:
                    page = int(args[1])-1
            listFilt = []
            for i in range(0+20*page, 19+20*page):
                try:
                    listFilt.append(f"[{filtered[i][0]}]({filtered[i][1]}) - {filtered[i][2]}")
                except Exception:
                    break
            if len(listFilt) > 0: await ctx.send("\n".join(listFilt))
            else: await ctx.send("No reports to see.")
    elif mode in ["s", "send"]:
        reports.append(["UNVIEWED", args])
        if _type == "bug":
            saveJSON(reports, "bugs.json", "data")
        elif _type in ["request", "req", "suggestion", "suggest", "sug"]:
            saveJSON(reports, "requests.json", "data")
        await ctx.send("Sent report. :thumbsup:")

polls = []

@commands.command()
async def poll(ctx, duration, *, string):
    """Start a poll! Democracy!"""
    embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
    embed.add_field(name="Poll", value=string, inline=False)
    embed.add_field(name="This poll is still running.", value="\u2714 0\n\u274C 0", inline=False)
    botMessage = await ctx.send(embed=embed)
    await botMessage.add_reaction(u"\u2714")
    await botMessage.add_reaction(u"\u274C")
    polls.append([botMessage, duration*4, 0, 0])

@commands.Cog.listener()
async def on_reaction_add(reaction, user):
    text.log("Reaction detected.")
    for message in polls:
        if reaction.message in message:
            if reaction.emoji == u"\u2714": message[2] += 1
            if reaction.emoji == u"\u274C": message[3] += 1
            poll = message[0]
            embed = poll.embeds[0]
            embed.fields[1].value = f"\u2714 {message[2]}\n\u274C {message[3]}"
            await poll.edit(embed = embed)
