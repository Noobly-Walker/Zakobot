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
local = loadJSON('.\\locals\\locals.json')
PATH = load(".\\locals\\%PATH%")

def commandList():
    return [ping, echo, emoji, joined, now, invite, 
            echoformat, changelog, embed, report, webhook]

def categoryDescription():
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

e!emojiname - Replaces with emote.
e[string] - Emojifies part of string.
<t> - Inserts timestamp."""
    await ctx.send(formatText(string))

@commands.command()
async def webhook(ctx):
    """Forces your message to be turned into a webhook!
Accepts formatting!

e!emojiname - Replaces with emote.
e[string] - Emojifies part of string.
<t> - Inserts timestamp."""
    # This command is here so it can be found with z!cmd. It is handled in zakobot.py.
    return

@commands.command()
async def embed(ctx, color, title, *, string):
    """I will turn text into a custom embed!

Separate fields into <1024 character chunks using <field>.
Maximum 1024 characters per field, 6 fields per embed.

Color can be defined as three numbers in the format RRR,GGG,BBB, where RGB is decimal
Color can be defined as three numbers in the format 0xxRR,0xGG,0xBB, where RGB is hexadecimal
Color can also be named using the table found using this command.
  z!file read colors
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
    """Returns a list of all emojis available to Zako.
These emojis can be called the same way that they would be if they were on the server, or if you had nitro.
++:emoji: - Reacts to the replied to message, or the most recent message.
+++:emoji: - Turns the emoji into a sticker."""
    eml = loadJSON("emojis.json", "data")
    out = ""
    for e in list(sorted(eml.keys())):
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
    timestamp = int(ctx.message.created_at.replace(tzinfo=timezone.utc).timestamp())
    dt = datetime.now()
    if dt.month in [11, 12, 1, 2]: DST = False
    else: DST = True
    if dt.month in [5, 6, 7, 8]: DST_South = False
    else: DST_South = True

    def queryTZ(DST:bool, region:str):
        if region == "US":
            if DST: return "Daylight"
            else: return "Standard"
        if region == "EU":
            if DST: return "Summer"
            else: return "Standard"
    
    out = f"**Your Time**: <t:{timestamp}>\n\n\
**Anchorage {queryTZ(DST, 'US')} Time**: {current_time(-9+DST)}\n\n\
**Pacific {queryTZ(DST, 'US')} Time**: {current_time(-8+DST)}\n\n\
**Mountain {queryTZ(DST, 'US')} Time**: {current_time(-7+DST)}\n\n\
**Central {queryTZ(DST, 'US')} Time**: {current_time(-6+DST)}\n\n\
**Eastern {queryTZ(DST, 'US')} Time**: {current_time(-5+DST)}\n\n\
**Atlantic {queryTZ(DST, 'US')} Time**: {current_time(-4+DST)}\n\n\
**Brasília Time**: {current_time(-3)}\n\n\
**Universal Coordinated Time**: {current_time(0)}\n\n\
**British {queryTZ(DST, 'EU')} Time**: {current_time(0+DST)}\n\n\
**Central European {queryTZ(DST, 'EU')} Time**: {current_time(1+DST)}\n\n\
**Eastern European {queryTZ(DST, 'EU')} Time**: {current_time(2+DST)}\n\n\
**Moscow Standard Time**: {current_time(3)}\n\n\
**China Standard Time**: {current_time(8)}\n\n\
**Singapore Time**: {current_time(8)}\n\n\
**Philipines Standard Time**: {current_time(8)}\n\n\
**Korea Standard Time**: {current_time(9)}\n\n\
**Japan Standard Time**: {current_time(9)}\n\n\
**Australia Eastern {queryTZ(DST_South, 'EU')} Time**: {current_time(10+DST_South)}"
    await ctx.send(out)

@commands.command()
async def changelog(ctx, version=""):
    """View changes to Zako's code!
Key:
+ Item added.
- Item removed.
× Item changed.
% Item patched or bugfixed.
‼ Comment
> Item List (for listing multiple aspects of the same change)
# Technical change.
! Unimplemented item."""
    changeFile = loadJSON(f"changelog.txt", PATH)
    versionList = list(changeFile.keys())
    if version == "":
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")), title="Zako Zaun Changelog - Table of Contents")
        embed.add_field(name="Development Stages", value=f"1.0 (2018 Jan 25th ~ 2018 Mar 21st)\n\
2.0 (2019 Dec 14th ~ 2021 Apr 14th)\n\
3.0 (2023 Jan 1st ~ Present)", inline=False)
        embed.add_field(name="Snapshots", value=f"3.0s (2021 May 14th ~ 2022 Dec 31st)\n\
3.1s (2023 Jan 3rd ~ Present)", inline=False)
        await ctx.send(embed=embed)
        
    elif version in ["1.0", "2.0", "3.0s", "3.0", "3.1s"]:
        versionList1 = ""
        versionList2 = ""
        versionList3s = ""
        versionList3 = ""
        versionList3_1s = ""
        for v in versionList:
            if v[:2] == "1.": versionList1 += f"{v}, "
            if v[:2] == "2.": versionList2 += f"{v}, "
            if v[:5] == "3.0_s": versionList3s += f"{v}, "
            elif v[:2] == "3.": versionList3 += f"{v}, "
            if v[:5] == "3.1_s": versionList3_1s += f"{v}, "
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")), title="Zako Zaun Changelog - Table of Contents")
        if version == "1.0": embed.add_field(name=f"1.X Releases (2018 Jan 25th ~ 2018 Mar 21st)", value=versionList1[:-2], inline=False)
        if version == "2.0": embed.add_field(name=f"2.X Releases (2019 Dec 14th ~ 2021 Apr 14th)", value=versionList2[:-2], inline=False)
        if version == "3.0s": embed.add_field(name=f"3.0 Snapshots (2021 May 14th ~ 2022 Dec 30th)", value=versionList3s[:-2], inline=False)
        if version == "3.0": embed.add_field(name=f"3.X Releases (2022 Dec 30th ~ Present)", value=versionList3[:-2], inline=False)
        if version == "3.1s": embed.add_field(name=f"3.1 Snapshots (2023 Jan 3rd ~ Present)", value=versionList3_1s[:-2], inline=False)
        await ctx.send(embed=embed)
    elif version in versionList:
        for i in ["\n".join(changeFile[version].split('\n')[start:start+15]) for start in range(0, len(changeFile[version].split('\n')), 15)]:
            await ctx.send(i)
    else: await ctx.send("Error: Version is either invalid or was never documented. Versions between α1.3.2 and α2.4.0 are undocumented.")

@commands.command()
async def invite(ctx):
    """Invite the bot to your server!"""
    await ctx.send(f"Invite Zako Zaun{local['branch']} to your server!\nhttps://discord.com/oauth2/authorize?client_id={local['id']}&scope=bot&permissions=511")

@commands.command()
async def report(ctx, _type, mode, *, args:str):
    """Request features and report bugs!
Types:
  bug/bugs                           - Something's not working right, or at all.
  request/req/suggest/suggestion/sug - Something should be added or removed (please provide reason).

Modes:
  r/read/v/view/search               - Read report logs.
  s/send/add                         - Send report log.

Args:
  read (ID:int)                      - Returns a given report ID.
  read page (page:int=1)             - Returns a page of reports.
  read (status:str) (page:int=1)     - Returns all reports with that status, 20 at a time.
  send (message:str)                 - Sends a report.

Statuses:
  OPEN                               - Unaddressed bug/feature.
  TRIAGE                             - Bug under investigation.
  UNVERIFIED                         - Bug cannot be found or replicated, but it might exist.
  VERIFIED                           - Bug/feature may be fixed/added.
  INVALID                            - Bug cannot be found or replicated, because it doesn't exist.
  INTENDED                           - Bug isn't bug because it was designed that way on purpose.
  DUPLICATE                          - Bug/feature has been mentioned before.
  WONTDO                             - Bug/feature won't be worked on.
  CLOSED                             - Bug/feature is fixed/added.
"""
    
    _type = str.lower(_type)
    mode = str.lower(mode)
    statuses = ["OPEN", "TRIAGE", "UNVERIFIED", "VERIFIED", "INVALID",
                "INTENDED", "WONTDO", "CLOSED", "DUPLICATE"]
    
    if _type in ["bug", "bugs"]:
        if exists(f"{PATH}\\bugs.json"): reports = loadJSON("bugs.json", PATH)
        else: reports = []
    elif _type in ["request", "req", "suggestion", "suggest", "sug"]:
        if exists(f"{PATH}\\requests.json"): reports = loadJSON(f"requests.json", PATH)
        else: reports = []
    else: await ctx.send(f"Invalid type. Use {local['prefix']}help report for info, then try again."); return
    
    if mode in ["r", "read", "v", "view", "search"]:
        args = args.split()
        if args[0].isdigit():
            await ctx.send(f"\[{int(args[0])}\]\({reports[int(args[0])][0]}\) - {reports[int(args[0])][1]}")
            return
        else:
            filtered = []
            if args[0].upper() in statuses:
                for i in range(len(reports)):
                    if str.upper(args[0]) in i[0]: filtered.append([i, *reports[i]])
            elif args[0].lower() == "page":
                for i in range(len(reports)):
                    filtered.append([i, *reports[i]])
            else: await ctx.send(f"No args provided. Used {local['prefix']}help reports for info, then try again.")
            page = 0
            if len(args) == 2:
                if args[1].isdigit:
                    page = int(args[1])-1
            listFilt = []
            for i in range(0+10*page, 10+10*page):
                try:
                    listFilt.append(f"\[{filtered[i][0]}\]\({filtered[i][1]}\) - {filtered[i][2]}")
                except Exception:
                    break
            if len(listFilt) > 0: await ctx.send("\n".join(listFilt))
            else: await ctx.send("No reports to see.")
    elif mode in ["s", "send", "add"]:
        reports.append(["OPEN", args])
        if _type in ["bug", "bugs"]:
            saveJSON(reports, "bugs.json", PATH)
        elif _type in ["request", "req", "suggestion", "suggest", "sug"]:
            saveJSON(reports, "requests.json", PATH)
        await ctx.send("Sent report. :thumbsup:")
