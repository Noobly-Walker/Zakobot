import asyncio
from discord.ext import commands
import traceback
from util.SLHandle import *
import json
from fuzzywuzzy import process
import re
import discord
from string import capwords
# This code has been imported, but it's not of Zako.
from util.cmdutil import cmdutil
text = cmdutil()

def _cmdl_():
    return []

def _catdesc_():
    return "Commands for Backpack Bot"

def readBpHItemJSON():
    # Read Item list
    item_file=open("data\\BpHItemData.json","r")
    item_string=item_file.read()
    # clean invalid trailing commas
    item_string=re.sub("],\n}", "]}", item_string)
    # parse
    items=json.loads(item_string)["items"]
    item_file.close()
    # Create list of item names for fuzzy searching
    itemNames=[]
    typeNames=[]
    for item in items:
        itemNames.append(item["name"])
        for _type in item["types"]:
            if _type not in typeNames: typeNames.append(_type)
    #l.info("Read Item File Success")
    text.log("Read Item File Success") #line temporary for use in Zako
    return items, itemNames, typeNames

@commands.command()
async def bphtype(ctx, *, search:str):
    """Lists items of a given type. Accepts up to two types."""
    #global items, typeNames
    items, itemNames, typeNames = readBpHItemJSON() #line temporary for use in Zako

    search = search.split()
    typeResults = []
    
    #Perform fuzzy search on type list
    for _type in search:
        typeResults.append(process.extractOne(_type,typeNames))

    #Type not found (match not close enough)  
    typeSearch = []
    for typeResult in typeResults:
        if typeResult[1] <= 85:
            #l.info("Type %s not found, closest match %s", search, typeResult)
            text.warn("Type %s not found, closest match %s", search, typeResult) #line temporary for use in Zako
            await ctx.channel.send("Type not recognized. Did you mean "+typeResult[0].title()+"?")
            return
        typeSearch.append(typeResult[0].title())
    #Building array nest for multiple result types: has both types, has one type, has the other type
    resultLists = []
    for searchLength in range(len(typeSearch)):
        j = 0
        while j <= searchLength:
            resultLists.append([])
            j += 1

    #Getting results of all items from the specified type
    for item in items:
        if len(typeSearch) == 2:
            #both items match
            if set(typeSearch) == set(item["types"]): resultLists[0].append(item["name"])
            #the first item matches
            elif typeSearch[0] in set(item["types"]): resultLists[1].append(item["name"])
            #the second item matches
            elif typeSearch[1] in set(item["types"]): resultLists[2].append(item["name"])
        elif len(typeSearch) == 1:
            #the first item matches
            if typeSearch[0] in set(item["types"]): resultLists[0].append(item["name"])
    
    #Turning item lists into str
    stringItemLists = []
    for resultList in resultLists:
        #check to see if there are any items in this list
        if len(resultList) == 0:
            stringItemLists.append("There are no items of the specified type(s)!")
            continue
        #stringify list
        stringItemList = ""
        for item in resultList:
            item = capwords(item)
            if len(stringItemList + item + ", ") <= 1021: stringItemList += item + ", "
            elif len(stringItemList + item + ", ") > 1021: stringItemList += "..."
        #clipping off trailing comma at end of list if it does manage to fit in embed field after all
        if stringItemList[-2:] == ", ":
            stringItemList = stringItemList[:-2]
        stringItemLists.append(stringItemList)

    #Building embed
    embed = discord.Embed(color=0xFF00FF, title="Type Results")
    if len(typeSearch) == 2:
        embed.add_field(name=typeSearch[0]+" + "+typeSearch[1], value=stringItemLists[0])
        embed.add_field(name=typeSearch[0], value=stringItemLists[1])
        embed.add_field(name=typeSearch[1], value=stringItemLists[2])
    elif len(typeSearch) == 1:
        embed.add_field(name=typeSearch[0], value=stringItemLists[0])
    else: #Too many types input!
        embed.add_field(name="Error!", value="Only two types can be filtered for.")

    await ctx.channel.send(embed=embed)

@commands.command()
async def bphsearch(ctx, *, search:str):
    """Searches for Backpack Hero items and returns all containing the given keyword(s)."""
    #global itemNames
    items, itemNames, typeNames = readBpHItemJSON() #line temporary for use in Zako

    #if someone forgot to provide search arguments
    if search == "": await ctx.channel.send("No keywords? <:Nobackpack:964753218204733501>"); return
    
    #search for exact or partial matches
    search = search.lower()
    searchKW = search.split()
    exactMatches = []
    partialMatches = []
    approxMatches = []
    approxPartMatches = []
    for item in itemNames:
        #exact search - find the whole string in an item name
        if search in item.lower(): exactMatches.append(item); continue
        #fuzzy search - find an approximation of the whole string in an item name
        else:
            fuzzy = process.extractOne(search,[item])
            if fuzzy[1] >= 85: approxMatches.append(item); continue
            
        #if there's only one word, this is redundant and doesn't need to be done
        if len(searchKW) > 1:
            for kw in searchKW:
                #approximate search - find individual words from the string in an item name
                if kw in item.lower(): partialMatches.append(item); break
                #approximate fuzzy search - find approximations of individual words from the string in an item name
                else:
                    fuzzy = process.extractOne(kw,[item])
                    if item == "KNIGHT'S ARMOR":
                        text.debug(fuzzy[1])
                    if fuzzy[1] >= 70: approxPartMatches.append(item)
    resultLists = [exactMatches, partialMatches, approxMatches, approxPartMatches]
    text.debug(resultLists)
    #Turning item list into str
    stringItemLists = []
    for resultList in resultLists:
        #check to see if there are any items in this list
        if len(resultList) == 0:
            stringItemLists.append(None)
            continue
        #stringify list
        stringItemList = ""
        for item in resultList:
            item = capwords(item)
            if len(stringItemList + item + ", ") <= 1021: stringItemList += item + ", "
            elif len(stringItemList + item + ", ") > 1021: stringItemList += "..."
        #clipping off trailing comma at end of list if it does manage to fit in embed field after all
        if stringItemList[-2:] == ", ":
            stringItemList = stringItemList[:-2]
        stringItemLists.append(stringItemList)

    #Building embed
    embed = discord.Embed(color=0xFF00FF, title="Item Search Results")
    if stringItemLists[0] != None: embed.add_field(name="Exact matches", value=stringItemLists[0], inline=False)
    if stringItemLists[1] != None: embed.add_field(name="Partial Matches", value=stringItemLists[1], inline=False)
    if stringItemLists[2] != None: embed.add_field(name="Approximate Matches", value=stringItemLists[2], inline=False)
    if stringItemLists[3] != None: embed.add_field(name="Approximate Partial Matches", value=stringItemLists[3], inline=False)
    if len(embed.fields) == 0: embed.add_field(name="Error!", value="No results.")

    await ctx.channel.send(embed=embed)
