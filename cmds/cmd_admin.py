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
local = loadJSON('.\\locals\\locals.json')

def commandList():
    return [kick, ban, role, server, curses, script, purge,
            announcechannel, censor, toggleimages, togglelinks,
            toggleemojis, ignorechannel, adminchannel, unban]

def categoryDescription():
    return "Administrator tools."
        
@commands.command()
async def kick(ctx, user, *, reason=None):
    """Kick people. Requires Kick Members permission."""
    try:
        if not ctx.message.author.guild_permissions.kick_members:
            await ctx.send("You do not have permission to perform this action.")
            return
        admin = GuilddataGetFile(ctx.guild, "admin.json")
        if admin["Admin Channel"] is not None:
            converter = commands.TextChannelConverter()
            adminChannel = await converter.convert(ctx, admin["Admin Channel"])
        converter = commands.MemberConverter()
        userobj = await converter.convert(ctx, user)
        await ctx.guild.kick(userobj)
        out = f"{userobj.name} was kicked from {ctx.guild.name}"
        if reason != None:
            out += f" for: {reason}"
        out += "."
        await adminChannel.send(out)
    except Exception as e:
        await ctx.send(f"Error: {e}")

@commands.command()
async def ban(ctx, user, *, reason=None):
    """Banish people. Requires Ban Members permission."""
    try:
        if not ctx.message.author.guild_permissions.ban_members:
            await ctx.send("You do not have permission to perform this action.")
            return
        admin = GuilddataGetFile(ctx.guild, "admin.json")
        if admin["Admin Channel"] is not None:
            converter = commands.TextChannelConverter()
            adminChannel = await converter.convert(ctx, admin["Admin Channel"])
        converter = commands.MemberConverter()
        userobj = await converter.convert(ctx, user)
        await ctx.guild.ban(userobj)
        out = f"{userobj.name} was banned from {ctx.guild.name}"
        if reason != None:
            out += f" for: {reason}"
        out += "."
        await adminChannel.send(out)
    except Exception as e:
        await ctx.send(f"Error: {e}")

@commands.command(aliases=['pardon'])
async def unban(ctx, *, user):
    """Pardon the banished. Requires Ban Members permission."""
    if not ctx.message.author.guild_permissions.ban_members:
        await ctx.send("You do not have permission to perform this action.")
        return
    admin = GuilddataGetFile(ctx.guild, "admin.json")
    if admin["Admin Channel"] is not None:
        converter = commands.TextChannelConverter()
        adminChannel = await converter.convert(ctx, admin["Admin Channel"])
    unbanned = None
    banlist = await ctx.guild.bans()
    for ban in banlist:
        target = ban.user
        if user in [target.name, target.name+"#"+target.discriminator, target.id]:
            await ctx.guild.unban(target)
            unbanned = target
    out = f"{unbanned.name} was unbanned from {ctx.guild.name}."
    await adminChannel.send(out)

@commands.command()
async def role(ctx, mode, user, role):
    """Give or take roles from people. Requires Manage Roles permission.
role <give|take> <user> <role>"""
    try:
        if not ctx.message.author.guild_permissions.manage_roles:
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
    if not ctx.message.author.guild_permissions.manage_guild and len(setting) > 0:
        await ctx.send("You do not have permission to perform this action.")
        return
    guildSettings = GuilddataGetFile(ctx.guild, "settings.json")
    guildStats = GuilddataGetFile(ctx.guild, "stats.json")
    guildAdmin = GuilddataGetFile(ctx.guild, "admin.json")
    channelConverter = commands.TextChannelConverter()
    announcementChannel = "(None)"
    adminChannel = "(None)"
    imageChannels = "(None)"
    linkChannels = "(None)"
    emojiChannels = "(None)"
    ignoredChannels = "(None)"
    censoredUsers = "(None)"

    if guildAdmin["Update Channel"] != None:
        announcementChannel = await channelConverter.convert(ctx, guildAdmin["Update Channel"])
        announcementChannel = "<#" + str(announcementChannel.id) + ">"

    if guildAdmin["Admin Channel"] != None:
        adminChannel = await channelConverter.convert(ctx, guildAdmin["Admin Channel"])
        adminChannel = "<#" + str(adminChannel.id) + ">"
    
    for i in range(len(guildAdmin["Image Blocked Channels"])):
        channel = await channelConverter.convert(ctx, guildAdmin["Image Blocked Channels"][i])
        guildAdmin["Image Blocked Channels"][i] = str(channel.id)
        
    for i in range(len(guildAdmin["Link Blocked Channels"])):
        channel = await channelConverter.convert(ctx, guildAdmin["Link Blocked Channels"][i])
        guildAdmin["Link Blocked Channels"][i] = str(channel.id)
        
    if len(guildAdmin["Image Blocked Channels"]) > 0: imageChannels = "<#" + ">, <#".join(guildAdmin["Image Blocked Channels"]) + ">"
    if len(guildAdmin["Link Blocked Channels"]) > 0: linkChannels = "<#" + ">, <#".join(guildAdmin["Link Blocked Channels"]) + ">"
    if len(guildAdmin["Emoji Blocked Channels"]) > 0: emojiChannels = "<#" + ">, <#".join(guildAdmin["Emoji Blocked Channels"]) + ">"
    if len(guildAdmin["Zako Ignored Channels"]) > 0: ignoredChannels = "<#" + ">, <#".join(guildAdmin["Zako Ignored Channels"]) + ">"
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
Admin Channel: {adminChannel}\n\
Image Blocked Channels: {imageChannels}\n\
Link Blocked Channels: {linkChannels}\n\
Emoji Blocked Channels: {emojiChannels}\n\
Zako Ignored Channels: {ignoredChannels}\n\
\n\
Censored Users: {censoredUsers}"
        modules = ""
        for setn in list(guildSettings.keys()):
            if setn in ["Counting", "Levels", "LvUpReacts", "PublicScripts", "GlobalLevel", "SomeonePing", "CharacterLimit",
                        "GetUpdates", "Prefix"]: modules += setn.ljust(10) + " = " + str(guildSettings[setn]) + "\n"
        embed = discord.Embed(title = f"__{ctx.guild.name} ({ctx.guild.id})__", color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
        embed.add_field(name=f"*=== Basic Info ===*", value=basic, inline=False)
        embed.add_field(name=f"*=== Admin Info ===*", value=admin, inline=False)
        embed.add_field(name=f"*=== Settings ===*", value=modules, inline=False)
        await ctx.send(embed=embed)
    else:
        if setting not in guildSettings: await ctx.send(f"Invalid setting. Do {local['prefix']}server for a list of settings."); return
        if type(guildSettings[setting]) is bool:
            if newValue == None: guildSettings[setting] = not guildSettings[setting]
            else:
                if str.lower(newValue) in ["yes", "on", "1", "true"]: newValue = True
                elif str.lower(newValue) in ["no", "off", "0", "false"]: newValue = False
                else: await ctx.send("Invalid boolean input."); return
                guildSettings[setting] = newValue
            await ctx.send("Updated. :thumbsup:")
        elif type(guildSettings[setting]) is int:
            if newValue == None: await ctx.send(f"Please provide an integer value for this setting."); return
            try: newValue = int(newValue)
            except Exception: await ctx.send(f"Please provide an integer value for this setting."); return
            guildSettings[setting] = newValue
            await ctx.send("Updated. :thumbsup:")
        elif type(guildSettings[setting]) is str:
            if newValue == None: await ctx.send(f"Please provide a string value for this setting."); return
            guildSettings[setting] = newValue
            await ctx.send("Updated. :thumbsup:")
                
        GuilddataSetFile(ctx.guild, "settings.json", guildSettings)

@commands.command()
async def curses(ctx, mode, word=""):
    """Prevents people from saying certain words you don't want said. Requires Manage Messages permission.
Modes: ban, unban, list"""
    if not ctx.message.author.guild_permissions.manage_messages:
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
async def announcechannel(ctx):
    """Sets this channel to be the channel announcements are posted to.
Requires Manage Messages permission."""
    if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send("You do not have permission to perform this action.")
        return
    admin = GuilddataGetFile(ctx.guild, "admin.json")
    if admin["Update Channel"] == str(ctx.channel.id):
        admin["Update Channel"] = None
        await ctx.send("This channel will no longer get announcements. :thumbsup:")
    else:
        admin["Update Channel"] = str(ctx.channel.id)
        await ctx.send("This channel will now get enabled announcements. :thumbsup:")
    GuilddataSetFile(ctx.guild, "admin.json", admin)

@commands.command()
async def adminchannel(ctx):
    """Sets this channel to be the channel admin notifications are posted to.
Requires Administrator permission."""
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send("You do not have permission to perform this action.")
        return
    admin = GuilddataGetFile(ctx.guild, "admin.json")
    if admin["Admin Channel"] == str(ctx.channel.id):
        admin["Admin Channel"] = None
        await ctx.send("This channel will no longer get admin notifications. :thumbsup:")
    else:
        admin["Admin Channel"] = str(ctx.channel.id)
        await ctx.send("This channel will get admin notifications. :thumbsup:")
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

@commands.command(aliases=["togimg", "togimage", "togimages", "toggleimage", "toggleimg", "toggleimgs"])
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

@commands.command(aliases=["togli", "toglink", "toglinks", "togglelink", "toggleli"])
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

@commands.command(aliases=["togem", "togemotes", "togemojis", "toggleemotes", "toggleem"])
async def toggleemojis(ctx):
    """Toggles whether emojis can be sent in this channel. Does not affect reactions.
People with Manage Messages are immune. Requires Manage Messages permission."""
    if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send("You do not have permission to perform this action.")
        return
    admin = GuilddataGetFile(ctx.guild, "admin.json")
    if str(ctx.channel.id) in admin["Emoji Blocked Channels"]:
        admin["Emoji Blocked Channels"].remove(str(ctx.channel.id))
        await ctx.send(f"Emojis can now be posted in this channel. :thumbsup:")
    else:
        admin["Emoji Blocked Channels"].append(str(ctx.channel.id))
        await ctx.send(f"Emojis can no longer be posted in this channel. :thumbsup:")
    GuilddataSetFile(ctx.guild, "admin.json", admin)

@commands.command(aliases=["ignore"])
async def ignorechannel(ctx):
    """Toggles whether I ignore commmands in this channel.
People with Manage Messages are immune. Requires Manage Messages permission."""
    if not ctx.message.author.guild_permissions.manage_messages:
        await ctx.send("You do not have permission to perform this action.")
        return
    admin = GuilddataGetFile(ctx.guild, "admin.json")
    if str(ctx.channel.id) in admin["Zako Ignored Channels"]:
        admin["Zako Ignored Channels"].remove(str(ctx.channel.id))
        await ctx.send(f"I will no longer ignore this channel. :thumbsup:")
    else:
        admin["Zako Ignored Channels"].append(str(ctx.channel.id))
        await ctx.send(f"I will now ignore this channel. :thumbsup:")
    GuilddataSetFile(ctx.guild, "admin.json", admin)

@commands.command()
async def purge(ctx, mode, quantity:int, var1=None, var2=None):
    """Clear large amounts of text! Requires Manage Messages permission.
No bot can delete messages older than 6 months.

Modes:
clear (quantity)          - Clears all messages
user (quantity) (userID)  - Clears messages from a user
"""
    if not ctx.message.author.guild_permissions.manage_messages:
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
  onMemberJoin             - Triggers whenever someone joins a guild
  onMemberLeave            - Triggers whenever someone leaves a guild
  function                 - Triggers whenever run
  
Output keywords:
  react (emote)            - Reacts to message
  send (string)            - Adds string to send buffer
  print                    - Sends string into discord and clears send buffer
  pull (varName)           - Combines contents of send buffer into a variable and clears the buffer
  br (int)                 - Inserts newline character into send buffer
  var (name) = (value)     - Creates a variable
  return (varName)         - Adds a variable's value to send buffer
  save (varName)           - Saves a variable to file
  load (varName)           - Loads a variable from file
  calc (varName), (string) - Does math, returns expol
  eval (varName), (case)   - Generic token; can do comparisons, math, and more
  if (case)                - Conditional token; every line after must have >> preceeding
  back                     - Must be at the end of every conditional block
  run (function)           - Triggers a function

Global Variables:
  serverName               - Returns the name of the server.
  serverID                 - Returns the ID of the server.
  memberCount              - Returns the number of unique accounts on the server.
  userCount                - Returns the number of real accounts on the server.
  botCount                 - Returns the number of bot accounts on the server.
  userName                 - Returns the name of the person who triggered the script.
  userNick                 - Returns the nickname of the person who triggered the script.
  userPing                 - Pings the person who triggered the script.
  userID                   - Returns the ID of the person who triggered the script.
  message                  - Returns the message that triggered the script, minus input.
  channelName              - Returns the name of the channel.
  channelID                - Returns the ID of the channel.
  printChannel             - Returns the ID of the channel that print prints to. Same as channelID by default.

Each output must be on a new line."""
    if not (GuilddataGetFileIndex(ctx.guild, "settings.json", "PublicScripts") or ctx.message.author.guild_permissions.manage_messages):
        out = "You do not have permission to perform this action."
        return
    if trigger not in ["onMessageIs", "onMessageHas", "onMemberJoin", "onMemberLeave", "function"]: 
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
    else: await ctx.send(f"Invalid mode. Use {local['prefix']}help script for a list of modes.")
    GuilddataSetFile(ctx.guild, f"scripts\\{trigger}.json", eventFile)
