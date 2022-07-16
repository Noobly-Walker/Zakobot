import asyncio
import discord
from discord.ext import commands
import traceback
from os.path import isdir,exists
from datetime import datetime
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.GuildDataHandler import *
from util.PlayerDataHandler import *
from util.SLHandle import *
from util.ColorUtil import rectColor
from util.expol import expol
from util.DataHandlerUtil import *
from util.cmdutil import cmdutil
text = cmdutil()

def _cmdl_():
    return ["kick", "ban", "role", "server", "curses", "script", "purge",
            "getupdates", "censor", "toggleimages", "togglelinks"]

def _catdesc_():
    return "Administrator tools."
        
@commands.command()
async def kick(ctx, user, *, reason=None):
    """Kick people. Requires Kick Members permission."""
    try:
        if reason == "devBypass" and ctx.author.id == 248641004993773569:
            await ctx.send(f"**¿!¡? Alert ¡?¿!**\n{ctx.author.name} assuming my permission rank.")
        elif not ctx.message.author.guild_permissions.kick_members:
            await ctx.send("You do not have permission to perform this action.")
            return
        converter = commands.MemberConverter()
        userobj = await converter.convert(ctx, user)
        await ctx.guild.kick(userobj)
        out = f"{userobj.name} was kicked from {ctx.guild.name}"
        if reason != None:
            out += f" for: {reason}"
        out += "."
    except Exception as e:
        out = f"Error: {e}"
    await ctx.send(out)

@commands.command()
async def ban(ctx, user, *, reason=None):
    """Banish people. Requires Ban Members permission."""
    try:
        if reason == "devBypass" and ctx.author.id == 248641004993773569:
            await ctx.send(f"**¿!¡? Alert ¡?¿!**\n{ctx.author.name} assuming my permission rank.")
        elif not ctx.message.author.guild_permissions.ban_members:
            await ctx.send("You do not have permission to perform this action.")
            return
        converter = commands.MemberConverter()
        userobj = await converter.convert(ctx, user)
        await ctx.guild.ban(userobj)
        out = f"{userobj.name} was banned from {ctx.guild.name}"
        if reason != None:
            out += f" for: {reason}"
        out += "."
    except Exception as e:
        out = f"Error: {e}"
    await ctx.send(out)

@commands.command()
async def role(ctx, mode, user, role, *args):
    """Give or take roles from people. Requires Manage Roles permission.
z/role <give|take> <user> <role>"""
    try:
        if len(args) == 1:
            if args[0] == "devBypass" and ctx.author.id == 248641004993773569:
                await ctx.send(f"**¿!¡? Alert ¡?¿!**\n{ctx.author.name} assuming my permission rank.")
        elif not ctx.message.author.guild_permissions.manage_roles:
            await ctx.send("You do not have permission to perform this action.")
            return
        memberconverter = commands.MemberConverter()
        userobj = await memberconverter.convert(ctx, user)
        roleconverter = commands.RoleConverter()
        roleobj = await roleconverter.convert(ctx, role)
        if mode == 'give':
            await userobj.add_roles(roleobj)
            out = f"{user} was given {role}."
        elif mode == 'take':
            await userobj.remove_roles(roleobj)
            out = f"{role} was removed from {user}."
        else: out = "Invalid mode. Valid modes are: give, take"
    except Exception as e:
        out = f"Error: {e}"
    await ctx.send(out)

@commands.command()
async def server(ctx, setting="", newValue=None):
    """Change how Zako interacts with your server! Requires Manage Guild permission."""
    if setting == "devBypass" and ctx.author.id == 248641004993773569:
        await ctx.send(f"**¿!¡? Alert ¡?¿!**\n{ctx.author.name} assuming my permission rank.")
        setting = ""
    elif not ctx.message.author.guild_permissions.manage_guild and len(setting) > 0:
        await ctx.send("You do not have permission to perform this action.")
        return
    guildSettings = GuilddataGetFile(ctx.guild, "settings.json")
    guildStats = GuilddataGetFile(ctx.guild, "stats.json")
    guildAdmin = GuilddataGetFile(ctx.guild, "admin.json")
    channelConverter = commands.TextChannelConverter()
    announcementChannel = "(None)"
    imageChannels = "(None)"
    linkChannels = "(None)"
    censoredUsers = "(None)"

    if guildAdmin["Update Channel"] != None:
        announcementChannel = await channelConverter.convert(ctx, guildAdmin["Update Channel"])
        announcementChannel = "<#" + str(announcementChannel.id) + ">"
    
    for i in range(len(guildAdmin["Image Blocked Channels"])):
        channel = await channelConverter.convert(ctx, guildAdmin["Image Blocked Channels"][i])
        guildAdmin["Image Blocked Channels"][i] = str(channel.id)
        
    for i in range(len(guildAdmin["Link Blocked Channels"])):
        channel = await channelConverter.convert(ctx, guildAdmin["Link Blocked Channels"][i])
        guildAdmin["Link Blocked Channels"][i] = str(channel.id)
        
    if len(guildAdmin["Image Blocked Channels"]) > 0: imageChannels = "<#" + ">, <#".join(guildAdmin["Image Blocked Channels"]) + ">"
    if len(guildAdmin["Link Blocked Channels"]) > 0: linkChannels = "<#" + ">, <#".join(guildAdmin["Link Blocked Channels"]) + ">"
    memberConverter = commands.MemberConverter()
    
    for i in range(len(guildAdmin["Censored Users"])):
        user = await memberConverter.convert(ctx, guildAdmin["Censored Users"][i])
        guildAdmin["Censored Users"][i] = user.name
        
    if len(guildAdmin["Censored Users"]) > 0: censoredUsers = ", ".join(guildAdmin["Censored Users"])
    
    if setting == "":
        ts = datetime.timestamp(datetime.now())
        basic = f"Total visible accounts (this guild): {guildStats['Members']}\n\
> Members: {guildStats['Users']} ({guildStats['Users']/guildStats['Members']*100:.1f}%)\n\
> Bots: {guildStats['Bots']} ({guildStats['Bots']/guildStats['Members']*100:.1f}%)\n\
\n\
Server Activity Statistics\n\
> Messages sent: {guildStats['Messages Sent']}\n\
> Average Msgs/dy (60d): {get60DayActivity(guildStats):.3f}\n\
> Average Msgs/dy (all time): {getActivity(guildStats):.3f}\n\
> Rating: {getActivityRating(ctx.guild)}\n\
\n\
Account Creation: {getAcctAgeYMDAsStr(guildStats)} ago\n\
\n\
Counting Done (Guild): {expol(guildStats['Counting Done']):{GetNotationCode(ctx.author)}}"

        admin = f"Announcement Channel: {announcementChannel}\n\
Image Blocked Channels: {imageChannels}\n\
Link Blocked Channels: {linkChannels}\n\
\n\
Censored Users: {censoredUsers}"
        modules = ""
        for setn in list(guildSettings.keys()):
            if setn in ["Counting", "Levels", "LvUpReacts", "PublicEvents"]: modules += setn.ljust(10) + " = " + str(guildSettings[setn]) + "\n"
        embed = discord.Embed(title = f"__{ctx.guild.name} ({ctx.guild.id})__", color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"*=== Basic Info ===*", value=basic, inline=False)
        embed.add_field(name=f"*=== Admin Info ===*", value=admin, inline=False)
        embed.add_field(name=f"*=== Modules ===*", value=modules, inline=False)
        await ctx.send(embed=embed)
    else:
        if setting not in guildSettings: await ctx.send("Invalid setting. Do z/server for a list of settings."); return
        if type(guildSettings[setting]) is bool:
            if newValue == None: guildSettings[setting] = not guildSettings[setting]
            else: guildSettings[setting] = bool(newValue)
            await ctx.send("Updated. :thumbsup:")
        GuilddataSetFile(ctx.guild, "settings.json", guildSettings)

@commands.command()
async def curses(ctx, mode, word="", newValue=None):
    """Prevents people from saying certain words you don't want said. Requires Manage Messages permission.
Modes: ban, unban, list"""
    if word == "devBypass" and ctx.author.id == 248641004993773569:
        await ctx.send(f"**¿!¡? Alert ¡?¿!**\n{ctx.author.name} assuming my permission rank.")
        word = newValue
    elif not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send("You do not have permission to perform this action.")
        return
    word = str.lower(word)
    guildCurses = GuilddataGetFile(ctx.guild, "curses.json")
    if mode == "ban":
        if word in guildCurses: await ctx.send("That word is already banned.")
        else: guildCurses.append(word); await ctx.send("That word is now banned. :thumbsup:")
    elif mode == "unban":
        if word not in guildCurses: await ctx.send("That word isn't banned.")
        else: guildCurses.remove(word); await ctx.send("That word is no longer banned. :thumbsup:")
    elif mode == "list":
        out = ", ".join(guildCurses)
        if out == "": out = "(none to show)"
        await ctx.send("Banned words: " + out)
    GuilddataSetFile(ctx.guild, "curses.json", guildCurses)

@commands.command()
async def getupdates(ctx):
    """Sets this channel to be the channel Zako updates and announcements are posted to.
Requires Manage Messages permission."""
    if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send("You do not have permission to perform this action.")
        return
    admin = GuilddataGetFile(ctx.guild, "admin.json")
    if admin["Update Channel"] == str(ctx.channel.id):
        admin["Update Channel"] = None
        await ctx.send("This channel will no longer get updates on Zako. :thumbsup:")
    else:
        admin["Update Channel"] = str(ctx.channel.id)
        await ctx.send("This channel will get updates on Zako. :thumbsup:")
    GuilddataSetFile(ctx.guild, "admin.json", admin)

@commands.command()
async def censor(ctx, user):
    """Any censored users will have their messages deleted. For when someone needs to sit down and shut up.
People with Manage Messages are immune. Requires Manage Messages permission."""
    if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send("You do not have permission to perform this action.")
        return
    admin = GuilddataGetFile(ctx.guild, "admin.json")
    converter = commands.MemberConverter()
    user = await converter.convert(ctx, user)
    if str(user.id) in admin["Censored Users"]:
        admin["Censored Users"].remove(str(user.id))
        await ctx.send(f"**{user.name}** is no longer getting censored. :thumbsup:")
    else:
        admin["Censored Users"].append(str(user.id))
        await ctx.send(f"**{user.name}** will be censored. :thumbsup:")
    GuilddataSetFile(ctx.guild, "admin.json", admin)

@commands.command(aliases=["togimg"])
async def toggleimages(ctx):
    """Toggles whether images can be sent in this channel.
People with Manage Messages are immune. Requires Manage Messages permission."""
    if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send("You do not have permission to perform this action.")
        return
    admin = GuilddataGetFile(ctx.guild, "admin.json")
    if str(ctx.channel.id) in admin["Image Blocked Channels"]:
        admin["Image Blocked Channels"].remove(str(ctx.channel.id))
        await ctx.send(f"Images can now be posted in this channel. :thumbsup:")
    else:
        admin["Image Blocked Channels"].append(str(ctx.channel.id))
        await ctx.send(f"Images can no longer be posted in this channel. :thumbsup:")
    GuilddataSetFile(ctx.guild, "admin.json", admin)

@commands.command(aliases=["togli"])
async def togglelinks(ctx):
    """Toggles whether links can be sent in this channel.
People with Manage Messages are immune. Requires Manage Messages permission."""
    if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send("You do not have permission to perform this action.")
        return
    admin = GuilddataGetFile(ctx.guild, "admin.json")
    if str(ctx.channel.id) in admin["Link Blocked Channels"]:
        admin["Link Blocked Channels"].remove(str(ctx.channel.id))
        await ctx.send(f"Links can now be posted in this channel. :thumbsup:")
    else:
        admin["Link Blocked Channels"].append(str(ctx.channel.id))
        await ctx.send(f"Links can no longer be posted in this channel. :thumbsup:")
    GuilddataSetFile(ctx.guild, "admin.json", admin)

@commands.command()
async def purge(ctx, mode, quantity:int, var1=None, var2=None):
    """Clear large amounts of text! Requires Manage Messages permission.
No bot can delete messages older than 6 months.

Modes:
clear (quantity)          - Clears all messages
user (quantity) (userID)  - Clears messages from a user
"""
    if var1 == "devBypass" and ctx.author.id == 248641004993773569:
        await ctx.send(f"**¿!¡? Alert ¡?¿!**\n{ctx.author.name} assuming my permission rank.")
        var1 = var2
    elif not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send("You do not have permission to perform this action.")
        return
    deleted = 0
    if mode == "clear":
        def compareID(m):
            return m.id != ctx.message.id
        q = quantity+1
        try:
            while q > 0:
                d = await ctx.channel.purge(limit=min(q, 100), check=compareID)
                deleted += len(d)
                q -= min(q, 100)
        except discord.errors.NoMoreItems: pass
    elif mode == "user":
        def compareID(m):
            return m.author.id == int(var1) and m.id != ctx.message.id
        deleted = 0
        q = quantity
        try:
            while q > 0:
                d = await ctx.channel.purge(limit=min(q, 100), check=compareID)
                deleted += len(d)
                q -= min(q, 100)
        except discord.errors.NoMoreItems: pass
    await discord.Message.delete(ctx.message)
    await ctx.send(f"Deleted {deleted} messages! :thumbsup:")

@commands.command(aliases=["scripts", "scr"])
async def script(ctx, mode, trigger, _input="", *, output=""):
    """Program the bot to do stuff! Supports formatting.

Modes:
  add                      - Adds a script
  remove, delete, rem, del - Removes a script
  list                     - Lists all scripts
  view, display, dis       - Views an script's code
  
Triggers:
  onMessageIs              - Triggers whenever someone sends a message that matches desired input
  onMessageHas             - Triggers whenever someone sends a message that contains desired input
  function                 - Triggers whenever run
  
Output keywords:
  react (emote)            - Bot reacts to message
  send (string)            - Bot replies to message
  print                    - Bot sends string into discord and clears send buffer
  pull (varName)           - Bot combines contents of send buffer into a variable and clears the buffer
  br (int)                 - Inserts newline character
  var (name) = (value)     - Bot creates a variable
  return (varName)         - Bot prints a variable's value
  save (varName)           - Bot saves a variable
  load (varName)           - Bot loads a variable
  calc (varName), (string) - Does math, returns expol
  eval (varName), (case)   - Generic token; can do comparisons, math, and more
  if (case)                - Conditional token; every line after must have >> preceeding
  back                     - Must be at the end of every conditional block
  run (function)           - Triggers a function

Global Variables:
  serverName               - Returns the name of the server
  serverID                 - Returns the ID of the server
  memberCount              - Returns the number of unique accounts on the server
  userCount                - Returns the number of real accounts on the server
  botCount                 - Returns the number of bot accounts on the server
  userName                 - Returns the name of the person who triggered the script
  userNick                 - Returns the nickname of the person who triggered the script
  userPing                 - Pings the person who triggered the script
  userID                   - Returns the ID of the person who triggered the script
  message                  - Returns the message that triggered the script, minus input.

Each output must be on a new line."""
    if not (GuilddataGetFileIndex(ctx.guild, "settings.json", "PublicScripts") or ctx.message.author.guild_permissions.manage_messages):
        out = "You do not have permission to perform this action."
        return
    if trigger not in ["onMessageIs", "onMessageHas", "function"]: 
        await ctx.send("This trigger isn't valid.")
    eventFile = GuilddataGetFile(ctx.guild, f"scripts\\{trigger}.json")
    if mode == "add":
        kws = output.split("\n")
        for kw in range(len(kws)): kws[kw] = kws[kw].strip()
        if _input in list(eventFile.keys()):
            eventFile[_input] = kws
            await ctx.send(f"{trigger} script '{_input}' modified. :thumbsup:")
        else:
            eventFile[_input] = kws
            await ctx.send(f"{trigger} script '{_input}' added. :thumbsup:")
    elif mode in ["remove", "delete", "rem", "del"]:
        if _input not in list(eventFile.keys()):
            await ctx.send(f"{trigger} script '{_input}' doesn't exist."); return
        del eventFile[_input]
        await ctx.send(f"{trigger} script '{_input}' deleted. :thumbsup:")
    elif mode == "list":
        if len(eventFile) > 0:
            inputs = []
            outputs = []
            for event in eventFile:
                inputs.append(event)
                outputs.append(f"{len(eventFile[event])} lines")
            embed = discord.Embed(title=f"{trigger} Events", color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
            embed.add_field(name="Inputs", value="\n".join(inputs))
            embed.add_field(name="Outputs", value="\n".join(outputs))
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No {trigger} scripts to show.")
    elif mode in ["view", "dis", "display"]:
        if _input not in list(eventFile.keys()):
            await ctx.send(f"{trigger} script '{_input}' doesn't exist."); return
        await ctx.send(f"{trigger} Script '{_input}':\n> " + "\n> ".join(eventFile[_input]))
    else: await ctx.send("Invalid mode. Use z/help script for a list of modes.")
    GuilddataSetFile(ctx.guild, f"scripts\\{trigger}.json", eventFile)