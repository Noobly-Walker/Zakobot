import os
import json
from datetime import datetime
import shutil

from bot.UserData import UserData
from bot.ServerData import ServerData
from bot.ToolUtil import *

dataFile = os.path.dirname(os.path.abspath(__file__))
num = [1]

def get_global_file(filetype, filename): # Filetype = [table, user]
    return dataFile + '\\' + filetype + '\\' + filename


def get_user_data(discord_id) -> UserData:
    discord_id = str(discord_id)
    foundfile = False
    try:
        filename = get_global_file('user', discord_id + '.txt')
        user_data = UserData()
        if os.path.isfile(filename):
            with open(filename, 'r+') as file:
                data = json.loads(file.read())
                if type(data) == dict:
                    user_data.set_data(data)
                    foundfile = True
    except json.decoder.JSONDecodeError:
        os.chdir(dataFile+"\\backup")
        backup_snapshots = os.listdir()
        backup_snapshots.sort(reverse=True)
        for directory in backup_snapshots:
            thispath = os.path.dirname(os.path.abspath(directory))
            try:
                filename = f'{thispath}\\user\\{discord_id}.txt'
                user_data = UserData()
                if os.path.isfile(filename):
                    with open(filename, 'r+') as file:
                        data = json.loads(file.read())
                        if type(data) == dict:
                            user_data.set_data(data)
                            foundfile = True
                            break
            except json.decoder.JSONDecodeError:
                continue
    if not foundfile:
        user_data = "[BRICKED]"
    else:
        user_data.data['id'] = discord_id
    return user_data

def save_user_data(user_data: UserData):
    if len(user_data.data) < 3:
        raise("[ZAKO FILE_ERROR_HANDLER] I'm gonna stop you right there. (Blocked userdata wipe!)\n>\n>\n>\n>\n>\n>\n>\nPlease check the code, something's gone horribly wrong!")
        return
    with open(get_global_file('user', user_data.data['id'] + '.txt'), 'w+') as file:
        data = json.dumps(user_data.data, sort_keys=True, indent=4)
        file.write(data)

def get_server_data(discord_id) -> ServerData:
    discord_id = str(discord_id)
    filename = get_global_file('server', discord_id + '.txt')
    server_data = ServerData()
    if os.path.isfile(filename):
        with open(filename, 'r+') as file:
            data = json.loads(file.read())
            if type(data) == dict:
                server_data.set_data(data)
    server_data.data['id'] = discord_id
    return server_data


def save_server_data(server_data: ServerData):
    with open(get_global_file('server', server_data.data['id'] + '.txt'), 'w+') as file:
        data = json.dumps(server_data.data, sort_keys=True, indent=4)
        file.write(data)

def backup():
    try:
        os.mkdir(dataFile + f'\\backup\\{datetime.now().date()}')
        os.mkdir(dataFile + f'\\backup\\{datetime.now().date()}\\user')
        os.mkdir(dataFile + f'\\backup\\{datetime.now().date()}\\server')
    except FileExistsError:
        pass
    root_user = get_global_file("user", "")
    root_server = get_global_file("server", "")
    for root, dirs, files in os.walk(root_user):
        for file in files:
            try:
                shutil.copyfile(dataFile + f'\\user\\{file}', dataFile + f'\\backup\\{datetime.now().date()}\\user\\{file}')
            except FileExistsError:
                continue
    for root, dirs, files in os.walk(root_server):
        for file in files:
            
            try:
                shutil.copyfile(dataFile + f'\\server\\{file}', dataFile + f'\\backup\\{datetime.now().date()}\\server\\{file}')
            except FileExistsError:
                continue
            
