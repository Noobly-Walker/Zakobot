import asyncio
from discord.ext import commands
import traceback
from util.SLHandle import *
from os.path import isdir,exists
from os import remove, walk
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import expol
from util.TextFormat import *
from cmds.cmd_tools import parenthesisFinder, calculatorFunct
from util.cmdutil import cmdutil
text = cmdutil()
PATH = load(".\\locals\\%PATH%")

def commandList():
    return [file]

def categoryDescription():
    return "Commands involving information storage."

        
@commands.command(aliases=['files'])
async def file(ctx, mode, filename="", *, texts=""):
    """A file management system! Take notes, save funny messages, and more!

Modes:
file read <filename> - Returns the content of the file, if allowed.
file write <filename> <permission> <texts> - Writes to a file, if allowed.
    File names cannot be larger than 50 characters.
    Files cannot be larger than 10,000 characters.
    May overwrite a file that already exists.
    In case of overwrite, permission need not be defined.
file append <filename> <texts> - Appends text to a file, if allowed.
    Files cannot be larger than 10,000 characters.
file delete <filename> - Deletes a file, if allowed. Deleted files cannot be recovered.
file modify <filename> <permission> - Modifies the permission state of a file.
file list <filter> - Lists files.

Permissions:
r - Read-only: anyone can read this file. Recommended permission mode.
ra - Read/Append: anyone can read or append to this file.
rw - Read/Write: anyone can read, write, or append to this file.
pb - Public: anyone can read, write, modify, or delete this file. Not recommended.
pv - Private: only the file's creator can read this file.
The creators of files always have full perms to do with files what they wish."""

    path = f"{PATH}\\library\\"
    modes = ["read", "write", "append", "delete", "modify", "list"]
    illegalChars = ["\\", "<", ">", ":", "\"", "/", "|", "?", "*"]
    illegalNames = ["con", "prn", "aux", "nul",
                    "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9", "com0",
                    "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9", "lpt0"]
    permissions = {
        "r": ["read"],
        "ra": ["read", "append"],
        "rw": ["read", "write", "append"],
        "pb": ["read", "write", "append", "modify", "delete"],
        "pv": []
        }

    mode = mode.lower()
    if mode not in modes: await ctx.send("Invalid mode."); return
    
    for char in illegalChars:
        if char in filename: filename.replace(char, "_") # removing illegal characters from the filename
        
    if filename.lower() in illegalNames: # outright blocking the creation of a file with an illegal name
        await ctx.send("Zako has encountered an exception with Windows.")
        await ctx.send("https://cdn.discordapp.com/attachments/304362989799079937/969152125605146665/unknown.png")
        return

    if "[ZAKO]" in filename and ctx.author.id != 248641004993773569:
        await ctx.send("The [ZAKO] tag in filename is reserved for Zako devs."); return

    texts = formatText(texts) # formatting text
    
    if mode != "list":
        if testForFile(filename+".json", path):
            file = loadJSON(filename+".json", path)
            userPermission = "pv" #no permission
            if file["id"] == str(ctx.author.id): userPermission = "pb" #full permission
            else: userPermission = file["permission"]
            if mode not in permissions[userPermission]: await ctx.send("You do not have permission to perform this action."); return
            if mode == "modify":
                if texts not in list(permissions.keys()): await ctx.send("Invalid permission."); return
                file["permission"] = texts[:2]
                await ctx.send("Permission updated.")
            if mode == "delete":
                remove(path+filename+".json")
                await ctx.send("File deleted.")
            if mode == "read":
                converter = commands.MemberConverter()
                user = await converter.convert(ctx, file["id"])
                await ctx.send('Loading file "' + filename.replace(".json", "") + '" by ' + user.name + '...\n===========================================')
                out = ""
                try:
                    await ctx.send(file["text"])
                except Exception: #either file length is too long or empty
                    if file["text"] == "": await ctx.send("<Read Error: Blank File>"); return
                    chunks, chunk_size = len(file["text"]), 2000
                    brokenFile = [ file["text"][i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
                    for page in brokenFile: await ctx.send(page)
            if mode == "write":
                if "http://" in texts or "https://" in texts: await ctx.send("Write failed: Possible hyperlink detected. Links are not allowed."); return
                file["text"] = texts
                await ctx.send("File overwritten.")
            if mode == "append":
                if "http://" in texts or "https://" in texts: await ctx.send("Append failed: Possible hyperlink detected. Links are not allowed."); return
                if len(file["text"]) + len(texts) > 10000: await ctx.send("Append failed: Resulting file too large."); return
                file["text"] += "\n" + texts
                await ctx.send("File appended.")
            if mode in ["write", "append", "modify"]:
                try: saveJSON(file, filename+".json", path)
                except Exception as e: await ctx.send(f"An unexpected error occurred when I attempted to save this file: {e}")
        elif mode != "write": await ctx.send("File not found."); return
        else: #mode IS write
            if "http://" in texts or "https://" in texts: await ctx.send("Append failed: Possible hyperlink detected. Links are not allowed."); return
            if texts[:2].replace(" ", "") not in list(permissions.keys()): await ctx.send("Invalid permission."); return
            if len(filename) > 50: await ctx.send("Filename is too long. Keep it down to 50 chars or less."); return
            file = {
                "id": str(ctx.author.id),
                "permission": texts[:2].replace(" ", ""),
                "text": texts[2:]
                }
            await ctx.send("File written.")
            try: saveJSON(file, filename+".json", path)
            except Exception as e: await ctx.send(f"An unexpected error occurred when I attempted to save this file: {e}")
    else: #mode is list
        try: filename = int(filename)
        except Exception: pass #filename is a filter
        fileList = []
        for root, dirs, files in walk(path):
            for file in files:
                fileTitle = file.replace(".json",'')
                fileData = loadJSON(fileTitle + ".json", path)
                filePerm = fileData["permission"]
                fileLength = str(len(fileData["text"]))

                try:
                    fileAuthor = loadJSON("playerNameDB.json", PATH)[fileData["id"]]
                except Exception as e:
                    fileAuthor = fileData["id"]
                
                fileList.append([fileTitle, fileAuthor, filePerm, fileLength])
        filteredList = []
        if type(filename) is int:
            i = (filename-1)*50
            while i < (filename)*50: #filter by page
                try:
                    filteredList.append(fileList[i])
                    i += 1
                except Exception: break #reached end of list
        else:
            i, j = 0, 0
            while i < 50:
                try:
                    for k in fileList[j]: #allows filtering by author, filename, or perms
                        if filename.lower() in k.lower():
                            filteredList.append(fileList[j])
                            i += 1
                            break
                    j += 1
                except Exception: break #reached end of list
        longestFileName = 5
        longestAuthorName = 7
        for i in filteredList: #getting spacing for strings
            longestFileName = max(longestFileName, len(i[0]))
            longestAuthorName = max(longestAuthorName, len(i[1]))
        printList = "```" + "Files".ljust(longestFileName+2) + "Author".ljust(longestAuthorName+2) + "Perm".center(4) + "  " + "Size".center(6) + "\n" + \
                    "="*(29 + longestFileName + longestAuthorName)
        if len(filteredList) > 0:
            for i in filteredList: printList += "\n" + i[0].ljust(longestFileName+2) + i[1].ljust(longestAuthorName+2) + i[2].center(4) + "  " + f"{i[3]}B".rjust(6)
        else: printList += "\nThere are no files to display."
        await ctx.send(printList + "```")
