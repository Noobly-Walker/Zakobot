from os.path import splitext
from sqlite3 import connect as sqlConnect
from datetime import datetime
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import *
from util.SLHandle import *
from util.DataHandlerUtil import *
from util.cmdutil import cmdutil
from util.GuildDataHandler import GuilddataGetFile
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
    dataSettings.setdefault("Notation", "e")
    dataSettings.setdefault("Rounding", "5")
    for key in list(dataSettings.keys()): #clean up my blunders
        if key in ["LvUpReacts", "Color", "Notation", "Rounding"]: pass
        else: del dataSettings[key]
    PlayerdataSetFile(user, "settings.json", dataSettings)

    if not exists(f"{path}multis.json"): dataMultis = {}
    else: dataMultis = PlayerdataGetFile(user, "multis.json")
    dataMultis.setdefault("ShopCountingMulti", 1)
    for key in list(dataMultis.keys()): #clean up my blunders
        if key in ["ShopCountingMulti"]: pass
        else: del dataMultis[key]
    PlayerdataSetFile(user, "multis.json", dataMultis)

    if not exists(f"{path}backpack.json"): dataBackpack = {}
    else: dataBackpack = PlayerdataGetFile(user, "backpack.json")
    dataBackpack.setdefault("cards", {})
    for key in list(dataBackpack.keys()): #clean up my blunders
        if key in ["cards"]: pass
        else: del dataBackpack[key]
    PlayerdataSetFile(user, "backpack.json", dataBackpack)

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
    dataWallet.setdefault("Gems", 0)
    for key in list(dataWallet.keys()): #clean up my blunders
        if key in ["Kups", "Args", "Aurus", "BankKups", "BankArgs", "BankAurus", "BankLedger", "Gems"]: pass
        else: del dataWallet[key]
    dataWallet["BankAurus"], dataWallet["BankArgs"], dataWallet["BankKups"] = IntToGSC(GSCToInt(dataWallet["BankAurus"], dataWallet["BankArgs"], dataWallet["BankKups"]))
    PlayerdataSetFile(user, "wallet.json", dataWallet)

def incrementXP(ctx, userLevelFile, experienceGain, globalScope=True):
    guild = ctx.guild
    message = ctx.message
    author = message.author

    if globalScope: scope = "Global"
    else: scope = guild.name
    
    userLevelFile["Experience"] += experienceGain
    if userLevelFile["Level"] < 200:
        if userLevelFile["Experience"] >= 20+(userLevelFile["Level"]**2*20):
            userLevelFile["Experience"] -= 20+(userLevelFile["Level"]**2*20)
            userLevelFile["Level"] += 1
            text.log(f"{author.name} is now level {userLevelFile['Level']} in scope {scope}.")

            if globalScope:
                userSilver = PlayerdataGetFileIndex(author, "wallet.json", "Args")
                userSilver += 10*userLevelFile["Level"]
                PlayerdataSetFileIndex(author, "wallet.json", "Args", userSilver)
            return userLevelFile, True
        else: return userLevelFile, False

async def reactToLvUp(ctx, integer):
    message = ctx.message
    author = message.author
    guild = ctx.guild
    guildSettings = GuilddataGetFile(guild, "settings.json")
    
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

def UpdateTimers(user):
    dataTimers = PlayerdataGetFile(user, "timers.json")
    elapses = (dataTimers["Timestamp"] - dataTimers["DayTimer"]) // 86400
    bankElapses = (dataTimers["Timestamp"] - dataTimers["BankInterest"]) // 86400
    if dataTimers["Timestamp"] > dataTimers["BankInterest"]+86400:
        dataWallet = PlayerdataGetFile(user, "wallet.json")
        balance = GSCToInt(dataWallet["BankAurus"], dataWallet["BankArgs"], dataWallet["BankKups"])
        if balance >= 1000000:
            interest = balance * (1 + 0.0025/bankElapses)**bankElapses - balance
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
    code = f"{userSettings['Notation']}.{userSettings['Rounding']}"
    return code

def AddCards(user, cards):
    cardbook = PlayerdataGetFileIndex(user, "backpack.json", "cards")
    for card in cards:
        if card[2] not in cardbook.keys():
            cardbook[card[2]] = [card[1], 0, 0]
        if card[0] == "cardbase":
            cardbook[card[2]][1] += 1
        elif card[0] == "cardbase-shiny":
            cardbook[card[2]][2] += 1
    PlayerdataSetFileIndex(user, "backpack.json", "cards", cardbook)

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
