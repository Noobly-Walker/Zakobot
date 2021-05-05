from datetime import *
from setup import Config
import os

prefix = Config().read_config('config.txt')['bot_info']['prefix']

num = [0]
def breakpoint(comment=""):
    print("Point ", num[0], ": ", datetime.now().time(), "\t\tComment: ",comment)
    num[0] = num[0] + 1

def openfile(path, mode):
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file = open(base + "\\" + path, mode)
    return file

def bool_emoji(boolean):
    if boolean == True:
        return ':white_check_mark:'
    elif boolean == False:
        return ':x:'
    else:
        return ':grey_question:'
    
def lcd_translate(input_string, library):
    lcditem = ''
    libs = {'lcd':lcd,'lcdr':lcdr}
    font = libs[library]
    for letter in input_string:
        try:
            lcditem += font[letter]
        except Exception:
            lcditem += letter
    return lcditem

def fetch(dictionary, entry):
    result = "dictionary"
    for each in entry.split(","):
        result += f"[{each}]"
    return eval(result)
