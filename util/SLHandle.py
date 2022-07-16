from os import mkdir,remove
from os.path import isdir,exists
import json
from json import dump
from json import load as jload
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.cmdutil import cmdutil
text = cmdutil()

def pathfind(path: str):
    if not isdir(path):
        pathlist = path.split("\\")
        for i in range(len(pathlist)):
            if pathlist[i] == "": pathlist.pop(i)
        toVerify = ""
        for j in pathlist:
            toVerify += j + "\\"
            if not isdir(toVerify):
                mkdir(toVerify)
                text.log(f"Created directory \"{toVerify}\" successfully.")

def testForFile(filename: str, *filepath: str):
    if len(filepath) > 0: path = filepath[0]
    else: path = "."
    if not isdir(path): return False
    elif not exists(path+"\\"+filename): return False
    else: return True

def save(filedata:str, filename: str, *filepath: str):
    if len(filepath) > 0:
        path = filepath[0]
        pathfind(path)
    else: path = "."
    save_file = open(path+"\\"+filename,"w")
    save_file.write(filedata)
    save_file.close()

def load(filename: str, *filepath: str):
    if len(filepath) > 0: path = filepath[0]
    else: path = "."
    if not isdir(path): text.warn(f"LoadError: The path \"{path}\" is invalid.")
    elif not exists(path+"\\"+filename): text.warn(f"LoadError: The file \"{path}\\{filename}\" does not exist.")
    else:
        file = open(path+"\\"+filename,"r")
        fileData = file.read()
        file.close()
        return fileData

def saveJSON(filedata:str, filename: str, *filepath: str):
    if len(filepath) > 0:
        path = filepath[0]
        pathfind(path)
    else: path = "."
    with open(path+"\\"+filename,"w") as file:
        dump(filedata, file)

def loadJSON(filename: str, *filepath: str):
    if len(filepath) > 0: path = filepath[0]
    else: path = "."
    if not isdir(path): text.warn(f"LoadJSONError: The path \"{path}\" is invalid.")
    elif not exists(path+"\\"+filename): text.warn(f"LoadJSONError: The file \"{path}\\{filename}\" does not exist.")
    else:
        try:
            with open(path+"\\"+filename,"r") as file:
                return jload(file)
        except json.decoder.JSONDecodeError:
            text.warn(f"File {filepath}\\{filename} is corrupted.")
            return

def delete(filename: str, *filepath: str):
    if len(filepath) > 0: path = filepath[0]
    else: path = "."
    if not isdir(path): text.warn(f"DeleteError: The path \"{path}\" is invalid.")
    elif not exists(path+"\\"+filename): text.warn(f"DeleteError: The file \"{path}\\{filename}\" does not exist.")
    else:
        remove(path+"\\"+filename)
        text.log(f"File \"{path}\\{filename}\" successfully deleted.")
