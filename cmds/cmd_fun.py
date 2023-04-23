import asyncio
import discord
from discord.ext import commands
import traceback
from os.path import isdir,exists
from math import factorial
import random
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import expol
from util.SLHandle import *
from util.PlayerDataHandler import *
from util.GuildDataHandler import *
from util.ColorUtil import rectColor
from util.cmdutil import cmdutil
text = cmdutil()
PATH = load(".\\locals\\%PATH%")

def commandList():
    return [count, minesweeper, farkle]

def categoryDescription():
    return "Games and other fun things."

@commands.command(aliases=['cnt', 'counting'])
async def count(ctx):
    """Count forever!
Every power of 10, the counting multiplier increases!
Algorithm: increment = 2^count.exponent×(1+(userLevel/4))"""
    guildSettings = GuilddataGetFile(ctx.guild, "settings.json")
    if guildSettings["Counting"]:
        pathfind(PATH)
        if exists(f"{PATH}\\counting.txt"): globalCount = expol(load("counting.txt", PATH))
        else: globalCount = expol("0E0")
        pathfind(f".\\guilddata\\{ctx.guild.id}\\")
        personalCount = expol(PlayerdataGetFileIndex(ctx.author, "stats.json", "Counting Done"))
        guildCount = expol(GuilddataGetFileIndex(ctx.guild, "stats.json", "Counting Done"))
        
        userGlobalLevel = PlayerdataGetFileIndex(ctx.author, "level.json", "Level")
        userGuildLevel = GuilddataGetFile(ctx.guild, "levels.json")[str(ctx.author.id)]["Level"]        
        userMultis = PlayerdataGetFile(ctx.author, "multis.json")
        globalIncrement = expol(2)**expol(globalCount.exponent)*(1+(userGlobalLevel/4))*(expol(userMultis['ShopCountingMulti']).log10()+1)
        if guildSettings["GlobalLevel"]: guildIncrement = globalIncrement
        else: guildIncrement = expol(2)**expol(globalCount.exponent)*(1+(userGuildLevel/4))*(expol(userMultis['ShopCountingMulti']).log10()+1)
        
        
        newGlobalCount = globalCount + globalIncrement
        newGuildCount = guildCount + guildIncrement
        newPersonalCount = personalCount + globalIncrement
        
        save(str(newGlobalCount),"counting.txt",PATH)
        save(str(newGuildCount),"counting.txt",f".\\guilddata\\{ctx.guild.id}")
        GuilddataSetFileIndex(ctx.guild, "stats.json", "Counting Done", str(newGuildCount))
        PlayerdataSetFileIndex(ctx.author, "stats.json", "Counting Done", str(newPersonalCount))

        notation = GetNotationCode(ctx.author)

        embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"Zako - Global Count", value=f"{globalCount:{notation}} + {globalIncrement:{notation}} = **{newGlobalCount:{notation}}**", inline=False)
        embed.add_field(name=f"{ctx.guild.name} - Guild Count", value=f"{guildCount:{notation}} + {guildIncrement:{notation}} = **{newGuildCount:{notation}}**", inline=False)
        embed.add_field(name=f"{ctx.author.name} - Personal Count", value=f"{personalCount:{notation}} + {globalIncrement:{notation}} = **{newPersonalCount:{notation}}**", inline=False)

        if globalCount.exponent < newGlobalCount.exponent:
            reward = 5**newGlobalCount.exponent #SP
            PlayerdataSetFileIndex(ctx.author, "wallet.json", "Args", PlayerdataGetFileIndex(ctx.author, "wallet.json", "Args")+reward)
            embed.add_field(name=f"Reward for reaching {expol([1,newGlobalCount.exponent]):{notation}}", value=f"{ctx.author.name} gained **{reward}SP**!", inline=False)
        
        await ctx.send(embed=embed)

@commands.command(aliases=['msw'])
async def minesweeper(ctx, map_size: int, bombchance: int):
    """Generates a minesweeper game!
    map_size 4 <= x <= 12
    bombchance -30 <= y =< -1 and 1 <= y <= 30 (lower number means more bombs)"""
    if map_size > 12 or map_size < 4:
        await ctx.send("Error: The given map size is too large or small!")
        return
    if abs(bombchance) > 30 or abs(bombchance) < 1:
        await ctx.send("Error: The given bomb chance is too large or small!")
        return
    grid = []
    drops = []
    numbers = ["", "<:msw1:739810675747979314>", "<:msw2:739810675827933274>", "<:msw3:739810675844448367>", "<:msw4:739810675584663576>", "<:msw5:739810675819413625>", "<:msw6:739810675878264872>", "<:msw7:739810675685064815>", "<:msw8:739810675819413614>"]
    Bombs = 0
    if bombchance > 0:
        for i in range(abs(bombchance)):
            drops.append("None")
        drops.append("Bomb")
    elif bombchance < 0:
        for i in range(abs(bombchance)):
            drops.append("Bomb")
        drops.append("None")
    for i in range(map_size): #Generate grid and place bombs!
        grid.append([])
        for j in range(map_size):
            type = random.choice(drops)
            grid[i].append(type)
    for i in range(map_size): #Place numbers!
        for j in range(map_size):
            count = 0
            if grid[i][j] == "None":
                if j != 0 and grid[i][j-1] == "Bomb":
                    count += 1
                if j != map_size-1 and grid[i][j+1] == "Bomb":
                    count += 1
                if i != 0 and grid[i-1][j] == "Bomb":
                    count += 1
                if i != map_size-1 and grid[i+1][j] == "Bomb":
                    count += 1
                if i != 0 and j != 0 and grid[i-1][j-1] == "Bomb":
                    count += 1
                if i != 0 and j != map_size-1 and grid[i-1][j+1] == "Bomb":
                    count += 1
                if i != map_size-1 and j != 0 and grid[i+1][j-1] == "Bomb":
                    count += 1
                if i != map_size-1 and j != map_size-1 and grid[i+1][j+1] == "Bomb":
                    count += 1
                if count > 0:
                    grid[i][j] = "||" + numbers[count] + "||"
                else:
                    grid[i][j] = "||:black_large_square:||"
    out = ""
    out2 = ""
    for i in range(map_size): #Generate map!
        for j in range(map_size):
            if grid[i][j] == "Bomb":
                grid[i][j] = "||:bomb:||"
                Bombs += 1
            if (map_size > 5 and i < map_size//2) or (map_size <= 5):
            	out += grid[i][j]
            else:
                out2 += grid[i][j]
        if (map_size > 5 and i < map_size//2) or (map_size <= 5):
            out += "\n"
        else:
            out2 += "\n"
    if Bombs == map_size**2:
        await ctx.send(f"Minesweeper - Oops! All bombs! ({Bombs}×Bombs)")
        await ctx.send("https://cdn.discordapp.com/attachments/601422216394965023/863777069581074512/unknown.png")
    else:
        out = f"Minesweeper - {Bombs}×Bombs\n" + out
    await ctx.send(out)
    if out2 != "":
        await ctx.send(out2)


@commands.command()
async def farkle(ctx):
    """Runs a game of Farkle!.
Rules:
  Roll 6d6, remove any dice worth anything, and repeat until you Farkle (run out of moves).
  If all six dice are used, roll all six again.

Values:
  1           -   100pts
  5           -    50pts

  Three of a Kind
  1,1,1       - 1,000pts
  A,A,A       - (A != 1) 100pts×Face Value

  Four of a Kind
  1,1,1,1     - 2,000pts
  A,A,A,A     - (A != 1) 200pts×Face Value

  Five of a Kind
  1,1,1,1,1   - 4,000pts
  A,A,A,A,A   - (A != 1) 400pts×Face Value

  Six of a Kind
  1,1,1,1,1,1 - 8,000pts
  A,A,A,A,A,A - (A != 1) 800pts×Face Value

  Three Pairs
  A,A,B,B,C,C - 1,500pts
  A,A,A,A,B,B - 4 of A value + 500pts

  Two Triplets
  A,A,A,B,B,B - 3 of A value + 3 of B value + 500pts

  Straight
  1,2,3,4,5,6 - 2,500pts"""

    def d6():
        return random.randrange(6)+1

    dice = []
    farkled = False
    score = 0
    out = []
    _round = 0
    hand = -1
    while not farkled:
        faceCounts = [0,0,0,0,0,0]
        _round += 1
        toAdd = 0
        foundCombo = False
        foundRun = False
        if len(dice) == 0:
            #if there aren't any dice left, get six new ones
            hand += 1
            _round = 1
            out.append("")
            dice = [1,1,1,1,1,1]
        for die in range(len(dice)):
            #Roll the dice
            dice[die] = d6()
            faceCounts[dice[die]-1] += 1
        dice.sort()

        out[hand] += f"**Roll {_round}:** " + ", ".join(map(str, dice)) + "\n"
            
        if faceCounts.count(1) == 6:
            #Check for a straight
            dice = []
            toAdd += 2500
            out[hand] += f"> Straight!"
        elif faceCounts.count(2) == 3:
            #Check for three pairs
            dice = []
            toAdd += 1500
            out[hand] += "> Three Pairs!"
            foundCombo = True
        elif faceCounts.count(2) == 1 and faceCounts.count(4) == 1:
            #Check for pair and quadruplet
            dice = []
            toAdd += 500
            for face in range(len(faceCounts)):
                if faceCounts[face] == 4:
                    if face+1 == 1: toAdd += 2000
                    else: toAdd += 200 * (face+1)
            out[hand] += "> Three Pairs!"
            foundCombo = True
        elif faceCounts.count(3) == 2:
            #Check for two triplets
            dice = []
            toAdd += 500
            for face in range(len(faceCounts)):
                if faceCounts[face] == 3:
                    if face+1 == 1: toAdd += 1000
                    else: toAdd += 100 * (face+1)
            out[hand] += "> Two Triplets!"
            foundCombo = True
        if foundCombo:
            score += toAdd
            out[hand] += f" +{toAdd}pts\n"
        else:
            for face in range(len(faceCounts)):
                if faceCounts[face] == 6:
                    #Check for sextuplet
                    if face+1 == 1: toAdd += 8000
                    else: toAdd += 800 * (face+1)
                    out[hand] += f"> Six of a Kind!"
                    foundRun = True
                elif faceCounts[face] == 5:
                    #Check for quintuplet
                    if face+1 == 1: toAdd += 4000
                    else: toAdd += 400 * (face+1)
                    out[hand] += f"> Five of a Kind!"
                    foundRun = True
                elif faceCounts[face] == 4:
                    #Check for quadruplet
                    if face+1 == 1: toAdd += 2000
                    else: toAdd += 200 * (face+1)
                    out[hand] += f"> Four of a Kind!"
                    foundRun = True
                elif faceCounts[face] == 3:
                    #Check for triplet
                    if face+1 == 1: toAdd += 1000
                    else: toAdd += 100 * (face+1)
                    out[hand] += f"> Three of a Kind!"
                    foundRun = True
                if foundRun:
                    while face+1 in dice: dice.remove(face+1)
                    out[hand] += f" +{toAdd}pts\n"
                    break
            toAdd += faceCounts[0]*100 + faceCounts[4]*50
            score += toAdd
            while 1 in dice: dice.remove(1)
            while 5 in dice: dice.remove(5)
            if toAdd == 0: farkled = True
            
    out[hand] += f"**Farkled!** But you made it out with a score of {score:,}."
    
    embed = discord.Embed(color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")), title="Farkle")
    for hand in range(len(out)):
        embed.add_field(name=f"Round #{hand+1}", value=out[hand], inline=False)
    await ctx.send(embed=embed)
