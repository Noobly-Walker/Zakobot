from os.path import splitext
from sqlite3 import connect as sqlConnect
from datetime import datetime
import requests
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import *
from util.SLHandle import *
from util.DataHandlerUtil import *
from util.cmdutil import cmdutil
from util.GuildDataHandler import GuilddataGetFile
text = cmdutil()
local = loadJSON('.\\locals\\locals.json')

def preloadFile(path, user, file, defaults:dict):
    if not exists(f"{path}{file}.json"): data = {}
    else: data = PlayerdataGetFile(user, f"{file}.json")
    for i in defaults:
        data.setdefault(i, defaults[i])
    if file == "wallet":
        # a3.1_s42 patch to ensure everyone's balance is fixed
        if "BankKups" in data.keys():
            BankArgs = data["BankKups"] + data["BankArgs"]*1000 + data["BankAurus"]*1000000 + data["BankPluots"]*1000000
            data["BankArgs"] = BankArgs
            data["Args"] *= 1000
    for key in list(data.keys()): #clean up my blunders
        if key in defaults.keys(): pass
        else: del data[key]
    PlayerdataSetFile(user, f"{file}.json", data)
    return data

def preloadPlayerdata(user):
    path = f".\\playerdata\\{user.id}\\"
    pathfind(path)
    ts = datetime.timestamp(datetime.now())

    defaultsProfile = {
        "Name": global_name(user),
        "ID": user.id,
        "canDaily": True
        }
    defaultsLevel = {
        "Experience": 0,
        "Level": 0
        }
    defaultsTimers = {
        "Timestamp": ts,
        "BankInterest": ts,
        "Daily": ts,
        "DayTimer": ts,
        "EXPTimer": ts,
        "WeatherTimer": ts
        }
    defaultsSettings = {
        "LvUpReacts": True,
        "Color": "teal",
        "Notation": "e",
        "Rounding": "5"
        }
    defaultsMultis = {
        "ShopCountingMulti": 1
        }
    defaultsBackpack = {
        "cards": {}
        }
    defaultsStats = {
        "Messages Sent": 0,
        "Dailys Claimed": 0,
        "Counting Done": [0.0, 0],
        "Acct Creation": ts,
        "Activity Board": [],
        "Last Update": 0
        }
    defaultsWallet = {
        "Args": 100000, #PKA, ÷1000 (kup subunit)
        "BankArgs": 0, #Bank balance, in PKA
        "eUSD": 0, #United States Dollar, ÷100 (cent subunit)
        "eEUR": 0, #European Euro, ÷100 (cent subunit)
        "eCNY": 0, #Chinese Yuan
        "eJPY": 0, #Japanese Yen
        "eGBP": 0, #British Pound Stirling, ÷100 (cent subunit)
        "eCHF": 0, #Swiss Frank, ÷100 (cent subunit)
        "eAUD": 0, #Australian Dollar, ÷100 (cent subunit)
        "eCAD": 0, #Canadian Dollar, ÷100 (cent subunit)
        "eHKD": 0, #Hong Kong Dollar, ÷100 (cent subunit)
        "eSGD": 0, #Singapore Dollar, ÷100 (cent subunit)
        "eBTC": 0, #Bitcoin, ÷100M (satoshi subunit)
        "eETH": 0, #Ethereum, ÷1Qi (wei subunit)
        "eUST": 0, #Tether, ÷1M
        "eXRP": 0, #XRP, ÷1M (drop subunit)
        "eBNB": 0, #Binance Coin, ÷100M (jager subunit)
        "BankLedger": {},
        "Gems": 0
        }
    preloadFile(path, user, "profile", defaultsProfile)
    preloadFile(path, user, "level", defaultsLevel)
    preloadFile(path, user, "timers", defaultsTimers)
    preloadFile(path, user, "settings", defaultsSettings)
    preloadFile(path, user, "multis", defaultsMultis)
    preloadFile(path, user, "backpack", defaultsBackpack)
    dataStats = preloadFile(path, user, "stats", defaultsStats)
    dataWallet = preloadFile(path, user, "wallet", defaultsWallet)

    if len(dataStats["Activity Board"]) == 0:
        try:
            average = int(getActivity(dataStats)//1)
            for i in range(getAcctAge(dataStats)):
                dataStats["Activity Board"].append(average)
            dataStats["Last Update"] = getAcctAge(dataStats)
        except ZeroDivisionError:
            dataStats["Activity Board"].append(0)
    PlayerdataSetFile(user, "stats.json", dataStats)
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
                userSilver += 10000*userLevelFile["Level"]
                PlayerdataSetFileIndex(author, "wallet.json", "Args", userSilver)
            return userLevelFile, True
        else: return userLevelFile, False

def global_name(user):
    key = loadJSON(".\\locals\\keys.json")["discord"]
    headers = {
        'Authorization': f'Bot {key}',  # Replace with your bot token
        'User-Agent': f'DiscordBot {local["id"]}',  # Replace with your bot ID
    }
    response = requests.get(f'https://discord.com/api/v10/users/{user.id}', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        global_name = user_data['global_name']
        if global_name is not None: return global_name
        else: return user.name
    else:
        text.warn(f"[HTTP] Status code: {response.status_code}")

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
    if dataTimers["Timestamp"] > dataTimers["BankInterest"]+2629744:
        dataWallet = PlayerdataGetFile(user, "wallet.json")
        if dataWallet["BankArgs"] >= 1000000:
            interest = balance * (1 + 0.01/bankElapses)**bankElapses - balance
            dataTimers["BankInterest"] += 2629744 * bankElapses
            dataWallet["BankLedger"][dataTimers["BankInterest"]] = ["INT", round(interest/1000,3)]
            dataWallet["BankArgs"] += int(interest)
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
        # card = [isShiny, rarity, cardID]
        if str(card[2]) not in list(cardbook.keys()):
            cardbook[str(card[2])] = [card[1], 0, 0]
        if card[0] == "cardbase":
            cardbook[str(card[2])][1] += 1
        elif card[0] == "cardbase-shiny":
            cardbook[str(card[2])][2] += 1
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

def PayOtherPlayer(user, recipiant, value, coinType="Args"):
    donorBal = PlayerdataGetFileIndex(user, "wallet.json", coinType)
    if value <= donorBal: # Check if donor can afford it
        PlayerdataSetFileIndex(user, "wallet.json", coinType, donorBal-value)
        recipiantBal = PlayerdataGetFileIndex(recipiant, "wallet.json", coinType)
        PlayerdataSetFileIndex(recipiant, "wallet.json", coinType, recipiantBal+value)
        return True
    else: return False
