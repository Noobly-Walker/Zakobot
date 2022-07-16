from os.path import splitext
from sqlite3 import connect as sqlConnect
from datetime import datetime
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import *
from util.SLHandle import *
from util.DataHandlerUtil import *
from util.cmdutil import cmdutil
text = cmdutil()

def preloadPlayerdata(user):
    path = f".\\playerdata\\{user.id}\\"
    pathfind(path)
    
    if not exists(f"{path}profile.json"): dataProfile = {}
    else: dataProfile = PlayerdataGetFile(user, "profile.json")
    dataProfile.setdefault("Name", user.name)
    dataProfile.setdefault("ID", user.id)
    dataProfile.setdefault("canDaily", True)
    for key in list(dataProfile.keys()): #clean up my blunders
        if key in ["Name", "ID", "canDaily"]: pass
        else: del dataProfile[key]
    PlayerdataSetFile(user, "profile.json", dataProfile)
    
    if not exists(f"{path}level.json"): dataLevel = {}
    else: dataLevel = PlayerdataGetFile(user, "level.json")
    dataLevel.setdefault("Experience", 0)
    dataLevel.setdefault("Level", 0)
    for key in list(dataLevel.keys()): #clean up my blunders
        if key in ["Experience", "Level"]: pass
        else: del dataLevel[key]
    PlayerdataSetFile(user, "level.json", dataLevel)
    
    if not exists(f"{path}timers.json"): dataTimers = {}
    else: dataTimers = PlayerdataGetFile(user, "timers.json")
    ts = datetime.timestamp(datetime.now())
    dataTimers.setdefault("Timestamp", ts)
    dataTimers.setdefault("BankInterest", ts)
    dataTimers.setdefault("Daily", ts)
    dataTimers.setdefault("DayTimer", ts)
    dataTimers.setdefault("EXPTimer", ts)
    for key in list(dataTimers.keys()): #clean up my blunders
        if key in ["Timestamp", "BankInterest", "Daily", "DayTimer",
                   "EXPTimer"]: pass
        else: del dataTimers[key]
    PlayerdataSetFile(user, "timers.json", dataTimers)

    if not exists(f"{path}settings.json"): dataSettings = {}
    else: dataSettings = PlayerdataGetFile(user, "settings.json")
    dataSettings.setdefault("LvUpReacts", True)
    dataSettings.setdefault("Color", "teal")
    dataSettings.setdefault("ExpolNotation", "e")
    dataSettings.setdefault("ExpolRounding", "5")
    for key in list(dataSettings.keys()): #clean up my blunders
        if key in ["LvUpReacts", "Color", "ExpolNotation", "ExpolRounding"]: pass
        else: del dataSettings[key]
    PlayerdataSetFile(user, "settings.json", dataSettings)

    if not exists(f"{path}stats.json"): dataStats = {}
    else: dataStats = PlayerdataGetFile(user, "stats.json")
    ts = datetime.timestamp(datetime.now())
    dataStats.setdefault("Messages Sent", 0)
    dataStats.setdefault("Dailys Claimed", 0)
    dataStats.setdefault("Counting Done", [0.0, 0])
    dataStats.setdefault("Acct Creation", ts)
    dataStats.setdefault("Activity Board", [])
    dataStats.setdefault("Last Update", 0)
    if len(dataStats["Activity Board"]) == 0:
        try:
            average = int(getActivity(dataStats)//1)
            for i in range(getAcctAge(dataStats)):
                dataStats["Activity Board"].append(average)
            dataStats["Last Update"] = getAcctAge(dataStats)
        except ZeroDivisionError:
            dataStats["Activity Board"].append(0)
    for key in list(dataStats.keys()): #clean up my blunders
        if key in ["Messages Sent", "Dailys Claimed", "Counting Done", "Acct Creation",
                   "Activity Board", "Last Update"]: pass
        else: del dataStats[key]
    PlayerdataSetFile(user, "stats.json", dataStats)
    
    if not exists(f"{path}wallet.json"): dataWallet = {}
    else: dataWallet = PlayerdataGetFile(user, "wallet.json")
    dataWallet.setdefault("Kups", 0)
    dataWallet.setdefault("Args", 100)
    dataWallet.setdefault("Aurus", 0)
    dataWallet.setdefault("BankKups", 0)
    dataWallet.setdefault("BankArgs", 0)
    dataWallet.setdefault("BankAurus", 0)
    dataWallet.setdefault("BankLedger", {})
    for key in list(dataWallet.keys()): #clean up my blunders
        if key in ["Kups", "Args", "Aurus", "BankKups", "BankArgs", "BankAurus", "BankLedger"]: pass
        else: del dataWallet[key]
    dataWallet["BankAurus"], dataWallet["BankArgs"], dataWallet["BankKups"] = IntToGSC(GSCToInt(dataWallet["BankAurus"], dataWallet["BankArgs"], dataWallet["BankKups"]))
    PlayerdataSetFile(user, "wallet.json", dataWallet)

def UpdateTimers(user):
    dataTimers = PlayerdataGetFile(user, "timers.json")
    elapses = (dataTimers["Timestamp"] - dataTimers["DayTimer"]) // 86400
    bankElapses = (dataTimers["Timestamp"] - dataTimers["BankInterest"]) // 86400
    if dataTimers["Timestamp"] > dataTimers["BankInterest"]+86400:
        dataWallet = PlayerdataGetFile(user, "wallet.json")
        balance = GSCToInt(dataWallet["BankAurus"], dataWallet["BankArgs"], dataWallet["BankKups"])
        if balance >= 1000000:
            interest = balance * (1 + 0.001/bankElapses)**bankElapses - balance
            dataTimers["BankInterest"] += 86400 * bankElapses
            dataWallet["BankLedger"][dataTimers["BankInterest"]] = ["INT", round(interest/1000,3)]
            dataWallet["BankAurus"], dataWallet["BankArgs"], dataWallet["BankKups"] = IntToGSC(balance + int(interest))
            PlayerdataSetFile(user, "wallet.json", dataWallet)
    if dataTimers["Timestamp"] > dataTimers["Daily"]+86400:
        PlayerdataSetFileIndex(user, "profile.json", "canDaily", True)
        dataTimers["Daily"] = dataTimers["Timestamp"]
    if dataTimers["Timestamp"] > dataTimers["DayTimer"]+86400:
        dataTimers["DayTimer"] += elapses * 86400
    if dataTimers["Timestamp"] > dataTimers["BankInterest"]+86400:
        dataTimers["BankInterest"] += elapses * 86400
    PlayerdataSetFile(user, "timers.json", dataTimers)

def GetNotationCode(user):
    userSettings = PlayerdataGetFile(user, "settings.json")
    code = f"{userSettings['ExpolNotation']}.{userSettings['ExpolRounding']}"
    return code

def PlayerdataGetFile(user, filename):
    """File extension must be supplied."""
    path = f".\\playerdata\\{user.id}\\"
    if splitext(filename)[1] == ".json":
        file = loadJSON(filename, path)
        return file
    elif splitext(filename)[1] == ".txt":
        file = load(filename, path)
        return file

def PlayerdataSetFile(user, filename, data):
    """File extension must be supplied."""
    path = f".\\playerdata\\{user.id}\\"
    if splitext(filename)[1] == ".json":
        saveJSON(data, filename, path)
    elif splitext(filename)[1] == ".txt":
        save(data, filename, path)

def PlayerdataGetFileIndex(user, filename, key):
    """Only to be used on JSON files."""
    path = f".\\playerdata\\{user.id}\\"
    file = loadJSON(filename, path)
    return file[key]

def PlayerdataSetFileIndex(user, filename, key, value):
    """Only to be used on JSON files."""
    path = f".\\playerdata\\{user.id}\\"
    file = loadJSON(filename, path)
    if key in file: file[key] = value
    else: raise KeyError("The key you're trying to raise doesn't exist.")
    saveJSON(file, filename, path)
