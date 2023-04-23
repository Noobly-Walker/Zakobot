from os.path import splitext
from sqlite3 import connect as sqlConnect
from datetime import datetime
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import *
from util.SLHandle import *
from util.DataHandlerUtil import *
from util.cmdutil import cmdutil
text = cmdutil()
local = loadJSON('.\\locals\\locals.json')

def preloadGuilddata(guild):
    path = f".\\guilddata\\{guild.id}\\"
    pathfind(path)
    pathfind(path + "scripts\\")
    pathfind(path + "data\\")

    if not exists(f"{path}profile.json"): dataProfile = {}
    else: dataProfile = GuilddataGetFile(guild, "profile.json")
    dataProfile.setdefault("Name", guild.name)
    dataProfile.setdefault("ID", guild.id)
    for key in list(dataProfile.keys()): #clean up my blunders
        if key in ["Name", "ID"]: pass
        else: del dataProfile[key]
    GuilddataSetFile(guild, "profile.json", dataProfile)

    if not exists(f"{path}settings.json"): dataSettings = {}
    else: dataSettings = GuilddataGetFile(guild, "settings.json")
    dataSettings.setdefault("Levels", True)
    dataSettings.setdefault("LvUpReacts", True)
    dataSettings.setdefault("Counting", True)
    dataSettings.setdefault("PublicScripts", False)
    dataSettings.setdefault("GlobalLevel", False)
    dataSettings.setdefault("SomeonePing", False)
    dataSettings.setdefault("CharacterLimit", 4000)
    dataSettings.setdefault("GetUpdates", False)
    dataSettings.setdefault("Prefix", local["prefix"])
    dataSettings.setdefault("AnnounceBirthdays", False)
    for key in list(dataSettings.keys()): #clean up my blunders
        if key in ["Levels", "LvUpReacts", "Counting", "PublicScripts",
                   "GlobalLevel", "SomeonePing", "CharacterLimit",
                   "GetUpdates", "AnnounceBirthdays", "Prefix"]: pass
        else: del dataSettings[key]
    GuilddataSetFile(guild, "settings.json", dataSettings)
    
    if not exists(f"{path}curses.json"): dataCurses = []
    else: dataCurses = GuilddataGetFile(guild, "curses.json")
    GuilddataSetFile(guild, "curses.json", dataCurses)
    
    if not exists(f"{path}levels.json"): localLevels = {}
    else: localLevels = GuilddataGetFile(guild, "levels.json")
    GuilddataSetFile(guild, "levels.json", localLevels)

    if not exists(f"{path}scripts\\onMessageIs.json"): eventOnMessageIs = {}
    else: eventOnMessageIs = GuilddataGetFile(guild, "scripts\\onMessageIs.json")
    GuilddataSetFile(guild, "scripts\\onMessageIs.json", eventOnMessageIs)

    if not exists(f"{path}scripts\\onMessageHas.json"): eventOnMessageHas = {}
    else: eventOnMessageHas = GuilddataGetFile(guild, "scripts\\onMessageHas.json")
    GuilddataSetFile(guild, "scripts\\onMessageHas.json", eventOnMessageHas)

    if not exists(f"{path}scripts\\onMemberJoin.json"): eventOnMemberJoin = {}
    else: eventOnMemberJoin = GuilddataGetFile(guild, "scripts\\onMemberJoin.json")
    GuilddataSetFile(guild, "scripts\\onMemberJoin.json", eventOnMemberJoin)

    if not exists(f"{path}scripts\\onMemberLeave.json"): eventOnMemberLeave = {}
    else: eventOnMemberLeave = GuilddataGetFile(guild, "scripts\\onMemberLeave.json")
    GuilddataSetFile(guild, "scripts\\onMemberLeave.json", eventOnMemberLeave)

    if not exists(f"{path}scripts\\function.json"): eventFunction = {}
    else: eventFunction = GuilddataGetFile(guild, "scripts\\function.json")
    GuilddataSetFile(guild, "scripts\\function.json", eventFunction)

    if not exists(f"{path}stats.json"): dataStats = {}
    else: dataStats = GuilddataGetFile(guild, "stats.json")
    ts = datetime.timestamp(datetime.now())
    memberParse = realUsers(guild)
    dataStats.setdefault("Messages Sent", 0)
    dataStats.setdefault("Counting Done", [0.0, 0])
    dataStats.setdefault("Acct Creation", ts)
    dataStats.setdefault("Members", memberParse[0])
    dataStats.setdefault("Users", memberParse[1])
    dataStats.setdefault("Bots", memberParse[2])
    dataStats.setdefault("Last Update", 0)
    dataStats.setdefault("Activity Board", [])
    if len(dataStats["Activity Board"]) == 0:
        try:
            average = int(getActivity(dataStats)//1)
            for i in range(getAcctAge(dataStats)):
                dataStats["Activity Board"].append(average)
            dataStats["Last Update"] = getAcctAge(dataStats)
        except ZeroDivisionError:
            dataStats["Activity Board"].append(0)
    for key in list(dataStats.keys()): #clean up my blunders
        if key in ["Messages Sent", "Counting Done", "Acct Creation", "Members",
                   "Users", "Bots", "Activity Board", "Last Update"]: pass
        else: del dataStats[key]
    GuilddataSetFile(guild, "stats.json", dataStats)

    if not exists(f"{path}admin.json"): dataAdmin = {}
    else: dataAdmin = GuilddataGetFile(guild, "admin.json")
    dataAdmin.setdefault("Update Channel", None)
    dataAdmin.setdefault("Admin Channel", None)
    dataAdmin.setdefault("Censored Users", [])
    dataAdmin.setdefault("Image Blocked Channels", [])
    dataAdmin.setdefault("Link Blocked Channels", [])
    dataAdmin.setdefault("Emoji Blocked Channels", [])
    dataAdmin.setdefault("Zako Ignored Channels", [])
    for key in list(dataAdmin.keys()): #clean up my blunders
        if key in ["Update Channel", "Admin Channel", "Censored Users",
                   "Image Blocked Channels", "Link Blocked Channels", 
                   "Emoji Blocked Channels", "Zako Ignored Channels"]: pass
        else: del dataAdmin[key]
    GuilddataSetFile(guild, "admin.json", dataAdmin)

def updateMemberCount(guild):
    dataStats = GuilddataGetFile(guild, "stats.json")
    memberParse = realUsers(guild)
    dataStats["Members"] = memberParse[0]
    dataStats["Users"] = memberParse[1]
    dataStats["Bots"] = memberParse[2]
    GuilddataSetFile(guild, "stats.json", dataStats)
    
def getActivityRating(guild):
    stats = GuilddataGetFile(guild, "stats.json")
    activity = get60DayActivity(stats) / stats["Users"]
    out = ""
    limit = 100
    if activity < limit*0.01: out += "F"
    elif limit*0.02 <= activity < limit*0.05: out += "D-"
    elif limit*0.05 <= activity < limit*0.1: out += "D"
    elif limit*0.1 <= activity < limit*0.15: out += "D+"
    elif limit*0.15 <= activity < limit*0.2: out += "C-"
    elif limit*0.2 <= activity < limit*0.3: out += "C"
    elif limit*0.3 <= activity < limit*0.4: out += "C+"
    elif limit*0.4 <= activity < limit*0.5: out += "B-"
    elif limit*0.5 <= activity < limit*0.6: out += "B"
    elif limit*0.6 <= activity < limit*0.7: out += "B+"
    elif limit*0.7 <= activity < limit*0.8: out += "A-"
    elif limit*0.8 <= activity < limit*0.9: out += "A"
    elif limit*0.9 <= activity < limit: out += "A+"
    elif limit <= activity: out += "A++"
    return out

def GuilddataGetFile(guild, filename):
    """File extension must be supplied."""
    path = f".\\guilddata\\{guild.id}\\"
    if splitext(filename)[1] == ".json":
        file = loadJSON(filename, path)
        return file
    elif splitext(filename)[1] == ".txt":
        file = load(filename, path)
        return file

def GuilddataSetFile(guild, filename, data):
    """File extension must be supplied."""
    
    path = f".\\guilddata\\{guild.id}\\"
    if splitext(filename)[1] == ".json":
        saveJSON(data, filename, path)
    elif splitext(filename)[1] == ".txt":
        save(data, filename, path)

def GuilddataGetFileIndex(guild, filename, key):
    """Only to be used on JSON files."""
    path = f".\\guilddata\\{guild.id}\\"
    file = loadJSON(filename, path)
    return file[key]

def GuilddataSetFileIndex(guild, filename, key, value):
    """Only to be used on JSON files."""
    path = f".\\guilddata\\{guild.id}\\"
    file = loadJSON(filename, path)
    if key in file: file[key] = value
    else: raise KeyError("The key you're trying to raise doesn't exist.")
    saveJSON(file, filename, path)

def realUsers(guild):
    botcount = 0
    usercount = guild.member_count
    users = guild.members
    for user in users:
        if user.bot: botcount += 1
    return (usercount, usercount-botcount, botcount)
