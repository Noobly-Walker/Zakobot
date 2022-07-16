import asyncio
from discord.ext import commands
import traceback
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
text = cmdutil()

def _cmdl_():
    return ["bank", "daily"]

def _catdesc_():
    return "Economy commands."

@commands.command()
async def bank(ctx, action="", *amount):
    """Access your bank account.

z/bank deposit <quantity>
  minimum deposit is 100SP
z/bank withdraw <quantity>
  quantity will be in SP
  5% processing fee on withdrawals
  minimum withdrawal is 20SP
  account will not accrue interest if balance is less than 1GP
z/bank balance
  1000CP = 1SP
  1000SP = 1GP
  gains 0.1% interest per day if there is a balance of at least 1GP"""
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
        ledgerDates = list(wallet["BankLedger"].keys())
        ledger = ""
        inverseIndex = -1
        while inverseIndex >= -10:
            try:
                convertedTimestamp = datetime.fromtimestamp(float(ledgerDates[inverseIndex]), tz=None)
                ledger = f"{convertedTimestamp} UTC: **{wallet['BankLedger'][ledgerDates[inverseIndex]][0]} {wallet['BankLedger'][ledgerDates[inverseIndex]][1]}SP**\n" + ledger
                inverseIndex -= 1
            except Exception: break #reached top of ledger
        netWorthAuru, netWorthArg, netWorthKup = regularizeGSC(wallet['Aurus']+wallet['BankAurus'], wallet['Args']+wallet['BankArgs'], wallet['Kups']+wallet['BankKups'])
        out = f"Your wallet balance is **{wallet['Aurus']}GP {wallet['Args']}SP {wallet['Kups']}CP**.\n\
Your account balance is **{wallet['BankAurus']}GP {wallet['BankArgs']}SP {wallet['BankKups']}CP**.\n\n\
Your net worth is **{netWorthAuru}GP {netWorthArg}SP {netWorthKup}CP**."
        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"**First Pikatonian Bank**", value=out, inline=False)
        embed.add_field(name=f"Ledger", value=ledger, inline=False)
        embed.set_footer(text="WITH = withdrawal, DEP = deposit, INT = interest")
        await ctx.send(embed=embed)

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

