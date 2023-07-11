import asyncio
from discord.ext import commands
import traceback
from os.path import isdir,exists
from math import factorial
from random import *
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.ItemRandomizer import itemGenerator
from util.SLHandle import load
from util.SLHandle import *
from util.expol import expol
from util.cmdutil import cmdutil
text = cmdutil()
PATH = load(".\\locals\\%PATH%")

def commandList():
    return [splash, joke, choose, generate,
            roll, namegenerator, chuck]

def categoryDescription():
    return "Random numbers and items from lists."

def get_rand_from_list(listName:str):
    file = load(listName + '.txt', PATH + '\\randlists\\')
    randStr = file.split("\n")
    randID = randrange(len(randStr))
    string = randStr[randID]
    return string.replace("\\n", "\n")

@commands.command()
async def splash(ctx):
    "Returns a random splash"
    await ctx.send(get_rand_from_list("splash"))

@commands.command()
async def joke(ctx):
    "Returns a random joke"
    await ctx.send(get_rand_from_list("jokes"))

@commands.command(aliases=['gen'])
async def generate(ctx, type_=None):
    """Returns a random item with random modifiers. For fun or roleplaying; has no bearing on anything else.
    Valid types: tool, melee, ranged, ammo, armor, jewelry, trinket, potion, furniture, any
    Type '[PREFIX]generate info' to learn more about formatting of items."""
    if type_ is None: type_ = "any"
    await ctx.send(itemGenerator(ctx, type_, {"debuff": True, "tf": True, "nsfw": False, "vore": False, "gore": False, "fetish": False}))

@commands.command()
async def chuck(ctx):
    "Returns a random Chuck Norris joke"
    await ctx.send(get_rand_from_list("chucks"))

@commands.command(aliases=['choice']) # Bot randomly chooses between the inputs.
async def choose(ctx, *, choices: str):
    """Lets me choose between a list of items. Separate items using commas."""
    vals = choices.split(",")
    options = [] # short for post-processed
    for val in vals:
      stripped = val.strip()
      if stripped: # Empty sequences are falsy.
        options.append(stripped)
    await ctx.send(choice(options))

@commands.command(aliases=['dice']) # Bot rolls X Y-sided dice. Not as nice as Tsumikibot's dice system, and that's okay.
async def roll(ctx, dice: str, *formating: str):
    """Rolls some dice.
    Example: [prefix]roll 2d6
    Returns: 6, 2"""
    try:
        if dice[0] == 'd': dice = '1' + dice
        try: rolls, limit = map(int, dice.split('d'))
        except Exception:
            out = 'Invalid dice! Proper syntax example: ' + prefix + 'roll 10d20'
            await ctx.send(out); return
        total = 0
        result = '('
        dieoutputs = {}
        singlerolls = True
        if rolls > 1000000:
            await ctx.send("Too many dice!")
            await ctx.send("https://cdn.discordapp.com/attachments/962661092440547358/982143645945847828/05d6fdefa75dfa9ff5e55245996a853e.jpg")
            return
            #There may be a way to use statistics to write an algorithm that would turn large amounts of dice into
            #  one dice roll, to save processing time.
            #10000000000d4 would result from 10 billion if we get 10 billion 1s, up to 40 billion, but it's most
            #  likely to be around 25 billion.
            #I'm not good at statistics.
        if rolls > 1: singlerolls = False
        while rolls > 0:
            roll = randint(1, limit)
            total += roll
            if len(formating) > 0:
                if formating[0] in 'cs':
                    dieoutputs[roll] = dieoutputs.setdefault(roll, 1)
            else: 
                result += str(roll)
                if rolls > 1: result += ', '
            rolls -= 1
        if len(formating) > 0:
            if formating[0] == 'c':
                for num in dieoutputs.keys():
                    result += '[{0} × {1}s], '.format(dieoutputs[num], num)
                result = result[:-2]
        if not singlerolls: result += ') Total: ' + str(total)
        else: result += ')'
        if len(result) > 2000: result = "Total: " + str(total)
    except Exception as e: result = f"Error: {e}"
    await ctx.send(result)

@commands.command(aliases=['namegen'])
async def namegenerator(ctx, tries=1):
    """Generate random names from consonants and vowels!
Clamped number of tries to 1 <= n <= 100"""
    consonants = []
    vowels = []

    def addToBag(bag:list,string:str,count:int):
        for i in range(count):
            bag.append(string)
        return bag

    consonants = addToBag(consonants, "r", 38)
    consonants = addToBag(consonants, "t", 35)
    consonants = addToBag(consonants, "n", 33)
    consonants = addToBag(consonants, "s", 29)
    consonants = addToBag(consonants, "l", 27)
    consonants = addToBag(consonants, "c", 23)
    consonants = addToBag(consonants, "d", 17)
    consonants = addToBag(consonants, "p", 16)
    consonants = addToBag(consonants, "m", 15)
    consonants = addToBag(consonants, "h", 15)
    consonants = addToBag(consonants, "g", 12)
    consonants = addToBag(consonants, "b", 10)
    consonants = addToBag(consonants, "ch", 10)
    consonants = addToBag(consonants, "sh", 10)
    consonants = addToBag(consonants, "th", 10)
    consonants = addToBag(consonants, "f", 9)
    consonants = addToBag(consonants, "y", 9)
    consonants = addToBag(consonants, "w", 6)
    consonants = addToBag(consonants, "k", 5)
    consonants = addToBag(consonants, "v", 5)
    consonants = addToBag(consonants, "x", 1)
    consonants = addToBag(consonants, "z", 1)
    consonants = addToBag(consonants, "j", 1)
    consonants = addToBag(consonants, "qu", 1)

    vowels = addToBag(vowels, "a", 43)
    vowels = addToBag(vowels, "e", 56)
    vowels = addToBag(vowels, "i", 38)
    vowels = addToBag(vowels, "o", 36)
    vowels = addToBag(vowels, "u", 18)
    vowels = addToBag(vowels, "y", 9)
    vowels = addToBag(vowels, "ee", 3)
    vowels = addToBag(vowels, "oo", 3)
    vowels = addToBag(vowels, "ae", 2)
    vowels = addToBag(vowels, "ea", 2)
    vowels = addToBag(vowels, "ie", 1)
    vowels = addToBag(vowels, "ue", 1)
    vowels = addToBag(vowels, "ei", 1)
    vowels = addToBag(vowels, "ai", 1)

    def wordGenerator(minBlocks,randAddedBlocks):
        boolean = choice([True, False])
        newName = ""
        if boolean: newName += choice(consonants) # start name with consonant
        newName += choice(vowels) # start name with vowel or finish first block
        minBlocks -= 1
        blocks = randrange(randAddedBlocks)+minBlocks
        for i in range(blocks):
            coin = randrange(2)
            if coin == 1:
                newName += choice(consonants) + choice(vowels)
            else:
                newName += choice(consonants) + choice(consonants) + choice(vowels)
        boolean = choice([True, False])
        if boolean: newName += choice(consonants)
        return newName

    tries = max(1, min(tries, 100))
    out = ""
    for i in range(tries):
        out += wordGenerator(2,2).title() + " " + wordGenerator(3,2).title() + "\n"
    await ctx.send(out)
