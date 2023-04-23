import asyncio
from discord.ext import commands
import traceback
from os import walk
from os.path import isdir,exists
from math import factorial
from random import *
from datetime import datetime
import discord
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import expol
from util.PlayerDataHandler import *
from util.DataHandlerUtil import *
from util.SLHandle import *
from util.ColorUtil import rectColor
from util.cmdutil import cmdutil
from util.CardUtil import *
from util.coinStacker import *
text = cmdutil()

def commandList():
    return [bank, daily, shop]

def categoryDescription():
    return "Economy commands."

@commands.command(aliases=["bal"])
async def bank(ctx, action="", *amount):
    """Access your bank account.

bank deposit <quantity>
  minimum deposit is 100SP
bank withdraw <quantity>
  quantity will be in SP
  5% processing fee on withdrawals
  minimum withdrawal is 20SP
  account will not accrue interest if balance is less than 1GP
bank balance
  1000CP = 1SP
  1000SP = 1GP
  gains 0.25% interest per day if there is a balance of at least 1GP"""
    if action in ["withdraw", "with", "w", "deposit", "dep", "d"]:
        if len(amount) == 0: await ctx.send("You must specify an amount for this action."); return
        else:
            try: amount = int(amount[0])
            except Exception: await ctx.send(f"Improper argument {amount[0]}. Argument must be a number."); return
    wallet = PlayerdataGetFile(ctx.author, "wallet.json")
    ts = datetime.timestamp(datetime.now())
            
    if action in ["deposit", "dep", "d"]:
        if amount > wallet["Args"]: await ctx.send(f"You cannot afford to deposit **{wallet['Args']}SP**."); return
        elif amount < 100: await ctx.send(f"You must deposit a minimum of **100SP**."); return
        wallet["Args"] -= amount
        wallet["BankArgs"] += amount
        wallet["BankLedger"][ts] = ["DEP", amount]
        bankAurusPrint, bankArgsPrint, bankKupsPrint = regularizeGSC(wallet['BankAurus'], wallet['BankArgs'], wallet['BankKups'])
        out = f"You've deposited **{amount}SP** into your account.\n\
Your wallet balance is now **{wallet['Aurus']}GP {wallet['Args']}SP {wallet['Kups']}CP**.\n\
Your account balance is now **{bankAurusPrint}GP {bankArgsPrint}SP {bankKupsPrint}CP**."
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"**First Pikatonian Bank**", value=out)
        await ctx.send(embed=embed)
    if action in ["withdraw", "with", "w"]:
        if amount > wallet["BankArgs"] + wallet["BankAurus"]*1000: await ctx.send(f"You cannot afford to withdraw **{wallet['Args']}SP**."); return
        elif amount*1.05 > wallet["BankArgs"] + wallet["BankAurus"]*1000: await ctx.send(f"You cannot afford the 5% processing fee to withdraw **{wallet['Args']}SP**."); return
        elif amount < 20: await ctx.send(f"You must withdraw a minimum of **20SP**."); return
        bankBal = wallet["BankArgs"] + wallet["BankAurus"]*1000
        wallet["Args"] += amount
        bankBal -= int(amount*1.05)
        wallet["BankAurus"] = int(bankBal // 1000)
        wallet["BankArgs"] = int(bankBal % 1000)
        wallet["BankLedger"][ts] = ["WITH", int(amount*1.05)]
        out = f"You've withdrawn **{int(amount)}SP** from your account.\n\
A 5% processing fee (**{round(amount*0.05,3)}SP**) has automatically been deducted.\n\
Your wallet balance is now **{wallet['Aurus']}GP {wallet['Args']}SP {wallet['Kups']}CP**.\n\
Your account balance is now **{wallet['BankAurus']}GP {wallet['BankArgs']}SP {wallet['BankKups']}CP**."
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"**First Pikatonian Bank**", value=out)
        await ctx.send(embed=embed)
    if action in ["balance", "bal", "b", ""]:
        #generate ledger string
        ledgerDates = list(wallet["BankLedger"].keys())
        ledger = ""
        inverseIndex = -1
        while inverseIndex >= -10:
            try:
                convertedTimestamp = datetime.fromtimestamp(float(ledgerDates[inverseIndex]), tz=None)
                ledger = f"{convertedTimestamp} UTC: **{wallet['BankLedger'][ledgerDates[inverseIndex]][0]} {wallet['BankLedger'][ledgerDates[inverseIndex]][1]}SP**\n" + ledger
                inverseIndex -= 1
            except Exception: break #reached top of ledger
        if ledger == "": ledger = "No transactions to show."

        #generate coinpile
        coinPile = None
        coinColors = {
            1: (200, 100, 64),
            50: (164, 114, 96),
            1000: (128, 128, 128),
            50000: (164, 164, 96),
            1000000: (200, 200, 64)
            }
        coinRender = coinStacker(coinColors)
        if wallet['BankKups'] + wallet['BankArgs']*1000 + wallet['BankAurus']*1000000 > 0:
            coinPile = coinRender.createPile(wallet['BankKups'] + wallet['BankArgs']*1000 + wallet['BankAurus']*1000000)
            coinPile = discord.File(coinPile, filename="coinpile.png")
        
        netWorthAuru, netWorthArg, netWorthKup = regularizeGSC(wallet['Aurus']+wallet['BankAurus'], wallet['Args']+wallet['BankArgs'], wallet['Kups']+wallet['BankKups'])
        out = f"Your wallet balance is **{wallet['Aurus']}GP {wallet['Args']}SP {wallet['Kups']}CP**.\n\
Your account balance is **{wallet['BankAurus']}GP {wallet['BankArgs']}SP {wallet['BankKups']}CP**.\n\n\
Your net worth is **{netWorthAuru}GP {netWorthArg}SP {netWorthKup}CP**."
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"**First Pikatonian Bank**", value=out, inline=False)
        embed.add_field(name=f"Ledger", value=ledger, inline=False)
        embed.set_footer(text="WITH = withdrawal, DEP = deposit, INT = interest")
        if coinPile is not None:
            embed.set_image(url="attachment://coinpile.png")
            await ctx.send(file=coinPile, embed=embed)
        else:
            await ctx.send(embed=embed)
        coinRender.purge()

    PlayerdataSetFile(ctx.author, "wallet.json", wallet)

@commands.command()
async def daily(ctx):
    """Get your daily allowance of silver here, based on level!"""
    userProfile = PlayerdataGetFile(ctx.author, "profile.json")
    if userProfile["canDaily"]:
        userWallet = PlayerdataGetFile(ctx.author, "wallet.json")
        userLevel = PlayerdataGetFile(ctx.author, "level.json")
        userWallet["Args"] += 10*userLevel["Level"]
        await ctx.send(f"Thanks for checking in, {ctx.author.name}! Here's your **{10*userLevel['Level']}SP**.")
        userProfile["canDaily"] = False
        PlayerdataSetFile(ctx.author, "wallet.json", userWallet)
        PlayerdataSetFile(ctx.author, "profile.json", userProfile)
        
        PlayerdataSetFileIndex(ctx.author, "stats.json", "Dailys Claimed",
            PlayerdataGetFileIndex(ctx.author, "stats.json", "Dailys Claimed") + 1)
    else: await ctx.send("It appears you've already claimed this. Try again later.")


outText = None
outFile = None

@commands.command()
async def shop(ctx, category=None, action="list", selection=None, quantity=1):
    """Buy stuff or get out!

Categories:
  multi, cards

Actions:
  buy, list
"""
    global outText, outFile
    embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
    action = action.lower()
    quantity = int(quantity)
    path = ".\\shopdata\\"
    if category == None:
        cats = []
        descs = []
        for root, dirs, files in walk(path):
            for directory in dirs:
                if directory == path: continue
                cats.append(directory)
                descs.append(load("desc.txt", f"{path}{directory}\\"))
        embed.add_field(name=f"Categories", value="\n".join(cats), inline=True)
        embed.add_field(name=f"Description", value="\n".join(descs), inline=True)
        await ctx.send(embed=embed)
    elif action == "list":
        shop = loadJSON("shop.json", f"{path}{category}\\")
        items = list(shop.keys())
        prices = []
        descs = []
        for item in shop:
            if shop[item]['currency'] == "Kups": prices.append(f"{shop[item]['price']}CP")
            elif shop[item]['currency'] == "Args": prices.append(f"{shop[item]['price']}SP")
            elif shop[item]['currency'] == "Aurus": prices.append(f"{shop[item]['price']}GP")
            elif shop[item]['currency'] == "Gems": prices.append(f":gem:{shop[item]['price']}")
            else: prices.append(f"{shop[item]['price']}")
            descs.append(shop[item]['description'])
        embed.add_field(name=f"Item", value="\n".join(items), inline=True)
        embed.add_field(name=f"Price", value="\n".join(prices), inline=True)
        embed.add_field(name=f"Description", value="\n".join(descs), inline=True)
        await ctx.send(embed=embed)
    elif action == "buy":
        if selection == None:
            await ctx.send("You must select an item from this store to buy!"); return
        shop = loadJSON("shop.json", f"{path}{category}\\")
        item = shop[selection]
        wallet = PlayerdataGetFile(ctx.author, "wallet.json")
        if wallet[item['currency']] < item['price']*quantity:
            await ctx.send(f"You cannot afford {quantity}×{selection}!"); return
        wallet[item['currency']] -= item['price']*quantity
        payload = item['payload']
        author=ctx.author
        _locals = locals()
        exec(payload, globals(), _locals)
        currencyNameConversion = {"Kups":"CP", "Args":"SP", "Aurus":"GP"}
        await ctx.send(f"{quantity}×{selection} purchased successfully for {item['price']*quantity}{currencyNameConversion[item['currency']]}!")
        if outText not in [None, "", " ", "\n"]: await ctx.send(outText)
        if outFile != None: await ctx.send(file=discord.File(outFile))
        outText = None
        outFile = None
        PlayerdataSetFile(ctx.author, "wallet.json", wallet)
        
