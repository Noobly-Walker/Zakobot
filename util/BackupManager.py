from os import listdir
from os.path import exists,isdir,join
from shutil import copytree,copy2,SameFileError
from datetime import datetime
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from SLHandle import pathfind
from util.cmdutil import cmdutil
text = cmdutil()

def copy(src: str, dst: str):
    try:
        if isdir(src):
            dirname = src.split("\\")[-1]
            pathfind(dst+"\\"+dirname)
            copytree(src, dst+"\\"+dirname, dirs_exist_ok=True)
        else: copy2(src, dst)
    except SameFileError:
        pass

def createBackup(directory: str, files: list, backupFolder: str):
    """All files must be in the same directory."""
    now = datetime.now()
    destination = backupFolder + "\\" + now.strftime('%Y-%m-%d')
    pathfind(destination)
    for file in files:
        if not exists(directory + "\\" + file): text.warn("The file or directory \"{directory}\\{file}\" does not exist.")
        else:
            copy(directory + "\\" + file, destination)
            text.log(f"Created backup of \"{directory}\\{file}\", saved to \"{destination}\".")
    
def loadBackup(destination: str, backupFolder: str, date: str, *files: list):
    """Date must be in the format YYYY-MM-DD.
If *files is blank, then all possible files will be loaded."""
    pathfind(destination)
    if not isdir(backupFolder): text.warn(f"The directory \"{backupFolder}\" does not exist.")
    else:
        backup = backupFolder + "\\" + date
        if not isdir(backup): text.warn(f"There isn't a backup from {date}.")
        else:
            if len(files) == 0: #load full backup
                for file in listdir(backup):
                    copy(file, destination)
                    text.log(f"Loaded \"{file}\" from {date} backup, saved to \"{destination}\".")
            else: #load partial backup
                filelist = files[0]
                for file in filelist:
                    if not exists(backup + "\\" + file): text.warn(f"The file or directory \"{backup}\\{file}\" does not exist.")
                    else:
                        copy(backup + "\\" + file, destination)
                        text.log(f"Loaded \"{file}\" from {date} backup, saved to \"{destination}\".")

def loadLatestBackup(destination: str, backupFolder: str, *files: list):
    now = datetime.now()
    if not isdir(backupFolder): text.warn(f"The directory \"{backupFolder}\" does not exist.")
    else: loadBackup(destination, backupFolder, listdir(backupFolder)[-1], *files)
