import asyncio
from discord.ext import commands

def __cmdl__():
    return ["ping", "echo"]

@commands.command()
async def ping(ctx):
    """Kinda like poking me in the shoulder to see if I\'m awake."""
    await ctx.send('Yes? Hello.')

@commands.command()
async def echo(ctx, *, string):
    """I will repeat whatever text is put into this command!"""
    await ctx.send(string)
