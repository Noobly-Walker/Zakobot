import os
from bot.ShopHandler import *
from bot.UserData import *
from bot.ResourceParse import *
from data.FileHandler import *
from bot.ToolUtil import *
import discord
from discord.ext import commands

async def shop(ctx: commands.Context, user_data: UserData, args, crafted: bool):
    if len(args) == 0:
        page = 1
    else:
        page = int(args[0])
    if crafted:
        title = "Craft Items"
    else:
        title = "Global Shop"
    embed = discord.Embed(title=title, description="Page " + str(page), color=0x8000FF)
    purchaseables = []
    for shop_item in ShopItem.shop_items:
        if shop_item.is_visible(user_data, crafted):
            purchaseables.append(shop_item)
    for i in range(page * 10 - 10, page * 10):
        if i >= len(purchaseables):
            break
        shop_item = purchaseables[i]
        embed.add_field(name=shop_item.get_id(), value=shop_item.get_text(), inline=False)
    if len(embed.fields) == 0:
        if crafted:
            embed.add_field(name="Error!", value="You cannot craft anything!")
        else:
            embed.add_field(name="Error!", value="You cannot buy anything!")
    await ctx.send(embed=embed)


async def show_cost(ctx: commands.Context, user_data: UserData, args, crafted: bool):
    if len(args) == 0:
        await ctx.send("No recipe provided. Why'd this function get invoked, anyway?")
        return
    if crafted:
        title = "Recipe"
    else:
        title = "Price Tag"
    embed = discord.Embed(title=title, color=0x8000FF)
    cost = None
    for item in ShopItem.shop_items:
        if item.same_id(args):
            cost = item
    if cost == None:
        embed.add_field(name="Error!", value="Unknown item.")
    else:
        embed.add_field(name=cost.get_id(), value=cost.get_text(), inline=False)
    if len(embed.fields) == 0:
        if crafted:
            embed.add_field(name="Error!", value="Unknown error occurred that led to a blank embed.")
        else:
            embed.add_field(name="Error!", value="Unknown error occurred that led to a blank embed.")
    await ctx.send(embed=embed)


async def buy(ctx: commands.Context, user_data: UserData, args, crafted: bool):
    if len(args) == 0:
        await ctx.send("Please input a shop item ID!")
        return
    shop_id = args
    shop_item = None
    for item in ShopItem.shop_items:
        if item.same_id(shop_id):
            shop_item = item
            break
    if shop_item is None:
        if crafted:
            await ctx.send("Invalid Recipe!")
        else:
            await ctx.send("Invalid Shop Item!")
        return "HALT"
    if not shop_item.can_buy(user_data, crafted):
        if crafted:
            await ctx.send("You cannot craft that!")
        else:
            await ctx.send("You cannot buy that!")
        return "HALT"
    shop_item.buy(user_data, crafted)
    ShopItem.infinite_autocraft_all(user_data) #Autocrafting disabled. It does not save!
    if crafted:
        await ctx.send("Successfully crafted {}".format(shop_item.name))
    else:
        await ctx.send("Successfully bought {}".format(shop_item.name))
    return "OK"
