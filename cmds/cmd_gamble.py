import asyncio
import discord
from discord.ext import commands
import traceback
from os.path import isdir,exists
from math import factorial
from random import *
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.PlayerDataHandler import *
from util.DataHandlerUtil import *
from util.ColorUtil import rectColor
from util.ToolsUtil import bubbleSort
from util.SLHandle import *
from util.expol import expol
from util.cmdutil import cmdutil
text = cmdutil()

def commandList():
    return [roulette, headsgame, doubleornothing, coingame]

def categoryDescription():
    return "Gamble. Maybe you'll win. Probably, you'll lose. >:D"

@commands.command()
async def roulette(ctx, wager, bet, *bet2):
    """Roll the wheel. Watch the mesmerizing circle. See where the ball lands. Fail to notice as I take all of your money.\n\
roulette <wager> <bet> *<bet2>

Bet colors: red, black, row
Bet evenness: even, odd, row
Bet numbers: 00, 0-36

Winnings per bet:
  red, black, even, odd: 1.8×
  row: 10×
  given number: 28×

If two bets are taken, the wager is divided in half between the two.
Wagers are in Silver Pieces.
Max wager is 100000 SP."""
    pockets = {
        "0": ["row", "row"],
        "2": ["even", "black"],
        "14": ["even", "red"],
        "35": ["odd", "black"],
        "23": ["odd", "red"],
        "4": ["even", "black"],
        "16": ["even", "red"],
        "33": ["odd", "black"],
        "21": ["odd", "red"],
        "6": ["even", "black"],
        "18": ["even", "red"],
        "31": ["odd", "black"],
        "19": ["odd", "red"],
        "8": ["even", "black"],
        "12": ["even", "red"],
        "29": ["odd", "black"],
        "25": ["odd", "red"],
        "10": ["even", "black"],
        "27": ["odd", "red"],
        "00": ["row", "row"],
        "1": ["odd", "red"],
        "13": ["odd", "black"],
        "36": ["even", "red"],
        "24": ["even", "black"],
        "3": ["odd", "red"],
        "15": ["odd", "black"],
        "34": ["even", "red"],
        "22": ["even", "black"],
        "5": ["odd", "red"],
        "17": ["odd", "black"],
        "32": ["even", "red"],
        "20": ["even", "black"],
        "7": ["odd", "red"],
        "11": ["odd", "black"],
        "30": ["even", "red"],
        "26": ["even", "black"],
        "9": ["odd", "red"],
        "28": ["even", "black"]}

    wager = int(wager)
    wager2 = 0
    balance = PlayerdataGetFileIndex(ctx.author, "wallet.json", "Args")
    
    if balance < wager:
        await ctx.send("You've wagered more than you can afford.")
        return
    if balance > 100000:
        await ctx.send("You've wagered more than the max wager.")
        return

    balance -= wager
    if len(bet2) == 1:
        bet2 = bet2[0].lower()
        wager, wager2 = wager//2, wager//2
        
    ball = choice(list(pockets.keys()))
    payout = 0
    out = f"The ball landed in {str.capitalize(pockets[ball][1])} {ball} {str.capitalize(pockets[ball][0])}.\n\nBet 1: "

    if bet == ball:
        payout += 28*wager
        out += f"**Won Straight Up!!!** Payout: {25*wager}SP"
    elif bet in pockets[ball]:
        if bet == "row":
            payout += 10*wager
            out += f"**Won Row!!** Payout: {10*wager}SP"
        else:
            payout += int(1.5*wager)
            out += f"Won {str.capitalize(bet)}! Payout: {int(1.5*wager)}SP"
    else:
        out += f"No win..."

    if type(bet2) == str:
        out += "\nBet 2: "
        if bet2 == ball:
            payout += 25*wager2
            out += f"**Won Straight Up!!!** Payout: {25*wager2}SP"
        elif bet2 in pockets[ball]:
            if bet2 == "row":
                payout += 10*wager2
                out += f"**Won Row!!** Payout: {10*wager2}SP"
            else:
                payout += int(1.5*wager2)
                out += f"Won {str.capitalize(bet2)}! Payout: {int(1.5*wager2)}SP"
        else:
            out += f"No win..."
        out += f"\n\nTotal winnings: {payout}SP"

    await ctx.send(out)
    balance += payout
    PlayerdataSetFileIndex(ctx.author, "wallet.json", "Args", balance)

@commands.command(aliases=['heads', 'hGame', 'hgame']) # Gain silver based on how many heads are flipped
async def headsgame(ctx):
    """A coin will be flipped until it lands on tails. Each time it lands on heads, the money doubles!
Each coin flip costs 6SP. Winnings are potentially infinite, though the house wins more than loses."""
    wallet = PlayerdataGetFileIndex(ctx.author, "wallet.json", "Args")
    if wallet < 6: await ctx.send('You cannot afford to gamble!'); return
    coin = randrange(2)
    winnings = 0
    wins = 0
    silver = -6
    while coin == 1:
        wins += 1
        winnings = 2**wins*5
        silver -= 6
        coin = randrange(2)
    silver += winnings
    if wins < 2:
        flash = '**Loss!**'
        net = 'losing'
    if wins >= 2:
        net = 'winning'
        if wins < 5: flash = '**Win!**'
        elif wins < 10: flash = '**Big Win!**'
        elif wins < 15: flash = '***Huge Win!***'
        elif wins < 20: flash = '***JACKPOT!!!***'
        elif wins >= 20: flash = '__***SUPER JACKPOT!!!***__'
    PlayerdataSetFileIndex(ctx.author, "wallet.json", "Args", wallet+silver)
    await ctx.send(f"{flash} {global_name(author)} flipped heads {wins} times, {net} {silver:,}SP.")

@commands.command(aliases=['dn', 'doublenothing']) # Double or nothing.
async def doubleornothing(ctx, wager: int):
    """Double or nothing! Place your bets and flip the coin! Max bet is 500,000SP"""
    wallet = PlayerdataGetFileIndex(ctx.author, "wallet.json", "Args")
    if wager < 1: await ctx.send('You cannot wager less than one silver!'); return
    if wallet < wager: await ctx.send('You cannot afford to wager this much!'); return
    if 500000 < wager: await ctx.send('This is over the maximum wager! You can only bet 500kSP or less!'); return
    coin = randrange(2)
    if coin == 0:
        flash = '**Loss!**'
        net = 'lost and got nothing!'
        silver = -wager
    if coin == 1:
        flash = '**Win!**'
        net = f'won an additional {wager}SP!!!'
        silver = wager
    PlayerdataSetFileIndex(ctx.author, "wallet.json", "Args", wallet+silver)
    await ctx.send(f"{flash} {global_name(author)} {net}")

@commands.command(aliases=['cg3']) # Gain or lose silver based on how many heads or tails are flipped
async def coingame(ctx):
    """A coin will be flipped until the state changes. Each heads means greater winnings, and each tails means greater losses! Debt is possible, too."""
    wallet = PlayerdataGetFileIndex(ctx.author, "wallet.json", "Args")
    if wallet < 6: await ctx.send('You cannot afford to gamble!'); return
    coin = randrange(2)
    state = coin
    change = 0
    loops = 0
    silver = -6
    while coin == state:
        loops += 1
        coin = randrange(2)
    if state == 1:
        coinside = 'heads'
        if loops < 1:
            flash = '**Loss!** '
            net = 'losing'
            change = -2**loops*5
        if loops >= 1:
            net = 'winning'
            change = 3**loops*5
            if loops < 5: flash = '**Win!**'
            elif loops < 10: flash = '**Big Win!**'
            elif loops < 15: flash = '***Huge Win!***'
            elif loops < 20: flash = '***JACKPOT!!!***'
            elif loops >= 20: flash = '__***SUPER JACKPOT!!!***__'
    elif state == 0:
        coinside = 'tails'
        net = 'losing'
        change = -2**loops*5
        if loops < 5: flash = '**Loss!**'
        elif loops < 10: flash = '**Big Loss!**'
        elif loops < 15: flash = '***Huge Loss!***'
        elif loops < 20: flash = '***BANKRUPCY!!!***'
        elif loops >= 20: flash = '__***SUPER BANKRUPCY!!!***__'
    silver += change
    PlayerdataSetFileIndex(ctx.author, "wallet.json", "Args", wallet+silver)
    await ctx.send(f"{flash} {global_name(author)} flipped {coinside} {loops} times, {net} {silver:,}SP.")
