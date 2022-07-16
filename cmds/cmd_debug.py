import asyncio
import discord
from discord.ext import commands
from os.path import isdir,exists
from os import walk
import traceback
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.SLHandle import *
from util.expol import expol
from util.UsernameToUUID import UsernameToUUID
from util.PlayerDataHandler import *
from util.DataHandlerUtil import *
from util.cmdutil import cmdutil
text = cmdutil()

def _cmdl_():
    return ["source", "zblacklist", "zwhitelist", "linkacct", "resetval",
            "midvillaswhitelist", "lvtoexp", "reloadall", "raiseerror"]

def _catdesc_():
    return "Debug commands."

developers = ["248641004993773569", #Noobly
              "200697539467542528", #Zecca
              "205011703891623936", #Tsumiki
              "614768116009795585"] #Wenlock

midvillasStaff = ["248641004993773569", #Noobly
                  "377295541916401664", #Texas
                  "717575616177766420", #Spoon
                  "282831627397365760"] #Kaiser

@commands.command()
async def dbgArbExec(ctx, *, code):
    """Debug Command: Enables arbitrary execution of code."""
    out = ""
    if str(ctx.author.id) == '248641004993773569':
        try: exec(code)
        except Exception: out = traceback.format_exc().splitlines()[-1]
        if out not in [None, ""]: await ctx.send(str(out))
    else: await ctx.send('You do not have permission to perform this action.')

@commands.command()
async def zblacklist(ctx, userid):
    """Dev Command: Bans someone from using Zako."""
    if str(ctx.author.id) not in developers:
        await ctx.send('You do not have permission to perform this action.'); return
    if not exists(f".\\data\\zakoBlacklist.json"):
        blacklist = []
        text.warn("File .\\data\\zakoBlacklist.json not found.")
    else: blacklist = loadJSON("zakoBlacklist.json", "data")
    blacklist.append(int(userid))
    saveJSON(blacklist, "zakoBlacklist.json", "data")
    await ctx.send(f"Blacklisted {userid}. :thumbsup:")

@commands.command()
async def zwhitelist(ctx, userid):
    """Dev Command: Unbans someone from using Zako."""
    if str(ctx.author.id) not in developers:
        await ctx.send('You do not have permission to perform this action.'); return
    if not exists(f".\\data\\zakoBlacklist.json"):
        blacklist = []
        text.warn("File .\\data\\zakoBlacklist.json not found.")
    else: blacklist = loadJSON("zakoBlacklist.json", "data")
    blacklist.remove(int(userid))
    saveJSON(blacklist, "zakoBlacklist.json", "data")
    await ctx.send(f"Whitelisted {userid}. :thumbsup:")

@commands.command()
async def linkacct(ctx, main, alt):
    """Dev Command: Links alt accounts."""
    if str(ctx.author.id) not in developers:
        await ctx.send('You do not have permission to perform this action.'); return
    if not exists(f".\\data\\playerAltDB.json"):
        alts = {}
        text.warn("File .\\data\\playerAltDB.json not found.")
    else: alts = loadJSON("playerAltDB.json", "data")
    alts[alt] = main
    saveJSON(alts, "playerAltDB.json", "data")
    await ctx.send(f"Linked {alt} to {main}. :thumbsup:")

@commands.command()
async def lvtoexp(ctx, level):
    """Debug Command: Converts an arbitrary level to experience. You DO have permission to perform this action."""
    await ctx.send(levelToExp(int(level)))

class fakeuser:
    def __init__(self, ID):
        text.log(f"Spoofing {ID}!")
        self.ID = ID
        self.Name = "?????"

    @property
    def id(self):
        return self.ID

    @property
    def name(self):
        return self.Name

@commands.command()
async def reloadall(ctx):
    """Dev Command: Reloads all userdata files, to update variables."""
    if str(ctx.author.id) not in developers:
        await ctx.send('You do not have permission to perform this action.'); return
    botMembers = []
    for root, dirs, files in walk("playerdata"):
        if root == "playerdata": continue
        botMembers.append(root.replace("playerdata\\",''))
    for member in botMembers:
        fake = fakeuser(int(member))
        preloadPlayerdata(fake)

@commands.command()
async def resetval(ctx, table, value):
    """Dev Command: Wipes a variable in all userdata files."""
    if str(ctx.author.id) not in developers:
        await ctx.send('You do not have permission to perform this action.'); return
    affected = 0
    for root, dirs, files in walk("playerdata"):
        if root == "playerdata": continue
        memberID = root.replace("playerdata\\",'')
        path = f".\\playerdata\\{memberID}\\"
        if not exists(f"{path}{table}.json"): continue
        file = loadJSON(f"{table}.json", path)
        if value not in list(file.keys()): continue
        del file[value]
        saveJSON(file, f"{table}.json", path)
        affected += 1
    await ctx.send(f"Reset {value} in {table} in {affected} players.")

@commands.command()
async def raiseerror(ctx, *, errortext):
    """Dev Command: Raises a python exception."""
    if str(ctx.author.id) not in developers:
        await ctx.send('You do not have permission to perform this action.'); return
    raise Exception(errortext)

@commands.command(aliases=["mvwl", "mvwhitelist"])
async def midvillaswhitelist(ctx, mcUsername, discordID):
    """MidVillas Staff Command: Whitelists users to both MidVillas servers, and links their Minecraft accounts to Zako."""
    if str(ctx.author.id) not in midvillasStaff:
        await ctx.send('You do not have permission to perform this action.'); return
        
    #get player uuid
    converter = UsernameToUUID(mcUsername)
    uuid = converter.get_uuid()
    if uuid is None: await ctx.send("No UUID was returned."); return
    mcPlayer = {"uuid": uuid, "name": mcUsername}

    #whitelist to alpha
    whitelistA = loadJSON("whitelist.json", "E:\\Mid Villas Server Old")
    whitelistA.append(mcPlayer)
    saveJSON(whitelistA, "whitelist.json", "E:\\Mid Villas Server")
    await ctx.send(f"Whitelisted {mcUsername} with UUID {uuid} to Mid Villas Alpha!")

    #whitelist to beta
    whitelistB = loadJSON("whitelist.json", "E:\\Mid Villas Server")
    whitelistB.append(mcPlayer)
    saveJSON(whitelistB, "whitelist.json", "E:\\Mid Villas Server")
    await ctx.send(f"Whitelisted {mcUsername} with UUID {uuid} to Mid Villas Beta!")

    #link accounts
    if not exists(f".\\data\\mcUserConvert.json"):
        mcUserDict = {}
        text.warn("File .\\data\\mcUserConvert.json not found.")
    else: mcUserDict = loadJSON("mcUserConvert.json", "data")
    mcUserDict[mcUsername] = discordID
    saveJSON(mcUserDict, "mcUserConvert.json", "data")
    await ctx.send("Linked minecraft account! :thumbsup:")

@commands.command() #I hope you guys found this tool useful.
async def source(ctx, filepath="zakobot.py"):
    """Returns chunks of Zako's source code.
Pathing:
    zakobot.py
    cmds\\
        cmd_admin.py
        cmd_core.py
        cmd_debug.py
        cmd_econ.py
        cmd_files.py
        cmd_fun.py
        cmd_gamble.py
        cmd_profile.py
        cmd_random.py
        cmd_tools.py
    util\\
        BackupManager.py
        ColorUtil.py
        DataHandlerUtil.py
        expol.py
        GuildDataHandler.py
        InventoryHandler.py
        PlayerDataHandler.py
        PotionRandomizer.py
        SLHandle.py
        TextFormat.py
        TimeUtil.py
        UsernameToUUID.py
        """
    if str(ctx.author.id) not in developers:
        await ctx.send('You do not have permission to perform this action.'); return
    if filepath != "zakobot.py":
        if "cmds\\" not in filepath and "util\\" not in filepath or "__pycache__" in filepath:
            await ctx.send("Access permission denied."); return
    file = None
    try:
        file = load(filepath).splitlines()
    except (FileNotFoundError, AttributeError) as e:
        await ctx.send("File not found.")
        text.warn(e)
        return
    sourcecode = "```py\n"
    for line in file:
        if len(sourcecode)+len(line.replace("```", "`\``") + "\n") <= 1900:
            sourcecode += line.replace("```", "`\``") + "\n"
        else:
            sourcecode += "```"
            await ctx.send(sourcecode)
            sourcecode = "```py\n" + line.replace("```", "`\``") + "\n"
    sourcecode += "```"
    await ctx.send(sourcecode)
