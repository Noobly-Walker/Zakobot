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

def preloadFile(path, guild, file, defaults, skipCheck=False):
    if not exists(f"{path}{file}.json"): data = {}
    else: data = GuilddataGetFile(guild, f"{file}.json")
    for i in defaults:
        data.setdefault(i, defaults[i])
    if not skipCheck and type(data) is dict:
        for key in list(data.keys()): #clean up my blunders
            if key in defaults.keys(): pass
            else: del data[key]
    GuilddataSetFile(guild, f"{file}.json", data)
    return data

def preloadGuilddata(guild):
    path = f".\\guilddata\\{guild.id}\\"
    pathfind(path)
    pathfind(path + "scripts\\")
    pathfind(path + "data\\")
    ts = datetime.timestamp(datetime.now())
    memberParse = realUsers(guild)

    defaultsProfile = {
        "Name": guild.name,
        "ID": guild.id
        }
    defaultsSettings = {
        "Levels": True,
        "LvUpReacts": True,
        "Counting": True,
        "PublicScripts": False,
        "GlobalLevel": False,
        "SomeonePing": False,
        "CharacterLimit": 4000,
        "GetUpdates": False,
        "Prefix": local["prefix"],
        "AnnounceBirthdays": False,
        "NewUserRoleID": "None"
        }
    defaultsStats = {
        "Messages Sent": 0,
        "Counting Done": [0.0, 0],
        "Acct Creation": ts,
        "Members": memberParse[0],
        "Users": memberParse[1],
        "Bots": memberParse[2],
        "Last Update": 0,
        "Activity Board": []
        }
    defaultsAdmin = {
        "Update Channel": None,
        "Admin Channel": None,
        "Censored Users": [],
        "Image Blocked Channels": [],
        "Link Blocked Channels": [],
        "Emoji Blocked Channels": [],
        "Zako Ignored Channels": []
        }

    preloadFile(path, guild, "profile", defaultsProfile)
    preloadFile(path, guild, "settings", defaultsSettings)
    preloadFile(path, guild, "curses", [], True)
    preloadFile(path, guild, "levels", {}, True)
    preloadFile(path, guild, "scripts\\onMessageIs", {}, True)
    preloadFile(path, guild, "scripts\\onMessageHas", {}, True)
    preloadFile(path, guild, "scripts\\onMemberJoin", {}, True)
    preloadFile(path, guild, "scripts\\onMemberLeave", {}, True)
    preloadFile(path, guild, "scripts\\function", {}, True)
    dataStats = preloadFile(path, guild, "stats", defaultsStats)
    preloadFile(path, guild, "admin", defaultsAdmin)

    if len(dataStats["Activity Board"]) == 0:
        try:
            average = int(getActivity(dataStats)//1)
            for i in range(getAcctAge(dataStats)):
                dataStats["Activity Board"].append(average)
            dataStats["Last Update"] = getAcctAge(dataStats)
        except ZeroDivisionError:
            dataStats["Activity Board"].append(0)
    GuilddataSetFile(guild, "stats.json", dataStats)

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
