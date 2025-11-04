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
local = loadJSON('.\\locals\\locals.json')

def commandList():
    return [bank, daily, shop, pay]

def categoryDescription():
    return "Economy commands."

@commands.command(aliases=["bal"])
async def bank(ctx, action="", amount:float=0):
    """Access your bank account.

bank deposit <quantity>
  minimum deposit is 100SP
bank withdraw <quantity>
  quantity will be in SP
  5% processing fee on withdrawals
  minimum withdrawal is 20SP
  account will not accrue interest if balance is less than 1GP
bank balance
  CP: Copper Pieces (Kup)
      Billon Pieces (Argikup)       =   50CP
  SP: Silver Pieces (Arg)           = 1000CP
      Electrum Pieces (Auriarg)     =   50SP
  GP: Gold Pieces (Auru)            = 1000SP
      Plutaurum Pieces (Pluotauri)  =   50GP
  PP: Plutonium Pieces (Pluot)      = 1000GP
  gains 0.25% interest per day if there is a balance of at least 1GP"""
    
    if action in ["withdraw", "with", "w", "deposit", "dep", "d"]:
        if amount == 0: await ctx.send("You must specify an amount for this action."); return
        else:
            try: amount = int(1000*amount)
            except Exception: await ctx.send(f"Improper argument {amount}. Argument must be a number."); return
    wallet = PlayerdataGetFile(ctx.author, "wallet.json")
    ts = datetime.timestamp(datetime.now())
            
    if action in ["deposit", "dep", "d"]:
        if amount > wallet["Args"]: await ctx.send(f"You cannot afford to deposit **{argsAsString(amount)}**."); return
        elif amount < 100000: await ctx.send(f"You must deposit a minimum of **100SP**."); return
        wallet["Args"] -= amount
        wallet["BankArgs"] += amount
        wallet["BankLedger"][ts] = ["DEP", amount]
        out = f"You've deposited **{argsAsString(amount)}** into your account.\n\
Your wallet balance is now **{argsAsString(wallet['Args'])}**.\n\
Your account balance is now **{argsAsString(wallet['BankArgs'])}**."
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"**First Pikatonian Bank**", value=out)
        await ctx.send(embed=embed)
    if action in ["withdraw", "with", "w"]:
        if amount > wallet["BankArgs"]: await ctx.send(f"You cannot afford to withdraw **{argsAsString(amount)}**."); return
        elif amount*1.05 > wallet["BankArgs"]: await ctx.send(f"You cannot afford the 5% processing fee to withdraw **{argsAsString(amount)}**."); return
        elif amount < 20: await ctx.send(f"You must withdraw a minimum of **20CP**."); return
        wallet["Args"] += amount
        wallet["BankArgs"] -= int(amount*1.05)
        wallet["BankLedger"][ts] = ["WITH", int(amount*1.05)/1000]
        out = f"You've withdrawn **{argsAsString(amount)}** from your account.\n\
A 5% processing fee (**{argsAsString(round(amount*0.05,3))}**) has automatically been deducted.\n\
Your wallet balance is now **{argsAsString(wallet['Args'])}**.\n\
Your account balance is now **{argsAsString(wallet['BankArgs'])}**."
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
                convertedTimestamp = datetime.fromtimestamp(int(float(ledgerDates[inverseIndex])), tz=None)
                ledger = f"{convertedTimestamp} UTC: **{wallet['BankLedger'][ledgerDates[inverseIndex]][0]} {argsAsString(wallet['BankLedger'][ledgerDates[inverseIndex]][1])}**\n" + ledger
                inverseIndex -= 1
            except Exception: break #reached top of ledger
        if ledger == "": ledger = "No transactions to show."

        #generate coinpile
        coinPile = None
        coinColors = {
            1: (184, 115, 51),
            50: (188, 154, 121),
            1000: (192, 192, 192),
            50000: (221, 196, 111),
            1000000: (250, 201, 31),
            50000000: (205, 178, 93),
            1000000000: (155, 155, 155)
            }
        coinRender = coinStacker(coinColors)
        if wallet['BankArgs'] > 0:
            coinPile = coinRender.createPile(wallet['BankArgs'])
            coinPile = discord.File(coinPile, filename="coinpile.png")

        out = f"Your wallet balance is **{argsAsString(wallet['Args'])}**.\n\
Your account balance is **{argsAsString(wallet['BankArgs'])}**.\n\n\
Your net worth is **{argsAsString(wallet['Args']+wallet['BankArgs'])}**."
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
        userWallet["Args"] += 10000*userLevel["Level"]
        await ctx.send(f"Thanks for checking in, {global_name(ctx.author)}! Here's your **{argsAsString(10*userLevel['Level'])}**.")
        userProfile["canDaily"] = False
        PlayerdataSetFile(ctx.author, "wallet.json", userWallet)
        PlayerdataSetFile(ctx.author, "profile.json", userProfile)
        
        PlayerdataSetFileIndex(ctx.author, "stats.json", "Dailys Claimed",
            PlayerdataGetFileIndex(ctx.author, "stats.json", "Dailys Claimed") + 1)
    else: await ctx.send("It appears you've already claimed this. Try again later.")

@commands.command()
async def pay(ctx, recipiant, value:float):
    """Give other players money."""
    if value < 0:
        await ctx.send("Don't be a thief!")
        return
    converter = commands.MemberConverter()
    recipUser = await converter.convert(ctx, recipiant)
    value = int(value*1000)
    status = PayOtherPlayer(ctx.author, recipUser, value)

    donorProfile = PlayerdataGetFile(ctx.author, "profile.json")
    recipProfile = PlayerdataGetFile(recipUser, "profile.json")
    if status: await ctx.send(f"{donorProfile['Name']} paid {recipProfile['Name']} **{argsAsString(value)}**.")
    else: await ctx.send(f"You can't afford this transaction!")

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
            if shop[item]['currency'] == "Args": prices.append(f"{argsAsString(shop[item]['price'])}")
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
        currencyNameConversion = {"Kups":"CP", "Args":"SP", "Aurus":"GP", "Pluots":"PP"}
        await ctx.send(f"{quantity}×{selection} purchased successfully for {item['price']*quantity}{currencyNameConversion[item['currency']]}!")
        if outText not in [None, "", " ", "\n"]: await ctx.send(outText)
        if outFile != None: await ctx.send(file=discord.File(outFile))
        outText = None
        outFile = None
        PlayerdataSetFile(ctx.author, "wallet.json", wallet)
        
