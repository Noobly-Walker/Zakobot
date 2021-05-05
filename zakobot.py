print('Starting up...')
import discord
from discord.ext import commands
import random
import os
import typing
from datetime import *
import sys
from discord.ext.commands import BadArgument
import math
import traceback
import shutil
import asyncio

print("Importing commands from file...")

dataFile = os.path.dirname(os.path.abspath(__file__))

print("Constructing bot instance...")
intents = discord.Intents(messages=True, guilds=True, members=True)
bot = commands.Bot(command_prefix="z/", description="Beta branch of Zako!", intents=intents)

print('Finding server...')
@bot.event
async def on_ready():  # Bot boot-up. Below text appears if it successfully boots.
    to_print = 'Logged in as ' + bot.user.name + ' with ID <' + str(bot.user.id) + '>'
    to_print += "\nLogged into {0} guilds.".format(len(bot.guilds))
    print(to_print)
    print('------')
        
## ----- Commands ----- ##
print('Loading commands...')

__cmdl__ = []
working_import = None
for root, dirs, files in os.walk("cmds"):
    for file in files:
        if "cpython-38.pyc" in file:
            continue
        file = file[:-3]
        print(f"> Loading commands from *\\cmds\\{file}.py...")
        exec(f"from cmds import {file}; working_import = {file}.__cmdl__()")
        for cmd in working_import:
            exec(f"__cmdl__.append(file+'.'+cmd)")
            print(f">> Found z/{cmd}.")
for cmd in __cmdl__:
    print(f"> Implementing {cmd}...")
    exec(f"bot.add_command({cmd})")

#this command is too important to leave anywhere else.
@bot.command(aliases=['reset', 'reboot', 'reload'])
async def restart(ctx): #Runs z/debug restart
    if str(user_data.data['id']) == '248641004993773569':
        mess = 'Zakobot is restarting!'
        await ctx.send(mess)
        print(mess)
        sys.exit(99999)
    else:
        out = 'You do not have permission to perform this action.'
        await ctx.send(out)

@bot.event
async def on_message(message):
    author = message.author
    if author.bot:
        return
    await bot.process_commands(message)

print("Loading error handler...")

@bot.event
async def on_command_error(ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Not a command. Do z/help for a list of commands.')
        return

    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'I lack the **{}** permission(s) needed to run this command.'.format(fmt)
        await ctx.send(_message)
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send('This command has been disabled.')
        return

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is on cooldown, please retry in {}s.".format(math.ceil(error.retry_after)))
        return

    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
        await ctx.send(_message)
        return

    if isinstance(error, commands.UserInputError):
        await ctx.send("Args are either too short or otherwise wrong for this command. Check z/help <command> and try again.")
        return

    if isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send('This command cannot be used in direct messages.')
        except discord.Forbidden:
            pass
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
        return

    # ignore all other exception types, but print them to stderr
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# ----- Bot Load Finalization ----- #
print('Inserting key...')
bot.run("ODA3NTkzMzIyMDMzOTcxMjMx.YB6P5A.rav6XypTqH3CRhVeypg5NuHNBP8")
print('Running!')
