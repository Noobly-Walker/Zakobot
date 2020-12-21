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

print('Importing files...')
print('> .\\data\\FileHandler.py', end="")
from data.FileHandler import *
print("\r> .\\LoadUserData.py\\load_all_users()" + " "*20, end="")
from LoadUserData import load_all_users
print("\r> .\\bot\\Purchases.py" + " "*20, end="")
from bot import Purchases
print("\r> .\\bot\\ShopItems.py" + " "*20, end="")
from bot import ShopItems
print("\r> .\\bot\\CraftItems.py" + " "*20, end="")
from bot import CraftItems
print("\r> .\\bot\\ShopHandler.py" + " "*20, end="")
from bot.ShopHandler import ShopItem as ShopHandler
print("\r> .\\bot\\ResourceParse.py" + " "*20, end="")
from bot import ResourceParse
print("\r> .\\bot\\PotionRandomizer.py" + " "*20, end="")
from bot import PotionRandomizer
print("\r> .\\bot\\ServerData.py" + " "*20, end="")
from bot import ServerData
print("\r> .\\bot\\NumberCronch.py\\*" + " "*20, end="")
from bot.NumberCronch import *
print("\r> .\\bot\\ToolUtil.py\\*" + " "*20, end="")
from bot.ToolUtil import *
print("\r> .\\setup.py\\Config()" + " "*20, end="")
from setup import Config
print('\rReading config...' + " "*20)
config = Config()
config.read_config('config.txt')
dev_info = config.dev_info
bot_info = config.bot_info
prefix = bot_info['prefix']
if "<update>" in bot_info['desc']:
    array = bot_info['desc'].split("<update>")
    desc = ''
    for i in range(len(array)-1):
        desc += array[i] + dev_info["version"]
    desc += array[-1]
else:
    desc = bot_info['desc']
botdata = get_user_data('405968021337669632')
#######################
#Config
mining_clover_event = False #True allows three clovers to be used
lootcrate_multi_event = True #True allows one Multi Crate to be opened per day
fast_stats = True #True replaces the Max Resources line in 'z!debug stats' with a pre-written string.
experience_rate = 1 #1 is default
global_event = "" #must be prefaced by newline if not blank
#######################
    
print('Fetching variables...')
## ----- Global Variables ----- ##
collection_names = ['Animal', 'Space', 'Weapon', 'Treasure', 'Medicine']
collItems = [':dog: Dog', ':cat: Cat', ':mouse: Mouse', ':rabbit: Rabbit', ':fox: Fox', ':sunny: Sun', ':crescent_moon: Moon', ':star: Star',
             ':earth_americas: Earth', ':ringed_planet: Saturn', ':axe: Axe', ':bomb: Bomb', '<:six_shooter:644544991955386400> Gun',
             ':firecracker: Firecracker', ':knife: Knife', ':money_with_wings: Flying Money', ':dollar: Dollar', ':moneybag: Moneybag',
             ':credit_card: Credit Card', ':gem: Diamond', ':microbe: Microbe', ':dna: DNA', ':syringe: Syringe', ':pill: Pill',
             ':microscope: Microscope']
user_name = {
    437527904486686730 : 'Voltê',
    158360754041389056 : 'Nitsche',
    333858113121812481 : 'DiFiCL',
    200697539467542528 : 'Zecca',
    281278537883713539 : 'Niko',
    626814739254607922 : 'Beiderman',
    411338364931801108 : 'Kai',
    422596200206827531 : 'Ender',
    300703483957477388 : 'Unknown',
    614768116009795585 : 'Wenlock',
    343823737897877515 : 'Lunar',
    344990569556082718 : 'Sparky',
    506978561517944864 : 'Roman',
    569843596996378624 : 'Jane Cho',
    157162544472129536 : 'ReScott',
    325401372675801088 : 'Kyro',
    297296619877957632 : 'Giorno',
    465217371691548672 : 'Snevets',
    282790530994143232 : 'Christian',
    494680263088013312 : 'King',
    300420039255916547 : 'Ace',
    413262943665389579 : 'Franklin',
    324566300817096706 : 'Festiv',
    271149686377807872 : 'Vivic',
    580256574300225537 : 'Scripter',
    301108937602629634 : 'Johnson',
    145359213131071488 : 'Darby',
    463770349209649163 : 'Limburgian',
    247211036740943873 : 'Atomic',
    168618507746017280 : 'Zavalosa',
    212143378152816641 : 'Shiny',
    377244092599369729 : 'Pines',
    371192515086254081 : 'Noisyash',
    285948308487274498 : 'Mama',
    272146054726680587 : 'Iggy',
    234769983731662849 : 'Eliza',
    261339200832405504 : 'Karma',
    300416545744486400 : 'Eko',
    419115637110079488 : 'Data',
    165823885063880704 : 'Matthew',
    594977808703291402 : 'Asbestos',
    465634309609357333 : 'Squonkie',
    525182365828644874 : 'Wynesons',
    242459261106520064 : 'Silverwind',
    128696692735344641 : 'Kappa',
    283374697603661824 : 'Paw Lord',
    377121840373563395 : 'Echo',
    280481560052891653 : 'Voided',
    289142048056147968 : 'Dokego',
    190964732835004425 : 'Visurient',
    274985917347921925 : 'Supernerd',
    242115934918148096 : 'Cosmic',
    124549827739648001 : 'Chomp',
    517272448073465856 : 'Enigmont',
    590110055769309194 : 'ViL',
    162333443521249281 : 'Inoka',
    431282475818418187 : 'Caleb',
    208278773798273024 : 'Lucid',
    221619081701228548 : 'MacGeek',
    493223279780298752 : 'Fury',
    274775575455989760 : 'ProtonFox',
    487322281404792842 : 'Saoshi',
    284459435152113664 : 'Meowstic Jones',
    290568916109885441 : 'Vi Foxe',
    611217574864355328 : 'Taurine',
    290329667985211404 : 'William',
    372200516953833502 : 'Maxx',
    651540318155440188 : 'Alex',
    420741085925736459 : 'RainbowStrings',
    578807817587392522 : 'Miyamoto',
    203142592957906944 : 'David',
    450649074258018306 : 'Adam',
    115191919708995586 : 'Bleach',
    432854305129758720 : 'Dr. K',
    585811085030981645 : 'Ancestor',
    260089613740146689 : 'Pitbuki',
    213330030342701056 : 'Siegfried',
    481610265197150228 : 'Shawn',
    282128189382328320 : 'Ryan',
    546712976950951936 : 'LatviaGamer',
    357582672262070272 : 'Damien',
    650977914635943957 : 'Midnite',
    660377013466562570 : 'Naofumi',
    282901939895795714 : 'Thom',
    399392114611585025 : 'Cody',
    399628469748760578 : 'Yeetmaster',
    272209285356716042 : 'Toyo',
    210237386171482113 : 'Cross',
    240017448118517761 : 'DM',
    239084267710316544 : 'Angel',
    135676575826837504 : 'Aislin',
    166981826219474944 : 'Charcoal',
    174298918413271040 : 'Shadow Knight',
    481192994574434315 : 'Kunzite',
    347866851977592833 : 'Placebo',
    194796337844191232 : 'Brandon',
    318839556072013825 : 'SkyChaser',
    234343413191933962 : 'Slate',
    107304072176013312 : 'Spirit Speaker',
    380847202916106250 : 'Irish King',
    239548418630877185 : 'Setnour',
    281079467588190208 : 'Kolambe',
    390617260567298062 : 'Iron',
    283495365284462593 : 'Corza',
    334573351085539330 : 'Chapter\'s End',
    191934024195768320 : 'Al',
    212053244992684042 : 'Kapriznyy',
    154064865084964865 : 'Om',
    296829886570561536 : 'Will the Axolotl',
    290980633524830208 : 'Richard',
    224667683076046848 : 'Pixel',
    190454985136275456 : 'Steph',
    301842365620944897 : 'Riverina',
    222474255697182720 : 'Ariel',
    401899199471419392 : 'Boneka'
    }
rank = {
    0 : 'user',
    1 : 'VIP',
    2 : 'VIP+',
    3 : 'Prem',
    4 : 'Elit',
    5 : 'Supr',
    6 : 'Ulti',
    7 : 'Ult+',
    }
alts = { # alt:main
    346836668852207626 : 344990569556082718,
    288105216413532161 : 205011703891623936,
    563204853023899668 : 611217574864355328,
    311558009061113858 : 248641004993773569,
    313004537491226625 : 300416545744486400,
    296430479043985408 : 300416545744486400,
    427951719813742593 : 377121840373563395,
    509006017644855297 : 272209285356716042,
    576362922134208523 : 585811085030981645,
    766798572673826826 : 205011703891623936
    }
lcd = {' ':ResourceParse.emojidata['0020'],'!':ResourceParse.emojidata['0021'],
       '"':ResourceParse.emojidata['0022'],'#':ResourceParse.emojidata['0023'],
       '$':ResourceParse.emojidata['0024'],'%':ResourceParse.emojidata['0025'],
       '&':ResourceParse.emojidata['0026'],"'":ResourceParse.emojidata['0027'],
       '(':ResourceParse.emojidata['0028'],')':ResourceParse.emojidata['0029'],
       '*':ResourceParse.emojidata['002A'],'+':ResourceParse.emojidata['002B'],
       ',':ResourceParse.emojidata['002C'],'-':ResourceParse.emojidata['002D'],
       '.':ResourceParse.emojidata['002E'],'/':ResourceParse.emojidata['002F'],
       '0':ResourceParse.emojidata['0030'],'1':ResourceParse.emojidata['0031'],
       '2':ResourceParse.emojidata['0032'],'3':ResourceParse.emojidata['0033'],
       '4':ResourceParse.emojidata['0034'],'5':ResourceParse.emojidata['0035'],
       '6':ResourceParse.emojidata['0036'],'7':ResourceParse.emojidata['0037'],
       '8':ResourceParse.emojidata['0038'],'9':ResourceParse.emojidata['0039'],
       ':':ResourceParse.emojidata['003A'],';':ResourceParse.emojidata['003B'],
       '<':ResourceParse.emojidata['003C'],'=':ResourceParse.emojidata['003D'],
       '>':ResourceParse.emojidata['003E'],'?':ResourceParse.emojidata['003F'],
       '@':ResourceParse.emojidata['0040'],'A':ResourceParse.emojidata['0041'],
       'B':ResourceParse.emojidata['0042'],'C':ResourceParse.emojidata['0043'],
       'D':ResourceParse.emojidata['0044'],'E':ResourceParse.emojidata['0045'],
       'F':ResourceParse.emojidata['0046'],'G':ResourceParse.emojidata['0047'],
       'H':ResourceParse.emojidata['0048'],'I':ResourceParse.emojidata['0049'],
       'J':ResourceParse.emojidata['004A'],'K':ResourceParse.emojidata['004B'],
       'L':ResourceParse.emojidata['004C'],'M':ResourceParse.emojidata['004D'],
       'N':ResourceParse.emojidata['004E'],'O':ResourceParse.emojidata['004F'],
       'P':ResourceParse.emojidata['0050'],'Q':ResourceParse.emojidata['0051'],
       'R':ResourceParse.emojidata['0052'],'S':ResourceParse.emojidata['0053'],
       'T':ResourceParse.emojidata['0054'],'U':ResourceParse.emojidata['0055'],
       'V':ResourceParse.emojidata['0056'],'W':ResourceParse.emojidata['0057'],           
       'X':ResourceParse.emojidata['0058'],'Y':ResourceParse.emojidata['0059'],
       'Z':ResourceParse.emojidata['005A'],'[':ResourceParse.emojidata['005B'],
       '\\':ResourceParse.emojidata['005C'],']':ResourceParse.emojidata['005D'],
       '^':ResourceParse.emojidata['005E'],'_':ResourceParse.emojidata['005F'],
       '`':ResourceParse.emojidata['0060'],'a':ResourceParse.emojidata['0061'],
       'b':ResourceParse.emojidata['0062'],'c':ResourceParse.emojidata['0063'],
       'd':ResourceParse.emojidata['0064'],'e':ResourceParse.emojidata['0065'],
       'f':ResourceParse.emojidata['0066'],'g':ResourceParse.emojidata['0067'],
       'h':ResourceParse.emojidata['0068'],'i':ResourceParse.emojidata['0069'],
       'j':ResourceParse.emojidata['006A'],'k':ResourceParse.emojidata['006B'],
       'l':ResourceParse.emojidata['006C'],'m':ResourceParse.emojidata['006D'],
       'n':ResourceParse.emojidata['006E'],'o':ResourceParse.emojidata['006F'],
       'p':ResourceParse.emojidata['0070'],'q':ResourceParse.emojidata['0071'],
       'r':ResourceParse.emojidata['0072'],'s':ResourceParse.emojidata['0073'],
       't':ResourceParse.emojidata['0074'],'u':ResourceParse.emojidata['0075'],
       'v':ResourceParse.emojidata['0076'],'w':ResourceParse.emojidata['0077'],
       'x':ResourceParse.emojidata['0078'],'y':ResourceParse.emojidata['0079'],
       'z':ResourceParse.emojidata['007A'],'{':ResourceParse.emojidata['007B'],
       '|':ResourceParse.emojidata['007C'],'}':ResourceParse.emojidata['007D'],
       '~':ResourceParse.emojidata['007E']}

lcdr = {'a':ResourceParse.emojidata['oc2_ay'],'b':ResourceParse.emojidata['oc2_be'],
       'c':ResourceParse.emojidata['oc2_ce'],'ч':ResourceParse.emojidata['oc2_che'],
       'd':ResourceParse.emojidata['oc2_de'],'e':ResourceParse.emojidata['oc2_eh'],
       'f':ResourceParse.emojidata['oc2_ef'],'g':ResourceParse.emojidata['oc2_ge'],
       'h':ResourceParse.emojidata['oc2_he'],'i':ResourceParse.emojidata['oc2_ie'],
       'j':ResourceParse.emojidata['oc2_je'],'k':ResourceParse.emojidata['oc2_ke'],
       'l':ResourceParse.emojidata['oc2_el'],'m':ResourceParse.emojidata['oc2_em'],
       'n':ResourceParse.emojidata['oc2_en'],'o':ResourceParse.emojidata['oc2_oh'],
       'p':ResourceParse.emojidata['oc2_pe'],'q':ResourceParse.emojidata['oc2_qe'],
       'r':ResourceParse.emojidata['oc2_ar'],'s':ResourceParse.emojidata['oc2_es'],
       't':ResourceParse.emojidata['oc2_te'],'u':ResourceParse.emojidata['oc2_uh'],
       'v':ResourceParse.emojidata['oc2_ve'],'w':ResourceParse.emojidata['oc2_wa'],
       'x':ResourceParse.emojidata['oc2_ex'],'y':ResourceParse.emojidata['oc2_wy'],
       'z':ResourceParse.emojidata['oc2_ze'],' ':ResourceParse.emojidata['oc2_voed'],
       '0':ResourceParse.emojidata['oc2_nil'],'1':ResourceParse.emojidata['oc2_un'],
       '2':ResourceParse.emojidata['oc2_duo'],'3':ResourceParse.emojidata['oc2_tre'],
       '4':ResourceParse.emojidata['oc2_qad'],'5':ResourceParse.emojidata['oc2_pent'],
       '6':ResourceParse.emojidata['oc2_hex'],'7':ResourceParse.emojidata['oc2_sept'],
       '8':ResourceParse.emojidata['oc2_okt'],'9':ResourceParse.emojidata['oc2_enn'],
       '.':ResourceParse.emojidata['oc2_pont'],',':ResourceParse.emojidata['oc2_koma'],
       '∞':ResourceParse.emojidata['oc2_lcdINF'],'þ':ResourceParse.emojidata['oc2_thorn'],
       '(':ResourceParse.emojidata['oc2_lcd('],')':ResourceParse.emojidata['oc2_lcd)'],
       '{':ResourceParse.emojidata['oc2_lcd{'],'}':ResourceParse.emojidata['oc2_lcd}'],
       '-':ResourceParse.emojidata['oc2_lcd-'],'_':ResourceParse.emojidata['oc2_lcd_'],
       '/':ResourceParse.emojidata['oc2_lcd/'],'\\':ResourceParse.emojidata['oc2_lcd\\'],
       ':':ResourceParse.emojidata['oc2_lcd:'],';':ResourceParse.emojidata['oc2_lcd;'],
       '!':ResourceParse.emojidata['oc2_lcd!'],'?':ResourceParse.emojidata['oc2_lcd?'],
       '+':ResourceParse.emojidata['oc2_lcd+'],'×':ResourceParse.emojidata['oc2_ex'],           
       '%':ResourceParse.emojidata['oc2_lcd%'],'&':ResourceParse.emojidata['oc2_lcd&'],
       '[':ResourceParse.emojidata['oc2_lcd['],']':ResourceParse.emojidata['oc2_lcd]'],
       '$':ResourceParse.emojidata['oc2_lcdDOLLAR'],'£':ResourceParse.emojidata['oc2_lcdPOUND'],
       '¥':ResourceParse.emojidata['oc2_lcdYEN'],'#':ResourceParse.emojidata['oc2_lcd#'],
       "'":ResourceParse.emojidata['oc2_lcd\''],'"':ResourceParse.emojidata['oc2_lcd"'],
       '^':ResourceParse.emojidata['oc2_lcd^'],'|':ResourceParse.emojidata['oc2_lcd|'],
       '*':ResourceParse.emojidata['oc2_lcd*'],'=':ResourceParse.emojidata['oc2_lcd='],
       'A':ResourceParse.emojidata['oc2_ay'],'B':ResourceParse.emojidata['oc2_be'],
       'C':ResourceParse.emojidata['oc2_ce'],'Ч':ResourceParse.emojidata['oc2_che'],
       'D':ResourceParse.emojidata['oc2_de'],'E':ResourceParse.emojidata['oc2_eh'],
       'F':ResourceParse.emojidata['oc2_ef'],'G':ResourceParse.emojidata['oc2_ge'],
       'H':ResourceParse.emojidata['oc2_he'],'I':ResourceParse.emojidata['oc2_ie'],
       'J':ResourceParse.emojidata['oc2_je'],'K':ResourceParse.emojidata['oc2_ke'],
       'L':ResourceParse.emojidata['oc2_el'],'M':ResourceParse.emojidata['oc2_em'],
       'N':ResourceParse.emojidata['oc2_en'],'O':ResourceParse.emojidata['oc2_oh'],
       'P':ResourceParse.emojidata['oc2_pe'],'Q':ResourceParse.emojidata['oc2_qe'],
       'R':ResourceParse.emojidata['oc2_ar'],'S':ResourceParse.emojidata['oc2_es'],
       'T':ResourceParse.emojidata['oc2_te'],'U':ResourceParse.emojidata['oc2_uh'],
       'V':ResourceParse.emojidata['oc2_ve'],'W':ResourceParse.emojidata['oc2_wa'],
       'X':ResourceParse.emojidata['oc2_ex'],'Y':ResourceParse.emojidata['oc2_wy'],
       'Z':ResourceParse.emojidata['oc2_ze'],'Þ':ResourceParse.emojidata['oc2_thorn']}

dataFile = os.path.dirname(os.path.abspath(__file__))

print('Fetching functions...')
## ----- Global Functions ----- ##

def openfile(path, mode):
    base = os.path.dirname(os.path.abspath(__file__))
    file = open(base + "\\" + path, mode)
    return file

def bool_emoji(boolean):
    if boolean == True:
        return ':white_check_mark:'
    elif boolean == False:
        return ':x:'
    else:
        return ':grey_question:'

def username(ctx, userid, *discord_data): #ctx = the unfiltered userdata, could be alt; userid = filtred user id
    player_data = get_user_data(userid)
    # find real name
    if player_data.realname() == '':
        try:
            player_data.data['realname'] = user_name[int(userid)]
        except Exception:
            player_data.data['realname'] = ctx.name
    realname = player_data.realname()
    # find nickname
    if player_data.nick() == '':
        name = realname
    else:
        name = '\*' + player_data.nick() + '\*'
    name = player_data.data['displayed badge'] + name
    return name, realname

def load_badges(player_data):
    realname = player_data.realname()
    if player_data.achievements()['TNG Overcharge'] > 0:
        #Nitro boost achievement
        player_data.add_badge(ResourceParse.emojidata['oc2_nitroboost'])
    if realname == 'Noobly' or realname == 'MacGeek' or realname == 'Ariel':
        #5th age legendaries
        player_data.add_badge(ResourceParse.emojidata['oc2_5th_age_legendary'])
    if realname == 'Bomboy' or realname == 'Pixel' or realname == 'Supernerd' or realname == 'Karma' or realname == 'Zecca' or realname == 'Minidragon':
        #6th age legendaries
        player_data.add_badge(ResourceParse.emojidata['oc2_6th_age_legendary'])
    if realname == 'Om' or realname == 'Ace' or realname == 'Toyo' or realname == 'Ryan' or realname == 'Riverina' or realname == 'Alex' or realname == 'Maxx' or realname == 'Echo' or realname == 'Paw Lord' or realname == 'Silverwind' or realname == 'Eko' or realname == 'Mama' or realname == 'Shiny' or realname == 'Sparky' or realname == 'Caleb' or realname == 'Steph':
        #7th age legendaries
        player_data.add_badge(ResourceParse.emojidata['oc2_7th_age_legendary'])
##    if name == '-----': # To be defined 51 Mar
##        #8th age legendaries
##        name = ResourceParse.emojidata['oc2_8th_age_legendary'] + name #Emoji doesn't exist.
    return player_data
    

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

def scan(text):
    list = text.split(' ')
    text = ''
    blacklist = ['http', 'www.', '.com', '.net', '.org', '.xyz', '@everyone', '@here']
    lcdtoggle = False
    lcdrtoggle = False
    for item in list:
        for word in blacklist:
            if word in item:
                text += '[REDACTED] '
                item = ''
                break
        if item[:2] == 'e!':
            emote = item[2:]
            item = ResourceParse.emojidata[emote]
        if '<timestamp>' in item:
            item = current_time()
        if item[:2] == '<@' or item[:3] == '\<@':
            item = '[REDACTED] '
        if item == '<lcd>':
            lcdtoggle = True
            lcdrtoggle = False
            continue
        if item in ['</lcd>', '</lcdr>']:
            lcdtoggle = False
            lcdrtoggle = False
            continue
        if item == '<lcdr>':
            lcdtoggle = False
            lcdrtoggle = True
            continue
        if lcdtoggle:
            lcditem = lcd_translate(item, 'lcd')
            text += lcditem + lcd[' ']
        elif lcdrtoggle:
            lcditem = lcd_translate(item, 'lcdr')
            text += lcditem + lcdr[' ']
        else:
            text += item + ' '
    return text

def treasure(remaining_deeds, treas): # Treasure, called when chests are to be opened in the mines or in loot crates.
    rupOut, silverOut, cloverOut, deedOut = 0, 0, 0, 0
    table_type = 'chest'
    memTable = open(get_global_file('table', table_type + '.txt'), 'r')
    memTable = memTable.readline()
    while treas > 0:
        treasHandle = random.randrange(20)
        memItem = memTable[treasHandle*9:treasHandle*9+4]
        memQuant = memTable[treasHandle*9+4:treasHandle*9+9]
        intQuant = int(memQuant)
        if memItem == 'Rupi':
            rupOut+=intQuant
        if memItem == 'Slvr':
            silverOut+=intQuant*1000
        if memItem == 'Clov':
            cloverOut+=intQuant
        if memItem == 'Land':
            if intQuant < remaining_deeds:
                deedOut += intQuant
                remaining_deeds -= intQuant
            elif intQuant >= remaining_deeds:
                deedOut += remaining_deeds
                remaining_deeds = 0
        treas -= 1
    rupOut = round(rupOut)
    silverOut = round(silverOut)
    cloverOut = round(cloverOut)
    deedOut = round(deedOut)
    return [rupOut, silverOut, cloverOut, deedOut]

def parseCollections(collType):  # Takes the list of strings and integers involving collectables and combines them into a list of strings
    item_message = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    global_lowest = 10000000000000
    local_lowest = [10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000]
    if type(collType[0]) == list:  # assume 2 dimensions. collType[x][y] is collection x, yth element.
        for i in range(0, 5):
            for j in range(0, 5):
                if collType[i][j] > 0:
                    index = 5*i + j
                    item_message[index] = '   {0}× {1}\n'.format(collType[i][j], collItems[index])
                if collType[i][j] < global_lowest:
                    global_lowest = collType[i][j]
                if collType[i][j] < local_lowest[i]:
                    local_lowest[i] = collType[i][j]
    else:  # array of 25 items, collType[5x + y] is collection x, yth element.
        for i in range(0,25):
            j = i//5
            if collType[i] > 0:
                item_message[i] = '   {0}× {1}\n'.format(collType[i], collItems[i])
            if collType[i] < global_lowest:
                global_lowest = collType[i]
            if collType[i] < local_lowest[j]:
                local_lowest[j] = collType[i]
    out_message = ""
    collection_message = ["", "", "", "", ""]
    for i in range(0, 5):
        for j in range(0, 5):
            index = i * 5 + j
            collection_message[i] += item_message[index]
        if collection_message[i] != '':
            out_message += '\n**' + collection_names[i] + f' Collection** - Completed {local_lowest[i]} times\n' + collection_message[i]
    if out_message != '':
        out_message += f"\n**All collections completed {global_lowest} times!**"
    else:
        out_message = '*<empty>*'
    return out_message

def dict_split2(dictin):
    d1 = dict(list(dictin.items())[:-(len(dictin)//-2)])
    d2 = dict(list(dictin.items())[-(len(dictin)//-2):])
    return d1, d2

def dict_split4(dictin):
    h1, h2 = dict_split2(dictin)
    d1, d2 = dict_split2(h1)
    d3, d4 = dict_split2(h2)
    return d1, d2, d3, d4

def parseInventory(ctx, inventory, submenu):
    out = ""
    out2 = ""
    subm = ""
    filtered = {}
    if submenu:
        subm = "|-» "
    for item in inventory:
        if type(inventory[item]) is int:
            if inventory[item] == 0:
                continue
            else:
                filtered[item] = inventory[item]
        elif type(inventory[item]) is list:
            if inventory[item][0] == 0:
                continue
            else:
                if len(inventory[item]) >= 2:
                    if inventory[item][1] == True:
                        filtered[item + ':star:'] = inventory[item][0]
                    else:
                        filtered[item] = inventory[item][0]
                else:
                    filtered[item] = inventory[item][0]
    user = testfor_alt(ctx.message.author.id)
    d1, d2 = dict_split2(filtered)
    for item in d1.keys():
        items = number_cronch(d1[item], user)
        out += subm + str(items) + "× " + item + '\n'
    for item in d2.keys():
        items = number_cronch(d2[item], user)
        out2 += subm + str(items) + "× " + item + '\n'
    if out == '' and out2 == '':
        out = '*<empty>*'
    if out != '' and out2 == '':
        out1 = out2
        out2 = '-----'
    return out, out2

def get_item_prices(): #only done once.
    base_price = max(get_all_user_sum('rupees')//100, 10000)
    meta_inv = get_all_user_inv()
    item_ct = len(meta_inv)
    item_no = 0
    percentage = int(item_no/item_ct*20)
    progress_bar = "[" + "\u2588"*percentage + " "*(20-percentage) + "]"
    minibar = [" ","\u258F","\u258E","\u258D","\u258C","\u258B","\u258A","\u2589",""]
    print(f"\r> {progress_bar} {item_no}/{item_ct}", end="")
    for item in meta_inv:
        item_no += 1
        quant = meta_inv[item]
        if quant > 0:
            price = base_price/quant
        else:
            price = 10001
        if price < 1:
            qpr = int(round(1/price))
            price = 1
        else:
            price = int(round(price))
            qpr = 1
        # Preparing display
        percentage = int(item_no/item_ct*160)
        percent = round(item_no/item_ct*100, 2)
        fudge = 0
        if 19-percentage//8 == -1:
            fudge = 1
        progress_bar = "[" + "\u2588"*(percentage//8) + minibar[(percentage)%8 - fudge] + " "*(19-percentage//8) + "]"
        #eta = int((item_ct-item_no)*0.55)
        #eta_txt = "{0}:{1:0>2}".format(eta//60, eta%60)
        print(f"\r> {progress_bar} Item {item_no} of {item_ct} - {percent: <5}% ({quant}×{item} @ {price}r per {qpr} items)" + " "*20, end="")
        botdata.data['prices'][item] = (quant, price, qpr)
    botdata.data['inflation'] = base_price
    save_user_data(botdata)

def add_items(userdata, dict_add: dict):
    base_price = botdata.data['inflation']
    for item in dict_add:
        userdata.data['inventory'][item][0] += dict_add[item][0]
        if userdata.data['inventory'][item][0] >= 3: #check to see if the user has enough items to be able to buy or dive for them
            userdata.inventory()[item][2] = True
        try: # Recalculating price.
            quant = botdata.data['prices'][item][0] + dict_add[item][0]
        except KeyError: # No price exists, emergency reload of price tables.
            quant = dict_add[item][0]
        if quant > 0:
            price = base_price/quant
        else:
            continue
        if price < 1:
            qpr = int(round(1/price))
            price = 1
        else:
            price = int(round(price))
            qpr = 1
        botdata.data['prices'][item] = (quant, price, qpr)
    save_user_data(botdata)
    return userdata

def parseAchievements(ctx, achievements):
    out = ""
    user = testfor_alt(ctx.message.author.id)
    for ach in achievements.keys():
        if achievements[ach] == 0:
            continue
        else:
            items = number_cronch(achievements[ach], user)
            out += ach + ' - Completed {} time(s)!\n'.format(items)
    if out == '':
        out = '*<empty>*'
    return out

def isFinished(crates): # A function used to determine if there are any crates left to open.
    for key in crates.keys():
        if(crates[key] > 0):
            return False # There are more unopened crates, aka is NOT Finished
    return True # There are no more unopened crates, aka isFinished

def testfor_alt(user):
    user = int(user)
    for key in alts.keys():
        if key == user:
            user = alts[key]
    user = str(user)
    return user

def get_all_user_sum(variable_name, *key):
    root_user = get_global_file("user", "")
    out = 0
    for root, dirs, files in os.walk(root_user):
        for file in files:
            file = file[:-4]  # Trim the .txt
            try:
                id = int(file)
            except ValueError:
                continue
            user = get_user_data(id)
            if isinstance(user.data.get(variable_name), (int, float)):
                out += user.data.get(variable_name)
            elif variable_name in ['inventory', 'wallet']:
                if len(key) >= 1:
                    try:
                        if variable_name == 'inventory':
                            out += user.data[variable_name][key[0]][0]
                        else:
                            out += user.data[variable_name][key[0]]
                    except Exception:
                        out += 0
    return out

def get_all_user_inv():
    root_user = get_global_file("user", "")
    out = {}
    for root, dirs, files in os.walk(root_user):
        for file in files:
            file = file[:-4]  # Trim the .txt
            try:
                id = int(file)
            except ValueError:
                continue
            user = get_user_data(id)
            try:
                for item in user.data['inventory']:
                    if item not in out.keys():
                        out[item] = 0
                    try:
                        out[item] += user.data['inventory'][item][0]
                    except Exception:
                        out[item] += user.data['inventory'][item]
            except Exception:
                continue
    return out

def get_all_server_net():
    root_server = get_global_file("server", "")
    out = {}
    for root, dirs, files in os.walk(root_server):
        for file in files:
            file = file[:-4]  # Trim the .txt
            try:
                id = int(file)
            except ValueError:
                continue
            server = get_server_data(id)
            try:
                out[server.data['name']] = {'name': server.data['name'],
                                            'users': server.data['users']-server.data['bad users'][0]-server.data['bad users'][1],
                                            **server.data['network data']}
            except Exception:
                continue
    return out

def write_all_user(*args): #int, int or list, key, list, key
    root_user = get_global_file("user", "")
    for root, dirs, files in os.walk(root_user):
        for file in files:
            file = file[:-4]  # Trim the .txt
            try:
                id = int(file)
            except ValueError:
                continue
            if id == 405968021337669632:
                continue
            user = get_user_data(id)
            i = 0
            j = 1
            if args[0] == 'double':
                i += 1
                j += 1
            if isinstance(user.data.get(args[i]), (int, float, str)): # Find the source, assuming it's a var.
                old_var = user.data[args[i]]
                if isinstance(user.data[args[i]], int):
                    user.data[args[i]] = 0
                if isinstance(user.data[args[i]], float):
                    user.data[args[i]] = 0.0
                if isinstance(user.data[args[i]], str):
                    user.data[args[i]] = '*wiped*'
                i += 1
            elif isinstance(user.data.get(args[i]), (dict, list)): # Find the source, assuming it's a list.
                old_var = user.data[args[i]][args[i+1]]
                if isinstance(user.data[args[i]][args[i+1]], int):
                    user.data[args[i]][args[i+1]] = 0
                if isinstance(user.data[args[i]][args[i+1]], float):
                    user.data[args[i]][args[i+1]] = 0.0
                if isinstance(user.data[args[i]][args[i+1]], str):
                    user.data[args[i]][args[i+1]] = '*wiped*'
                i += 2
            if isinstance(user.data.get(args[i]), (int, float, str)): # Find the destination, assuming it's a var.
                user.data[args[i]] += old_var * j
            elif isinstance(user.data.get(args[i]), (dict, list)): # Find the destination, assuming it's a list.
                user.data[args[i]][args[i+1]] += old_var * j
            save_user_data(user)

def get_guild_data(ctx):
    guild_id = ctx.guild.id
    g_data = get_server_data(guild_id)
    g_data.data["name"] = ctx.guild.name
    save_server_data(g_data)
    return g_data

def real_users(ctx):
    g_data = get_guild_data(ctx)
    alts_cnt = 0
    bots_cnt = 0
    usercount = ctx.guild.member_count
    users = ctx.guild.members
    for user in users:
        if user.bot:
            bots_cnt += 1
        elif user.id in alts.keys():
            alts_cnt += 1
    g_data.data['users'] = usercount
    g_data.data['bad users'][0] = alts_cnt
    g_data.data['bad users'][1] = bots_cnt
    legit = usercount - bots_cnt - alts_cnt
    output = 'Total visible users (this guild): {0}\n> Legit: {1}\n> Alts: {2}\n> Bots: {3}\n\n'.format(usercount, legit, alts_cnt, bots_cnt)
    save_server_data(g_data)
    return output

def remaining_land(ctx):
    developed = get_all_user_sum('developed land')
    return get_all_user_sum('power') - (get_all_user_sum('wallet', 'Land') + developed)

def check_land(ctx):
    if remaining_land(ctx) <= 0:
        return 'There are no deeds left! Invite more people to increase power and conquer more land!'
    else:
        return ''
    
def finalize(ctx, command, send, errorcode, *args):
    time = current_time()
    if errorcode == 'OK':
        errormsg = 'Task completed successfully!'
    else:
        errormsg = errorcode
    base = f'[{time}, {ctx.message.guild.name}:#{ctx.message.channel.name}] {prefix}{command}:\n\
 - {errormsg}\n - User {username(ctx.message.author, testfor_alt(ctx.message.author.id))[0]} did "{prefix}{command}'
    if len(args) > 0:
        print(base + ' ' + args[0] + '\"')
    else:
        print(base + '"')
    if send != None:
        return send

def get_splash():
    file = openfile('data\\splash.txt', 'r')
    splashstr = file.readlines()
    splashid = random.randrange(len(splashstr))
    string = splashstr[splashid]
    string = string[:-1]
    return string

def get_time(datetime: datetime):
    microsecond = datetime.microsecond
    second = datetime.second
    minute = datetime.minute
    hour = datetime.hour
    day = datetime.day
    month = datetime.month
    year = datetime.year
    return [year, month, day, hour, minute, second, microsecond]

def translate_time(dattime):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    days = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
            '11th','12th','13th','14th','15th','16th','17th','18th','19th','20th',
            '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
    if type(dattime) is str:
        date, time = dattime.split(' ')
        dt = date.split('-')
        clock, ms = time.split('.')
        dt.append(*clock.split(':'), ms)
        dattime = dt
    if type(dattime) is datetime:
        dattime=list(dattime.timetuple())
    if type(dattime) in [list, tuple]:
        return [dattime[0]-1970, months[dattime[1]-1], days[dattime[2]-1], dattime[3], dattime[4], dattime[5], dattime[6]//1000, dattime[6]%1000]

def current_time(tzoffset:int=0):
    dt = get_time(datetime.now(timezone(timedelta(hours=tzoffset))))
    ttime = translate_time(dt)
    sign = ''
    if tzoffset >= 0:
        sign = '+'
    return "UNIX {} {:0>2} {:0>2}, {:0>2}:{:0>2}:{:0>2}.{:0>3}'{:0>3} UTC".format(ttime[0], ttime[1], ttime[2], ttime[3], ttime[4], ttime[5], ttime[6], ttime[7]) + sign + str(tzoffset)

def subtract_time(year, month, day, hour, minute, second):
    current_time = get_time(datetime.utcnow())
    current_y, current_mo, current_d, current_h, current_min, current_sec = current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5]
    new_sec = second-current_sec
    new_min = minute-current_min
    new_h = hour-current_h
    new_d = day-current_d
    new_mo = month-current_mo
    new_y = year-current_y
    if new_sec < 0:
        new_sec += 60
        new_min -= 1
    if new_min < 0:
        new_min += 60
        new_h -= 1
    if new_h < 0:
        new_h += 24
        new_d -= 1
    if new_d < 0:
        new_d += 30
        new_mo -= 1
    if new_mo < 0:
        new_mo += 12
        new_y -= 1
    if new_y < 0:
        new_sec = current_sec-second
        new_min = current_min-minute
        new_h = current_h-hour
        new_d = current_d-day
        new_mo = current_mo-month
        new_y = current_y-year
        if new_sec < 0:
            new_sec += 60
            new_min -= 1
        if new_min < 0:
            new_min += 60
            new_h -= 1
        if new_h < 0:
            new_h += 24
            new_d -= 1
        if new_d < 0:
            new_d += 30
            new_mo -= 1
        if new_mo < 0:
            new_mo += 12
            new_y -= 1
    return f"{new_y}yr {new_mo:0>2}mo {new_d:0>2}dy {new_h:0>2}:{new_min:0>2}:{new_sec:0>2}"

def draw_rating(rating, raters):
    star = ':star:'
    half_star = ResourceParse.emojidata['oc2_half_star']
    no_star = ResourceParse.emojidata['oc2_black_star']
    out = ''
    round0 = round(rating/raters, 1)
    round3 = round(rating/raters, 3)
    stars = 0
    while stars < 10:
        if round0 >= 1:
            round0 -= 1
            out += star
        elif round0 >= 0.5:
            round0 -= 0.5
            out += half_star
        else:
            out += no_star
        stars += 1
    out += f" ({round3}/10)"
    return out

def DictToList(dict):
    list = [] 
    for key in dict.keys(): 
        list.append(key) 
          
    return list

def find_key(input_dict, value):
    return next((k for k, v in input_dict.items() if v == value), None)

print("Constructing bot instance...")
print("> Finding prefixes...")
async def determine_prefix(bot, message):
    guild = message.guild
    g_data = get_guild_data(message)
    #Only allow custom prefixs in guild
    if guild:
        return g_data.data['prefix']
    else:
        return default_prefixes
print("> Showing intents...")
intents = discord.Intents(messages=True, guilds=True, members=True)
bot = commands.Bot(command_prefix=determine_prefix, description=desc, intents=intents)

print('Finding server...')
@bot.event
async def on_ready():  # Bot boot-up. Below text appears if it successfully boots.
    to_print = 'Logged in as ' + bot.user.name + ' with ID <' + str(bot.user.id) + '>'
    to_print += "\nLogged into {0} guilds.".format(len(bot.guilds))
    print(to_print)
    print('------')
        
## ----- Commands ----- ##
print('Fetching commands...')
#class Core(commands.cog):

    #def __init__(self, bot):
    #    self.bot = bot

@bot.command(aliases=['ev', 'event'])
async def events(ctx, *args):
    events = []
    out = ""
    out2 = ""
    out3 = ""
    events.append("Time until Christmas Day (8\u03C3):\n" + lcd_translate(subtract_time(2020, 12, 25, 0, 0, 0), 'lcd'))
    events.append("Time until the Xmas Multicrate event ends (7\u03C3):\n" + lcd_translate(subtract_time(2020, 12, 27, 0, 0, 0), 'lcd'))
    events.append("Time until the new year (8\u03C3):\n" + lcd_translate(subtract_time(2021, 1, 1, 0, 0, 0), 'lcd'))
    events.append("Time until the second COVID-19 lockdown reaches its peak (3.5\u03C3):\n" + lcd_translate(subtract_time(2021, 1, 3, 0, 0, 0), 'lcd'))
    events.append("Time until Groundhog Day (8\u03C3):\n" + lcd_translate(subtract_time(2021, 2, 2, 0, 0, 0), 'lcd'))
    events.append("Time until COVID-21 mutates/is released (4\u03C3):\n" + lcd_translate(subtract_time(2021, 2, 10, 0, 0, 0), 'lcd'))
    events.append("Time until Valentine's Day (8\u03C3):\n" + lcd_translate(subtract_time(2021, 2, 14, 0, 0, 0), 'lcd'))
    events.append("Approx time until the Ninth Age begins (7\u03C3):\n" + lcd_translate(subtract_time(2021, 3, 18, 0, 0, 0), 'lcd'))
    events.append("Time until Nil Update Day (April Fools' Day) (8\u03C3):\n" + lcd_translate(subtract_time(2021, 4, 1, 0, 0, 0), 'lcd'))
    events.append("Time until the third COVID-19/first COVID-21 lockdown begins (2.5\u03C3):\n" + lcd_translate(subtract_time(2021, 5, 1, 0, 0, 0), 'lcd'))
    events.append("Time until the third COVID-19/first COVID-21 lockdown peaks (1\u03C3):\n" + lcd_translate(subtract_time(2021, 6, 1, 0, 0, 0), 'lcd'))
    events.append("Time until Minecraft 1.17 is released (5.5\u03C3):\n" + lcd_translate(subtract_time(2021, 7, 15, 0, 0, 0), 'lcd'))
    try:
        if args[0] == 'future':
            for ev in range(2):
                out += events[ev+6] + "\n\n"
            #for ev in range(1):
            #    out2 += events[ev+8] + "\n\n"
        else:
            throw_error = args[99]
    except Exception:
        for ev in range(2):
            out += events[ev] + "\n\n"
        for ev in range(2):
            out2 += events[ev+2] + "\n\n"
        for ev in range(2):
            out3 += events[ev+4] + "\n\n"
    out2 += 'Sigma (\u03C3) indicates certainty. Lower values indicates less certainty.\n\
8\u03C3 = 100%\n\
7\u03C3 = 93.75%\n\
6\u03C3 = 87.5%\n\
5\u03C3 = 75%\n\
4\u03C3 = 50%\n\
3\u03C3 = 25%\n\
2\u03C3 = 12.5%\n\
1\u03C3 = 6.25%'
    message_return = finalize(ctx, 'events', out, "OK")
    await ctx.send(message_return)
    await ctx.send(out2)

@bot.command()
async def stats(ctx, *arg):
    """General bot information.
    /stats <page no./page name>
    Page 1 - stats
    Page 2 - econ
    Page 3 - server
    Page 4 - credits
    Page 5 - changelog"""
    user = testfor_alt(ctx.message.author.id)
    if len(arg) == 0 or arg[0] == '1' or arg[0] == 'stats':
        string = get_splash()
        ln0 = '**Statistics**\n'
        ln1 = desc + '\n'
        ln2 = '*\"' + string + '\"*\n\n'
        ln3 = '# of guilds: {0}\n'.format(len(bot.guilds))
        ln4 = '# of shards: 1\n'
        ln5 = 'Rating: ' + draw_rating(botdata.data['rating'][0], botdata.data['rating'][1]) + '\n'
        ln6 = 'No last page. | Page 1 of 5 | Next page: ' + prefix + 'stats econ'
        out = ln0 + ln1 + ln2 + ln3 + ln4 + ln5 + ln6
        message_return = finalize(ctx, 'stats', out, "OK", '1')
    elif arg[0] == '2' or arg[0] == 'econ':
        sum1 = get_all_user_sum('wallet', 'Rupees')
        sum2 = get_all_user_sum('wallet', 'Kups')
        sum3 = get_all_user_sum('wallet', 'Clovers')
        sum4 = get_all_user_sum('wallet', 'Land')
        sum5 = get_all_user_sum('wallet', 'OmniCoreCredits')
        sum6 = get_all_user_sum('developed land') + sum4
        sumpwr = get_all_user_sum('power')
        occ = ResourceParse.compress_rup_clov(sum5, 'oc2_occ', user)
        resources = ResourceParse.compress(sum1, sum2, sum3, sum6, user) + ', ' + occ
        max_land = ResourceParse.compress_land(sumpwr)
        remaining_land = ResourceParse.compress_land(sumpwr - sum6)
        float_max: int = 1000**100002
        rupeetreect = 0
        rupeetreeval = 0
        cointreect = 0
        cointreeval = 0
        totaltree = rupeetreect+cointreect
        ln0 = '**Economy**\n'
        ln1 = 'Total Resources:\n> ' + resources + '\n'
        if fast_stats == False:
            ln2 = 'Max resources:\n> ' + ResourceParse.compress(float_max, float_max, float_max, sumpwr, user) + ', ' + ResourceParse.emojidata['oc2_occ'] + f'{ResourceParse.number_cronch(float_max, user)}\n\n' # Blocked to prevent spam killing the bot.
        elif fast_stats == True:
            ln2 = 'Max resources:\n> ' + ResourceParse.emojidata['oc2_1Tr'] + '1.0×10^300006, ' + ResourceParse.emojidata['oc2_kaali'] + '1.0×10^300006, ' + ResourceParse.emojidata['oc2_clover'] + '1.0×10^300006, ' + max_land + ', ' + ResourceParse.emojidata['oc2_occ'] + f'1.0×10^300006\n\n'
        ln3 = 'Total Power: {0:,}\nRemaining land: {1}\n'.format(sumpwr, remaining_land)
        ln4 = 'Last page: ' + prefix + 'stats stats | Page 2 of 5 | Next page: ' + prefix + 'stats server'
        out = ln0 + ln1 + ln2 + ln3 + ln4
        message_return = finalize(ctx, 'stats', out, "OK", '2')
    elif arg[0] == '3' or arg[0] == 'server':
        ln0 = 'Want to join my server? Here\'s the link!\nhttps://discord.gg/uYJHP3m\n'
        ln1 = 'Last page: ' + prefix + 'stats econ | Page 3 of 5 | Next page: ' + prefix + 'stats credits'
        out = ln0 + ln1
        message_return = finalize(ctx, 'stats', out, "OK", '3')
    elif arg[0] == '4' or arg[0] == 'credits':
        ln0 = '**Credits**\n'
        ln1 = 'Noobly - It was his idea, totally. *cough*\n'
        ln2 = 'Miniwa - Meow! Wrote the shop and crafting system!\n'
        ln3 = 'Nitsche - Inspired the lootcrate system.\n'
        ln4 = 'Zecca - Nagged Noobly to learn Python.\n'
        ln5 = 'HyperCrafting - Helps with the tetration function\n'
        ln6 = 'Kraterocratic - Drew current PFP.'
        ln7 = '\nLast page: ' + prefix + 'stats server | Page 4 of 5 | Next page: ' + prefix + 'stats changelog'
        out = ln0 + ln1 + ln2 + ln3 + ln4 + ln5 + ln6 + ln7
        message_return = finalize(ctx, 'stats', out, "OK", str(arg[0]))
    elif arg[0] == '5' or arg[0] == 'changelog':
        try:
            versions = []
            with openfile('data\\changelog.txt', 'r') as file:
                changelog = json.loads(file.read())
            for version in changelog:
                versions.append(version)
            ln0 = '**Changelog**\n'
            ln1 = changelog[versions[-5]] + '\n'
            ln2 = changelog[versions[-4]] + '\n'
            ln3 = changelog[versions[-3]] + '\n'
            ln4 = changelog[versions[-2]] + '\n'
            ln5 = changelog[versions[-1]]
            ln6 = '\nLast page: ' + prefix + 'stats credits | Page 5 of 5 | There is no next page...'
            if len(arg) >= 2:
                try:
                    if len (changelog[arg[1]]) <= 2000:
                        out = changelog[arg[1]]
                    else:
                        out = 'Error: Message length over 2000 characters.\n'
                except Exception:
                    out = "Error: Version is either invalid or was never documented. Versions after α1.3.2 before α2.4.0 are undocumented."
            else:
                if len(ln0 + ln1 + ln2 + ln3 + ln4 + ln5 + ln6) <= 2000:
                    out = ln0 + ln1 + ln2 + ln3 + ln4 + ln5 + ln6
                elif len(ln0 + ln2 + ln3 + ln4 + ln5 + ln6) <= 2000:
                    out = ln0 + ln2 + ln3 + ln4 + ln5 + ln6
                elif len(ln0 + ln3 + ln4 + ln5 + ln6) <= 2000:
                    out = ln0 + ln3 + ln4 + ln5 + ln6
                elif len(ln0 + ln4 + ln5 + ln6) <= 2000:
                    out = ln0 + ln4 + ln5 + ln6
                elif len(ln0 + ln5 + ln6) <= 2000:
                    out = ln0 + ln5 + ln6
                else:
                    out = ln0 + 'Error: Message length over 2000 characters.\n' + ln6
            message_return = finalize(ctx, 'stats', out, "OK", str(arg[0]))
        except Exception as e:
            out = f"Error: {e}"
            message_return = finalize(ctx, 'stats', out, out, str(arg[0]))
    else:
        out = 'Invalid page!'
        message_return = finalize(ctx, 'stats', out, "OK", str(arg[0]))
    await ctx.send(message_return)

@bot.command()
async def invite(ctx):
    """Invite the bot to a server!"""
    out = "Follow this link to add the bot to your server!\nhttps://discord.com/oauth2/authorize?client_id=405968021337669632&scope=bot&permissions=999999"
    message_return = finalize(ctx, 'invite', out, "OK")
    await ctx.send(message_return)

portal_ids = {}
portals = {}
connections = {}
private_ids = {}
private = {}
secure_connections = {}

@bot.command()
async def portal(ctx, setting, *gate_id): #Opens a comms portal.
    """Opens a portal for communication. Portals close automatically upon restart.
toggle|power - Toggles whether the portal is open or closed.
open <gate_id> - Opens a portal.
close - Closes a portal.
switch|change <gate_id> - Changes the destination portal.
status|stats|info - Gets status on the portal.
lock|private - Stablizes the connection so it cannot be interrupted, changed, or disconnected.
unlock|public - Destablizes a stable connection so it may be interrupted, changed, or disconnected."""
    g_data = get_guild_data(ctx)
    if not g_data.data['portal']:
        return
    gate = ctx.message.guild.name + ':#' + ctx.message.channel.name
    if setting in ['toggle', 'power']: #opens or closes a portal
        if gate in portals.keys(): #if the portal is open
            setting == 'close'
        else:
            setting == 'open'
    if setting in ['close']:
        if gate in portals.keys(): #if the portal is open
            portals.pop(gate) #make it not open
            if gate in connections: #if there are other portals open
                oldgate = portals[connections[gate]] #check to see if this portal was connected to another and alert the remote portal that the connection has ended
                await oldgate.send(f"Alert: The connection with `{gate}` ({find_key(portal_ids, gate)}) has been terminated, as their portal has closed.")
                connections.pop(connections[gate]) #destroy the connection
                connections.pop(gate)
                portal_ids.pop(find_key(portal_ids, gate)) #delete the portal's ID.
            out = 'Portal closed.'
        else:
            out = 'The portal is already closed.'
    if setting in ['open']:
        if gate in portals.keys(): #if the portal is open
            out = 'The portal is already open.'
        else:
            out = 'A portal to the hyperverse has opened!'
            if gate not in portal_ids.values(): #if there is no portal ID
                while True: #roll a portal ID, and make sure it's unique
                    possible_id = random.randint(1, 65536)
                    if possible_id in portal_ids or possible_id in private_ids:
                        continue
                    else:
                        portal_ids[possible_id] = gate
                        break
            if len(portals) >= 1: #if there is at least one other portal open
                if len(gate_id) == 1: #if a gate ID has been requested to connect to
                    gate_id = gate_id[0]
                    if int(gate_id) in portal_ids.keys(): #if the requested portal ID is registered (assume the portal is open)
                        destination = portal_ids[int(gate_id)] #set the requested portal as destination
                    else: #if the ID is invalid or the portal is closed, throw an error
                        out = 'Invalid key provided. The portal failed to activate.'
                        portal_ids.pop(find_key(portal_ids, gate)) #delete this portal's ID, as it won't be opening
                        message_return = finalize(ctx, 'portal', out, "OK", setting)
                        await ctx.send(message_return)
                        return
                else: #if no gate ID was requested
                    destination = random.choice(DictToList(portals)) #pick a random portal to connect to
                newgate = portals[destination] #get CTX for the destination portal
                if destination in connections: #if the portal we're connecting to is connected to something else
                    oldgate = portals[connections[destination]] #get CTX for the portal the destination is connected to and tell them the connection was cut by a third party
                    await oldgate.send(f"Alert: The connection with `{destination}` ({find_key(portal_ids, destination)}) has been destablized by a portal connecting to it from `{gate}` ({find_key(portal_ids, gate)}).")
                    connections.pop(connections[destination]) #destroy the connection, tell the destination portal that their destination portal has changed.
                    await newgate.send(f"Alert: The connection with `{connections[destination]}` ({find_key(portal_ids, connections[destination])}) has been replaced with a connection from `{gate}` ({find_key(portal_ids, gate)}).")
                else: #if the portal we're connecting to is NOT connected to anything, tell them that a connection has been made
                    await newgate.send(f"Alert: A portal from `{gate}` ({find_key(portal_ids, gate)}) has connected to this portal.")
                connections[gate] = destination #set up a portal connection
                connections[destination] = gate
                out += f' Connected to `{destination}` ({find_key(portal_ids, destination)})!' #give confirmation that this portal has connected to a destination.
            portals[gate] = ctx #save this portal's CTX for future use
    if setting in ['change', 'switch']:
        if gate not in portals.keys(): #if the portal is not open
            out = 'The portal cannot change channels if it\'s closed.'
        else:
            if len(portals) >= 2: #if there is another portal besides this one and the one it's currently connected to
                destination = 'NA'
                if len(gate_id) == 1: #if a gate ID has been requested to connect to
                    gate_id = gate_id[0]
                    if int(gate_id) in portal_ids.keys(): #if the requested portal ID is registered
                        destination = portal_ids[int(gate_id)] #set the requested portal as destination
                    else: #if the ID is invalid or the portal is closed, throw an error
                        out = 'Invalid key provided. The portal\'s channel failed to change.'
                        message_return = finalize(ctx, 'portal', out, "OK", setting)
                        await ctx.send(message_return)
                        return
                else: #if no gate ID was requested
                    if gate in connections:
                        bad_gates = [connections[gate], gate, 'NA']
                    else:
                        bad_gates = [gate, 'NA']
                    i = 0
                    while destination in bad_gates and i < 20:
                        destination = random.choice(DictToList(portals)) #pick a random portal to connect to
                        i += 1
                    if destination in bad_gates:
                        out = "The portal failed to find another portal to establish a connection with (failed to find a good connection after 20 tries)."
                        message_return = finalize(ctx, 'portal', out, "OK", setting)
                        await ctx.send(message_return)
                        return
                newgate = portals[destination] #get CTX for the destination portal
                if destination in connections: #if the portal we're connecting to is connected to something else
                    oldgate = portals[connections[destination]] #get CTX for the portal the destination is connected to and tell them the connection was cut by a third party
                    await oldgate.send(f"Alert: The connection with `{destination}` ({find_key(portal_ids, destination)}) has been destablized by a portal connecting to it from `{gate}` ({find_key(portal_ids, gate)}).")
                    connections.pop(connections[destination]) #destroy the connection, tell the destination portal that their destination portal has changed.
                    await newgate.send(f"Alert: The connection with `{connections[destination]}` ({find_key(portal_ids, connections[destination])}) has been replaced with a connection from `{gate}` ({find_key(portal_ids, gate)}).")
                else: #if the portal we're connecting to is NOT connected to anything, tell them that a connection has been made
                    await newgate.send(f"Alert: A portal from `{gate}` ({find_key(portal_ids, gate)}) has connected to this portal.")
                if gate in connections: #if this portal was already connected to someone
                    oldgate = portals[connections[gate]] #check to see if this portal was connected to another and alert the remote portal that the connection has ended
                    await oldgate.send(f"Alert: The connection with `{gate}` ({find_key(portal_ids, gate)}) has been terminated, as their portal connected to `{destination}` ({find_key(portal_ids, destination)}).")
                    connections.pop(connections[gate]) #destroy the connection
                    connections.pop(gate)
                connections[gate] = destination #set up a portal connection
                connections[destination] = gate
                out = f'Connected to `{destination}` ({find_key(portal_ids, destination)})!' #give confirmation that this portal has connected to a destination.
            else:
                out = "There are no available portals to connect to."
    if setting in ['status', 'stats', 'info']:
        connect = '<Err3001 - Broken Entry:#red-reality>'
        key = -1
        out = ''
        powered = False
        if gate in portals.keys():
            powered = True
            if gate in connections.keys():
                connect = connections[gate]
                key = find_key(portal_ids, connect)
            out += f"**Public Portal**\nPowered: {powered}\nPortal Key: {find_key(portal_ids, gate)}"
            if powered == True:
                out += f"\nConnected to: `{connect}` ({key})"
            else:
                out += f"Connected to: `nothing (portal offline)`"
                connect = '<Err3001 - Broken Entry:#red-reality>'
        key = -1
        powered = False
        if gate in private.keys():
            powered = True
            channel = 'Private'
            if gate in secure_connections.keys():
                connect = secure_connections[gate]
                key = find_key(private_ids, connect)
            out += f"\n\n**Private Portal**\nPowered: {powered}\nPortal Key: {find_key(private_ids, gate)}"
            if powered == True:
                out += f"\nConnected to: `{connect}` ({key})"
        if gate not in portals.keys() and gate not in private.keys():
            out += f"Connected to: `nothing (portal offline)`"
    if setting in ['private', 'lock', 'public', 'unlock']:
        if gate in portals.keys() and private.keys():
            out = 'The two opened portals cannot switch channels. Please close the public portal before trying this.'
            message_return = finalize(ctx, 'portal', out, "OK", setting)
            await ctx.send(message_return)
            return
    if setting in ['private', 'lock']:
        if gate in portals.keys():
            if gate in connections.keys():
                destination = connections[gate]
                if destination in portals.keys() and private.keys():
                    out = 'Something prevents this channel from switching to public. The other end may have their public channel busy.'
                    message_return = finalize(ctx, 'portal', out, "OK", setting)
                    await ctx.send(message_return)
                    return
                private[gate] = ctx
                private[destination] = portals[destination]
                portals.pop(gate)
                portals.pop(destination)
                secure_connections[gate] = destination
                secure_connections[destination] = gate
                connections.pop(gate)
                connections.pop(destination)
                private_ids[find_key(portal_ids, gate)] = gate
                private_ids[find_key(portal_ids, destination)] = destination
                portal_ids.pop(find_key(portal_ids, gate))
                portal_ids.pop(find_key(portal_ids, destination))
                out = 'Portal connection locked.'
                await private[destination].send('Portal connection locked.')
            else:
                out = 'Portal connection not made, and cannot be locked.'
        else:
            out = 'Portal must be open for a connection to be locked.'
    if setting in ['public', 'unlock']:
        if gate in private.keys():
            if gate in secure_connections.keys():
                destination = secure_connections[gate]
                if destination in portals.keys() and private.keys():
                    out = 'Something prevents this channel from switching to public. The other end may have their private channel busy.'
                    message_return = finalize(ctx, 'portal', out, "OK", setting)
                    await ctx.send(message_return)
                    return
                portals[gate] = ctx
                portals[destination] = private[destination]
                private.pop(gate)
                private.pop(destination)
                connections[gate] = destination
                connections[destination] = gate
                secure_connections.pop(gate)
                secure_connections.pop(destination)
                portal_ids[find_key(private_ids, gate)] = gate
                portal_ids[find_key(private_ids, destination)] = destination
                private_ids.pop(find_key(private_ids, gate))
                private_ids.pop(find_key(private_ids, destination))
                out = 'Portal connection unlocked.'
                await portals[destination].send('Portal connection unlocked.')
            else:
                out = 'Portal connection not made, and cannot be unlocked.'
        else:
            out = 'Portal must be open for a connection to be unlocked.'
    message_return = finalize(ctx, 'portal', out, "OK", setting)
    await ctx.send(message_return)
        
@bot.command()
async def changelog(ctx, *args): #Runs z!stats changelog
    cmd_stats = bot.get_command("stats")
    if len(args) != 0:
        await ctx.invoke(cmd_stats, 'changelog', args[0])
    else:
        await ctx.invoke(cmd_stats, 'changelog')

@bot.command(aliases=["d&d_treasure"])
async def dnd_treasure(ctx, treas_type, *args):
    """Roll from D&D treasure tables.
z!dnd_treasure single <cr>
  Values for <cr>: x where 0<=x 
z!dnd_treasure hoard <cr>
  Values for <cr>: x where 0<=x<=10
z!dnd_treasure gems <value> <quantity>
  Values for <value>: 10, 50, 100, 500, 1000, 5000
z!dnd_treasure arts <value> <quantity>
  Values for <value>: 25, 250, 750, 2500, 7500
z!dnd_treasure item <table> <quantity>
  Values for <table>: a, b, c, d, e, f, g, h"""
    try:
        g_data = get_guild_data(ctx)
        if not g_data.data['dice']:
            return
        def dice(dice_num, dice_size, multiplier):
            total = 0
            while dice_num > 0:
                roll = random.randint(1, dice_size)
                total += roll
                dice_num -= 1
            return total*multiplier

        arg = [0, 1]
        if treas_type != 'item':
            arg[0] = int(args[0])
        else:
            arg[0] = args[0]
        if len(args) == 2:
            arg[1] = int(args[1])
        
        CP = "Copper Pieces"
        SP = "Silver Pieces"
        EP = "Electrum Pieces"
        GP = "Gold Pieces"
        PP = "Platinum Pieces"
        
        mitA = []
        mitB = []
        mitC = []
        mitD = []
        mitE = []
        mitF = []
        mitG = []
        mitH = []
        mitI = []
        
        it0 = [[[dice(5,6,1), CP]],
               [[dice(4,6,1), SP]],
               [[dice(3,6,1), EP]],
               [[dice(2,6,1), GP]],
               [[dice(1,6,1), PP]]]
        
        it5 = [[[dice(4,6,100), CP], [dice(1,6,10), EP]],
               [[dice(6,6,10), SP], [dice(2,6,10), GP]],
               [[dice(3,6,10), EP], [dice(2,6,10), GP]],
               [[dice(4,6,10), GP]],
               [[dice(2,6,10), GP], [dice(3,6,1), PP]]]
        
        it11 = [[[dice(4,6,100), SP], [dice(1,6,100), GP]],
               [[dice(1,6,100), EP], [dice(1,6,100), GP]],
               [[dice(2,6,100), GP], [dice(1,6,10), PP]],
               [[dice(2,6,100), GP], [dice(2,6,10), PP]]]
        
        it17 = [[[dice(2,6,1000), EP], [dice(8,6,100), GP]],
               [[dice(1,6,1000), GP], [dice(1,6,100), PP]],
               [[dice(1,6,1000), GP], [dice(2,6,100), PP]]]
        gem10 = [["Azurite",[""]], ["Banded Agate",["Brown ", "Blue ", "White ", "Red "]], ["Blue Quartz",[""]],
                 ["Eye Agate",["Gray ", "White ", "Brown ", "Blue ", "Green "]], ["Hematite",[""]], ["Lapis Lazuli",[""]],
                 ["Malachite",[""]], ["Moss Agate",[""]], ["Obsidian",[""]], ["Rhodochrosite",[""]], ["Tiger Eye",[""]],
                 ["Turquoise",[""]]]
        gem50 = [["Bloodstone",[""]], ["Carnelian",[""]], ["Chalcedony",[""]], ["Chrysoprase",[""]], ["Citrine",[""]],
                 ["Jasper",["Blue ", "Black ", "Brown "]], ["Moonstone",[""]], ["Onyx",[""]], ["Quartz",["Clear ", "Smoky ", "Yellow "]],
                 ["Sardonyx",[""]], ["Star Rose Quartz",[""]], ["Zircon",[""]]]
        gem100 = [["Amber",[""]], ["Amethyst",[""]], ["Chrysoberyl",[""]], ["Coral",[""]], ["Garnet",["Red ", "Brown-Green ", "Violet "]],
                  ["Jade",["Light Green ", "Deep Green ", "White "]], ["Jet",[""]], ["Pearl",["White ", "Yellow ", "Pink "]],
                  ["Spinel",["Red ", "Red-Brown ", "Deep Green "]], ["Tourmaline",["Pale Green ", "Blue ", "Brown ", "Red "]]]
        gem500 = [["Alexandrite",[""]], ["Aquamarine",[""]], ["Black Pearl",[""]], ["Blue Spinel",[""]], ["Peridot",[""]], ["Topaz",[""]]]
        gem1k = [["Black Opal",[""]], ["Blue Sapphire",[""]], ["Emerald",[""]], ["Fire Opal",[""]], ["Opal",[""]], ["Star Ruby",[""]],
                 ["Star Sapphire",[""]], ["Sapphire",["Yellow ", "Yellow-Green "]]]
        gem5k = [["Black Sapphire",[""]], ["Diamond",["Blue-White ", "Canary ", "Pink ", "Brown ", "Blue "]], ["Jacinth",[""]],
                 ["Ruby",["Red ", "Deep Crimson "]]]

        def gem_identify(quantity, value):
            values = {10:gem10, 50:gem50, 100:gem100, 500:gem500, 1000:gem1k, 5000:gem5k}
            table = values[value]
            gems = {}
            while quantity > 0:
                gem = table[dice(1, len(table), 1)-1]
                gem = random.choice(gem[1]) + gem[0] + f" ({value}GP)"
                gems.setdefault(gem, 0)
                gems[gem] += 1
                quantity -= 1
            if len(gems) > 1:
                out1, out2 = parseInventory(ctx,gems,True)
                out = "Gems:\n" + out1 + out2
            else:
                for key in gems:
                    out = key
            return out
        
        art25 = ["Silver Ewer", "Carved Bone Statuette", "Small Gold Bracelet", "Cloth-of-gold Vestments",
                 "Black Velvet Mask stitched with Silver Thread", "Copper Clalice with Silver Filigree",
                 "Pair of Engraved Bone Dice", "Small Mirror set in a Painted Wooden Frame", "Embroidered Silk Handkerchief",
                 "Gold Locket with a Painted Portrait"]
        art250 = [f"Gold Ring set with {gem_identify(1, 50)}s", "Carved Ivory Statuette", "Large Gold Bracelet",
                  f"Silver Necklace with a {gem_identify(1, 50)} Pendant", "Bronze Crown", "Silk Robe with Gold Embroidery",
                  "Large well-made Tapestry", "Brass Mug with Jade Inlay", "Box of Turquoise Animal Figurines",
                  "Gold Bird Cage with Electrum Filigree"]
        art750 = [f"Silver Chalice set with {gem_identify(1, 50)}", f"Silver-plated Longsword with {gem_identify(1, 100)} set in Hilt",
                  f"Carved Harp of Exotic Wood with Ivory Inlay and {gem_identify(1, 50)} Gems", "Small Gold Idol",
                  f"Gold Dragon Comb set with {gem_identify(1, 100)}s as Eyes", f"Bottle Stopper Cork embossed with Gold Leaf and set with {gem_identify(1, 100)}",
                  f"Ceremonial Electrum Dagger with a {gem_identify(1, 500)} in the Pommel", "Silver and Gold Brooch",
                  "Obsidian Statuette with Gold Fittings and Inlay", "Painted Gold War Mask"]
        art2500 = [f"Fine Gold Chain set with a {gem_identify(1, 1000)}", "Old Masterpiece Painting",
                   f"Embroidered Silk and Velvet Mantle set with numerous {gem_identify(1, 50)}s", f"Platinum Bracelet set with a {gem_identify(1, 1000)}",
                   f"Embroidered Glove set with {gem_identify(1, 1000)} and {gem_identify(1, 500)} chips",
                   f"{gem_identify(1, 1000)} and {gem_identify(1, 500)}-jeweled Anklet",
                   f"Gold Music Box", f"Gold Circlet set with four {gem_identify(1, 500)}",
                   f"Eye Patch with a Mock Eye set in {gem_identify(1, 1000)} and Moonstone", "A Necklace String of Small Pink Pearls"]
        art7500 = [f"{gem_identify(1, 5000)} and {gem_identify(1, 1000)}-jeweled Gold Crown",
                   f"{gem_identify(1, 5000)} and {gem_identify(1, 1000)}-jeweled Platinum Ring",
                   f"Small Gold Statuette set with {gem_identify(1, 5000)}s", f"Gold Cup set with {gem_identify(1, 1000)}s",
                   "Gold Jewelry Box with Platinum Filigree", "Painted Gold Child's Sarcophagus", "Jade Board Game with Solid Gold Playing Pieces",
                   f"{gem_identify(1, 5000)} and {gem_identify(1, 1000)}-bejeweled Ivory Drinking Horn with Gold Filigree"]
        
        def art_identify(quantity, value):
            values = {25:art25, 250:art250, 750:art750, 2500:art2500, 7500:art7500}
            table = values[value]
            arts = {}
            while quantity > 0:
                art = table[dice(1, len(table), 1)-1] + f" ({value}GP)"
                arts.setdefault(art, 0)
                arts[art] += 1
                quantity -= 1
            out1, out2 = parseInventory(ctx,arts,True)
            out = "Arts:\n" + out1 + out2
            return out

        mia = [[[1,50], "Potion of Healing"],
               [[51,60], "Spell Scroll (Cantrip)"],
               [[61,70], "Potion of Climbing"],
               [[71,90], "Spell Scroll (Lv1)"],
               [[91,94], "Spell Scroll (Lv2)"],
               [[95,98], "Potion of Greater Healing"],
               [[99], "Bag of Holding"],
               [[100], "Driftglobe"]]
        mib = [[[1,15], "Potion of Greater Healing"],
               [[16,22], "Potion of Fire Breath"],
               [[23,29], "Potion of Resistance"],
               [[30,34], "Ammunition, +1"],
               [[35,39], "Potion of Animal Friendship"],
               [[40,44], "Potion of Hill Giant Strength"],
               [[45,49], "Potion of Growth"],
               [[50,54], "Potion of Water Breathing"],
               [[55,59], "Spell Scroll (Lv2)"],
               [[60,64], "Spell Scroll (Lv3)"],
               [[65,67], "Bag of Holding"],
               [[68,70], "Keoghtom's Ointment"],
               [[71,73], "Oil of Slipperiness"],
               [[74,75], "Dust of Disappearance"],
               [[76,77], "Dust of Dryness"],
               [[78,79], "Dust of Sneezing and Choking"],
               [[80,81], "Elemental Gem"],
               [[82,83], "Philter of Love"],
               [[84], "Alchemy Jug"],
               [[85], "Cap of Water Breathing"],
               [[86], "Cloak of the Manta Ray"],
               [[87], "Driftglobe"],
               [[88], "Goggles of Night"],
               [[89], "Helm of Comprehending Languages"],
               [[90], "Immovable Rod"],
               [[91], "Lantern of Revealing"],
               [[92], "Mariner's Armor"],
               [[93], "Mithral Armor"],
               [[94], "Potion of Poison"],
               [[95], "Ring of Swimming"],
               [[96], "Robe of Useful Items"],
               [[97], "Rope of Climbing"],
               [[98], "Saddle of the Cavalier"],
               [[99], "Wand of Magic Detection"],
               [[100], "Wand of Secrets"]]
        mic = [[[1,15], "Potion of Superior Healing"],
               [[16,22], "Spell Scroll (Lv4)"],
               [[23,27], "Ammunition, +2"],
               [[28,32], "Potion of Clairvoyance"],
               [[33,37], "Potion of Diminution"],
               [[38,42], "Potion of Gaseous Form"],
               [[43,47], "Potion of Frost Giant Strength"],
               [[48,52], "Potion of Stone Giant Strength"],
               [[53,57], "Potion of Heroism"],
               [[58,62], "Potion of Invulnerability"],
               [[63,67], "Potion of Mind Reading"],
               [[68,72], "Spell Scroll (Lv5)"],
               [[73,75], "Elixir of Health"],
               [[76,78], "Oil of Etherealness"],
               [[79,81], "Potion of Fire Giant Strength"],
               [[82,84], "Quaal's Feather Token"],
               [[85,87], "Scroll of Protection"],
               [[88,89], "Bag of Beans"],
               [[90,91], "Bead of Force"],
               [[92], "Chime of Opening"],
               [[93], "Decanter of Endless Water"],
               [[94], "Eyes of Minute Seeing"],
               [[95], "Folding Boat"],
               [[96], "Heward's Handy Haversack"],
               [[97], "Horseshoes of Speed"],
               [[98], "Necklace of Fireballs"],
               [[99], "Periapt of Health"],
               [[100], "Sending Stones"]]
        mid = [[[1,20], "Potion of Supreme Healing"],
               [[21,30], "Potion of Invisibility"],
               [[31,40], "Potion of Speed"],
               [[41,50], "Spell Scroll (Lv6)"],
               [[51,57], "Spell Scroll (Lv7)"],
               [[58,62], "Ammunition, +3"],
               [[63,67], "Oil of Sharpness"],
               [[68,72], "Potion of Flying"],
               [[73,77], "Potion of Cloud Giant Strength"],
               [[78,82], "Potion of Longevity"],
               [[83,87], "Potion of Vitality"],
               [[88,92], "Spell Scroll (Lv8)"],
               [[93,95], "Horseshoes of a Zephyr"],
               [[96,98], "Nolzur's Marvelous Pigments"],
               [[99], "Bag of Devouring"],
               [[100], "Portable Hole"]]
        mie = [[[1,30], "Spell Scroll (Lv8)"],
               [[31,55], "Potion of Storm Giant Strength"],
               [[56,70], "Potion of Supreme Healing"],
               [[71,85], "Spell Scroll (Lv9)"],
               [[86,93], "Universal Solvent"],
               [[94,98], "Arrow of Slaying"],
               [[99,100], "Sovereign Glue"]]
        mif = [[[1,15], "Weapon, +1"], [[16,18], "Shield, +1"],
               [[19,21], "Sentinel Shield"], [[22,23], "Amulet of Proof Against Detection and Location"],
               [[24,25], "Boots of Elvenkind"], [[26,27], "Boots of Striding and Springing"],
               [[28,29], "Bracers of Archery"], [[30,31], "Brooch of Shielding"],
               [[32,33], "Broom of Flying"], [[34,35], "Cloak of Elvenkind"],
               [[36,37], "Cloak of Protection"], [[38,39], "Gauntlets of Ogre Power"],
               [[40,41], "Hat of Disguise"], [[42,43], "Javelin of Lightning"],
               [[44,45], "Pearl of Power"], [[46,47], "Rod of the Pact Keeper, +1"],
               [[48,49], "Slippers of Spider Climbing"], [[50,51], "Staff of the Adder"],
               [[52,53], "Staff of the Python"], [[54,55], "Sword of Vengeance"],
               [[56,57], "Trident of Fish Command"], [[58,59], "Wand of Magic Missiles"],
               [[60,61], "Wand of the War Mage, +1"], [[62,63], "Wand of Web"],
               [[64,65], "Weapon of Warning"], [[66], "Adamantine Armor (Chain Mail)"],
               [[67], "Adamantine Armor (Chain Shirt)"], [[68], "Adamantine Armor (Scale Mail)"],
               [[69], "Bag of Tricks (Gray)"], [[70], "Bag of Tricks (Rust)"],
               [[71], "Bag of Tricks (Tan)"], [[72], "Boots of the Winterlands"],
               [[73], "Circlet of Blasting"], [[74], "Deck of Illusions"],
               [[75], "Eversmoking Bottle"], [[76], "Eyes of Charming"],
               [[77], "Eyes of the Eagle"], [[78], "Figurine of Wondrous Power (Silver Raven)"],
               [[79], "Gem of Brightness"], [[80], "Gloves of Missile Snaring"],
               [[81], "Gloves of Swimming and Climbing"], [[82], "Gloves of Thievery"],
               [[83], "Headband of Intellect"], [[84], "Helm of Telepathy"],
               [[85], "Instrument of the Bards (Doss Lute)"], [[86], "Instrument of the Bards (Fochlucan Bandore)"],
               [[87], "Instrument of the Bards (Mac-Fuimidh Cittern)"], [[88], "Medallion of Thoughts"],
               [[89], "Necklace of Adaptation"], [[90], "Periapt of Wound Closure"],
               [[91], "Pipes of Haunting"], [[92], "Pipes of the Sewers"],
               [[93], "Ring of Jumping"], [[94], "Ring of Mind Shielding"],
               [[95], "Ring of Warmth"], [[96], "Ring of Water Walking"],
               [[97], "Quiver of Ehlonna"], [[98], "Stone of Good Luck"],
               [[99], "Wind Fan"], [[100], "Winged Boots"]]
        FWP = ["Bronze Griffon", "Ebony Fly", "Golden Lions", "Ivory Goats", "Marble Elephant", "Onyx Dog", "Onyx Dog", "Serpentine Owl"]
        HoV = ["Silver", "Brass"]
        BoGS = ["Frost", "Stone"]
        MAT = ["Armor, +2 (Half Plate)", "Armor, +2 (Half Plate)", "Armor, +2 (Plate)", "Armor, +2 (Plate)",
               "Armor, +3 (Studded Leather)", "Armor, +3 (Studded Leather)", "Armor, +3 (Breastplate)", "Armor, +3 (Breastplate)",
               "Armor, +3 (Splint)", "Armor, +3 (Splint)", "Armor, +3 (Half Plate)", "Armor, +3 (Plate)"]

        def subtable(item):
            table = {0:FWP,1:HoV,2:BoGS,3:MAT}[item]
            out = table[dice(1, len(table), 1)-1]
            return out
        
        mig = [[[1,11], "Weapon, +2"], [[12,14], f"Figurine of Wondrous Power ({subtable(0)})"],
               [[15], "Adamantine Armor (Breastplate)"], [[16], "Adamantine Armor (Splint)"],
               [[17], "Amulet of Health"], [[18], "Armor of Vulnerability"],
               [[19], "Arrow-catching Shield"], [[20], "Belt of Dwarvenkind"],
               [[21], "Belt of Hill Giant Strength"], [[22], "Berserker Axe"],
               [[23], "Boots of Levitation"], [[24], "Boots of Speed"],
               [[25], "Bowl of Commanding Water Elementals"], [[26], "Bracers of Defense"],
               [[27], "Braizer of Commanding Fire Elementals"], [[28], "Cape of the Mountebank"],
               [[29], "Censer of Controlling Air Elementals"], [[30], "Armor, +1 (Chain Mail)"],
               [[31], "Armor of Resistance (Chain Mail)"], [[32], "Armor, +1 (Chain Shirt)"],
               [[33], "Armor of Resistance (Chain Shirt)"], [[34], "Cloak of Displacement"],
               [[35], "Cloak of the Bat"], [[36], "Cube of Force"],
               [[37], "Daern's Instant Darkness"], [[38], "Dagger of Venom"],
               [[39], "Dimensional Shackles"], [[40], "Dragon Slayer"],
               [[41], "Elven Chain"], [[42], "Flame Tongue"],
               [[43], "Gem of Seeing"], [[44], "Giant Slayer"],
               [[45], "Glamoured Studded Leather"], [[46], "Helm of Teleportation"],
               [[47], "Horn of Blasting"], [[48], f"Horn of Valhalla ({subtable(1)})"],
               [[49], "Instrument of the Bards (Canaith Mandolin)"], [[50], "Instrument of the Bards (Cli Lyre)"],
               [[51], "Ioun Stone (Awareness)"], [[52], "Ioun Stone (Protection)"],
               [[53], "Ioun Stone (Reserve)"], [[54], "Ioun Stone (Sustenance)"],
               [[55], "Iron Bands of Bilarro"], [[56], "Armor, +1 (Leather)"],
               [[57], "Armor of Resistance (Leather)"], [[58], "Mace of Disruption"],
               [[59], "Mace of Smiting"], [[60], "Mace of Terror"],
               [[61], "Mantle of Spell Resistance"], [[62], "Necklace of Prayer Beads"],
               [[63], "Periapt of Proof Against Poison"], [[64], "Ring of Animal Influence"],
               [[65], "Ring of Evasion"], [[66], "Ring of Feather Falling"],
               [[67], "Ring of Free Action"], [[68], "Ring of Protection"],
               [[69], "Ring of Resistance"], [[70], "Ring of Spell Storing"],
               [[71], "Ring of the Ram"], [[72], "Ring of X-ray Vision"],
               [[73], "Robe of Eyes"], [[74], "Rod of Rulership"],
               [[75], "Rod of the Pact Keeper, +2"], [[76], "Rope of Entanglement"],
               [[77], "Armor, +1 (Scale Mail)"], [[78], "Armor of Resistance (Scale Mail)"],
               [[79], "Shield, +2"], [[80], "Shield of Missile Attraction"],
               [[81], "Staff of Charming"], [[82], "Staff of Healing"],
               [[83], "Staff of Swarming Insects"], [[84], "Staff of the Woodlands"],
               [[85], "Staff of Withering"], [[86], "Stone of Controlling Earth Elementals"],
               [[87], "Sun Blade"], [[88], "Sword of Life Stealing"],
               [[89], "Sword of Wounding"], [[90], "Tentacle Rod"],
               [[91], "Vicious Weapon"], [[92], "Wand of Binding"],
               [[93], "Wand of Enemy Detection"], [[94], "Wand of Fear"],
               [[95], "Wand of Fireballs"], [[96], "Wand of Lightning Bolts"],
               [[97], "Wand of Paralysis"], [[98], "Wand of the War Mage, +2"],
               [[99], "Wand of Wonder"], [[100], "Wings of Flying"]]
        mih = [[[1,10], "Weapon, +3"], [[11,12], "Amulet of the Planes"],
               [[13,14], "Carpet of Flying"], [[15,16], "Crystal Ball (Very Rare)"],
               [[17,18], "Ring of Regeneration"], [[19,20], "Ring of Shooting Stars"],
               [[21,22], "Ring of Telekinesis"], [[23,24], "Robe of Scintillating Colors"],
               [[25,26], "Robe of Stars"], [[27,28], "Rod of Absorption"],
               [[29,30], "Rod of Alertness"], [[31,32], "Rod of Security"],
               [[33,34], "Rod of the Pact Keeper, +3"], [[35,36], "Scimitar of Speed"],
               [[37,38], "Shield, +3"], [[39,40], "Staff of Fire"],
               [[41,42], "Staff of Frost"], [[43,44], "Staff of Power"],
               [[45,46], "Staff of Striking"], [[47,48], "Staff of Thunder and Lightning"],
               [[49,50], "Sword of Sharpness"], [[51,52], "Wand of Polymorph"],
               [[53,54], "Wand of the War Mage, +3"], [[55], "Adamantine Armor (Half Plate)"],
               [[56], "Adamantine Armor (Plate)"], [[57], "Animated Shield"],
               [[58], "Belt of Fire Strength"], [[59], f"Belt of {subtable(2)} Giant Strength"],
               [[60], "Armor, +1 (Breastplate)"], [[61], "Armor of Resistance (Breastplate)"],
               [[62], "Candle of Invocation"], [[63], "Armor, +2 (Chain Mail)"],
               [[64], "Armor, +2 (Chain Shirt)"], [[65], "Cloak of Arachnida"],
               [[66], "Dancing Sword"], [[67], "Demon Armor"],
               [[68], "Dragon Scale Mail"], [[69], "Dwarven Plate"],
               [[70], "Dwarven Thrower"], [[71], "Efreeti Bottle"],
               [[72], "Figurine of Wondrous Power (Obsidian Steed)"], [[73], "Frost Brand"],
               [[74], "Helm of Brilliance"], [[75], "Horn of Valhalla (Bronze)"],
               [[76], "Instrument of the Bards (Anstruth Harp)"], [[77], "Ioun Stone (Absorption)"],
               [[78], "Ioun Stone (Agility)"], [[79], "Ioun Stone (Fortitude)"],
               [[80], "Ioun Stone (Insight)"], [[81], "Ioun Stone (Intellect)"],
               [[82], "Ioun Stone (Leadership)"], [[83], "Ioun Stone (Strength)"],
               [[84], "Armor, +2 (Leather)"], [[85], "Manual of Bodily Health"],
               [[86], "Manual of Gainful Exercise"], [[87], "Manual of Golems"],
               [[88], "Manual of Quickness of Action"], [[89], "Manual of Life Tapping"],
               [[90], "Nine Lives Stealer"], [[91], "Oathbow"],
               [[92], "Armor, +2 (Scale Mail)"], [[93], "Spellguard Shield"],
               [[94], "Armor, +1 (Splint)"], [[95], "Armor of Resistance (Splint)"],
               [[96], "Armor, +1 (Studded Leather)"], [[97], "Armor of Resistance (Studded Leather)"],
               [[98], "Tome of Clear Thought"], [[99], "Tome of Leadership and Influence"], [[100], "Tome of Understanding"]]
        mii = []

        def magic_identify(quantity, table_letter):
            table_letter = str.lower(table_letter)
            values = {'a':mia, 'b':mib, 'c':mic, 'd':mid, 'e':mie, 'f':mif, 'g':mig, 'h':mih, 'i':mii}
            table = values[table_letter]
            magic_items = {}
            while quantity > 0:
                die = dice(1, 100, 1)
                for item in table:
                    if len(item[0]) == 1:
                        if item[0][0] == die:
                            magic_items.setdefault(item[1], 0)
                            magic_items[item[1]] += 1
                            quantity -= 1
                    elif len(item[0]) == 2:
                        if item[0][0] <= die <= item[0][1]:
                            magic_items.setdefault(item[1], 0)
                            magic_items[item[1]] += 1
                            quantity -= 1
            out1, out2 = parseInventory(ctx,magic_items,False)
            out = out1 + out2
            return out

        hcoin0 = f"{dice(6,6,100)} {CP}, {dice(3,6,100)} {SP}, {dice(2,6,100)} {GP}\n"
        hcoin5 = f"{dice(2,6,100)} {CP}, {dice(2,6,1000)} {SP}, {dice(6,6,100)} {GP}, {dice(3,6,10)} {PP}\n"
        hcoin11 = f"{dice(4,6,1000)} {GP}, {dice(5,6,100)} {PP}\n"
        hcoin17 = f"{dice(12,6,1000)} {GP}, {dice(8,6,100)} {PP}\n"
        
        th0 = [[[1,6], hcoin0],
               [[7,16], hcoin0 + gem_identify(dice(2,6,1), 10)],
               [[17,26], hcoin0 + art_identify(dice(2,4,1), 25)],
               [[27,36], hcoin0 + gem_identify(dice(2,6,1), 50)],
               [[37,44], hcoin0 + gem_identify(dice(2,6,1), 10) + magic_identify(dice(1,6,1), 'a')],
               [[45,52], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,6,1), 'a')],
               [[53,60], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(dice(1,6,1), 'a')],
               [[61,65], hcoin0 + gem_identify(dice(2,6,1), 10) + magic_identify(dice(1,4,1), 'b')],
               [[66,70], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'b')],
               [[71,75], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(dice(1,4,1), 'b')],
               [[76,78], hcoin0 + gem_identify(dice(2,6,1), 10) + magic_identify(dice(1,4,1), 'c')],
               [[79,80], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'c')],
               [[81,85], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(dice(1,4,1), 'c')],
               [[86,92], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'f')],
               [[93,97], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(dice(1,4,1), 'f')],
               [[98,99], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(1, 'g')],
               [[100], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(1, 'g')]]
        th5 = [[[1,4], hcoin5],
               [[5,10], hcoin5 + art_identify(dice(2,4,1), 25)],
               [[11,16], hcoin5 + gem_identify(dice(3,6,1), 50)],
               [[17,22], hcoin5 + gem_identify(dice(3,6,1), 100)],
               [[23,28], hcoin5 + art_identify(dice(2,4,1), 250)],
               [[29,32], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,6,1), 'a')],
               [[33,36], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(dice(1,6,1), 'a')],
               [[37,40], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,6,1), 'a')],
               [[41,44], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,6,1), 'a')],
               [[45,49], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'b')],
               [[50,54], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(dice(1,4,1), 'b')],
               [[55,59], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,4,1), 'b')],
               [[60,63], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'b')],
               [[64,66], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'c')],
               [[67,69], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(dice(1,4,1), 'c')],
               [[70,72], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,4,1), 'c')],
               [[73,74], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'c')],
               [[75,76], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(1, 'd')],
               [[77,78], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(1, 'd')],
               [[79], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(1, 'd')],
               [[80], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(1, 'd')],
               [[81,84], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'f')],
               [[85,88], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(dice(1,4,1), 'f')],
               [[89,91], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,4,1), 'f')],
               [[92,94], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'f')],
               [[95,96], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,4,1), 'g')],
               [[97,98], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'g')],
               [[99], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(1, 'h')],
               [[100], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(1, 'h')]]
        th11 = []
        th17 = []

        def hoard_loot(cr):
            if 0 <= cr <= 4:
                table = th0
            if 5 <= cr <= 10:
                table = th5
            if 11 <= cr <= 16:
                table = th11
            if 17 <= cr:
                table = th17
            outcome = dice(1,100,1)
            for item in table:
                Bool = False
                if len(item[0]) == 1:
                    if item[0][0] == outcome:
                        out = item[1]
                elif len(item[0]) == 2:
                    if item[0][0] <= outcome <= item[0][1]:
                        out = item[1]
            return out
        
        if treas_type == "single":
            outcome = dice(1,100,1)
            if 0 <= arg[0] <= 4:
                if 1 <= outcome <= 30:
                    loot = it0[0]
                if 31 <= outcome <= 60:
                    loot = it0[1]
                if 61 <= outcome <= 70:
                    loot = it0[2]
                if 71 <= outcome <= 95:
                    loot = it0[3]
                if 96 <= outcome <= 100:
                    loot = it0[4]
            if 5 <= arg[0] <= 10:
                if 1 <= outcome <= 30:
                    loot = it5[0]
                if 31 <= outcome <= 60:
                    loot = it5[1]
                if 61 <= outcome <= 70:
                    loot = it5[2]
                if 71 <= outcome <= 95:
                    loot = it5[3]
                if 96 <= outcome <= 100:
                    loot = it5[4]
            if 11 <= arg[0] <= 16:
                if 1 <= outcome <= 20:
                    loot = it11[0]
                if 21 <= outcome <= 35:
                    loot = it11[1]
                if 36 <= outcome <= 75:
                    loot = it11[2]
                if 76 <= outcome <= 100:
                    loot = it11[3]
            if 17 <= arg[0]:
                if 1 <= outcome <= 15:
                    loot = it17[0]
                if 16 <= outcome <= 55:
                    loot = it17[1]
                if 56 <= outcome <= 100:
                    loot = it17[2]
            output = {}
            for item in loot:
                output[item[1]] = item[0]
            out1, out2 = parseInventory(ctx,output,False)
            out = out1 + out2
        if treas_type == "hoard":
            out = hoard_loot(arg[0])
        if treas_type == "gems":
            if len(arg) == 1:
                arg.append(1)
            out = gem_identify(arg[1], arg[0])
        if treas_type == "arts":
            if len(arg) == 1:
                arg.append(1)
            out = art_identify(arg[1], arg[0])
        if treas_type == "item":
            if len(arg) == 1:
                arg.append(1)
            out = magic_identify(arg[1], arg[0])
    except Exception as e:
        out = f"Error: {e}"
    message_return = finalize(ctx, 'dnd_treasure', out, "OK")
    await ctx.send(message_return)
    
        
@bot.command(aliases=['tut'])
async def tutorial(ctx, *page: int):
    """Learn how to use the more complex commands!"""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy'] and not g_data.data['crafting']:
        return
    if len(page) == 0:
        page = 1
    else:
        page = page[0]
    if page == 1:
        out = "Hello! I assume by the fact that you are looking into this that you are looking for help with using this bot. Firstly, I must give you the table of contents.```\
01 - Introduction/Table of Contents\n\
02 - Navigating profiles\n\
03 - Getting wood\n\
04 - Crafting items\n\
05 - Mining ores and buying upgrades\n\
06 - All About Ores\n\
07 - Special Crafting Buildings\n\
08 - Automation\n\
09 - Towns and Taxes\n\
10 - Special events\n\
11 - Setting your settings (TODO)\n\
12 - What to do when short on cash (TODO)\n\
13 - Other fun commands (TODO)\n``` `" + prefix + "help` is also useful. For more info about a given command, please use `" + prefix + "help <command>`."
    if page == 2:
        out = "The profile contains information and variables about a user. \
The profile is accessed by the command " + prefix + "profile on either bot. Do note that each bot has a different prefix. The syntax for " + prefix + "profile is \
`" + prefix + "profile <user> <page>`, where both <user> and <page> are optional arguments. `" + prefix + "profile` will show the first page of your profile. \
`" + prefix + "profile \"Noobly Walker\"` will show the first page of Noobly's profile. `" + prefix + "profile 3` will show the third page of your profile, and \
`" + prefix + " 「Toyo」 2` will show the second page of Toyo's profile. You cannot see the profile of someone who isn't on the server you are running on the command on, \
though. User IDs, pinging, and possibly guild nicknames will work for <user>.\n\nPage one of the profile shows a user's name, description, custom image, monetary balance, multipliers, \
and abilities.\nPage two shows a user's current tools, and will show their tool inventory later.\nPage three shows nothing, but will later show what cards a user has equipped, \
as well as their card inventory.\nPage four shows what buildings and trees they have in their civ.\nPage give shows what achievements a user has collected.\nPage six shows \
a user's collectables, and how many of each collection they have completed.\nPage seven shows a user's resource inventory.\nMore on these later."
    if page == 3:
        out = "You may notice that your resource inventory is void and empty. What might you be able to do about this, you may be thinking? Well, you could try to " + prefix + "mine, \
but you would likely break your fist and accomplish nothing but agony. Instead, you should " + prefix + "chop. It still makes your phalanges go crunch, but the tree goes crunch too.\
I expect that the average person should be able to punch down about five trees before the pain becomes too much. Each tree is between 1 and 5 meters tall, so that should yield around \
12 or 13 logs on average. Now, you may be asking, 'But <bot.name>, what do I do with these wood logs?' More about that in five hours. Do note, however, that it will take around a day for \
you to recover from this labor.\n\n`Disclaimer. We do not condone people punching \
trees IRL, and can not be held responsible if someone is stupid enough to try.`"
    if page == 4:
        out = "If you are following along, you now have around a dozen logs and two broken fists. Don't worry about the latter, I've heard human bones can heal exceptionally well. \
However, now that you have wood, what do you do with it? Do like Chuck Norris and tear it in half of course. Then do it again. But how?\nAssuming you have indeed punched down some \
trees, it is now time that you do your research. " + prefix + "blueprints has a list of everything you can " + prefix + "craft and their resource requirements. It is at this time \
that you ought to craft those logs into planks, and some of those planks into sticks (Remember, the code for planks and sticks is plank0 and stick0. Ain't pretty, but it is what \
it is). Now that you have some planks and sticks, you should make your first set of tools. Craft a wooden pickaxe and a wooden axe. These will making resource collection easier \
and less painful."
    if page == 5:
        out = "So, by this point, you should now have a pickaxe! Time to go into the " + prefix + "mine! Mining yields stone and ore, the type of stone and ore depends on how \
good your pickaxe is. There are around a dozen tiers of pickaxe, each one able to find more ore than the last. Occassionally, you may also discover a buried treasure, which you may \
open using `" + prefix + "boxes treasure <quantity to open>`. Treasures can contain all sorts of goodies.\n\n'But <bot.name>,' I hear you saying, 'These pickaxes are garbage and \
hardly get me anything before they break!' Well, that's where you must get upgrades. If you have rupees (gems) to spend, especially over 800, check the `" + prefix + "shop` listings. \
You should be able to `" + prefix + "buy` the three pickaxe upgrades, Pickaxe Sharpener, Extra Pick Head Weight, and Reinforced Pick Handle. The same upgrades exist for axes as well, \
but upgrading your pickaxe is decidedly more important. Also, if you have a large amount of clovers, you can use them while mining (`" + prefix + "mine 1`), and your pickaxe will take \
less damage, allowing you to use it longer! If you have a LOT of clovers, perhaps you should `" + prefix + "craft` a Pickaxe Wriststrap! This will give you an additional bonus to your \
tool's unbreaking-ness."
    if page == 6:
        out = "You have ores, but what are they for? What is a Tetrahedrite? What do you do to get metal? Well, one step at a time. First, you need to save up your stone and \
`" + prefix + "craft` a furnace. Next, get some coal (or craft charcoal) and two of any ore (except maybe a few that won't melt no matter how much coal you add), and craft an ingot. \
Later, you will discover how to craft a Blast Furnace, and the metals that would not melt before will finally submit, as pure Carbon burns hotter than Coal.\
While we used to have 'Copper Ore', 'Tin Ore', 'Iron Ore', etc, now we use their real names. There are several types of ore that yield the same metal, after all. Below is a chart \
of ores and what they yield.```\
Tetrahedrite - Copper\n\
Sphalerite - Zinc\n\
Cassiterite - Tin\n\
Hematite - Iron\n\
Native Silver - Silver (obviously)\n\
Native Gold - Gold (obviously)\n\
Native Platinum - Platinum (obviously)\n\
Franciscite - Californium (unofficial name for CfO3)\n\
Ringwoodite - is not ore (You will find out why once you have it, perhaps.)\n\
Carmeltazite - is not ore (It's like diamond, but better.)\n\
Rutile - Titanium\n\
Magnesite - Magnesium\n\
Pegmatite - Lithium\n\
Wolframite - Tungsten\n\
Cobaltite - Cobalt\n\
Quartz - Silicon\n\
Coal - Carbon (also known as Coke)\n\
Diamond - 3×Carbon (Turning diamonds into coke is an option, but not recommended unless you need coke more than diamonds.)```"
    if page == 7:
        out = "So, you've already learned of the furnace, but there are other buildings that you can make that allow you to craft new things. The logical next step after the furnace is the \
blast furnace, which requires lots of stone and a bit of iron. This also allows you to make alloys, though I will let you discover those for yourself. Aside from tools, you can make sawmills \
of every tier of tool-quality material (except wood). These will allow you to bulk craft stone bricks, planks, and sticks (hence the number on their IDs.) Each tier of sawmill allows +4 bulk \
over the last one. However, just because you can craft stick7 doesn't mean you can't also craft stick0. Craft what you need, don't be wasteful. More such buildings, such as generators, are \
coming soon."
    if page == 8:
        out = "By this point, you've been plugging away for a few weeks, likely have Hellstone or Carmeltazite tools, and tons of resources. You may have discovered the civ stuff (will be \
explained later if not), and have found that crafting civ things requires loads of repetitive, spammy crafting. At some point, you must've figured that there must be an easier option, but \
couldn't figure it out. You've seen " + prefix + "autocraft, but it doesn't seem to do anything. Well, let me tell you, it isn't broken. You need to " + prefix + "craft a Factory. \
A factory requires 20 steel and 1,000 stone bricks. Once you have made a factory, " + prefix + "autocraft will work for you, crafting an item every few seconds, like an idle game. \
Additionally, and I don't know if you know this yet, but you can craft multiple furnaces and blast furnaces now. You should craft an additional of both, and twenty gears. This will \
allow the factory to smelt ores and create alloys for you as well.\n\nAs for how to work the command, the syntax is `" + prefix + "autocraft list <page number>` and `" + prefix + "\
autocraft add <resource> <blueprint> <quantity>`, where if you have less than <quantity> of the defined <resource>, then <blueprint> will be crafted. If you want it such that if you \
have more than 0 of some resource that it crafts something, set <quantity> to 'Infinity'! Make sure of capitalization. Infinity is a float number, and can only be read as such if it \
is capitalized properly.\n\n\
`Disclaimer: 'Infinity' cannot actually be gotten as a float from commands like this, and turns into a string instead. However, the program reads it and turns it into 1000^1000, which is \
suitably big such that no matter how much technology increases the amount of bulk crafting, it should continue running indefinitely.`"
    if page == 9:
        out = "You have thousands of wood and stone, but nothing to do with it, right? You should build some houses or something! Houses yield some rupees every day through z!tax. It's a reliable \
source of income. Building more houses will require Food, so you should use some of that land and one of your larger houses to build a farm. Farms produce grain when taxed, and the grain can be \
turned into food to feed more people and build more houses. Build enough houses and dig a well, and you can make a village. Villages claim land when taxed, as well as producing grain and rupees. \
Bigger towns claim more land, so you might want to commit to investing in housing. The rewards are great."
    if page == 10:
        out = "On the first page of your profile, you may see a section for 'events'. Events randomly occur for each individual, and can impact how calculations are done. Often, they will boost \
the outputs of certain actions, usually for the better. They are rare, however. I think I heard a 1 in 10 chance of events occurring for a given person on a given day. When an event occurs, pay \
attention - you can get huge rewards for completing that action, so you should commit all your resources to completing that action the best way you can. Global events are rarer, and usually coincide \
with things such as the head programmer's birthday or Christmas. These events usually provide powerful buffs, or even unlock actions, such as with the multiplier crate. They usually last about a week \
though."
    message_return = finalize(ctx, 'tutorial', out, "OK", str(page))
    await ctx.send(message_return)

@bot.command(aliases=['dbg'])
async def debug(ctx, arg, *var):
    """Allows testing of various things.
    z!debug data: Runs several tools to clean up and correct issues with userdata, including updating.
    z!debug getsum <var>: Finds all values of a given variable between users and adds them together.
    z!debug nitro <user>: Gives user bot nitro badge.
    z!debug testperm: Tests to see if user is an admin.
    z!debug errorhandler: Forces an error to be thrown to test errorhandling.
    z!debug migrate <old userdata path> <new userdata path>: Moves variables.
    z!debug getvar <variable>: Dumps raw variables from userdata.
    z!debug restart: Restarts the bot.
    z!debug lcd: Gives test message in LCD font."""
    try:
        user = testfor_alt(ctx.message.author.id)
        user_data = get_user_data(user)
        if arg == 'data':
            for currency in user_data.data['wallet']:
                if type(user_data.data['wallet'][currency]) is float:
                    user_data.data['wallet'][currency] = int(user_data.data['wallet'][currency])
            for item in user_data.data['inventory']:
                if type(user_data.data['inventory'][item][0]) is float:
                    user_data.data['inventory'][item][0] = int(user_data.data['inventory'][item][0])
            for currency in botdata.data['wallet']:
                if type(botdata.data['wallet'][currency]) is float:
                    botdata.data['wallet'][currency] = int(botdata.data['wallet'][currency])
            for item in botdata.data['inventory']:
                if type(botdata.data['inventory'][item][0]) is float:
                    botdata.data['inventory'][item][0] = int(botdata.data['inventory'][item][0])
            save_user_data(botdata)
            await ctx.send('Your stats have been rounded.')
            save_user_data(user_data)
            
            inv = user_data.inventory()
            test = 0
            to_remove = []
            for item in inv:
                try:
                    test += inv[item][0]
                except Exception:
                    await ctx.send(f"{item} is invalid, removing item...")
                    to_remove.append(item)
                    continue
                if inv[item][0] > 0:
                    user_data.inventory()[item][2] = True
            for item in to_remove:
                del user_data.inventory()[item]
            await ctx.send("Your inventory has been debugged.")
            save_user_data(user_data)
            
            user_data.updateBuildings()
            for building in user_data.data['civ'].keys():
                user_data.hasBuilding(building, 1, 1) #this function shouldn't be used here, but it should fix things
            await ctx.send("Your town has been debugged.")
            save_user_data(user_data)

            if user_data.data['lootbox_counting_multi'][1] == 0:
                user_data.data['lootbox_counting_multi'][1] = 1
            await ctx.send("Your counting multiplier has been debugged.")
            save_user_data(user_data)

            user_data = load_badges(user_data)
            await ctx.send("Your badges have been debugged.")
            save_user_data(user_data)
            
            await ctx.send("All userdata repair tools have been used.")
            return
        if arg == 'testnumcronch':
            for i in range(1000):
                out = number_cronch(i, user)
                print(out)
        if arg == 'getsum':
            if len(var) == 0:
                out = 'nul = nul'
                message_return = finalize(ctx, 'debug', out, "OK", 'getsum')
            else:
                if len(var) == 1:
                    sum = get_all_user_sum(var[0])
                    out = var[0] + ' = {0}'.format(sum)
                elif len(var) == 2:
                    sum = get_all_user_sum(var[0], var[1])
                    out = var[0] + '[' + var[1] + '] = {0}'.format(sum)
                message_return = finalize(ctx, 'debug', out, "OK", 'getsum ' + var[0])
        if arg == 'nitro':
            if ctx.message.author.id == '248641004993773569':
                subject = testfor_alt(var[0])
                subjectdata = get_user_data(subject)
                subjectdata.achievements()['TNG Overcharge'] += 1
                subjectdata.add_rupees(10000 * subjectdata.get_money_multiplier())
                save_user_data(subjectdata)
                out = username(ctx.message.author, subject)[0] + ' has been awarded **TNG Overcharge** and has gained ' + ResourceParse.compress_rup_clov(10000 * subjectdata.get_money_multiplier(), 'rupee', subject) + '!'
            else:
                out = 'You do not have permission to perform this action.'
            message_return = finalize(ctx, 'debug', out, "OK", 'nitro ' + var[0])
        if arg == 'testperm':
            out = ctx.message.author.guild_permissions.administrator
            message_return = finalize(ctx, 'debug', out, "OK", 'testperm')
        if arg == 'errorhandler':
            out = uninitialized_variable
        if arg == 'migrate':
            if user_data.data['id'] == '248641004993773569':
                write_all_user(*var)
                out = ":ok_hand:"
            else:
                out = 'You do not have permission to perform this action.'
        if arg == 'getvar':
            if len(var) == 2:
                out = f"{user_data.data[var[0]][var[1]]}"
            elif len(var) == 1:
                out = f"{user_data.data[var[0]]}"
        if arg == 'restart':
            if user_data.data['id'] == '248641004993773569':
                if len(portals) > 0:
                    for portal in portals:
                        await portals[portal].send("Alert: Bot is restarting. Closing portal...")
                    for portal in private:
                        await portals[portal].send("Alert: Bot is restarting. Closing portal...")
                mess = 'Zakobot is restarting!'
                await ctx.send(mess)
                print(mess)
                sys.exit(99999)
            else:
                out = 'You do not have permission to perform this action.'
        if arg == 'lcd':
            out = "Testing <:0053:770644509230628884><:006D:770644507968143420><:0061:770644508953018408><:006C:770644507892908033><:006C:770644507892908033><:0020:770644509272047626><:0074:770644509197467670><:0065:770644508714991627><:0078:770644509221453845><:0074:770644509197467670>"
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'debug', out, out, arg + " " + str(var))
        await ctx.send(message_return)
        return
    if len(out) > 2000:
        chunks, chunk_size = len(out), 2000
        all_chunks = [ out[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
        for chunk in all_chunks:
            await ctx.send(chunk)
        out = ''
    message_return = finalize(ctx, 'debug', out, "OK", arg + " " + str(var))
    await ctx.send(message_return)

@bot.command(aliases=['reset', 'reboot', 'reload'])
async def restart(ctx): #Runs z!debug restart
    cmd_debug = bot.get_command("debug")
    await ctx.invoke(cmd_debug, 'restart')

@bot.command()
async def rate(ctx, rate: int):
    """Rate the bot 1 to 10! Can only be used once a month."""
    user = testfor_alt(ctx.message.author.id)
    user_data = get_user_data(user)
    if not user_data.data['can rate bot']:
        out = "You've already rated me this month!"
    else:
        if not 1 <= rate <= 10:
            out = "Rating must be 1 at minimum, 10 at maximum."
        else:
            botdata.data['rating'][0] += rate
            botdata.data['rating'][1] += 1
            out = "Thank you for rating me! My new rating is:\n" + draw_rating(botdata.data['rating'][0], botdata.data['rating'][1])
            user_data.data['can rate bot'] = False
            save_user_data(user_data)
            save_user_data(botdata)
    message_return = finalize(ctx, 'rate', out, "OK")
    await ctx.send(message_return)
        

@bot.command(aliases=['guild'])
async def server(ctx, *args):
    """Admin command to modify serverdata"""
    try:
        server_data = get_guild_data(ctx)
        if len(args) == 0:
            hints = ["", "", "", "", "", "", "", "", "", "", "", "", ""]
            if server_data.data["show hints"]:
                hints = ["\n\n// *Used to help describe this server to other people.*",
                         "\n// *Used as prefix for emojis pulled from the server (to be added later).*",
                         "\n// *Used to help describe this server to the bot.*",
                         "\n// *If true, enables z!tcp and allows this server to advertise through the bot. Does not prevent other people from posting discord.gg links on this server.*",
                         "\n> // *If Allow Ads is true, this link will be shared through z!tcp to advertize the server.*",
                         '\n// *If true, XP can be gained and levels show up on z!profile. Also enables z!prestige and z!resetmulti*',
                         '\n> // *If true, a message will display whenever a user levels up on this server.*',
                         '\n// *If true, z!boxes, z!cards, z!trade, z!tutorial, and crafting-related commands will be enabled.*',
                         '\n// *If true, z!boxes, z!cards, z!trade, z!tutorial, and economy-related commands will be enabled.*',
                         '\n// *If true, z!choose, z!roll, and z!dnd_treasure will be enabled.*',
                         '\n> // *If true, z!potion will be enabled.*',
                         '\n// *If true, z!counting will be enabled.*',
                         '\n// *If true, z!portal will be enabled.*']
            embed = discord.Embed(color=8388863)
            embed.title = '\n__**'+ server_data.data["name"] + ' (' + server_data.data["id"] + ')**__'
            general = "**Prefix:** " + server_data.data["prefix"] + \
                      "\n**Show Hints:** " + bool_emoji(server_data.data["show hints"]) + \
                      "\n**Description:\n** " + server_data.data["network data"]['description'] + hints[0]
            embed.add_field(name='*** === Basic Info === ***', value="*To change the strings, do z!server <prefix|hints|desc> <new value>. To toggle bools, do z!server ads.*\n\n" + real_users(ctx) + general, inline=False)
            network = "**Acronym:** " + server_data.data["network data"]['acronym'] + hints[1] + \
                      "\n**Category:** " + server_data.data["network data"]['category'] + hints[2] + \
                      "\n**Allow Ads:** " + bool_emoji(server_data.data["network data"]['allow ads']) + hints[3] + \
                      "\n> **Server Link:** " + server_data.data["network data"]['server link'] + hints[4]
            embed.add_field(name='*** === Network === ***', value="*To change the strings, do z!server <acronym|tag|link> <new value>. To toggle bools, do z!server ads.*\n\n" + network, inline=False)
            modules = "**Levels:** " + bool_emoji(server_data.data["levels"]) + hints[5] + \
                      "\n> **Level Messages:** " + bool_emoji(min(server_data.data["lv_msg"], server_data.data["levels"])) + hints[6] + \
                      "\n**Crafting:** " + bool_emoji(server_data.data["crafting"]) + hints[7] + \
                      "\n**Economy:** " + bool_emoji(server_data.data["economy"]) + hints[8] + \
                      "\n**Dice:** " + bool_emoji(server_data.data["dice"]) + hints[9] + \
                      "\n> **Potions:** " + bool_emoji(min(server_data.data["potion"], server_data.data["dice"])) + hints[10] + \
                      "\n**Counting:** " + bool_emoji(server_data.data["counting"]) + hints[11] + \
                      "\n**Portals:** " + bool_emoji(server_data.data["portal"]) + hints[12]
            embed.add_field(name='*** === Modules === ***', value="*To toggle a module, do z!server <levels|lvmsg|crafting|econ|dice\n|potion|counting|portals>*\n\n"+modules, inline=False)
            if server_data.data["dice"] and server_data.data["potion"]:
                potions = "**Debuff:** " + bool_emoji(server_data.data["potions"]["debuff"]) + \
                          "\n**Transformative:** " + bool_emoji(server_data.data["potions"]["tf"]) + \
                          "\n**Fetish**: " + bool_emoji(server_data.data["potions"]["fetish"]) + \
                          "\n**Vore:** " + bool_emoji(server_data.data["potions"]["vore"]) + \
                          "\n**NSFW**: " + bool_emoji(server_data.data["potions"]["nsfw"]) + \
                          "\n**Gore:** " + bool_emoji(server_data.data["potions"]["gore"]) 
                embed.add_field(name='*** === Potions === ***', value="*To toggle a potion class, do z!server potions <debuff|tf|fetish|vore|nsfw|gore>*\n\n" + potions, inline=False)
            await ctx.send(embed=embed)
        else:
            if not ctx.message.author.guild_permissions.administrator:
                out = "You do not have permission to perform this action."
                message_return = finalize(ctx, 'server', out, "OK")
                await ctx.send(message_return)
                return
            if args[0] in ['prefix']:
                server_data.data['prefix'] = args[1]
            if args[0] in ['acronym']:
                server_data.data["network data"]['acronym'] = args[1]
            if args[0] in ['category', 'tag', 'tags']:
                if args[1] in ['rp', 'roleplay', 'roleplaying']:
                    server_data.data["network data"]['category'] = "Roleplay"
                elif args[1] in ['erp', 'erotic rp', 'erotic roleplay', 'erotic roleplaying']:
                    server_data.data["network data"]['category'] = "NSFW"
                elif args[1] in ['erotica', 'erotic', 'NSFW', 'porn']:
                    server_data.data["network data"]['category'] = "Erotic Roleplay"
                elif args[1] in ['game', 'games', 'gaming']:
                    server_data.data["network data"]['category'] = "Gaming"
                elif args[1] in ['general', 'misc', 'miscellaneous', 'other']:
                    server_data.data["network data"]['category'] = "General"
                elif args[1] in ['guild', 'group', 'team', 'clan']:
                    server_data.data["network data"]['category'] = "Clan"
                elif args[1] in ['meme', 'memes', 'dank', 'dank meme', 'dank memes']:
                    server_data.data["network data"]['category'] = "Meme"
                elif args[1] in ['fetish', 'kink', 'kinks', 'vore']:
                    server_data.data["network data"]['category'] = "Fetish"
                else:
                    out = "Available categories so far: General, Gaming, Clan, Meme, Roleplay, Erotic Roleplay, Fetish, NSFW"
                    message_return = finalize(ctx, 'server', out, "OK")
                    await ctx.send(message_return)
                    return
            if args[0] in ['desc', 'description']:
                server_data.data["network data"]['description'] = args[1]
            if args[0] in ['ads', 'adverts', 'advertisement', 'advertisements', 'ad', 'advert', 'advertizement', 'advertizements']:
                server_data.data["network data"]["allow ads"] = not server_data.data["network data"]["allow ads"]
            if args[0] in ['link', 'invite']:
                if args[1][:-7] == "https://discord.gg/":
                    server_data.data["network data"]['server link'] = args[1][-7:]
                else:
                    out = "Invalid link given."
                    message_return = finalize(ctx, 'server', out, "OK")
                    await ctx.send(message_return)
                    return
            if args[0] in ['hints', 'hint']:
                server_data.data["show hints"] = not server_data.data["show hints"]
            if args[0] in ['levels', 'level', 'lvl', 'lv']:
                server_data.data["levels"] = not server_data.data["levels"]
            if args[0] in ['lvmsg', 'lvlmsg', 'levelmsg']:
                server_data.data["lv_msg"] = not server_data.data["lv_msg"]
            if args[0] == 'crafting':
                server_data.data["crafting"] = not server_data.data["crafting"]
            if args[0] == 'dice':
                server_data.data["dice"] = not server_data.data["dice"]
            if args[0] in ['econ', 'economy']:
                server_data.data["economy"] = not server_data.data["economy"]
            if args[0] in ['ct', 'cnt', 'count', 'counting']:
                server_data.data["counting"] = not server_data.data["counting"]
            if args[0] in ['portal', 'portals']:
                server_data.data["portal"] = not server_data.data["portal"]
            if args[0] in ['pot', 'potion', 'potions']:
                if len(args) == 1 or not server_data.data["potion"]:
                    server_data.data["potion"] = not server_data.data["potion"]
                else:
                    if args[1] == 'debuff':
                        server_data.data["potions"]["debuff"] = not server_data.data["potions"]["debuff"]
                    if args[1] in ['tf', 'transform', 'transformation']:
                        server_data.data["potions"]["tf"] = not server_data.data["potions"]["tf"]
                    if args[1] == 'fetish':
                        server_data.data["potions"]["fetish"] = not server_data.data["potions"]["fetish"]
                    if args[1] == 'vore':
                        server_data.data["potions"]["vore"] = not server_data.data["potions"]["vore"]
                    if args[1] == 'nsfw':
                        server_data.data["potions"]["nsfw"] = not server_data.data["potions"]["nsfw"]
                    if args[1] == 'gore':
                        server_data.data["potions"]["gore"] = not server_data.data["potions"]["gore"]
            if len(args) == 1:
                out = f"{args[0]} has been toggled."
            elif len(args) == 2:
                out = f"{args[0]} has been set to: \"{args[1]}\"."
            save_server_data(server_data)
            message_return = finalize(ctx, 'server', out, "OK", args[0])
            await ctx.send(message_return)
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'server', out, out)
        await ctx.send(message_return)

@bot.command()
async def tcp(ctx, *arg):
    """Displays info on other servers on the Trans-Core Pipeline!
Requires ads to be enabled and a valid invite link to be given."""
    g_data = get_guild_data(ctx)
    if not g_data.data['network data']['allow ads']:
        return
    servers = get_all_server_net()
    page = 1
    embed = discord.Embed(title="__***Trans-Core Pipeline***__",color=8388863)

    def spf(serverdata, detailed: bool):
        name = f"**{serverdata['name']}** "
        if serverdata['acronym'] != "":
            name += f"({serverdata['acronym']})"
        out = f"> Category: {serverdata['category']}\n> Pop.: {serverdata['users']}"
        if detailed:
            out += f"\n> Description: {serverdata['description']}\n> Invite Link: https://discord.gg/{serverdata['server link']}"
        out += "\n\n"
        return name, out
    rem = []
    for server in servers.keys():
        if not servers[server]['allow ads'] or servers[server]['server link'] == '':
            rem.append(server)
    for server in rem:
        del servers[server]
    if len(arg) >= 1:
        filt = arg[0]
        try:
            page = arg[1]
        except Exception:
            pass
        if str.lower(filt) in ['rp', 'roleplay', 'roleplaying']:
            filt = "Roleplay"
        elif str.lower(filt) in ['erp', 'erotic rp', 'erotic roleplay', 'erotic roleplaying']:
            filt = "NSFW"
        elif str.lower(filt) in ['erotica', 'erotic', 'NSFW', 'porn']:
            filt = "Erotic Roleplay"
        elif str.lower(filt) in ['game', 'games', 'gaming']:
            filt = "Gaming"
        elif str.lower(filt) in ['general', 'misc', 'miscellaneous', 'other']:
            filt = "General"
        elif str.lower(filt) in ['guild', 'group', 'team', 'clan']:
            filt = "Clan"
        elif str.lower(filt) in ['meme', 'memes', 'dank', 'dank meme', 'dank memes']:
            filt = "Meme"
        elif str.lower(filt) in ['fetish', 'kink', 'kinks', 'vore']:
            filt = "Fetish"
        if filt in ['General', 'Gaming', 'Clan', 'Meme', 'Roleplay', 'Erotic Roleplay', 'Fetish', 'NSFW']:
            filtered = {}
            for server in servers.keys():
                if filt == servers[server]['category']:
                    filtered[server] = servers[server]
            out = ""
            skeys = DictToList(filtered)
            for server in range(len(filtered)%10+10*(page-1)):
                name, out = spf(servers[skeys[server]], False)
                embed.add_field(name=name, value=out, inline=False)
            message_return = finalize(ctx, 'tcp', None, "OK")
            if len(embed.fields) == 0:
                embed.add_field(name='Error!', value="Invalid/empty category!", inline=False)
            await ctx.send(embed=embed)
            return
        for server in servers.keys():
            if filt in [servers[server]['name'], servers[server]['acronym']]:
                name, out = spf(servers[server], True)
                embed.add_field(name=name, value=out, inline=False)
                message_return = finalize(ctx, 'tcp', None, "OK")
                if len(embed.fields) == 0:
                    embed.add_field(name='Error!', value="Invalid server!", inline=False)
                await ctx.send(embed=embed)
                return
        try:
            page = int(filt)
        except Exception:
            pass
    skeys = DictToList(servers)
    print(skeys)
    for server in range(len(servers)%10+10*(page-1)):
        name, out = spf(servers[skeys[server]], False)
        embed.add_field(name=name, value=out, inline=False)
    message_return = finalize(ctx, 'tcp', None, "OK")
    if len(embed.fields) == 0:
        embed.add_field(name='Error!', value="No servers to show!", inline=False)
    await ctx.send(embed=embed)
    return

@bot.command()
async def kick(ctx, user):
    """Kick people. Admin command."""
    try:
        if not ctx.message.author.guild_permissions.administrator:
            out = "You do not have permission to perform this action."
            message_return = finalize(ctx, 'kick', out, "OK")
            await ctx.send(message_return)
            return
        converter = commands.MemberConverter()
        userobj = await converter.convert(ctx, user)
        await ctx.guild.kick(userobj)
        out = f"{userobj.name} was kicked from {ctx.guild.name}."
        message_return = finalize(ctx, 'kick', out, "OK")
        await ctx.send(message_return)
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'kick', out, out)
        await ctx.send(message_return)

@bot.command()
async def ban(ctx, user):
    """Banish people. Admin command."""
    try:
        if not ctx.message.author.guild_permissions.administrator:
            out = "You do not have permission to perform this action."
            message_return = finalize(ctx, 'ban', out, "OK")
            await ctx.send(message_return)
            return
        converter = commands.MemberConverter()
        userobj = await converter.convert(ctx, user)
        await ctx.guild.ban(userobj)
        out = f"{userobj.name} was banned from {ctx.guild.name}."
        message_return = finalize(ctx, 'ban', out, "OK")
        await ctx.send(message_return)
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'ban', out, out)
        await ctx.send(message_return)

@bot.command()
async def role(ctx, mode, user, role):
    """Give or take roles from people. Admin command.
z!role <give|take> <user> <role>"""
    try:
        if not ctx.message.author.guild_permissions.administrator:
            out = "You do not have permission to perform this action."
            message_return = finalize(ctx, 'unban', out, "OK")
            await ctx.send(message_return)
            return
        memberconverter = commands.MemberConverter()
        userobj = await memberconverter.convert(ctx, user)
        roleconverter = commands.RoleConverter()
        roleobj = await roleconverter.convert(ctx, role)
        if mode == 'give':
            await userobj.add_roles(roleobj)
            out = f"{user} was given {role}."
        if mode == 'take':
            await userobj.remove_roles(roleobj)
            out = f"{role} was removed from {user}."
        message_return = finalize(ctx, 'giverole', out, "OK")
        await ctx.send(message_return)
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'giverole', out, out)
        await ctx.send(message_return)
        
@bot.command() # Simple command used to see if the bot is running.
async def ping(ctx):
    """Kinda like poking me in the shoulder to see if I\'m awake."""
    out = 'Yes? Hello.'
    message_return = finalize(ctx, 'ping', out, "OK")
    await ctx.send(message_return)

@bot.command(aliases=['pot'])
async def potion(ctx):
    """Consumes a random potion, displays potion color, effect, and duration."""
    g_data = get_guild_data(ctx)
    if not g_data.data['dice']:
        return
    out = PotionRandomizer.potion_randomizer(ctx, g_data.data['potions'])
    message_return = finalize(ctx, 'potion', out, "OK")
    await ctx.send(message_return)

@bot.command() # Bot copies input text verbatum.
async def sudo(ctx, *, text):
    """I am able to say whatever you like. Almost.
Other options:
  e! - put before emojicode to convert into an emoji
  <timestamp> - inserts timestamp
  <lcd> - replaces all text after with white, 41-unit LCD characters
  </lcd>|</lcdr> - cancels LCD mode
  <lcdr> - replaces all text after with red, 16-unit LCD characters"""
    try:
        out = scan(text)
        message_return = finalize(ctx, 'sudo', out, "OK", text)
        await ctx.send(message_return)
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'sudo', out, out, text)
        await ctx.send(message_return)

@bot.command(aliases=['dice']) # Bot **s X Y-sided dice. Not as nice as Tsumikibot's dice system, and that's okay.
async def roll(ctx, dice: str, *formating: str):
    """Rolls some dice.
    Example: /roll 2d6
    Returns: 6, 2"""
    try:
        g_data = get_guild_data(ctx)
        if not g_data.data['dice']:
            return
        if dice[0] == 'd':
            dice = '1' + dice
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            out = 'Invalid dice! Proper syntax example: ' + prefix + 'roll 10d20'
            message_return = finalize(ctx, 'roll', out, "OK", dice)
            await ctx.send(message_return)
            return
        total = 0
        result = '('
        dieoutputs = {}
        singlerolls = True
        if rolls > 1:
            singlerolls = False
        while rolls > 0:
            roll = random.randint(1, limit)
            total += roll
            if len(formating) > 0:
                if formating[0] in 'cs':
                    dieoutputs[roll] = dieoutputs.setdefault(roll, 1)
            else: 
                result += str(roll)
                if rolls > 1:
                    result += ', '
            rolls -= 1
        if len(formating) > 0:
            if formating[0] == 'c':
                for num in dieoutputs.keys():
                    result += '[{0} × {1}s], '.format(dieoutputs[num], num)
                result = result[:-2]
        if not singlerolls:
            result += ') Total: ' + str(total)
        else:
            result += ')'
        message_return = finalize(ctx, 'roll', result, "OK", dice)
        await ctx.send(message_return)
    except Exception as e:
        result = f"Error: {e}"
        message_return = finalize(ctx, 'roll', result, result, dice)
        await ctx.send(message_return)

@bot.command(aliases=['choice']) # Bot randomly chooses between the inputs.
async def choose(ctx, *choices: str):
    """Lets me choose between two items."""
    message_return = finalize(ctx, 'choose', random.choice(choices), "OK", choices[0] + ' ' + choices[1])
    await ctx.send(message_return)

@bot.command() # Bot returns the date a given user joined.
async def joined(ctx, member):
    """Returns the date when a user joined this server."""
    memberconverter = commands.MemberConverter()
    userobj = await memberconverter.convert(ctx, member)
    ttime = translate_time(userobj.joined_at)
    datejoined = "UNIX {} {} {}, {}:{}:{}.{}'{} UTC".format(ttime[0], ttime[1], ttime[2], ttime[3], ttime[4], ttime[5], ttime[6], ttime[7])
    out = f'{userobj.name} joined this server on {datejoined}.'
    message_return = finalize(ctx, 'joined', out, "OK", member)
    await ctx.send(message_return)

@bot.command()
async def now(ctx):
    """Shows the current time anywhere on Earth."""
    DST = False
    out = f"San Francisco: {current_time(-8+DST)}\n\
Dallas: {current_time(-6+DST)}\n\
Washington DC: {current_time(-5+DST)}\n\
New York City: {current_time(-5+DST)}\n\
Universal Time: {current_time(0)}\n\
London: {current_time(0+DST)}\n\
Berlin: {current_time(1+DST)}\n\
Moscow: {current_time(3)}\n\
Beijing: {current_time(8)}\n\
Pyongyang: {current_time(9)}\n\
Tokyo: {current_time(9)}"
    message_return = finalize(ctx, 'now', out, "OK")
    await ctx.send(message_return)

@bot.command(aliases=['command', 'commands'])
async def cmd(ctx, *category):
    """Shows a list of available commands."""
    try:
        if len(category) == 1:
            category = str.lower(category[0])
        g_data = get_guild_data(ctx)
        tableOfContents = "```Commands:\nCore  - Basic commands."
        core = "```" + desc + """

Core Commands:
ach          Look at your achievements.
    Aliases: achieve, achievement, achievements
calc         Calculates equations.
    Aliases: calculate, calculator
changelog    Shows the changelog of this bot.
cmd          Shows this message
    Aliases: command, commands
debug        Allows testing of various things.
    Aliases: dbg
define       Returns the definition of the entered term. Use /define help for...
    Aliases: def, definition
emoji        Returns any emoji in my database!
    Aliases: em
emojilist    Lists global emojis! Use /emoji to return just one!
    Aliases: eml
events       Shows a list countdowns towards future events.
    Aliases: ev, event
help         Shows a list of all commands.
invite       Invite the bot to a server!
joined       Returns the date when a user joined this server.
joke         Cracks a joke.
minesweeper  Sweep the mines. The classic game, recreated in only 78 lines of code.
    Aliases: msw
now          Shows the current time anywhere on Earth.
ping         Kinda like poking me in the shoulder to see if I'm awake.
profile      Shows the profile and statistics of others.
    Aliases: pf
rate         Rate the bot 1 to 10! Can only be used once a month.
    Aliases: guild
speedcalc    Calculates speed! Input m/s. Mode 'long' unabbreviates everything.
    Aliases: spdcalc, spdcalculate, spdcalculator, speedcalculate, speedcalculator
splash       Returns a random splash
stats        General bot information.
sudo         I am able to say whatever you like. Almost.
set          /set <notation/desc/image/seeImg/muteLevelup/nick/color> (args...)
    Aliases: setting, settings
tcp          Displays info on other servers on the Trans-Core Pipeline!

```"""
        core2 = """```Notepad Commands:
append       Append text files! Be careful not to go over the 2k char limit!
read         Read text files! /read (userdata) (filenumber)
write        Write text files! Each user gets ten pages, 2000 characters each!"""
        if g_data.data['counting']:
            core2 += "\ncounting     Count forever!\n\
    Aliases: cnt, count"
        if g_data.data['portal']:
            core2 += "\nportal       Opens a portal for communication. Portals close automatically up..."
        core2 += '```'
        admin = """```Admin Commands:
ban          Ban people.
role         Give people roles.
kick         Kick people.
server       Admin command to modify serverdata.```"""
        core_ext = ""
        economy = ""
        crafting = ""
        levels = ""
        dice = ""
        if g_data.data['economy'] or g_data.data['crafting']:
            tableOfContents += "\nExt   - Commands that fit in multiple categories.\nAdmin - Admin commands."
            core_ext = """```Core Extended Commands:
boxes        Open treasure chests and crates!
    Aliases: box, open
cards        Look at your cards. (TODO)
trade        Trade or gift people your resources!
    Aliases: give, gift
tutorial     Learn how to use the more complex commands!
    Aliases: tut```"""
        if g_data.data['levels']:
            tableOfContents += "\nLevel - Commands involving experience, levels, and prestige."
            levels = """```Level Commands:
prestige     Increase your prestige level! You can only prestige after Lv50.
    Aliases: prst
resetmulti   Resets a multiplier for experience!
    Aliases: rsm```"""
        if g_data.data['dice']:
            tableOfContents += "\nDice  - Commands involving dice and randomness."
            dice = """```Randomizer Commands:
choose       Lets me choose between two items.
    Aliases: choice
roll         Rolls some dice.
    Aliases: dice
dnd_treasure Rolls treasure hoards and other stuff for D&D 5e!
    Aliases: d&d_treasure"""
        if g_data.data['dice'] and g_data.data['potion']:
            dice += "\npotion     Consumes a random potion, displays potion color, effect, and dur...\n\
    Aliases: pot"
        dice += "```"
        if g_data.data['economy']:
            tableOfContents += "\nEcon  - Commands involving money, shopping, and trading."
            economy = """```Economy Commands:
balance      Shows your rupees, coins, etc in an uncompressed format.
    Aliases: bal, money
buy          Buys an object from the shop. Parameters: <Item ID>
coingame     A coin will be flipped until it lands on tails. Each time it lan...
    Aliases: cg, cg1, coingame1
coingame2    Double or nothing! Place your bets and flip the coin! Max bet is...
    Aliases: cg2
coingame3    A coin will be flipped until the state changes. Each heads means...
    Aliases: cg3
col          View your collections.
    Aliases: col, collect, collection, collections
exchange     Exchange rupees and coins! Can only be used once daily.
    Aliases: xchg, exchg, exch
item         Buy or sell an item.
ibuy         Buy an item.
    Aliases: ib
isell        Sell an item.
    Aliases: is
iinfo        Get info on an item.
    Aliases: ii
lootcrate    Open loot crates!
    Aliases: crate, crates, lootcrates, lootbox, lootboxes
meow         Play with meow.
shop         Shows the things that you can buy. Parameters: <Page #>```"""
        if g_data.data['crafting']:
            tableOfContents += '\nCraft - Commands that involve resource management, crafting, and items.'
            crafting = """```Crafting Commands:
autocraft  Allows autocrafting of items. Requires a factory to be built.
    Aliases: ac, autocrafting
builds     Look at your civ.
    Aliases: trees, town, village
chop       Chop down trees. You can only do so once per day.
craft      Crafts an object from the blueprint library. Parameters: <Item I...
dumpdive   Retrieves a random item from the landfill.
    Aliases: dive
inv        View your inventory.
    Aliases: inventory
mine       Mine ore. You can only do so once per day. Clovers get you a bit...
recipes    Shows the things that you can craft. Parameters: <Page #>
    Aliases: recipe, blueprint, blueprints
tax        Tax your land's tenants!
tools      Look at your tools.
trash      Remove items from your inventory.
    Aliases: garbage```"""
        tableOfContents += "\n\nType z!cmd <category> to get info on individual commands.```"
        if len(category) == 0:
            out = tableOfContents
        else:
            toc = {'core':core2, 'ext':core_ext, 'admin':admin, 'level':levels, 'dice':dice, 'econ':economy, 'craft':crafting}
            out = toc[category]
            if category == "core":
                await ctx.send(core)
            out += """```Type z!help <command> for more info on a command.```"""
        #await ctx.send(core)
        #await ctx.send(core2)
        #if economy != "```":
        #    await ctx.send(economy)
        message_return = finalize(ctx, 'cmd', out, "OK")
        await ctx.send(message_return)     
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'cmd', out, out)
        await ctx.send(message_return)        

@bot.command() # Meow!
async def meow(ctx, *pat_the_meow):
    """Play with meow.
Please 'pat' the meow."""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy'] or not g_data.data['crafting']:
        return
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    embed = discord.Embed(color=0x8000FF)
    if len(pat_the_meow) == 0:
        link = 'https://cdn.discordapp.com/emojis/484904964985061376.gif?v=1'
        if user_data.haz_meow() == False:
            embed.title="There is no meow here... ;w;"
        else:
            embed.title="Meow!"
            embed.set_image(url=link)
        message_return = finalize(ctx, 'meow', None, "OK")
        await ctx.send(embed=embed)
    elif str.lower(pat_the_meow[0]) == 'pat' or str.lower(pat_the_meow[0]) == 'pet':
        link = 'https://cdn.discordapp.com/attachments/620517688288215041/690706710284730399/019.gif'
        if user_data.haz_meow() == False:
            embed.title="There is no meow to pat... ;w;"
        else:
            embed.title="Meow! :heart:"
            embed.set_image(url=link)
            user_data.data['haz pet meow'] = True
            save_user_data(user_data)
        message_return = finalize(ctx, 'meow', None, "OK", 'pat')
        await ctx.send(embed=embed)

@bot.command()
async def splash(ctx):
    "Returns a random splash"
    message_return = finalize(ctx, 'splash', get_splash(), "OK")
    await ctx.send(message_return)
    
@bot.command(aliases=['eml'])
async def emojilist(ctx, *page_req: int):
    """Lists global emojis! Use /emoji to return just one!"""
    if len(page_req) == 0:
        show_all = True
    else:
        page_req = page_req[0]
        show_all = False
    page = 0
    total_emoji = len(ResourceParse.emojidata.keys())
    emoteperpage = 30
    pagecursor = emoteperpage
    pages = total_emoji // emoteperpage
    emojis = 0
    line = ''
    emoji_list = []
    out = ['']
    if show_all == False:
        if page_req < 1 or page_req > pages+1:
            errout = 'Desired page does not exist!'
            message_return = finalize(ctx, 'emojilist', errout, "OK", str(page_req))
            await ctx.send(message_return)
            return
    for key in ResourceParse.emojidata.keys():
        emoji_list.append(key)
    while page <= pages:
        page += 1
        header = '`=== Emoji List - Page {0} ===\n===========================\n`'.format(page)
        out.append(header)
        while emojis < pagecursor:
            line = emoji_list[emojis] + ' - ' + ResourceParse.emojidata[emoji_list[emojis]] + '     '
            emojis += 1
            out[page] = out[page] + line
        if show_all == True:
            await ctx.send(out[page])
        pagecursor += min(emoteperpage, total_emoji - pagecursor)

    if show_all == True:
        message_return = finalize(ctx, 'emojilist', None, "OK")
    elif show_all == False:
        message_return = finalize(ctx, 'emojilist', out[page_req], "OK", str(page_req))
        await ctx.send(message_return)
    
@bot.command(aliases=['em', 'emoj'])
async def emoji(ctx, emoji):
    """Returns any emoji in my database!"""
    message_return = finalize(ctx, 'emoji', ResourceParse.emojidata[emoji], "OK", str(emoji))
    await ctx.send(message_return)

@bot.command()
async def joke(ctx, *id: int):
    """Cracks a joke."""
    jokes = ['What do you get when you cross the language of Romans with the language of swine?\n\n\nPiglatin.',
             'Yo mama so fat she needs cheat codes for Wii Fit!',
             'I\'m So Meta Even This Acronym',
             'Knock knock!\nWho\'s there?\nThe door!',
             'Your face!',
             'What did the meat say to the other meat?\n\n\n"Nice to meat you!"',
             'Prophecy Class cancelled due to unforseen circumstances.',
             'What do you call a fruit that polishes shoes?\n\n\nFruit cobbler.',
             'Why do people in Athens hate getting up early?\n\n\nBecause Dawn is tough on Greece',
             'I started a band with 999 Megabytes. Still can\'t get a gig.',
             'You meet a man on the Oregon Trail.\nHe tells you his name is Terry.\nYou laugh and tell him, "That\'s a girl\'s name!"\nTerry shoots you.\nYou have died of dissin\' Terry.',
             'If “K” is short for OK and some people call their grandpa “pop”, then “k-pop” is another way of saying “ok boomer”',
             'Nothing starts with N and ends with G.']
    if len(id) == 0:
        rand = random.randrange(len(jokes)-1)
    else:
        rand = id[0]-1
    try:
        out = str(rand+1) + ': ' + jokes[rand]
    except Exception:
        out = "Those arguments must be a joke, because they don't work in practice. There are only {} jokes in the list.".format(len(jokes))
    message_return = finalize(ctx, 'joke', out, "OK")
    await ctx.send(message_return)

@bot.command(aliases=['calculate', 'calculator'])
async def calc(ctx, x: int, funct: str, y: int):
    """Calculates equations.
    Addition: +, [1]
    Subtraction: -, [-1]
    Multiplication: ×, x, *, [2]
    Division: /, ÷, [-2]
    Floor Div: //
    Modulo: %, mod
    Exponent: ^, **, [3]
    Root: root, √, [-3]
    Multiplication by ten raised to a power: e, E, ×10^
    Multiplication by one thousand raised to a power: k, K, ×1000^"""
##    Tetration: ^^, ***, [4]
##    Super Root: sr, √√, [-4]"""
    out = '{0} {1} {2} = '.format(x, funct, y)
    string = ''
    integer = '{ℤ}, where ℤ = the set of all integer numbers.'
    real = '{ℝ}, where ℝ = the set of all real numbers'
    surreal = '{**No**}, where **No** = the class containing all surreal numbers'
    whole_surreal = '{**No**(ℤ)}, where **No**(ℤ) = the set of all surreal numbers where **No**(ℤ) % 1 = 0'
    if funct in ['+', '[1]']:
        result = x + y
    if funct in ['-', '[-1]']:
        result = x - y
    if funct in ['x', '*', '×', '[2]']:
        result = x * y
    if funct in ['/', '÷', '[-2]']:
        if y == 0:
            result = ''
            string = surreal
        else:
            result = x / y
    if funct in ['^', '**', '[3]']:
        if y < 0 < x < 1:
            y = abs(y)
            result = x**y
            string = 'i'
        elif x == 0 and y == 0:
            result = ''
            string = '{0, 1}'
        else:
            if abs(y) <= 3000003 and abs(x) <= 3000003:
                result = x ** y
            else:
                x, xk = infinityOverflow(x)
                y, yk = infinityOverflow(y)
                result = ''
                string = number_cronch([x**y, xk+yk], testfor_alt(ctx.message.author.id))
    if funct in ['root', '√', '[-3]']:
        if y < 0:
            y = abs(y)
            result = x**(1/y)
            string = 'i'
        elif x == 0 and y == 0:
            result = ''
            string = '{0, 1}'
        else:
            result = x**(1/y)
    if funct in ['e', 'E', '×10^', '*10^', 'x10^', '[2]10^', '×10**', '*10**', 'x10**', '[2]10**', '×10[3]', '*10[3]', 'x10[3]', '[2]10[3]']:
        if x == 0:
            result = 0
        else:
            if abs(y) <= 3000003:
                result = x * 1000 ** y
            else:
                result = ''
                string = number_cronch([x, y*3], testfor_alt(ctx.message.author.id))
    if funct in ['k', 'K', '×1000^', '*1000^', 'x1000^', '[2]1000^', '×1000**', '*1000**', 'x1000**', '[2]1000**', '×1000[3]', '*1000[3]', 'x1000[3]', '[2]1000[3]']:
        if x == 0:
            result = 0
        else:
            if abs(y) <= 1000001:
                result = x * 1000 ** y
            else:
                result = ''
                string = number_cronch([x, y], testfor_alt(ctx.message.author.id))
##    if funct in ['^^', '***', '[4]']:
##        k = [1]
##        loop = y
##        if (y > 10000 and x > 1) or (x > 10000 and y > 1):
##            result = 'Error: While loop too long, got dizzy.'
##            string = '\nTetration is a struct of great power. With great power comes great responsibility, and you, sir, did not use this great power responsibly.'
##            loop = 0
##        if x == 1:
##            result = 1
##            loop = 0
##        while loop > 0:
##            e = math.log10(x)
##            kpart = e/3
##            k.append(kpart)
##            loop -= 1
##        result = ''
##        string = number_cronch(k, testfor_alt(ctx.message.author.id))
##    if funct in ['sr', '√√', '[-4]']:
##        result = ''
##        string = '\nsr{0}[0,∞)→[0,∞) to be defined as sr{0}(n)={1} such that {1}^^{0}=n\nTell me what this means, and only then can I solve super roots.'.format('k', 'x')
    if funct in ['//']:
        if y == 0:
            result = ''
            string = whole_surreal
        else:
            result = x // y
    if funct in ['%', 'mod']:
        if y == 0:
            result = ''
            string = surreal
        else:
            result = x % y
    if not isinstance(result, str):
        if ResourceParse.is_infinite(result) and isinstance(result, float):
            out = out + '>k+102 (Float ∞)'
        result = number_cronch(result, testfor_alt(ctx.message.author.id))
    out = out + result + string
    message_return = finalize(ctx, 'calc', out, "OK", str(x) + funct + str(y))
    await ctx.send(message_return)
    return

@bot.command()
async def report(ctx, report_type, *, content:str):
    """Request features and report bugs!
Request types:
Bug - Something's not working right, or at all.
Request - Something should be added or removed (please provide reason).
Tweak - Something is a bit overpowered or underpowered."""
    if ctx.message.author.id == 569843596996378624:
        out = "User 'ChloroB' has been banned from using this command.\nReason: Duplicate report spam\n\
[000025 - BUG] Autocraft doesn't seem to work\n\
//[000026 - BUG DENIED] autocraft brok `(denied because duplicate of 000025)`\n\
//[000028 - BUG DENIED] autocraft stil brok pls fix my inv is ful `(denied because duplicate of 000025)`\n\
//[000029 - BUG DENIED] ac stil brok `(denied because duplicate of 000025)`\n\
//[000030 - BUG DENIED] give me my autocraft back >:( `(denied because duplicate of 000025)`"
    if str.upper(report_type) in ["BUG", "REQUEST", "TWEAK"] and content != "":
        filename = os.path.dirname(os.path.abspath(__file__)) + "\\data\\reports.txt"
        print(filename)
        with open(filename, 'a') as file:
            report = f"\n[{botdata.data['report ticket']:0>6} - {str.upper(report_type)}] {content}"
            file.write(report)
            file.close()
        botdata.data['report ticket'] += 1
        save_user_data(botdata)
        out = f"Report sent:{report}"
    else:
        out = "Either no report type was chosen, or no content was attached."
    message_return = finalize(ctx, 'report', out, "OK")
    await ctx.send(message_return)

@bot.command(aliases=['def', 'definition'])
async def define(ctx, *, term):
    """Returns the definition of the entered term. Use /define help for list of all definitions."""
    term = str.lower(term)
    definitions = {'small farm' : "Pop: 6\nArea: 12 ac\nTax: N/A\nA seedy place to work.",
                   'medium farm' : "Pop: 29\nArea: 51 ac\nTax: N/A\nWelcome to the rice fields, [REDACTED]. This is where you\'ll be working.",
                   'well' : "A deep subject that quenches people's thirst for both water and gossip.",
                   'silo' : "A tower that stores grain or other crops.",
                   'pickaxe' : "Can you dig it? With this, you sure can!",
                   'axe' : "Used for cutting down trees. Timber!",
                   'wood' : "Knocking on it is said to bring good luck. Might be an innuendo, however.",
                   'wood log' : "A thick, strong chunk of tree flesh that is used to make many things.",
                   'wood plank' : "Tier I tool-grade material. A slab of processed wood. Treat it with cyanide to keep termites from eating your precious creations.",
                   'wood stick' : "A rod made of wood. Might make a good handle, or support, or walking stick. Or poke someone with it, I don't care.",
                   'stone' : "Tier II tool-grade material. Perfectly generic rock. What type of rock is it? Granite, perhaps? Basalt? No one knows.",
                   'coal' : "A common fossil fuel produced by swamp plants being crushed and heated over a significant amount of time. Used for smelting.",
                   'coal block' : "1.33 metric tons of coal, compressed into a block one meter on a side.",
                   'tetrahedrite' : "Tetrahedrite is a teal-gray cubic crystal from which copper is extracted. It is composed of copper, iron, antimony, and sulphur. May also contain arsenic, zinc, silver, mercury, and lead.",
                   'copper block' : "8.96 metric tons of hard, conductive, shiny, orange metal, compressed into a block one meter on a side.",
                   'cassiterite' : "Cassiterite is a grey, silvery, or black tetragonal crystal made of tin oxide.",
                   'tin block' : "7.27 metric tons of grey metal, compressed into a block one meter on a side.",                   'bronze block' : "8.72 metric tons of hard orange metal, compressed into a block one meter on a side.",
                   'hematite' : "Hematite is a black, trigonal crystal. It is the most common iron oxide.",
                   'iron block' : "7.8 metric tons of iron, compressed into a cube one meter on a side.",
                   'diamond' : "Tier VI tool-grade material. Diamonds are often found in an ore known as Kimberlite. These colorless octahedral crystals of near pure carbon form under the immense heat and pressure found in the upper mantle.",
                   'diamond block' : "3.52 metric tons of shiny crystal, compressed into a cube one meter on a side.",
                   'native silver' : "Native silver is amorphous in shape and pure.",
                   'silver block' : "10.5 metric tons of shining silver, compressed into a cube one meter on a side.",
                   'steel block' : "7.83 metric tons of steel, compressed into a cube one meter on a side.",
                   'carbon block' : "2.1 metric tons of pure carbon, compressed into a block a meter on a side.",
                   'native gold' : "Native gold is amorphous in shape and pure. Gold nuggets are lumps of native gold that have come loose and have moved downstream from the main ore.",
                   'gold block' : "19.3 metric tons of soft, glistening metal.",
                   'native platinum' : "Native platinum is amorphous and pure. It requires extremely high temperatures in order to melt.",
                   'platinum block' : "21.5 metric tons of pure platinum",
                   'plutonite' : "Plutonium dioxide is a chartreuse cubic crystal. It glows yellow in the dark.",
                   'plutonium block' : "19.8 tons of slightly radioactive metal.",
                   'obsidian' : "A black, amorphous rock that forms when rhyolite lavas cool down too quickly. It shatters like glass, causing extremely sharp edges.",
                   'franciscite' : "Franciscite is a chartreuse, cubic crystal of californium(III) oxide. How does one even find this...?",
                   'californium block' : "15.1 metric tons of super-critical radioactive metal, shaped into a cube one meter on a side. You will probably die from handling this.",
                   'ringwoodite' : "Sometimes known as hellstone ore, this red, cubic rock forms super deep beneath the ground under high pressures. It must remain pressurized, otherwise it will decompose.",
                   'netherite ingot' : "An alloy of ringwoodite and gold. It has the durability of steel. *This is NOT Minecraft, please alloy ringwoodite with obsidian instead.*",
                   'hellstone block' : "3.3 metric tons of blisteringly hot metal, formed into the shape of a cube a meter per side.",
                   'carmeltazite' : "Tier IX tool-grade material. A strange and unusual mineral normally found within sapphire. This green, orthorhombic crystal is composed of titanium, aluminum, zirconium, and oxygen. It was discovered in UNIX 48, and is extremely rare and valuable.",
                   'carmeltazite block' : "3.52 metric tons of carmeltazite.",
                   'rutile' : 'Rutile is a blackish, tetragonal crystal composed of titanium dioxide.',
                   'titanium block' : '4.51 metric tons of titanium, compressed into a cubic meter. Titanium is corrosion-resistant.',
                   'titanium carbide block' : '4.93 tons of super hard metal.',
                   'megasick block' : '4.38 metric tons of magnesium carborundum, compressed into a cubic meter',
                   'majestic block' : '4.4 metric tons of magnesium titanium carborundum, compressed into a cubic meter.',
                   'ether' : 'A strange, otherworldly gas that composes the soul. Density cannot be determined, however it is known that around 100 grams of ether can be found in the average living human. This was discovered by weighing a dying person. Whether corruption has any physical effect on ether is unknown, but it is assumed that corruption binds to ether, making it heavier.',
                   'aetheric' : 'A colorless, near weightless gyro-shaped crystal. Binds to ether and magic energy extremely well, and can be used for data storage.',
                   'mithril block' : '700 kilograms of glowing, bluish metal, compressed into a block one meter per side.',
                   'rupee' : 'A hexagonal crystal of variable color, most commonly being green. Often used as a currency. Can be mined, however some species of trees grow the crystals on their bark.',
                   'coin' : 'A round, flat cylinder of metal, usually precious metal. Used as currency.',
                   'kup' : 'From Pikatonian *kuprium* and Latin *cuprum*. It is a coin made of copper. On the front, an image of Noobly\'s face as he is in his human form. On the back, an image of the Pikatonian flag.',
                   'arg' : 'From Pikatonian *argentium* and Latin *argentum*. It is a coin made of silver. On the front, an image of Ariel\'s face. On the back, an image of the Pikatonian flag.',
                   'auru' : 'From Pikatonium *aurium* and Latin *aurum*. It is a coin made of gold. On the front, an image of Pixel. On the back, an image of the Pikatonian flag.',
                   'pletus' : 'From Pikatonian *pletium* and Spanish *platino*. It is a coin made of platinum. On the front, an image of Scorch. On the back, an image of the Pikatonian flag.',
                   'kaali' : 'From Pikatonian *kälifurnium*, and English *californium*. It is a coin made out of californium. On the front, an image of Miniwa. On the back, an image of the Pikatonian flag.',
                   'clover' : 'A strange mutation of the common clover that imbued it with an extreme amount of luck, while giving it an extra leaf.',
                   'meow' : 'The sound a cat makes when attempting to get the attention of a human. I believe it is more like a roar, but quiet and squeaky. Rouw!',
                   'lathe' : 'A device that spins an item super fast, so it may be cut perfectly circular. The beginning of automation started here.',
                   'steam engine' : 'A machine that burns wood, coal, or oil to boil water, and use the expanding steam to turn a motor. Useful for automation. If placed on a car, the vehicle may reach a speed of 100km/h.',
                   'gasoline engine' : 'A machine that burns a petrolium byproduct to do work. If placed on a car, the vehicle may achieve a speed of up to 250km/h.',
                   'jet engine' : 'A machine that burns diesel fuel to turn a fan so quickly that extreme amounts of thrust are produced. If placed on a car, the vehicle will probably get flung and crash into the ground. If placed on an airplane, the vehicle will travel at a speed 1.2Mm/h or 12km/s.',
                   'rocket' : 'A vertical tube full of solid and/or liquid fuel components with a powerful engine on one end and a nose cone on the other. Depending on engine and thrust to weight ratio, the engine may achieve speeds of over 10km/s.',
                   'ion drive' : 'A special engine that uses the release of ionized xenon to propel a vehicle forward. The thrust is extremely low, but the fuel is really light, so it adds up. If placed onto a rocket, the vehicle may be able to reach a speed of 50km/s, though given enough fuel (and vacuum), could potentially reach Warp 0.5 with ease.',
                   'warp drive' : 'A drive that generates high mass in front of a vehicle, and negative mass behind to push objects through space. Is capable of speeds between 300Mm/s and 37.5Gm/s (Warp 1 and 5).',
                   'warp factor' : 'Cube root(Metric speed ÷ 300 million). Warp 1 is the speed of light, Warp 2 is 8c, Warp 3 is 27c, etc.',
                   'meta drive' : 'The powers of light and darkness, tamed and trapped, to spin forever. A Meta Drive ejects one Omni-0 core and one Omni-3 core into a cylindrical chamber at just the right speed, distance, and angle, that they orbit each other at unmeasurable velocities. This can be used to turn a turbine fast enough to generate effectively infinite energy, or if the cores are jettisoned, can cause a vehicle to slingshot off into red reality at speeds excess of 215.4 MWf (10 septillion ×c, 3 decillion m/s). This is the third fastest method of interversal transportation, still slower than teleportation and The Flash.',
                   'magnesite' : 'A pale, transluscent cubic crystal, from which magnesium may be obtained.',
                   'magnesium block' : '1.74 metric tons of soft, silvery metal, shaped into a cube a meter across.',
                   'quartz' : 'A transparent trigonal or hexagonal crystal of silicon dioxide.',
                   'silicon block' : '2.33 metric tons of pure silicon, shaped into a cube a meter across.',
                   'sphalerite' : 'A black to blue-gray cubic crystal of zinc sulfide.',
                   'zinc block' : '7.14 metric tons of silvery metal, shaped into a cube.',
                   'brass block' : '8.55 metric tons of shiny amber metal, shaped into a cube.',
                   'pegmatite' : 'An igneous rock that contains large mineral crystals, such as quartz, tourmaline, various salts, and much more. Lithium chloride can be extracted from it.',
                   'lithium block' : '534 kilograms of soft, reactive metal, shaped into a cube.',
                   'wolframite' : 'A blue-gray monoclinic crystal of ferrium wolfram tetroxide or manganese wolfram tetroxide.',
                   'tungsten block' : '19.3 metric tons of tungsten, shaped into a cube. To melt this much tungsten must\'ve been expensiv- wait, this was made by hand? How?',
                   'adamantium block' : '1.35 metric tons of adamantium, shaped into a cube. Might be useful for trapping powerful entities.',
                   'cobaltite' : 'A reddish orthorhombic crystal of cobalt, sulphur, and arsenic.',
                   'cobalt block' : '8.9 metric tons of cobalt, shaped into a cube a meter across.',
                   'lithium cobalt oxide block' : '5.4 metric tons of black, shiny salt, shaped into a cube a meter across.',
                   'pipe' : 'A tube of plastic or metal that can carry fluids, items, or gasses from one place to another.',
                   'gear' : 'A wheel with teeth that can interlock to transfer work from one place to another. Gears of different sizes act as mechanical transformers.',
                   'logging hut' : "Pop: 3\nArea: 2 ac\nTax: 0\nThe hut lumberjacks live in. There's a shed built onto the side of the hut where the gathered logs are stored."}
    with openfile('data\\item_list.txt', 'r') as file:
        itemlist = json.loads(file.read())
    for item in itemlist:
        if itemlist[item][3] != "":
            definitions[str.lower(item)] = itemlist[item][3]
    out = ''
    if term in ['help', 'list']:
        for definition in definitions:
            if len(out + definition + ', ') < 2000:
                out += definition
                if definition != list(definitions.keys())[len(definitions)-1]:
                    out += ', '
            else:
                await ctx.send(out)
                out = ''
    else:
        try:
            out = definitions[term]
            message_return = finalize(ctx, 'define', out, "OK", term)
            await ctx.send(message_return)
            return
        except Exception:
            out = 'This has not been defined yet or is misspelled.'
    message_return = finalize(ctx, 'define', out, "OK", term)
    await ctx.send(message_return)

@bot.command(aliases=['spdcalc', 'spdcalculate', 'spdcalculator', 'speedcalculate', 'speedcalculator'])
async def speedcalc(ctx, speed: float, *mode):
    """Calculates speed! Input m/s. Mode 'long' unabbreviates everything."""
    if len(mode) == 0:
        mode = 0
    elif mode[0] == 'long':
        mode = 1
    else:
        mode = 0
    metric = speed
    us = speed / 0.9144
    mach = speed / 340.3
    c = speed / 300000000
    wf = c**(1/3)
    perspective = {1: 'cross one meter', 24: 'cross a suburban lawn', 1100: 'travel one city block',
                   30000: 'cross a large city', 1400000: 'traverse the N/S length of the UK', 10800000: 'cross the width of Eurasia',
                   40000000: 'circumnavigate the Earth', 384500000: 'fly to Luna from Earth', 149500000000: 'fly to Sol from Earth',
                   778000000000: 'fly to Jupiter from Sol', 5000000000000: 'fly to Pluto from Sol', 9460*1000**4: 'travel one light year',
                   4.244*(9460*1000**4): 'travel to Alpha Centauri C', 100000*(9460*1000**4): 'travel across the Milky Way Galaxy',
                   2500000*(9460*1000**4): 'travel to the Andromeda Galaxy', 53800000*(9460*1000**4): 'travel to the Virgo Cluster',
                   500000000*(9460*1000**4): 'travel across the Laniakea Supercluster', 1000**3*(9460*1000**4): 'travel to the Sloan Great Wall',
                   440*1000**8: 'travel to the edge of the observable universe', 1000**9: 'travel to the edge of the universe',
                   6.25*1000**11: 'cross one multiverse', 22.456*1000**12: 'cross one metaverse', 512*1000**12: 'traverse the Core and reach the Inner Rim',
                   25.41*1000**13: 'reach the Middle Rim', 631.56*1000**13: 'reach the Outer Rim', 1000**14: 'cross from Red Reality into the eternal void'}
    metric_name = ['v', 'w', 'x', 'y', 'z', 'a', 'f', 'p', 'n', 'µ', 'm', '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'X', 'W', 'V',
                   'UDc ', 'DDc ', 'TDc ', 'QaDc ', 'QiDc ', 'SxDc ', 'SpDc ', 'ODc ', 'NDc ', 'Vg ', ]
    metric_name_long = ['Vendeko', 'Weko', 'Xoni', 'Yocto', 'Zepto', 'Atto', 'Femto', 'Pico', 'Nano', 'Micro', 'Milli', '',
                        'Kilo', 'Mega', 'Giga', 'Tera', 'Peta', 'Exa', 'Zeta', 'Yotta', 'Xona', 'Weka', 'Vendeka',
                        'Undecillion ', 'Duodecillion ', 'Tredecillion ', 'Quattordecillion ', 'Quindecillion ',
                        'Sexdecillion ', 'Septendecillion ', 'Octodecillion ', 'Novemdecillion ', 'Vigintillion ']
    met_orig = 11
    us_name = ['mil', 'p', 'P/', 'in', 'ft', 'yd', 'rd', 'ch', 'fl', 'mi', 'lea', 'LD', 'AU', 'ly', 'pc']
    us_name_long = ['Mils', 'Points', 'Pica', 'Inches', 'Feet', 'Yards', 'Rods', 'Chains', 'Furlongs', 'Miles',
                    'Leagues', 'Lunar Distances', 'Astronomical Units', 'Light Years', 'Parsecs']
    #calculate metric speed
    metric_name_marker = met_orig
    while metric >= 1000 and metric_name_marker <= len(metric_name)-2:
        metric /= 1000
        metric_name_marker += 1
    while metric < 1 and metric_name_marker > 0:
        metric *= 1000
        metric_name_marker -= 1
    if mode == 0:
        metric_out = 'Metric: {0} {1}m/sec\n'.format(round(metric, 3), metric_name[metric_name_marker])
    elif mode == 1:
        metric_out = 'Metric: {0} {1}Meters per Second\n'.format(round(metric, 3), metric_name_long[metric_name_marker])
    times = ['sec', 'min', 'hr', 'dy', 'mo', 'yr']
    times_long = ['Seconds', 'Minutes', 'Hours', 'Days', 'Months', 'Years']
    time_marker = 0
    time_out = ''
    clock_out = 2
    overflow = False
    #calculate perspective speed
    for length in perspective:
        if speed < length:
            time = length / speed
            if time > 60:
                time /= 60
                time_marker = 1
                if time > 60:
                    time /= 60
                    time_marker = 2
                    if time > 24:
                        time /= 24
                        time_marker = 3
                        if time > 30.4167:
                            time /= 30.4167
                            time_marker = 4
                            if time > 12:
                                time /= 12
                                time_marker = 5
                                time_metric = met_orig
                                overflow = True
                                while time >= 1000 and time_metric <= len(metric_name)-2:
                                    time /= 1000
                                    time_metric += 1
                                time = round(time, 3)
                                if mode == 0:
                                    time_out += '\nAt this speed, an object could ' + perspective[length] + ' in {0}{1}{2}'.format(time, metric_name[time_metric], times[time_marker])
                                elif mode == 1:
                                    time_out += '\nAt this speed, an object could ' + perspective[length] + ' in {0} {1}{2}'.format(time, metric_name_long[time_metric], times_long[time_marker])
            time = round(time, 3)
            if overflow == False:
                if mode == 0:
                    time_out += '\nAt this speed, an object could ' + perspective[length] + ' in {0}{1}'.format(time, times[time_marker])
                elif mode == 1:
                    time_out += '\nAt this speed, an object could ' + perspective[length] + ' in {0} {1}'.format(time, times_long[time_marker])
            if clock_out <= 0:
                break
            clock_out -= 1

    #calculate us custom speed
    us_name_marker = 5
    us_out = ''
    if us >= 5.5: #is at least 1 rod
        us /= 5.5
        us_name_marker = 6
        if us >= 4: #is at least 1 chain
            us /= 4
            us_name_marker = 7
            if us >= 10: # is at least 1 furlong
                us /= 10
                us_name_marker = 8
                if us >= 8: # is at least 1 mile
                    us /= 8
                    us_name_marker = 9
                    if us >= 3: # is at least 1 league
                        us /= 3
                        us_name_marker = 10
                        if us >= 80000: # is at least 1 lunar distance
                            us /= 80000
                            us_name_marker = 11
                            if us >= 1162.5: # is at least 1 astronomical unit
                                us /= 1162.5
                                us_name_marker = 12
                                if us >= 63241: # is at least 1 light year
                                    us /= 63241
                                    us_name_marker = 13
                                    if us >= 4.2: # is at least 1 parsec:
                                        us /= 4.2
                                        us_name_marker = 14
                                        us_metric_marker = met_orig
                                        while us >= 1000 and us_metric_marker <= len(metric_name)-2:
                                            us /= 1000
                                            us_metric_marker += 1
                                        if mode == 0:
                                            us_out = 'US Custom: {0} {1}{2}/sec\n'.format(round(us, 3), metric_name[us_metric_marker], us_name[us_name_marker])
                                        elif mode == 1:
                                            us_out = 'US Custom: {0} {1}{2} per Second\n'.format(round(us, 3), metric_name_long[us_metric_marker], us_name_long[us_name_marker])
    elif us < 1: # is less than 1 yard
        us *= 3
        us_name_marker = 4
        if us < 1: # is less than 1 foot
            us *= 12
            us_name_marker = 3
            if us < 1: # is less than 1 inch
                us *= 6
                us_name_marker = 2
                if us < 1: # is less than 1 pica
                    us *= 12
                    us_name_marker = 1
                    if us < 1: # is less than 1 point
                        us *= 13.8888888888
                        us_name_marker = 0
    if us_out == '':
        if mode == 0:
            us_out = 'US Custom: {0} {1}/sec\n'.format(round(us, 3), us_name[us_name_marker])
        elif mode == 1:
            us_out = 'US Custom: {0} {1} per Second\n'.format(round(us, 3), us_name_long[us_name_marker])

    #calculate mach speed
    mach_metric_marker = met_orig
    while mach >= 1000 and mach_metric_marker <= len(metric_name)-2:
        mach /= 1000
        mach_metric_marker += 1
    while mach < 1 and mach_metric_marker > 0:
        mach *= 1000
        mach_metric_marker -= 1
    if mode == 0:
        mach_out = 'Machspeed: {0}Ma {1}\n'.format(metric_name[mach_metric_marker], round(mach, 3))
    elif mode == 1:
        mach_out = 'Machspeed: {0}Mach {1}\n'.format(metric_name_long[mach_metric_marker], round(mach, 3))

    #calculate lightspeed
    c_metric_marker = met_orig
    while c >= 1000 and c_metric_marker <= len(metric_name)-2:
        c /= 1000
        c_metric_marker += 1
    while c < 1 and c_metric_marker > 0:
        c *= 1000
        c_metric_marker -= 1
    if mode == 0:
        c_out = 'Lightspeed: {0} {1}c\n'.format(round(c, 3), metric_name[c_metric_marker])
    elif mode == 1:
        c_out = 'Lightspeed: {0} {1}Celeritas\n'.format(round(c, 3), metric_name_long[c_metric_marker])

    #calculate warp factor
    wf_metric_marker = met_orig
    while wf >= 1000 and wf_metric_marker <= len(metric_name)-2:
        wf /= 1000
        wf_metric_marker += 1
    while wf < 1 and wf_metric_marker > 0:
        wf *= 1000
        wf_metric_marker -= 1
    if mode == 0:
        wf_out = 'Warp Factor: {0}wf {1}\n'.format(metric_name[wf_metric_marker], round(wf, 3))
    elif mode == 1:
        wf_out = 'Warp Factor: {0}Warp {1}\n'.format(metric_name_long[wf_metric_marker], round(wf, 3))

    out = metric_out + us_out + mach_out + c_out + wf_out + time_out
    message_return = finalize(ctx, 'speedcalc', out, "OK", str(speed))
    await ctx.send(message_return)

@bot.command(aliases=['rsm'])
async def resetmulti(ctx, multi): # multi can be money or pick
    """Resets a multiplier for experience!
    Reset types: money, pick"""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy'] or not g_data.data['crafting'] or not g_data.data['levels']:
        return
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    if multi == 'pick':
        multi_val = round(user_data.get_pickaxe_power()/50 - 10)
        user_data.add_exp(multi_val)
        user_data.reset_pickaxe_power()
        out = 'Pickaxe reset! Gained {0} XP!'.format(multi_val)
    if multi == 'money':
        multi_val = round(user_data.get_money_multiplier()/50 - 1)
        user_data.add_exp(multi_val * 25)
        user_data.reset_money_multiplier()
        out = 'Money multi reset! Gained {0} XP!'.format(multi_val * 25)
    save_user_data(user_data)
    message_return = finalize(ctx, 'resetmulti', out, "OK", multi)
    await ctx.send(message_return)

@bot.command(aliases=['prst'])
async def prestige(ctx):
    "Increase your prestige level! You can only prestige after Lv50."
    g_data = get_guild_data(ctx)
    if not g_data.data['levels']:
        return
    ping = '\n<@&657686368314589186> <@&601426305430323221> Get this user '
    prstAch = {1:ping + 'Prestige.mod!', 2:'', 3:'', 4:ping + 'a free Custom Color!', 5:'', 6:ping + 'a free Custom Role!', 8:'', 10:ping + 'a free Custom Channel!', 12:12, 15:15, 20:'a free Custom Module!'}
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    current_level = user_data.lv()
    prestige, rupOut = 0, 0
    achMsg = ''
    if user_data.lv() < 50:
        out = 'You must be at least Lv50 to prestige!'
        message_return = finalize(ctx, 'prestige', out, "OK")
        await ctx.send(message_return)
        return
    else:
        while current_level >= 50:
            current_level -= 50
            user_data.add_lv(-50)
            prestige += 1
            if (user_data.prst()+prestige) % 5 == 0:
                rupOut += (user_data.prst()+prestige) // 5 * 5000 * user_data.get_money_multiplier()
            for ach in prstAch:
                if (user_data.prst()+prestige) == ach:
                    user_data.achievements()['Prestige {}'.format(ach)] += 1
                    achMsg = ''
                    if g_data.data['id'] == '601420037445648385':
                        achMsg = prstAch[ach]
            rupOut += (user_data.prst()+prestige)*500*user_data.get_money_multiplier()
        user_data.add_lv(-current_level)
        user_data.add_exp(-user_data.exp())
        user_data.add_prst(prestige)
        user_data.add_rupees(rupOut)
        save_user_data(user_data)
        out = '**PRESTIGE UP!** You prestiged {0} time(s), and are now **Prst{1}! ({2})**'.format(prestige, user_data.prst(), ResourceParse.compress_rup_clov(rupOut, 'rupee', testfor_alt(ctx.message.author.id))) + achMsg
        message_return = finalize(ctx, 'prestige', out, "OK")
        await ctx.send(message_return)

@bot.command(aliases=['bal', 'money']) # Displays another user's ruppees, coins, land, clovers, pickaxe power, and collectables. 
async def balance(ctx, *args):
    """Shows the balance of a user."""
    identity = 0
    inputID = 'None'
    name = 'None'
    if len(args) == 0:
        converter = commands.MemberConverter()
        user = await converter.convert(ctx, ctx.message.author.name)
        identity = testfor_alt(ctx.message.author.id)
        user_data = get_user_data(identity)
        name = username(ctx.message.author, identity, user)[0]
        if user_data.nick() != '':
            name += ' (' + user_data.realname() + ')'
    if len(args) == 1:
        converter = commands.MemberConverter()
        user = await converter.convert(ctx, args[0])
        identity = testfor_alt(user.id)
        user_data = get_user_data(identity)
        name = username(user, identity, user)[0]
        if user_data.nick() != '':
            name += ' (' + user_data.realname() + ')'
    get_user_data(identity).loadall()
    if inputID != 'None':
        converter = commands.MemberConverter()
        user = await converter.convert(ctx, inputID)
        identity = testfor_alt(user.id)
        user_data = get_user_data(identity)
        name = username(ctx.message.author, identity)[0]
    if inputID == 'None' and name == 'None':
        identity = testfor_alt(ctx.message.author.id)
        user_data = get_user_data(identity)
        name = username(ctx.message.author, identity)[0]
    if user_data.rank() > 7:
        rank_msg = str(rank[7]) + str(user_data.rank()-7)
    else:
        rank_msg = str(rank[user_data.rank()])
    color = user_data.data['color']
    embed = discord.Embed(color=color)
    embed.title = '\n__**['+ rank_msg + '] ' + name + '\'s Balance**__'
    g_data = get_guild_data(ctx)
    own_data = get_user_data(testfor_alt(ctx.message.author.id))
    profile_img = ''
    files = user_data.data['zfiles']
    resourceMessage = ''
    if g_data.data['economy']:
        rupeeMessage = ResourceParse.rupEmojFind(user_data.rupees()) + format(int(user_data.rupees()), ',')
        silverMessage = ''
        if user_data.silver() >= 1000000000000:
            silverMessage += ResourceParse.compress_rup_clov(int(user_data.silver()//1000000000000), 'oc2_kaali', testfor_alt(ctx.message.author.id)) + '   '
        if user_data.silver() >= 1000000000:
            silverMessage += ResourceParse.compress_rup_clov(int(user_data.silver()//1000000000%1000), 'oc2_pluot', testfor_alt(ctx.message.author.id)) + '   '
        if user_data.silver() >= 1000000:
            silverMessage += ResourceParse.compress_rup_clov(int(user_data.silver()//1000000%1000), 'oc2_auru', testfor_alt(ctx.message.author.id)) + '   '
        if user_data.silver() >= 1000:
            silverMessage += ResourceParse.compress_rup_clov(int(user_data.silver()//1000%1000), 'oc2_arg', testfor_alt(ctx.message.author.id)) + '   '
        silverMessage += ResourceParse.compress_rup_clov(int(user_data.silver()%1000), 'oc2_kup', testfor_alt(ctx.message.author.id))
        cloversMessage = ResourceParse.compress_rup_clov(user_data.clovers(), 'oc2_clover', testfor_alt(ctx.message.author.id))
        landMessage = ResourceParse.emojidata["oc2_field"] + format(user_data.land(), ',') + ' acres'
        omnicreditMessage = ResourceParse.compress_rup_clov(user_data.omnicredits(), 'oc2_occ', testfor_alt(ctx.message.author.id))
        tixMessage = ':tickets:' + number_cronch(user_data.tickets(), testfor_alt(ctx.message.author.id))
        embed.add_field(name='*** === Rupees === ***', value=rupeeMessage, inline=False)
        embed.add_field(name='*** === Coins === ***', value=silverMessage, inline=False)
        embed.add_field(name='*** === Clovers === ***', value=cloversMessage, inline=False)
        embed.add_field(name='*** === Land === ***', value=landMessage, inline=False)
        embed.add_field(name='*** === OmniCredits === ***', value=omnicreditMessage, inline=False)
        embed.add_field(name='*** === Raffle Tickets === ***', value=tixMessage, inline=False)
    await ctx.send(embed=embed)
    save_user_data(user_data)
    message_return = finalize(ctx, 'balance', None, "OK", name)

@bot.command(aliases=['pf']) # Displays another user's ruppees, coins, land, clovers, pickaxe power, and collectables. 
async def profile(ctx, *args):
    """Shows the profile and statistics of others.
    /profile (user) (page)
    Page 1: Basic info
    Page 2: Tools (WIP)
    Page 3: Cards (TODO)
    Page 4: Trees & Land
    Page 5: Achievements
    Page 6: Collections
    Page 7: Inventory"""
    try:
        identity = 0
        page = 'None'
        inputID = 'None'
        name = 'None'
        if len(args) == 0:
            converter = commands.MemberConverter()
            user = await converter.convert(ctx, ctx.message.author.name)
            identity = testfor_alt(ctx.message.author.id)
            user_data = get_user_data(identity)
            if user_data == "[BRICKED]":
                pass
            name, realname = username(ctx.message.author, identity, user)
            if user_data.nick() != '':
                name += ' (' + user_data.realname() + ')'
        if len(args) == 2:
            converter = commands.MemberConverter()
            user = await converter.convert(ctx, args[0])
            name, realname = username(user, identity, user)
            inputID = args[0]
            page = int(args[1])
        if len(args) == 1:
            try:
                converter = commands.MemberConverter()
                user = await converter.convert(ctx, args[0])
                identity = testfor_alt(user.id)
                user_data = get_user_data(identity)
                if user_data == "[BRICKED]":
                    pass
                name, realname = username(user, identity, user)
                if user_data.nick() != '':
                    name += ' (' + user_data.realname() + ')'
            except BadArgument:  # first arg wasn't a member, but actually a page num
                identity = testfor_alt(ctx.message.author.id)
                user_data = get_user_data(identity)
                if user_data == "[BRICKED]":
                    pass
                page = int(args[0])
        get_user_data(identity).loadall()
        if page == 'None':
            page = 1
        if inputID != 'None':
            converter = commands.MemberConverter()
            user = await converter.convert(ctx, inputID)
            identity = testfor_alt(user.id)
            user_data = get_user_data(identity)
            if user_data == "[BRICKED]":
                pass
            name, realname = username(ctx.message.author, identity)
        if inputID == 'None' and name == 'None':
            identity = testfor_alt(ctx.message.author.id)
            user_data = get_user_data(identity)
            if user_data == "[BRICKED]":
                pass
            name, realname = username(ctx.message.author, identity)
        if user_data == "[BRICKED]":
            out = """```_ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___ ___
_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|__
_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|__
_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
___|___|___|___|___|_|                     |___|___|___|___|___|___|__
_|___|___|___|___|___|    USER DATA HAS    |_|___|___|___|___|___|___|
___|___|___|___|___|_|      BEEN FOUND     |___|___|___|___|___|___|__
_|___|___|___|___|___|       BRICKED       |_|___|___|___|___|___|___|
___|___|___|___|___|_|_____________________|___|___|___|___|___|___|__
_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|__
_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|__
_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|__
_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|
___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|__
Please contact Zako's administrator, Noobly Walker#4744```"""
            message_return = finalize(ctx, 'profile', out, "Error: Found Bricked Profile")
            await ctx.send(message_return)
            return
        user_data.data['realname'] = realname
        if user_data.rank() > 7:
            rank_msg = str(rank[7]) + str(user_data.rank()-7)
        else:
            rank_msg = str(rank[user_data.rank()])
        color = user_data.data['color']
        embed = discord.Embed(color=color)
        embed.title = '\n__**['+ rank_msg + '] ' + name + '\'s Profile**__'
        g_data = get_guild_data(ctx)
        user_data.inventory()
        user_data = load_badges(user_data)
        if page == 1:
            own_data = get_user_data(testfor_alt(ctx.message.author.id))
            profile_img = ''
            files = user_data.data['zfiles']
            if own_data.canSeeImages() == True:
                profile_img = user_data.profile_image()
            level_message = ''
            if g_data.data['levels']:
                level_message = user_data.get_level() + '\n'
            description_message = ''
            if user_data.desc() != '':
                description_message = '*\"{0}\"*\n'.format(user_data.desc())
            resourceMessage = ''
            if g_data.data['economy']:
                resourceMessage = '\n' + ResourceParse.compress(user_data.rupees(), user_data.silver(), user_data.clovers(),
                    user_data.land(), testfor_alt(ctx.message.author.id)) + ', ' + ResourceParse.compress_rup_clov(user_data.omnicredits(),
                    'oc2_occ', testfor_alt(ctx.message.author.id)) + ', :tickets:' + number_cronch(user_data.tickets(),
                    testfor_alt(ctx.message.author.id))
            pickaxe_message = ''
            meow_msg = ''
            mine_msg = ''
            chop_msg = ''
            edrink_msg = ''
            exch_msg = ''
            tax_msg = ''
            loot_msg = ''
            count_msg = ''
            bools2 = ''
            pickaxe = 0
            axe = 0
            moneymulti = 0
            countingmulti = 0
            rankcrates = {0 : 10, 1 : 15, 2 : 20, 3 : 30, 4 : 30, 5 : 30, 6 : 40, 7 : 50}
            rank2 = user_data.rank()
            if rank2 > 7:
                rank2 = 7
            rate_msg = ''
            if user_data.data['can rate bot']:
                rate_msg = '\nCan rate Zako: ' + bool_emoji(user_data.data['can rate bot']) + "\n> Rating the bot helps the devs know how well we're doing! You can only do this once a month."
            if g_data.data['crafting']:
                pickaxe = user_data.get_pickaxe_power()
                axe = user_data.get_axe_power()
                if user_data.haz_meow() == True:
                    meow_msg = '\nCan pet meow: ' + bool_emoji(not user_data.haz_pet_meow())
                mine_msg = '\nCan mine: ' + bool_emoji(user_data.data['can_mine'])
                chop_msg = '\nCan chop: ' + bool_emoji(user_data.data['can_chop'])
                edrink_msg = '\nCan drink E-drink: ' + bool_emoji(user_data.data['can drink e-drink'])
                dumpster_msg = '\nCan dumpdive: ' + bool_emoji(user_data.data['can dumpster dive'])
            if g_data.data['economy']:
                moneymulti = user_data.get_money_multiplier()
                countingmulti = user_data.get_counting_multiplier(botdata.lootbox_counting_multiplier())[0]
                exch_msg = '\nCan exchange: ' + bool_emoji(not user_data.data['exchange_cooldown'])
                tax_msg = '\nCan tax: ' + bool_emoji(not user_data.data['has_taxed'])
                loot_msg = '\nAvailable lootcrates: {}'.format(rankcrates[rank2]-user_data.data["crate_purchases"])
            if g_data.data['crafting'] or g_data.data['economy']:
                pickaxe_message = '\n' + ResourceParse.multi_compress(pickaxe, axe, moneymulti, countingmulti,
                    user_data.power(), testfor_alt(ctx.message.author.id)) + '\n'
                event = user_data.data['random event']
                event_msg = '**Current Event:** '
                if isinstance(event, str):
                    event_msg += event + global_event + '\n'
                elif isinstance(event, list):
                    event_msg += event[0] + '\n(' + event[1] + ')'+ global_event + '\n'
                bools2 = event_msg + mine_msg + chop_msg + edrink_msg + exch_msg + tax_msg + dumpster_msg + loot_msg + meow_msg + rate_msg
            if profile_img != '':
                embed.set_thumbnail(url=profile_img)
            writfiles = ''
            for file in files:
                if files[file] != '':
                    writfiles += file + ' '
            if writfiles == '':
                writfiles = 'None'
            badges = ''
            for badge in user_data.data['badges']:
                badges += badge
            if badges == '':
                badges = 'None'
            hexvalues = '0123456789ABCDEF'
            hexbits = [color//16**5%16, color//16**4%16, color//16**3%16, color//16**2%16, color//16**1%16, color//16**0%16]
            hexcolor = ''
            for bit in hexbits:
                hexcolor += hexvalues[bit]
            notat = {-1 : 'cubic', 0 : 'scientific', 1 : 'standard', 2 : 'engineering e', 3 : 'scientific e',
                     4 : 'k notation', 5 : 'illion', 6 : 'engineering', 7 : 'googology', 8 : 'engineering k',
                     9 : 'logarithm', 10 : 'exponential', 11 : 'roman/SI', 12 : 'long standard', 13 : 'long googology',
                     14 : 'hyper-e'}
            write = '\n**Pages:**\nOwned: {}\nWritten: '.format((user_data.bonus_slots()+1)*10) + writfiles + '\n\n**Badges:**\n' + badges + '\n\n'
            bools1 = 'Can see images: ' + bool_emoji(user_data.data['can see images']) + '\nMute levelup: ' + bool_emoji(user_data.data['mute levelup'])\
                     + '\nNotation: ' + notat[user_data.data['notation']] + '\nColor: ' + str(hexcolor) + '\n\n'
            if level_message + description_message != '':
                embed.add_field(name='*** === Basic Info === ***', value=level_message + description_message, inline=False)
            if resourceMessage + pickaxe_message + write != '':
                embed.add_field(name='*** === Balance & Multis === ***', value=resourceMessage + pickaxe_message + write, inline=False)
            if bools1 != '':
                embed.add_field(name='*** === Settings === ***', value=bools1, inline=False)
            if bools2 != '':
                embed.add_field(name='*** === Events & Abilities === ***', value=bools2, inline=False)
        elif page == 2:
            material = ['No', 'Wooden', 'Stone', 'Copper', 'Bronze', 'Iron', 'Diamond', 'Steel', 'Hellstone', 
                        'Carmeltazite', 'Titanium', 'Titanium Carbide', 'Magnesium Carborundium',
                        'Magnesium Titanium Carborundium', 'Mithril', 'Adamantium', 'Vibranium',
                        'Chlorophyte', 'Uru', 'Luminite', 'Megasteel']
            pickaxe = material[user_data.pickaxe_num()+1] + ' Pickaxe\n'
            pu = '  Sharpenened Tip: ' + bool_emoji(user_data.data['pick_sharpener']) + '\n  Extra Weight: ' + bool_emoji(user_data.data['pick_weight'])\
                 + '\n  Reinforced Handle: ' + bool_emoji(user_data.data['pick_handle']) + '\n  Lucky Wriststrap: ' + bool_emoji(user_data.data['pickaxe_wriststrap']) + '\n\n'
            axe = material[user_data.axe_num()+1] + ' Axe\n'
            au = '  Sharpenened Tip: ' + bool_emoji(user_data.data['axe_sharpener']) + '\n  Extra Weight: ' + bool_emoji(user_data.data['axe_weight'])\
                 + '\n  Reinforced Handle: ' + bool_emoji(user_data.data['axe_handle']) + '\n  Lucky Wriststrap: ' + bool_emoji(user_data.data['axe_wriststrap']) + '\n'
            if g_data.data['crafting']:
                embed.add_field(name='*** === Tools === ***', value=pickaxe + pu + axe + au, inline=False)
            else:
                embed.add_field(name='*** === Tools === ***', value="This page has been disabled in server settings.", inline=False)
        elif page == 3:
            embed.add_field(name='*** === Cards === ***', value='Cards will replace multipliers. They will act like inventory items, and five of the same card can be crafted together\
    to create a more powerful card. There will be ten levels, from 1.1× to 5×, and there will be several types of cards:\n× Pickaxes (pickaxe multiplier)\n\
    × Axes (axe multiplier)\n× Luck (causes pickaxes to be able to mine ores they can\'t otherwise)\n× Fortune (occasionally causes obtained items to duplicate)\n\
    × Internal Revenue (tax multiplier)\n× Military Power (military multiplier)\n× Crafting Efficiency (either consumes less resources or produces more output)', inline=False)
        elif page == 4:
            li = [user_data.data["civ"]["Simple Hut"]["count"], user_data.data["civ"]["Hut"]["count"], user_data.data["civ"]["Small Cottage"]["count"],
                  user_data.data["civ"]["Cottage"]["count"], user_data.data["civ"]["Small Village"]["count"], user_data.data["civ"]["Large Village"]["count"],
                  user_data.data["civ"]["Well"]["count"], user_data.data["civ"]["Silo"]["count"], user_data.data["civ"]["Small Farm"]["count"],
                  user_data.data["civ"]["Medium Farm"]["count"], user_data.data["civ"]["Clover Field"]["count"], user_data.data["civ"]["Beehive"]["count"],
                  user_data.data["civ"]["Furnace"]["count"], user_data.data["civ"]["Blast Furnace"]["count"], user_data.data["civ"]["Adamant Furnace"]["count"],
                  user_data.data['civ']['Factory']['count'], user_data.data["civ"]["Auto Furnace"]["count"], user_data.data["civ"]["Auto Blast Furnace"]["count"],
                  user_data.data["civ"]["Auto Adamant Furnace"]["count"], user_data.data["civ"]["Sawmill"]["count"], user_data.data["civ"]["Logging Hut"]["count"],
                  user_data.data["civ"]["Blacksmith"]["count"],
                  user_data.trees()['Oak Tree'], user_data.trees()['Maple Tree'], user_data.trees()['Spruce Tree'], user_data.trees()['Apple Tree'],
                  user_data.trees()['Rupee Tree'], user_data.trees()['Coin Tree'], user_data.trees()['Oak Grove'], user_data.trees()['Maple Grove'],
                  user_data.trees()['Spruce Grove'], user_data.trees()['Apple Grove'], user_data.trees()['Rupee Grove'], user_data.trees()['Coin Grove'],
                  user_data.trees()['Oak Forest'], user_data.trees()['Maple Forest'], user_data.trees()['Spruce Forest'], user_data.trees()['Apple Forest'],
                  user_data.trees()['Rupee Forest'], user_data.trees()['Coin Forest']]
            landitems = {0:[' Simple Hut\n', 2, 1, 5], 1:[' Hut\n', 3, 2, 7], 2:[' Small Cottage\n', 5, 3, 12], 3:[' Cottage\n', 10, 5, 15], #[name, pop, area, tax percapita]
                         4:[' Small Village\n', 28, 53, 20], 5:[' Large Village\n', 236, 368, 25], 6:[' Well\n', 0, 0, 0], 7:[' Silo\n', 0, 0, 0],
                         8:[' Small Farm\n', 6, 12, 5], 9:[' Medium Farm\n', 29, 51, 5], 10:[' Clover Field\n', 0, 1, 0], 11:[' Beehive\n', 0, 1, 0],
                         12:[' Furnace\n', 0, 0, 0], 13:[' Blast Furnace\n', 0, 0, 0], 14:[' Adamant Furnace\n', 0, 0, 0],
                         15:[' Factory\n', 0, 0, 0], 16:[' Furnace (Fac)\n', 0, 0, 0],
                         17:[' Blast Furnace (Fac)\n', 0, 0, 0], 18:[' Adamant Furnace (Fac)\n', 0, 0, 0], 19:['-bladed Sawmill\n', 0, 0, 0],
                         20:[' Logging Hut\n', 3, 2, 5], 21:[' Blacksmith\n', 3, 2, 5], 22:[' Oak Tree\n', 0, 1, 0],
                         23:[' Maple Tree\n', 0, 1, 0], 24:[' Spruce Tree\n', 0, 1, 0], 25:[' Apple Tree\n', 0, 1, 0], 26:[' Rupee Tree\n', 0, 3, 0],
                         27:[' Coin Tree\n', 0, 3, 0], 28:[' Oak Grove\n', 0, 10, 0], 29:[' Maple Grove\n', 0, 10, 0], 30:[' Spruce Grove\n', 0, 10, 0],
                         31:[' Apple Grove\n', 0, 10, 0], 32:[' Rupee Grove\n', 0, 30, 0], 33:[' Coin Grove\n', 0, 30, 0], 34:[' Oak Forest\n', 0, 100, 0],
                         35:[' Maple Forest\n', 0, 100, 0], 36:[' Spruce Forest\n', 0, 100, 0], 37:[' Apple Forest\n', 0, 100, 0], 38:[' Rupee Forest\n', 0, 300, 0],
                         39:[' Coin Forest\n', 0, 300, 0]}
            pop = 0
            area = 0
            income = 0
            text = ''
            mats = ['', 'Stone', 'Copper', 'Bronze', 'Iron', 'Diamond', 'Steel', 'Hellstone', 'Carmeltazite', 'Titanium', 'Titanium Carbide',
                    'Magnesium Carborundium', 'Majestic', 'Mithril', 'Adamantium', 'Vibranium', 'Chlorophyte', 'Uru', 'Luminite', 'Megasteel']
            for i in landitems:
                if i == 22:
                    text += 'Trees:\n'
                if li[i] != 0:
                    pop += li[i]*landitems[i][1]
                    area += li[i]*landitems[i][2]
                    if landitems[i][0] != '-bladed Sawmill\n':
                        text += str(li[i]) + landitems[i][0]
                    else:
                        text += mats[li[i]] + landitems[i][0]
                    if i in [5, 11, 20, 22]:
                        text += '\n'
                    income = li[i]*landitems[i][1]*landitems[i][3]
            grain = li[8]*10+li[9]*50
            user_data.set_developed_land(area)
            if g_data.data['crafting']:
                embed.add_field(name='*** === Trees and Land === ***', value='\n\nVillage Population: {0}\nArea: {1}\nTaxes (per day): \
                    {2}\nGrain (per day): {3}\n\n'.format(pop, ResourceParse.compress_land(area), income, grain) + text)
            else:
                embed.add_field(name='*** === Trees and Land === ***', value="This page has been disabled in server settings.", inline=False)
        elif page == 5:
            achievement_message = parseAchievements(ctx, user_data.achievements()) + '\n'
            embed.add_field(name='*** === Achievements === ***', value=achievement_message)
        elif page == 6:
            if g_data.data['economy']:
                collection_message = parseCollections(user_data.collections()) + '\n'
            else:
                collection_message = "This page has been disabled in server settings."
            embed.add_field(name='*** === Collections === ***', value=collection_message)
        elif page == 7:
            botdata.data['notation'] = -1
            save_user_data(botdata)
            inventory = user_data.inventory()
            if not g_data.data['economy'] and not g_data.data['crafting']:
                inventory_message = "This page has been disabled in server settings."
            else:
                inventory_message, inventory_message2 = parseInventory(ctx, inventory,False)
                inventory_message += '\n'
                inventory_message2 += '\n'
                volume = ResourceParse.number_cronch(user_data.get_inv_volume(), botdata.data['id'])
                maximum = ResourceParse.number_cronch(user_data.inv_size(), botdata.data['id'])
                embed.add_field(name=f"*** === Chests ({user_data.count_chests()}/{user_data.max_chests()}) - {volume}m³/{maximum}m³ === ***", value=user_data.chests_str(), inline=False)
            embed.add_field(name=f'*** === Inventory === ***', value=inventory_message)
            embed.add_field(name=' ⠀', value=inventory_message2)
            get_user_data("405968021337669632")
            botdata.data['notation'] = 0
            save_user_data(botdata)
        else:
            out_message = 'Page must be between 1 and 5.'
        pn = ['None', 'Basic Info', 'Tools', 'Cards', 'Trees and Land', 'Achievements', 'Collections', 'Inventory', 'None']
        embed.set_footer(text='Last Page: ' + pn[page-1] + ' | Page {0} of {1} | '.format(page, len(pn)-2) + 'Next Page: ' + pn[page+1])
        event_text = '' #Place custom text here.
        if mining_clover_event == True:
            event_text += '[EVENT] Three clovers can be used when using ' + prefix + 'mine!\n'
        if lootcrate_multi_event == True:
            event_text += '[EVENT] The special multi lootcrate can be obtained!\n'
        if event_text != '':
            await ctx.send('```' + event_text + '```')
        await ctx.send(embed=embed)
        save_user_data(user_data)
        message_return = finalize(ctx, 'profile', None, "OK", name)
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'profile', out, out)
        await ctx.send(message_return)

@bot.command()
async def tools(ctx, *args): #Runs z!profile <username> 2
    cmd_profile = bot.get_command("profile")
    if len(args) != 0:
        await ctx.invoke(cmd_profile, args[0], '2')
    else:
        await ctx.invoke(cmd_profile, ctx.message.author.name, '2')

@bot.command()
async def cards(ctx, *args): #Runs z!profile <username> 3
    cmd_profile = bot.get_command("profile")
    if len(args) != 0:
        await ctx.invoke(cmd_profile, args[0], '3')
    else:
        await ctx.invoke(cmd_profile, ctx.message.author.name, '3')

@bot.command(aliases=['town', 'village', 'trees'])
async def builds(ctx, *args): #Runs z!profile <username> 4
    cmd_profile = bot.get_command("profile")
    if len(args) != 0:
        await ctx.invoke(cmd_profile, args[0], '4')
    else:
        await ctx.invoke(cmd_profile, ctx.message.author.name, '4')

@bot.command(aliases=['achievements', 'achieve', 'achievement'])
async def ach(ctx, *args): #Runs z!profile <username> 5
    cmd_profile = bot.get_command("profile")
    if len(args) != 0:
        await ctx.invoke(cmd_profile, args[0], '5')
    else:
        await ctx.invoke(cmd_profile, ctx.message.author.name, '5')

@bot.command(aliases=['coll', 'collect', 'collection', 'collections'])
async def col(ctx, *args): #Runs z!profile <username> 6
    cmd_profile = bot.get_command("profile")
    if len(args) != 0:
        await ctx.invoke(cmd_profile, args[0], '6')
    else:
        await ctx.invoke(cmd_profile, ctx.message.author.name, '6')

@bot.command(aliases=['inventory'])
async def inv(ctx, *args): #Runs z!profile <username> 7
    cmd_profile = bot.get_command("profile")
    if len(args) != 0:
        await ctx.invoke(cmd_profile, args[0], '7')
    else:
        await ctx.invoke(cmd_profile, ctx.message.author.name, '7')

@bot.command(aliases=['cnt', 'count'])
async def counting(ctx, *args):
    """Count forever!
info|stats - Displays how your counting multi is calculated."""
    g_data = get_guild_data(ctx)
    if not g_data.data['counting']:
        return
    # Initializing current counts
    current_count = botdata.data.setdefault("current count", [0.0, 0])
    local_count = g_data.data.setdefault("current count", [0.0, 0])
    
    # Getting userdata
    identity = testfor_alt(ctx.message.author.id)
    user_data = get_user_data(identity)
    error_multi = user_data.event()['Rounding Error'] + 1
    counting_multi = user_data.get_counting_multiplier(botdata.lootbox_counting_multiplier())
    base = counting_multi[1]
    exponent = counting_multi[2] * 3 # ×3 to turn exponent from k to e

    embed = discord.Embed(color=0x8000FF)

    if len(args) == 0:
        # Global count setup
        bot_base = current_count[0]
        bot_exponent = current_count[1]
        bot_exponent_k = bot_exponent // 3
        bot_base_k = bot_base * 10**(bot_exponent - bot_exponent_k*3)
        bot_old = notatize(bot_base_k, bot_exponent_k, user_data.notation())
        
        # Local count setup
        local_base = local_count[0]
        local_exponent = local_count[1]
        local_exponent_k = local_exponent // 3
        local_base_k = local_base * 10**(local_exponent - local_exponent_k*3)
        local_old = notatize(local_base_k, local_exponent_k, user_data.notation())

        # Updating global exponent
        carryover = 1
        while exponent != bot_exponent:
            if bot_exponent > exponent:
                carryover /= 10
                exponent += 1
            if bot_exponent < exponent:
                carryover *= 10
                exponent -= 1
        bot_base += base * carryover * error_multi

        # Updating local exponent
        exponent = counting_multi[2]*3
        carryover = 1
        while exponent != local_exponent:
            if local_exponent > exponent:
                carryover /= 10
                exponent += 1
            if local_exponent < exponent:
                carryover *= 10
                exponent -= 1
        local_base += base * carryover * error_multi
        
        milestone = 0
        msout = ''

        # Global milestones
        milestones = ''
        mstitle = ''
        while bot_base > 10:
            bot_base /= 10
            bot_exponent += 1
            milestone += 200*bot_exponent
            if milestones != '':
                milestones += ','
            milestones += ' e' + str(bot_exponent)
        if milestone > 0:
            mstitle = '\nGlobal Milestones reached:' + milestones
            msout += '+' + ResourceParse.compress_rup_clov(milestone, 'rupee', identity) + ', '\
                    + ResourceParse.compress_coin(milestone*100, identity) + '\n\n'

        # Local milestones
        milestones = ''
        mstitle = ''
        while local_base > 10:
            local_base /= 10
            local_exponent += 1
            milestone += 20*local_exponent
            if milestones != '':
                milestones += ','
            milestones += ' e' + str(local_exponent)
        if milestone > 0:
            mstitle = '\nLocal Milestones reached:' + milestones
            msout += '+' + ResourceParse.compress_rup_clov(milestone, 'rupee', identity) + ', '\
                    + ResourceParse.compress_coin(milestone*100, identity)

        # Adding rupees from milestones
        if milestone > 0:
            user_data.add_rupees(milestone)
            user_data.add_silver(milestone*100)

        # Update global counting multi
        if botdata.data['counting highest exponent'] < bot_exponent:
            botdata.data['counting highest exponent'] = bot_exponent
        botdata.data['lootbox_counting_multi'] = [max(bot_exponent, botdata.data['counting highest exponent'])**2/100+1, 1]

        # Getting new global count
        bot_exponent_k = bot_exponent // 3
        bot_base_k = bot_base * 10**(bot_exponent - bot_exponent_k*3)
        bot_new = notatize(bot_base_k, bot_exponent_k, user_data.notation())

        # Getting new local count
        local_exponent_k = local_exponent // 3
        local_base_k = local_base * 10**(local_exponent - local_exponent_k*3)
        local_new = notatize(local_base_k, local_exponent_k, user_data.notation())

        # Preparing embed
        embed.title = username(ctx.message.author, identity)[0] + ' did a count!'
        embed.add_field(name="Global", value=bot_old + ' + ' + counting_multi[0] + ' =\n' + lcd_translate(bot_new, 'lcd'), inline=False)
        embed.add_field(name="Local", value=local_old + ' + ' + counting_multi[0] + ' =\n' + lcd_translate(local_new, 'lcd'), inline=False)

        # Saving data
        botdata.data["current count"] = [bot_base, bot_exponent]
        g_data.data["current count"] = [local_base, local_exponent]
        save_user_data(user_data)
        save_user_data(botdata)
        save_server_data(g_data)
        message_return = finalize(ctx, 'counting', None, "OK")

        # Displaying milestones and sending output
        if msout != '':
            embed.add_field(name=mstitle, value=msout, inline=False)
    elif len(args) == 1:
        if args[0] in ['info', 'stats']:
            zako = botdata.lootbox_counting_multiplier()
            bonus = user_data.lootbox_counting_multiplier()
            shop = user_data.get_shop_counting_multi()
            var = [number_cronch(zako[0]*10**((zako[1]-1)%3), identity, (zako[1]-1)//3),
                   number_cronch(user_data.prst()+1, identity),
                   number_cronch(user_data.rank()+1, identity),
                   number_cronch(user_data.lv()/2+1, identity),
                   number_cronch(bonus[0]*10**((bonus[1]-1)%3), identity, (bonus[1]-1)//3),
                   number_cronch(shop[0] ** shop[1], identity),
                   number_cronch(user_data.get_crafting_counting_multi(), identity),
                   number_cronch(base, identity, exponent//3)]
            embed.title = username(ctx.message.author, identity)[0] + '\'s Counting Multiplier'
            maths = "global × prestige × rank × level × lootbox × purchased × rune multi = counting multi"
            multi_calc = f"\n{var[0]} × {var[1]} × {var[2]} × {var[3]} × {var[4]} × {var[5]} × {var[6]} = {var[7]}"
            embed.add_field(name=" ⠀", value=maths + multi_calc)
    await ctx.send(embed=embed)

@bot.command()
async def read(ctx, *args):
    """Read text files! /read (userdata) (filenumber)"""
    identity = 0
    page = 'None'
    name = 'None'
    if len(args) == 0:
        out = prefix + 'read (userdata) (filenumber)'
        message_return = finalize(ctx, 'read', out, "OK", str(identity) + ' ' + page)
        await ctx.send(message_return)
        return
    if len(args) == 2:
        converter = commands.MemberConverter()
        user = await converter.convert(ctx, args[0])
        identity = user.id
        page = str(args[1])
    if len(args) == 1:
        identity = testfor_alt(ctx.message.author.id)
        page = str(args[0])
    user_data = get_user_data(identity)
    user_data.loadall()
    if user_data.nick() == '':
        name = username(ctx.message.author, identity)[0]
    else:
        realname = username(ctx.message.author, identity)[1]
        name = '\*' + user_data.nick() + '\*'
    if len(page) > 1:
        out = 'Invalid page number. Valid page numbers:\nN = 0123456789\nI = ABCDEFGHIJ\nII = KLMNOPQRST\nIII = UVWXYZabcd\nIV = efghijklmn\nV = opqrstuvwx\nVI = yz-_=+*/!?'
        message_return = finalize(ctx, 'read', out, "OK", name + ' ' + page)
        await ctx.send(message_return)
        return
    await ctx.send('Loading file ' + page + ' by ' + name + '...\n===========================================')
    try:
        out = user_data.data['zfiles'][page]
    except Exception:
        pass
    if out == '':
        out = '<Read Error: File Not Found>'
    message_return = finalize(ctx, 'read', out, "OK", name + ' ' + page)
    await ctx.send(message_return)
    return

@bot.command()
async def write(ctx, page: str, *, text):
    """Write text files! Each user gets ten pages, 2000 characters each!
To delete a file, just type /write <page> delete
Other options:
  e! - put before emojicode to convert into an emoji
  <timestamp> - inserts timestamp
  <lcd> - replaces all text after with LCD characters
  </lcd> - cancels LCD mode"""
    identity = testfor_alt(ctx.message.author.id)
    user_data = get_user_data(identity)
    err = ''
    slots = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_=+*/!?'
    if len(page) > 1 or page not in slots[:user_data.bonus_slots()*10+10]:
        err = 'Invalid page number. Valid page numbers:\nN = 0123456789\nI = ABCDEFGHIJ\nII = KLMNOPQRST\nIII = UVWXYZabcd\nIV = efghijklmn\nV = opqrstuvwx\nVI = yz-_=+*/!?'
    if text == ' ':
        err = 'The file is empty tho.'
    if err != '':
        message_return = finalize(ctx, 'write', err, "OK", page)
        await ctx.send(message_return)
        return
    if text == 'delete':
        user_data.data['zfiles'][page] = ''
        save_user_data(user_data)
        out = 'File ' + page + ' deleted.'
        message_return = finalize(ctx, 'write', out, "OK", page)
        await ctx.send(message_return)
        return
    text = scan(text)
    user_data.data['zfiles'][page] = text
    save_user_data(user_data)
    out = 'File ' + page + ' written successfully!'
    message_return = finalize(ctx, 'write', out, "OK", page)
    await ctx.send(message_return)

@bot.command()
async def append(ctx, page: str, *, text):
    """Append text files! Be careful not to go over the 2k char limit!"""
    identity = testfor_alt(ctx.message.author.id)
    user_data = get_user_data(identity)
    err = ''
    slots = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_=+*/!?'
    if len(page) > 1 or page not in slots[:user_data.bonus_slots()*10+10]:
        err = 'Invalid page number. Valid page numbers:\nN = 0123456789\nI = ABCDEFGHIJ\nII = KLMNOPQRST\nIII = UVWXYZabcd\nIV = efghijklmn\nV = opqrstuvwx\nVI = yz-_=+*/!?'
    if text == ' ':
        err = 'You cannot append a single space.'
    text = scan(text)
    try:
        file = user_data.data['zfiles'][page]
    except Exception:
        err = "You cannot append to a file that doesn't exist."
        file = ''
    if len(file + ' ' + text) > 2000:
        err = "File length too long!"
    if err != '':
        message_return = finalize(ctx, 'append', err, "OK", page)
        await ctx.send(message_return)
        return
    user_data.data['zfiles'][page] += ' ' + text
    save_user_data(user_data)
    out = 'File ' + page + ' written successfully!'
    message_return = finalize(ctx, 'append', out, "OK", page)
    await ctx.send(message_return)

@bot.command(aliases=['setting', 'settings'])
async def set(ctx, setting, *args):
    """/set <notation/desc/image/seeImg/muteLevelup/nick/color/badge> (args...)"""
    identity = testfor_alt(ctx.message.author.id)
    name = username(ctx.message.author, identity)[0]
    data = get_user_data(testfor_alt(ctx.message.author.id))
    if setting == 'desc':
        out = ''
        if len(args) == 0:
            args = ''
            out = '' + prefix + 'set desc <new description>\nYour description has been wiped.'
            data.set_desc(args)
            save_user_data(data)
            message_return = finalize(ctx, 'set', out, "OK", 'desc')
            await ctx.send(message_return)
            return
        cursor = 0
        string = ''
        while cursor < len(args)-1:
            string += args[cursor] + ' '
            cursor += 1
        string += args[cursor]
        args = string
        if len(args) > 255:
            out = 'Character limit exceeded! Description cannot be longer than 255 characters.'
            message_return = finalize(ctx, 'set', out, "OK", 'desc ' + args)
            await ctx.send(message_return)
            return
        args = scan(args)
        data.set_desc(args)
        save_user_data(data)
        out += '{0}\'s dscription now reads: \"{1}\"'.format(name, args)
        message_return = finalize(ctx, 'set', out, "OK", 'desc ' + args)
        await ctx.send(message_return)
    elif setting == 'notation':
        notat = {0 : 'scientific', 1 : 'standard', 2 : 'engineering e', 3 : 'scientific e',
        4 : 'k notation', 5 : 'illion', 6 : 'engineering', 7 : 'googology', 8 : 'engineering k',
        9 : 'logarithm', 10 : 'exponential', 11 : 'roman/SI', 12 : 'long standard', 13 : 'long googology',
        14 : 'hyper-e'}
        if len(args) == 0:
            out = prefix + 'set notation <notation id>\n0 - scientific: 1.234×10^2372\n1 - standard: 123.456NOgSpt\n2 - engineering e: 123.456e+2370\n\
3 - scientific e: 1.234e+2372\n4 - k notation: 123.456k+790\n5 - illion: 123.456 789-illion\n6 - engineering: 123.456×10^2370\n\
7 - googology: 123.456 NovemOctagintSeptingentillion\n8 - engineering k: 123.456×1000^790\n9 - logarithm: e265.424\n10 - exponential: e^5.782\n\
11 - roman/SI: 123.456DCCLXXXIX\n12 - long standard: 123.456kQaNgTt\n13 - long googology: 123.456 Thousand QuattorNonagintTrecentillion\n\
14 - hyper-e: e2.423#2'
            message_return = finalize(ctx, 'set', out, "OK", 'notation')
        else:
            notation = int(args[0])
            if notation > len(notat)+1 or notation < 0:
                out = 'Invalid notation!'
                message_return = finalize(ctx, 'set', out, "OK", 'notation ' + str(notation))
                await ctx.send(message_return)
                return
            data.set_notation(notation)
            save_user_data(data)
            out = 'Notation is set to ' + notat[notation]
            message_return = finalize(ctx, 'set', out, "OK", 'notation ' + str(notation))
        await ctx.send(message_return)
    elif setting == 'image':
        if len(args) == 0:
            out = prefix + 'set image <image url/clear>\nOnly supports PNG or GIF'
            message_return = finalize(ctx, 'set', out, "OK", 'image')
            await ctx.send(message_return)
            return
        else:
            data.profile_image()
            image = args[0]
            if image[-4:] == '.png' or image[-4:] == '.gif':
                data.data['profile image'] = image
                save_user_data(data)
                out = 'Image set!'
            elif image == 'clear':
                data.data['profile image'] = ''
                save_user_data(data)
                out = 'Image removed.'
            else:
                out = 'Invalid link provided. We only support PNG or GIF!'
            message_return = finalize(ctx, 'set', out, "OK", 'image ' + image)
            await ctx.send(message_return)
            return
    elif setting == 'seeImg' or setting == 'muteLevelup':
        if len(args) == 0 and setting == 'seeImg':
            out = prefix + 'set seeImg <true/false>\nToggles user images.'
            message_return = finalize(ctx, 'set', out, "OK", 'seeImg')
            await ctx.send(message_return)
            return
        elif len(args) == 0 and setting == 'muteLevelup':
            out = prefix + 'set muteLevelup <true/false>\nToggles whether you get notified whenever you level up.'
            message_return = finalize(ctx, 'set', out, "OK", 'muteLevelup')
            await ctx.send(message_return)
            return
        else:
            boolean = str.lower(args[0])
            data.canSeeImages()
            data.muteLevelup()
            stringdetail = {'seeImg' : ['the ability to see images on other\'s profiles!', 'can see images'], 'muteLevelup' : ['muted levelup notifications!', 'mute levelup']}
            if boolean == 'true' or boolean == 'on' or boolean == 'yes':
                data.data[stringdetail[setting][1]] = True
                out = name + ' now has ' + stringdetail[setting][0]
            elif boolean == 'false' or boolean == 'off' or boolean == 'no':
                data.data[stringdetail[setting][1]] = False
                out = name + ' no longer has ' + stringdetail[setting][0]
            else:
                out = 'Invalid input. This is a boolean, that means it can only be True or False.'
            save_user_data(data)
            message_return = finalize(ctx, 'set', out, "OK", setting + ' ' + boolean)
            await ctx.send(message_return)
            return
    elif setting == 'nick':
        out = ''
        if len(args) == 0:
            args = ''
            out = prefix + 'set nick <new nickname>\nYour nickname has been wiped.'
            data.data['nickname'] = ''
            save_user_data(data)
            message_return = finalize(ctx, 'set', out, "OK", 'nick')
            await ctx.send(message_return)
            return
        cursor = 0
        string = ''
        while cursor < len(args)-1:
            string += args[cursor] + ' '
            cursor += 1
        string += args[cursor]
        args = string
        if len(args) > 32:
            out = 'Character limit exceeded! Nickname cannot be longer than 32 characters.'
            message_return = finalize(ctx, 'set', out, "OK", 'nick ' + args)
            await ctx.send(message_return)
            return
        args = scan(args)
        data.data['nickname'] = args
        save_user_data(data)
        out += '{0}\'s nickname is now \"{1}\"'.format(name, args)
        message_return = finalize(ctx, 'set', out, "OK", 'nick ' + args)
        await ctx.send(message_return)
    elif setting == 'color':
        out = ''
        if len(args) == 0:
            args = ''
            out = prefix + 'set color <hex value>'
        if len(args[0]) != 6:
            out = 'Hexadecimal colors must be six digits long; RRGGBB.'
        hexchars = '0123456789abcdefABCDEF'
        if len(args[0]) == 6:
            if args[0][0] not in hexchars or args[0][1] not in hexchars or args[0][2] not in hexchars or args[0][3] not in hexchars or args[0][4] not in hexchars or args[0][5] not in hexchars:
                out = 'Hexadecimal has sixteen digits, 0123456789ABCDEF. The input color contains digits outside this range.'
        if out != '':
            message_return = finalize(ctx, 'set', out, "OK", 'color ' + args[0])
            await ctx.send(message_return)
            return
        hexd = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
        arg = str.upper(args[0])
        hexdec = {5 : arg[0], 4 : arg[1], 3 : arg[2], 2 : arg[3], 1 : arg[4], 0 : arg[5]}
        fromhex = 0
        for digit in hexdec:
            fromhex += hexd[hexdec[digit]] * 16 ** digit
        data.data['color'] = fromhex
        save_user_data(data)
        out = 'Color successfully set to ' + arg + '.'
        message_return = finalize(ctx, 'set', out, "OK", 'color ' + arg)
        await ctx.send(message_return)
    elif setting == 'badge':
        data = load_badges(data)
        if len(args) == 0:
            args = ''
            out = prefix + 'set badge <badge number>\nBadge number 0 means no badge.'
            arg = ''
        else:
            arg = int(args[0])
            bool1 = data.set_badge(arg)
            if bool1:
                badge = data.data["badges"][arg]
                if data.data["badges"][arg] == '':
                    badge = '<none>'
                out = f'Badge successfully set to {badge}'
            else:
                out = 'Badge was unable to be set.'
            save_user_data(data)
            message_return = finalize(ctx, 'set', out, "OK", f'badge {arg}')
            await ctx.send(message_return)
    else:
        out = prefix + 'set <notation/desc/image/seeImg/muteLevelup/nick/color> (args...)'
        message_return = finalize(ctx, 'set', out, "OK")
        await ctx.send(message_return)
        return

@bot.command(aliases=['msw'])
async def minesweeper(ctx, map_size: int, bombchance: int):
    """Generates a minesweeper game!
    map_size 4 <= x <= 12
    bombchance -30 <= y =< -1 and 1 <= y <= 30 (lower number means more bombs)"""
    if map_size > 12 or map_size < 4:
        out = "Error: The given map size is too large or small!"
        message_return = finalize(ctx, "minesweeper", out, "OK")
        await ctx.send(message_return)
        return
    if abs(bombchance) > 30 or abs(bombchance) < 1:
        out = "Error: The given bomb chance is too large or small!"
        message_return = finalize(ctx, "minesweeper", out, "OK")
        await ctx.send(message_return)
        return
    grid = []
    drops = []
    Bombs = 0
    if bombchance > 0:
        for i in range(abs(bombchance)):
            drops.append("None")
        drops.append("Bomb")
    elif bombchance < 0:
        for i in range(abs(bombchance)):
            drops.append("Bomb")
        drops.append("None")
    for i in range(map_size): #Generate grid and place bombs!
        grid.append([])
        for j in range(map_size):
            type = random.choice(drops)
            grid[i].append(type)
    for i in range(map_size): #Place numbers!
        for j in range(map_size):
            count = 0
            if grid[i][j] == "None":
                if j != 0 and grid[i][j-1] == "Bomb":
                    count += 1
                if j != map_size-1 and grid[i][j+1] == "Bomb":
                    count += 1
                if i != 0 and grid[i-1][j] == "Bomb":
                    count += 1
                if i != map_size-1 and grid[i+1][j] == "Bomb":
                    count += 1
                if i != 0 and j != 0 and grid[i-1][j-1] == "Bomb":
                    count += 1
                if i != 0 and j != map_size-1 and grid[i-1][j+1] == "Bomb":
                    count += 1
                if i != map_size-1 and j != 0 and grid[i+1][j-1] == "Bomb":
                    count += 1
                if i != map_size-1 and j != map_size-1 and grid[i+1][j+1] == "Bomb":
                    count += 1
                if count > 0:
                    grid[i][j] = "||" + scan(f"e!oc2_msw{count}")[:-1] + "||"
                else:
                    grid[i][j] = "||:black_large_square:||"
    out = ""
    out2 = ""
    for i in range(map_size): #Generate map!
        for j in range(map_size):
            if grid[i][j] == "Bomb":
                grid[i][j] = "||:bomb:||"
                Bombs += 1
            if (map_size > 5 and i < map_size//2) or (map_size <= 5):
            	out += grid[i][j]
            else:
                out2 += grid[i][j]
        if (map_size > 5 and i < map_size//2) or (map_size <= 5):
            out += "\n"
        else:
            out2 += "\n"
    if Bombs == map_size**2:
        out = f"Minesweeper - Oops! All bombs! ({Bombs}×Bombs)\n" + out
    else:
        out = f"Minesweeper - {Bombs}×Bombs\n" + out
    await ctx.send(out)
    if out2 != "":
        await ctx.send(out2)
    message_return = finalize(ctx, "minesweeper", None, "OK")

@commands.Cog.listener()
async def on_member_join(ctx, member): # Welcome message for when new users join. Untested.
    channel = member.guild.system_channel
    if channel is not None and developer_mode == 0:
        to_send = 'Welcome {0.mention} to {1.name}! Please read the server documentation in the Stats.mod, then pick out some #modules!'.format(member, ctx.guild)
        await channel.send(to_send)

#class Economy(commands.cog):

    #def __init__(self, bot):
    #    self.bot = bot
    #    self._last_member = None

@bot.command(aliases=['fav'])
async def favorite(ctx, *, args):
    """Mark an item as favorite to keep it from being sold in z!is all"""
    g_data = get_guild_data(ctx)
    if not g_data.data['crafting'] or not g_data.data['economy']:
        return
    user = get_user_data(testfor_alt(ctx.message.author.id))
    args = str.lower(args)
    args = args.split()
    arg2 = ''
    for arg in args:
        if arg != "of":
            if arg != args[len(args)-1]:
                arg2 += str.upper(arg[0]) + arg[1:] + ' '
            else:
                arg2 += str.upper(arg[0]) + arg[1:]
        else:
            if arg != args[len(args)-1]:
                arg2 += arg + ' '
            else:
                arg2 += arg
    args = arg2
    if args in user.inventory():
        user.inventory()[args][1] = not user.inventory()[args][1]
        save_user_data(user)
        if user.inventory()[args][1]:
            out = f"You marked {args} as favorite!"
        else:
            out = f"You have unmarked {args} as favorite!"
    else:
        out = f"\"{args}\" does not seem to exist. Please check your spelling and try again."
    message_return = finalize(ctx, 'favorite', out, "OK")
    await ctx.send(message_return)

@bot.command()
async def item(ctx, setting, *, args):
    """Buy or sell an item.\n/item <buy/sell/info> <item> <quantity>"""
    g_data = get_guild_data(ctx)
    if not g_data.data['crafting'] or not g_data.data['economy']:
        return
    user = get_user_data(testfor_alt(ctx.message.author.id))
    passin = ''
    args = str.lower(args)
    args = args.split()
    try:
        quantity = int(args[len(args)-1])
        args = args[:-1]
    except Exception:
        quantity = 1
    arg2 = ''
    for arg in args:
        if arg != args[len(args)-1]:
            arg2 += str.upper(arg[0]) + arg[1:] + ' '
        else:
            arg2 += str.upper(arg[0]) + arg[1:]
    args = arg2
    if quantity < 1:
        out = 'You cannot buy or sell any less than one item!'
        message_return = finalize(ctx, 'item', out, "OK", setting + ' ' + args)
        await ctx.send(message_return)
        return
    if args != 'All':
        if not user.inventory()[args][2]:
            out = 'You cannot trade an item you have not seen!'
            message_return = finalize(ctx, 'item', out, "OK", setting + ' ' + args)
            await ctx.send(message_return)
            return
    if setting == 'sell' and args == 'All':
        rupgain = 0
        to_remove = []
        for item in user.inventory():
            try:
                if user.inventory()[item][1] == True:
                    continue
                quant, price, qpr = botdata.data['prices'][item]
                quantity = user.inventory()[item][0]//qpr*qpr
                if quant < 25 or quantity == 0:
                    continue
                await ctx.send(f"Selling {quantity} of {item} for {price*quantity} rupees @ {price} rupees per {qpr} unit(s)...")
                botdata.inventory()[item][0] += quantity
                user.inventory()[item][0] -= quantity
                rupgain += price*quantity
            except Exception:
                await ctx.send(f"{item} is invalid, removing item and skipping...")
                to_remove.append(item)
        for item in to_remove:
            del user.inventory()[item]
        user.add_rupees(rupgain)
        out = 'You sold all items for {0} rupees.'.format(ResourceParse.compress_rup_clov(rupgain, 'rupee', testfor_alt(ctx.message.author.id)))
        save_user_data(user)
        save_user_data(botdata)
        message_return = finalize(ctx, 'item', out, "OK", setting + ' ' + args)
        await ctx.send(message_return)
        return
    quant, price, qpr = botdata.data['prices'][args]
    if quant < 25:
        out = f'There isn\'t a market for {args} yet.\nTotal amount of this item in circulation: ' + number_cronch(quant, testfor_alt(ctx.message.author.id)) + '\nWill be available for buying and selling once 25 are in circulation.'
        message_return = finalize(ctx, 'item', out, "OK", setting + ' ' + args)
        await ctx.send(message_return)
        return
    if setting == 'buy':
        quantity = int(-quantity//qpr*-1)
        if user.get_inv_volume() + quantity*qpr > user.inv_size():
            errout = "Your inventory is too full to do this!"
            message_return = finalize(ctx, 'item', errout, "OK")
            await ctx.send(message_return)
            return
        if botdata.inventory()[args][0] >= quantity*qpr and user.rupees() >= price*quantity:
            botdata.inventory()[args][0] -= quantity*qpr
            user.inventory()[args][0] += quantity*qpr
            user.add_rupees(-price*quantity)
            out = 'You bought {0} {1}(s) for {2} rupees.'.format(number_cronch(quantity*qpr,
                                                                testfor_alt(ctx.message.author.id)), args,
                                                                ResourceParse.compress_rup_clov(price*quantity, 'rupee',
                                                                testfor_alt(ctx.message.author.id)))
        else:
            out = 'Either you cannot afford this, or I am out of stock.'
    elif setting == 'sell':
        quantity = int(quantity//qpr)
        if user.inventory()[args][1] == True:
            out = 'You cannot sell a favorited item!'
        elif user.inventory()[args][0] >= quantity*qpr:
            botdata.inventory()[args][0] += quantity*qpr
            user.inventory()[args][0] -= quantity*qpr
            user.add_rupees(price*quantity)
            out = 'You sold {0} {1}(s) for {2} rupees.'.format(number_cronch(quantity*qpr,
                                                               testfor_alt(ctx.message.author.id)),
                                                               args, ResourceParse.compress_rup_clov(price*quantity,
                                                               'rupee', testfor_alt(ctx.message.author.id)))
        else:
            out = 'You don\'t have enough items to sell!'
    elif setting == 'info':
        botquant = botdata.inventory()[args][0]
        selfquant = user.inventory()[args][0]
        out = 'Item: ' + args + '\nTotal amount of this item in circulation: ' + number_cronch(quant, testfor_alt(ctx.message.author.id)) + '\nHow many I sell: ' + number_cronch(botquant, testfor_alt(ctx.message.author.id)) + '\nHow many you have: ' + number_cronch(selfquant, testfor_alt(ctx.message.author.id)) + '\nPrice: ' + ResourceParse.compress_rup_clov(price, 'rupee', testfor_alt(ctx.message.author.id)) + f" per {qpr} item(s)"
    save_user_data(user)
    save_user_data(botdata)
    message_return = finalize(ctx, 'item', out, "OK", setting + ' ' + args)
    await ctx.send(message_return)

@bot.command(aliases=['ib'])
async def ibuy(ctx, *, args): #Runs z!item buy
    cmd_item = bot.get_command("item")
    await ctx.invoke(cmd_item, 'buy', args=args)

@bot.command(aliases=['is'])
async def isell(ctx, *, args): #Runs z!item sell
    cmd_item = bot.get_command("item")
    await ctx.invoke(cmd_item, 'sell', args=args)

@bot.command(aliases=['ii'])
async def iinfo(ctx, *, args): #Runs z!item info
    cmd_item = bot.get_command("item")
    await ctx.invoke(cmd_item, 'info', args=args)

@bot.command(aliases=['cg', 'coingame1', 'cg1']) # Gain rupees based on how many heads are flipped
async def coingame(ctx):
    """A coin will be flipped until it lands on tails. Each time it lands on heads, the money doubles!"""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy']:
        return
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    user_rupees = user_data.rupees()
    if user_rupees < 6:
        out = 'You cannot afford to gamble!'
        message_return = finalize(ctx, 'coingame', out, "OK")
        await ctx.send(message_return)
        return
    coin = random.randrange(2)
    winnings = 0
    wins = 0
    rupee = -6
    while coin == 1:
        wins += 1
        winnings = 2**wins*5
        rupee -= 6
        coin = random.randrange(2)
    rupee += winnings
    if wins < 2:
        flash = '**Loss!** '
        net = ' losing '
    if wins >= 2:
        net = ' winning '
        if wins < 5:
            flash = '**Win!** '
        elif wins < 10:
            flash = '**Big Win!** '
        elif wins < 15:
            flash = '***Huge Win!*** '
        elif wins < 20:
            flash = '***JACKPOT!!!*** '
        elif wins >= 20:
            flash = '__***SUPER JACKPOT!!!***__ '
    user_data.add_rupees(rupee)
    save_user_data(user_data)
    out = flash + username(ctx.message.author, testfor_alt(ctx.message.author.id))[0] + ' flipped heads {0} times,'.format(wins) + net + '{0}'.format(ResourceParse.compress_rup_clov(rupee, 'rupee', testfor_alt(ctx.message.author.id)))
    message_return = finalize(ctx, 'coingame', out, "OK")
    await ctx.send(message_return)

@bot.command(aliases=['cg2']) # Double or nothing.
async def coingame2(ctx, wager: int):
    """Double or nothing! Place your bets and flip the coin! Max bet is 500kr"""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy']:
        return
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    user_rupees = user_data.rupees()
    if wager < 1:
        out = 'You cannot wager less than one rupee!'
        message_return = finalize(ctx, 'coingame2', out, "OK", str(wager))
        await ctx.send(message_return)
        return
    if user_rupees < wager:
        out = 'You cannot afford to wager this much!'
        message_return = finalize(ctx, 'coingame2', out, "OK", str(wager))
        await ctx.send(message_return)
        return
    if 500000 < wager:
        out = 'This is over the maximum wager! You can only bet 500k or less!'
        message_return = finalize(ctx, 'coingame2', out, "OK", str(wager))
        await ctx.send(message_return)
        return
    coin = random.randrange(2)
    if coin == 0:
        flash = '**Loss!** '
        net = ' lost and got nothing!'
        rupee = -wager
    if coin == 1:
        flash = '**Win!** '
        net = ' won an additional {}!!!'.format(ResourceParse.compress_rup_clov(wager, 'rupee', testfor_alt(ctx.message.author.id)))
        rupee = wager
    user_data.add_rupees(rupee)
    save_user_data(user_data)
    out = flash + username(ctx.message.author, testfor_alt(ctx.message.author.id))[0] + net
    message_return = finalize(ctx, 'coingame2', out, "OK", str(wager))
    await ctx.send(message_return)

@bot.command(aliases=['cg3']) # Gain or lose rupees based on how many heads or tails are flipped
async def coingame3(ctx):
    """A coin will be flipped until the state changes. Each heads means greater winnings, and each tails means greater losses! Debt is possible, too."""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy']:
        return
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    user_rupees = user_data.rupees()
    if user_rupees < 6:
        out = 'You cannot afford to gamble!'
        message_return = finalize(ctx, 'coingame', out, "OK")
        await ctx.send(message_return)
        return
    coin = random.randrange(2)
    state = coin
    change = 0
    loops = 0
    rupee = -6
    while coin == state:
        loops += 1
        change = 2**loops*5
        coin = random.randrange(2)
    if state == 0:
        change *= -1
    rupee += change
    if state == 1:
        coinside = 'heads'
        if loops < 1:
            flash = '**Loss!** '
            net = ' losing '
        if loops >= 1:
            net = ' winning '
            if loops < 5:
                flash = '**Win!** '
            elif loops < 10:
                flash = '**Big Win!** '
            elif loops < 15:
                flash = '***Huge Win!*** '
            elif loops < 20:
                flash = '***JACKPOT!!!*** '
            elif loops >= 20:
                flash = '__***SUPER JACKPOT!!!***__ '
    elif state == 0:
        coinside = 'tails'
        net = ' losing '
        if loops < 5:
            flash = '**Loss!** '
        elif loops < 10:
            flash = '**Big Loss!** '
        elif loops < 15:
            flash = '***Huge Loss!*** '
        elif loops < 20:
            flash = '***BANKRUPCY!!!*** '
        elif loops >= 20:
            flash = '__***SUPER BANKRUPCY!!!***__ '
    user_data.add_rupees(rupee)
    save_user_data(user_data)
    out = flash + username(ctx.message.author, testfor_alt(ctx.message.author.id))[0] + f' flipped {coinside} {loops} times,' + net + '{0}'.format(ResourceParse.compress_rup_clov(rupee, 'rupee', testfor_alt(ctx.message.author.id)))
    message_return = finalize(ctx, 'coingame3', out, "OK")
    await ctx.send(message_return)

@bot.command(aliases=['crate', 'crates', 'lootcrates', 'lootbox', 'lootboxes']) # Bot opens a specified number of lootcrates. Spaghet warning!
async def lootcrate(ctx, table_type: str, quantity: int):
    """Open loot crates!
    Crate types: common (250r), uncommon (2.5kr), rare (25kr), multiplier (0r)"""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy']:
        return
    # --- User Data --- #
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    multi = user_data.get_money_multiplier()
    user_data.daily_reset()
    crate_purchases = user_data.data.setdefault('crate_purchases', 0)
    multi_purchase = user_data.data.setdefault('event_daily', False)
    # --- Error Codes --- #
    err = ''
    if user_data.get_inv_volume() > user_data.inv_size():
        err = "Your inventory is too full to do this!"
    if quantity > 50:
        err = 'No more than 50 crates can be purchased at a time!'
    if table_type == 'multi' or table_type == 'm':
        if lootcrate_multi_event == False:
            err = 'Crate type locked!'
        elif lootcrate_multi_event == True:
            if multi_purchase == True:
                err = 'You have already opened your daily Multi Crate!'
            else:
                user_data.data['event_daily'] = True
            if quantity > 1:
                err = 'Only one crate of this type may be purchased!'
    if err != '':
        message_return = finalize(ctx, 'lootcrate', err, "OK", table_type + ' ' + str(quantity))
        await ctx.send(message_return)
        return
    # --- Variable Initialization --- #
    crates = {
        'commonCrate': 0,
        'uncommonCrate': 0,
        'rareCrate': 0,
        'multiCrate': 0
        }
    treas, rupOut, silverOut, cloverOut, deedOut, moneyMult, countMult, pickMult, rankOut = 0, 0, 0, 0, 0, 1, 1, 1, 0
    collType = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rupeeMessage, coinMessage, cloverMessage, deedMessage, moneyMessage, countMessage, pickMessage, rankMessage = '', '', '', '', '', '', '', ''
    remaining_deeds = remaining_land(ctx)
    # --- Converting crate name and setting variables --- #
    if table_type == 'common' or table_type == 'c':
        table_type = 'commonCrate'
        price = quantity*250
        crate_index = 0  # Common Crate
    elif table_type == 'uncommon' or table_type == 'u':
        table_type = 'uncommonCrate'
        price = quantity*2500
        crate_index = 1  # Uncommon Crate
    elif table_type == 'rare' or table_type == 'r':
        table_type = 'rareCrate'
        price = quantity*25000
        crate_index = 2  # Rare crate
    elif table_type == 'multi' or table_type == 'm':
        table_type = 'multiCrate'
        price = quantity*0
        crate_index = 3  # Multi Crate
    else:
        out = "Error: Crate type either wrong or none."
        message_return = finalize(ctx, 'lootcrate', out, "OK", table_type + ' ' + str(quantity))
        await ctx.send(message_return)
        return
    # Error codes, related to quantity and [30 crates per day]
    # Also one related to price.
    if price > user_data.rupees():
        out = "You do not have enough rupees!"
        message_return = finalize(ctx, 'lootcrate', out, "OK", table_type + ' ' + str(quantity))
        await ctx.send(message_return)
        return
    rankcrates = {0 : 10, 1 : 15, 2 : 20, 3 : 30, 4 : 30, 5 : 30, 6 : 40, 7 : 50}
    rank = user_data.rank()
    if rank > 7:
        rank = 7
    if quantity > rankcrates[rank] - crate_purchases:
        out = "No more than {0} crates can be purchased per day!".format(rankcrates[rank])
        message_return = finalize(ctx, 'lootcrate', out, "OK", table_type + ' ' + str(quantity))
        await ctx.send(message_return)
        return
    # Back to code.
    crate_purchases += quantity
    crates[table_type] += quantity
    rupOut -= price
    # --- Rolling Dice and Counting Treasures --- #
    memTable = open(get_global_file('table', table_type + '.txt'), 'r')
    memTable = memTable.readline()
    while isFinished(crates) == False:
        # -- Determining the size of dice to roll -- #
        for key in crates.keys():
            if crates[key] > 0:
                table_type = key
        if table_type == 'commonCrate' or table_type == 'uncommonCrate' or table_type == 'rareCrate':
            crateHandle = random.randrange(65)
        if table_type == 'multiCrate':
            crateHandle = random.randrange(13)
        # -- Reading file -- #
        memItem = memTable[crateHandle*9:crateHandle*9+4]
        memQuant = memTable[crateHandle*9+4:crateHandle*9+9]
        intQuant = int(memQuant)
        # -- Translating file into variables -- #
        if memItem == 'Coll':
            collType[intQuant] += 1
        if memItem == 'Rupi':
            rupOut+=intQuant
        if memItem == 'Cupr':
            silverOut+=intQuant
        if memItem == 'Slvr':
            silverOut+=intQuant*1000
        if memItem == 'Clov':
            cloverOut+=intQuant
        if memItem == 'Land':
            deedOut += intQuant
        if memItem == 'Tres':
            treas+=intQuant
        if memItem == 'Mony':
            moneyMult*=1+intQuant/10
        if memItem == 'Cont':
            countMult*=1+intQuant/10
        if memItem == 'Pick':
            pickMult*=1+intQuant/10
        if memItem == 'Rank':
            rankOut+=1
        if memItem == 'CCrt':
            crates['commonCrate'] += 1
        if memItem == 'UCrt':
            crates['uncommonCrate'] += 1
        if memItem == 'RCrt':
            crates['rareCrate'] += 1
        if memItem == 'MCrt':
            crates['multiCrate'] += 1
        crates[table_type] -= 1
    user_data.inventory()['Treasure'][0] += treas
    if deedOut >= remaining_deeds:
        deedOut = remaining_deeds
        remaining_deeds = 0
    # -- Rounding Variables -- #
    silverOut = round(silverOut, 6)
    rupOut = round(rupOut)
    moneyMult = round(moneyMult, 3)
    countMult = round(countMult, 3)
    pickMult = round(pickMult, 3)
    # --- Building Collection Strings --- #
    collMessage = parseCollections(collType)
    new_collections, reward = user_data.add_collections(collType)
    completion_msg = ""
    for i in range(0, 5):
        if new_collections[i] > 0:
            completion_msg += "\n" + collection_names[i] + " collection completed, " + str(new_collections[i]) + " times."
    if new_collections[5] > 0:
        completion_msg += "\n*All* collections completed " + str(new_collections[5]) + " times!"
    rupOut += reward
    # --- Saving User Resources --- #
    user_data.add_resources(rupOut, silverOut, cloverOut, deedOut)
    user_data.add_rank(rankOut)
    # --- Building Output Strings: Resources --- #
    resourceMessage = ResourceParse.compress(rupOut, silverOut, cloverOut, deedOut, testfor_alt(ctx.message.author.id))
    # --- Building Output Strings: Multipliers and Ranks --- #
    user_data.mult_lootbox_money_boost(moneyMult)
    user_data.mult_lootbox_count_boost(countMult)
    user_data.mult_lootbox_pick_boost(pickMult)
    treasMessage = ''
    if moneyMult > 1:
        moneyMessage = '×{0} Money'.format(number_cronch(moneyMult, testfor_alt(ctx.message.author.id)))
    if countMult > 1:
        countMessage = '×{0} Counting'.format(number_cronch(countMult, testfor_alt(ctx.message.author.id))) 
    if pickMult > 1:
        pickMessage = '×{0} Pickaxe'.format(number_cronch(pickMult, testfor_alt(ctx.message.author.id)))
    if rankOut > 0:
        rankMessage = '×{0} Rankup'.format(rankOut)
    if treas > 0:
        treasMessage = '×{0} Treasure'.format(treas)
    # --- Finalizing Everything --- #
    name = username(ctx.message.author, testfor_alt(ctx.message.author.id))[0]
    outMessage = '__**' + name + '\'s Crate Results**__\n>>> **Resources:** ' + resourceMessage + "\n\n**Multipliers:** " + moneyMessage + '   ' + countMessage + '   ' + pickMessage + '\n\n**Special:** ' + treasMessage + '   ' + rankMessage + "\n\n**Collections:** " + collMessage + '\n\n**Completed Collections:** ' + completion_msg + '\n\n' + check_land(ctx)
    user_data.data['crate_purchases'] = crate_purchases
    save_user_data(user_data)
    message_return = finalize(ctx, 'lootcrate', outMessage, "OK", table_type + ' ' + str(quantity))
    await ctx.send(message_return)

@bot.command()
async def tax(ctx):
    """Tax your land's tenants!"""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy'] or not g_data.data['crafting']:
        return
    user = get_user_data(testfor_alt(ctx.message.author.id))
    cooldown = user.data.setdefault('has_taxed',False)
    if user.get_inv_volume() > user.inv_size() and user.logging_hut()["count"] > 0:
        errout = "Your inventory is too full to do this!"
        message_return = finalize(ctx, 'tax', errout, "OK")
        await ctx.send(message_return)
        return
    if cooldown == True:
        out = 'You have already taxed your citizens! Come back tomorrow!'
        message_return = finalize(ctx, 'tax', out, "OK")
        await ctx.send(message_return)
        return
    else:
        user.data['has_taxed'] = True
    meow_var = user.haz_pet_meow()
    name = username(ctx.message.author, testfor_alt(ctx.message.author.id))[0]
    famine = user.event()['Famine']
    discovered = user.event()['Discovered Lands']
    hut1, hut2, hut3, hut4, town1, town2 = user.data['civ']['Simple Hut']["count"], user.data['civ']['Hut']["count"], user.data['civ']['Small Cottage']["count"], user.data['civ']['Cottage']["count"], user.data['civ']['Small Village']["count"], user.data['civ']['Large Village']["count"]
    farm1, farm2 = user.data['civ']['Small Farm']["count"], user.data['civ']['Medium Farm']["count"]
    clovf, hivef = user.data['civ']['Clover Field']["count"], user.data['civ']['Beehive']["count"]
    tree1, tree2, tree3, tree4, tree5, tree6 = user.trees()['Oak Tree'], user.trees()['Maple Tree'], user.trees()['Spruce Tree'], user.trees()['Apple Tree'], user.trees()['Rupee Tree'], user.trees()['Coin Tree'],
    grov1, grov2, grov3, grov4, grov5, grov6 = user.trees()['Oak Grove'], user.trees()['Maple Grove'], user.trees()['Spruce Grove'], user.trees()['Apple Grove'], user.trees()['Rupee Grove'], user.trees()['Coin Grove'],
    forest1, forest2, forest3, forest4, forest5, forest6 = user.trees()['Oak Forest'], user.trees()['Maple Forest'], user.trees()['Spruce Forest'], user.trees()['Apple Forest'], user.trees()['Rupee Forest'], user.trees()['Coin Forest']
    income = (hut1 * 10 + hut2 * 21 + hut3 * 60 + hut4 * 150 + town1 * 560 + town2 * 5900) * max(1, 2*meow_var)
    income = int(income//(famine+1))
    grain = farm1 * 2 + farm2 * 10 + town1 * 1 + town2 * 5//(famine+1)
    land = (town1 * 2 + town2 * 20) * (discovered+1)
    devarea = hut1 + hut2*2 + hut3*3 + hut4*5 + town1*53 + town2*419 + farm1*12 + farm2*51 + clovf + hivef + \
              tree1 + tree2 + tree3 + tree4 + tree5*3 + tree6*3 + grov1*10 + grov2*10 + grov3*10 + grov4*10 + grov5*30 + grov6*30 + \
              (forest1 + forest2 + forest3 + forest4)*100 + forest5*300 + forest6*300 + user.data['civ']['Logging Hut']["count"]*2
    user.set_developed_land(devarea)
    if income == 0:
        out = 'You have no one to tax...'
        message_return = finalize(ctx, 'tax', out, "OK")
        await ctx.send(message_return)
        return
    population = 2*hut1 + 3*hut2 + 5*hut3 + 10*hut4 + 28*town1 + 265*town2 + 6*farm1 + 29*farm2 + 3*user.data['civ']['Logging Hut']["count"]
    out = ''
    if population >= 10 and user.achievements()['Campers'] == 0:
        out += '**Achievement get:** Campers - House ten people\n> +{0}\n'.format(ResourceParse.compress_rup_clov(100 * user.get_money_multiplier(), 'rupee', user.data['id']))
        user.achievements()['Campers'] += 1
        user.add_rupees(100 * user.get_money_multiplier())
    if population >= 25 and user.achievements()['Village Idiots'] == 0:
        out += '**Achievement get:** Village Idiots - House twenty-five people\n> +{0}\n'.format(ResourceParse.compress_rup_clov(500 * user.get_money_multiplier(), 'rupee', user.data['id']))
        user.achievements()['Village Idiots'] += 1
        user.add_rupees(500 * user.get_money_multiplier())
    if population >= 50 and user.achievements()['Clan Encampment'] == 0:
        out += '**Achievement get:** Clan Encampment - House fifty people\n> +{0}\n'.format(ResourceParse.compress_rup_clov(1000 * user.get_money_multiplier(), 'rupee', user.data['id']))
        user.achievements()['Clan Encampment'] += 1
        user.add_rupees(1000 * user.get_money_multiplier())
    if population >= 100 and user.achievements()['Fort Rubble'] == 0:
        out += '**Achievement get:** Fort Rubble - House one hundred people\n> +{0}\n'.format(ResourceParse.compress_rup_clov(2000 * user.get_money_multiplier(), 'rupee', user.data['id']))
        user.achievements()['Fort Rubble'] += 1
        user.add_rupees(2000 * user.get_money_multiplier())
    if population >= 250 and user.achievements()['Feudal Life'] == 0:
        out += '**Achievement get:** Feudal Life - House two hundred fifty people\n> +{0}\n'.format(ResourceParse.compress_rup_clov(5000 * user.get_money_multiplier(), 'rupee', user.data['id']))
        user.achievements()['Feudal Life'] += 1
        user.add_rupees(5000 * user.get_money_multiplier())
    if population >= 500 and user.achievements()['On The Map'] == 0:
        out += '**Achievement get:** On The Map - House five hundred people\n> +{0}\n'.format(ResourceParse.compress_rup_clov(10000 * user.get_money_multiplier(), 'rupee', user.data['id']))
        user.achievements()['On The Map'] += 1
        user.add_rupees(10000 * user.get_money_multiplier())
    if population >= 1000 and user.achievements()['Township'] == 0:
        out += '**Achievement get:** Township - House one thousand people\n> +{0}\n'.format(ResourceParse.compress_rup_clov(20000 * user.get_money_multiplier(), 'rupee', user.data['id']))
        user.achievements()['Township'] += 1
        user.add_rupees(20000 * user.get_money_multiplier())
    user.inventory()['Grain'][0] += grain
    user.add_rupees(income)
    remaining_deeds = remaining_land(ctx)
    out += name + ' gained {} from their land\'s residents!'.format(ResourceParse.compress_rup_clov(income, 'rupee', testfor_alt(ctx.message.author.id)))
    if farm1 > 0 or farm2 > 0 or town1 > 0 or town2 > 0:
        out += '\n' + name + ' gained {} grain from their land\'s farms!'.format(number_cronch(grain, testfor_alt(ctx.message.author.id)))
    if land > 0:
        if land < remaining_deeds:
            user.add_land(land)
            out += '\n' + name + '\'s cities conquered {} acres of land from the wilderness!'.format(land)
        elif land >= remaining_deeds > 0:
            user.add_land(remaining_deeds)
            remaining_deeds = 0
            out += '\n' + name + '\'s cities conquered the last {} acre(s) of land from the wilderness!'.format(land)
    if user.data['civ']['Logging Hut']["count"] > 0:
        out += '\n' + name + ' gained the following from their land\'s orchards and forests:\n>>> ' + user.autochop()
    save_user_data(user)
    message_return = finalize(ctx, 'tax', out, "OK")
    await ctx.send(message_return)

@bot.command(aliases=['give', 'gift'])
async def trade(ctx, *args):
    """Trade or gift people your resources!
    /trade <recipient> <resource> <quantity>"""
    g_data = get_guild_data(ctx)
    global botdata
    if not g_data.data['economy'] and not g_data.data['crafting']:
        return
    if len(args) < 3:
        out = prefix + 'trade <recipient> <resource> <quantity>'
        message_return = finalize(ctx, 'trade', out, "OK")
        await ctx.send(message_return)
        return
    else:
        recipient = args[0]
        quantity = float(args[2])
        resource = ''
        cursor = 1
        while cursor < 2:
            resource += args[cursor]
            if cursor < 1:
                resource += ' '
            cursor += 1
    donor_identity = testfor_alt(ctx.message.author.id)
    donor_data = get_user_data(donor_identity)
    donor_name = username(ctx.message.author, donor_identity)[0]

    converter = commands.MemberConverter()
    reciever = await converter.convert(ctx, recipient)
    reciever_identity = testfor_alt(reciever.id)
    reciever_data = get_user_data(reciever_identity)
    reciever_name = username(ctx.message.author, reciever_identity)[0]
    resource = str.lower(resource)
    resource_name = ''
    isInv = False
    if donor_data.data['id'] == reciever_data.data['id'] and reciever_data.data['id'] != "248641004993773569":
        out = 'You cannot give items to yourself!'
        message_return = finalize(ctx, 'trade', out, "OK")
        await ctx.send(message_return)
        return
    resource_currency = {'r' : 'Rupees', 'rup' : 'Rupees', 'rupee' : 'Rupees', 'rupees' : 'Rupees',
                         'kyp' : 'Kups', 'kup' : 'Kups', 'cp' : 'Kups', 'copper' : 'Kups', 'c' : 'Kups', 'kups' : 'Kups',
                         'arg' : 'Args', 'sp' : 'Args', 'coin' : 'Args', 'coins' : 'Args', 'silver' : 'Args', 'args' : 'Args',
                         'ay' : 'Auru', 'au' : 'Auru', 'aur' : 'Auru', 'auri' : 'Auru', 'gold' : 'Auru', 'gp' : 'Auru', 'g' : 'Auru', 'auru' : 'Auru',
                         'pt' : 'Pluot', 'plat' : 'Pluot', 'plet' : 'Pluot', 'platinum' : 'Pluot', 'pp' : 'Pluot', 'pletus' : 'Pluot',
                         'ir' : 'Pluot', 'ire' : 'Pluot', 'iridum' : 'Pluot', 'ip' : 'Pluot', 'irid' : 'Pluot',
                         'plutonium' : 'Pluot', 'pluot' : 'Pluot', 'pu' : 'Pluot',
                         'ka' : 'Käli', 'cf' : 'Käli', 'ca' : 'Käli', 'cp' : 'Käli', 'cfp' : 'Käli', 'cali' : 'Käli', 'kali' : 'Käli',
                         'caali' : 'Käli', 'kaali' : 'Käli', 'cäli' : 'Käli', 'käli' : 'Käli', 'californium' : 'Käli',
                         'clov' : 'Clovers', 'clover' : 'Clovers', 'clovers' : 'Clovers',
                         'field' : 'Land', 'land' : 'Land', 'fields' : 'Land', 'acre' : 'Land',
                         'acres' : 'Land', 'deed' : 'Land', 'deeds' : 'Land',
                         'tix' : 'Tickets', 'tickets' : 'Tickets', 'ticket' : 'Tickets',
                         'oc' : 'OmniCoreCredits', 'occ' : 'OmniCoreCredits', 'omnicreds' : 'OmniCoreCredits',
                         'omnicredits' : 'OmniCoreCredits', 'zacreds' : 'OmniCoreCredits', 'zacredits' : 'OmniCoreCredits',
                         'omnicore creds' : 'OmniCoreCredits', 'omnicore credits' : 'OmniCoreCredits',
                         'zako creds' : 'OmniCoreCredits', 'zako credits' : 'OmniCoreCredits', 'zac' : 'OmniCoreCredits'}
    resource_inventory = {}
    for item in UserData.items:
        i = item
        j = str.lower(item)
        resource_inventory[j] = i
    
    for currency in resource_currency:
        if resource == currency:
            resource_name = resource_currency[currency]
            quantity = int(round(quantity))
    for item in resource_inventory:
        if resource == item:
            resource_name = resource_inventory[item]
            isInv = True
            quantity = int(round(quantity))
    if resource_name == '':
        out = '{0} either cannot be traded or doesn\'t exist!'.format(resource)
        message_return = finalize(ctx, 'trade', out, "OK", reciever_name + ' ' + resource + ' ' + str(quantity))
        await ctx.send(message_return)
        return
    if quantity <= 0:
        out = '{0} must be more than 0!'.format(resource_name)
        message_return = finalize(ctx, 'trade', out, "OK", reciever_name + ' ' + resource + ' ' + str(quantity))
        await ctx.send(message_return)
        return
    if isInv == False:
        if resource_name == 'Args':
            quantity = int(round(quantity*1000))
            resource_name = 'Kups'
        if resource_name == 'Auru':
            quantity = int(round(quantity*1000000))
            resource_name = 'Kups'
        if resource_name == 'Pluot':
            quantity = int(round(quantity*1000000000))
            resource_name = 'Kups'
        if resource_name == 'Käli':
            quantity = int(round(quantity*1000000000000))
            resource_name = 'Kups'
        if quantity > donor_data.wallet()[resource_name]:
            out = 'You cannot afford this!'
            message_return = finalize(ctx, 'trade', out, "OK", reciever_name + ' ' + resource + ' ' + str(quantity))
            await ctx.send(message_return)
            return
        else:
            quantity = int(round(quantity))
            donor_data.wallet()[resource_name] -= quantity
            reciever_data.wallet()[resource_name] += quantity
            save_user_data(donor_data)
            save_user_data(reciever_data)
            if resource_name == 'Rupees':
                reciept = ResourceParse.compress_rup_clov(quantity, 'rupee', testfor_alt(ctx.message.author.id))
            elif resource_name == 'Kups':
                reciept = ResourceParse.compress_coin(quantity, testfor_alt(ctx.message.author.id))
            elif resource_name == 'Clovers':
                reciept = ResourceParse.compress_rup_clov(quantity, 'oc2_clover', testfor_alt(ctx.message.author.id))
            elif resource_name == 'Land':
                reciept = ResourceParse.compress_land(quantity)
            elif resource_name == 'OmniCoreCredits':
                reciept = ResourceParse.compress_rup_clov(quantity, 'oc2_occ', testfor_alt(ctx.message.author.id))
    if isInv == True:
        quantity = int(round(quantity))
        if quantity > donor_data.inventory()[resource_name][0]:
            out = 'You don\'t have enough of this item to make this trade!'
            message_return = finalize(ctx, 'trade', out, "OK", reciever_name + ' ' + resource + ' ' + str(quantity))
            await ctx.send(message_return)
        if reciever_data.get_inv_volume() > reciever_data.inv_size() and reciever_data.data['id'] != botdata.data['id']:
            errout = "The recipient's inventory is too full to accept these items!"
            message_return = finalize(ctx, 'item', errout, "OK")
            await ctx.send(message_return)
            return
        else:
            if reciever_data.data['id'] != botdata.data['id']:
                donor_data.inventory()[resource_name][0] -= quantity
                reciever_data.inventory()[resource_name][0] += quantity
                save_user_data(donor_data)
                save_user_data(reciever_data)
            else:
                donor_data.inventory()[resource_name][0] -= quantity
                botdata.inventory()[resource_name][0] += quantity
                save_user_data(donor_data)
                save_user_data(botdata)
            reciept = '{}×'.format(quantity) + resource_name
            
    out = donor_name + ' put the following resources into ' + reciever_name + '\'s account:\n' + reciept
    message_return = finalize(ctx, 'trade', out, "OK", reciever_name + ' ' + resource + ' ' + str(quantity))
    await ctx.send(message_return)

@bot.command(aliases=['garbage'])
async def trash(ctx, *, args):
    g_data = get_guild_data(ctx)
    if not g_data.data['crafting']:
        return
    user = get_user_data(testfor_alt(ctx.message.author.id))
    passin = ''
    args = str.lower(args)
    args = args.split()
    try:
        quantity = int(args[len(args)-1])
        args = args[:-1]
    except Exception:
        quantity = 1
    arg2 = ''
    for arg in args:
        if arg != args[len(args)-1]:
            arg2 += str.upper(arg[0]) + arg[1:] + ' '
        else:
            arg2 += str.upper(arg[0]) + arg[1:]
    args = arg2
    if quantity < 1:
        out = 'You cannot trash any less than one item!'
        message_return = finalize(ctx, 'trash', out, "OK", setting + ' ' + args)
        await ctx.send(message_return)
        return
    if user.inventory()[args][0] >= quantity:
        botdata.data['landfill'][args] += quantity
        user = add_items(user, {args: [-quantity]})
        out = 'You threw away {0} {1}(s).'.format(number_cronch(quantity, testfor_alt(ctx.message.author.id)), args)
    else:
        out = 'You don\'t have that many items!'
    save_user_data(user)
    save_user_data(botdata)
    message_return = finalize(ctx, 'trash', out, "OK")
    await ctx.send(message_return)

@bot.command(aliases=['dive'])
async def dumpdive(ctx):
    """Dig around in the dump. Perhaps you will find something valuable."""
    try:
        g_data = get_guild_data(ctx)
        if not g_data.data['crafting']:
            return
        user = get_user_data(testfor_alt(ctx.message.author.id))
        if user.data['can dumpster dive'] == True:
            d = {}
            l = []
            count = 0
            for item in botdata.data['landfill']:
                if botdata.data['landfill'][item] > 0:
                    d[item] = botdata.data['landfill'][item]
                    count += botdata.data['landfill'][item]
                    l.append([item, botdata.data['landfill'][item]])
            if len(d) > 0:
                finds = {}
                for i in range(10):
                    chance = random.randint(1, count)
                    for item in l:
                        if not user.inventory()[item[0]][2]:
                            count -= 1
                            continue
                        if chance > item[1]:
                            chance -= item[1]
                        else:
                            finds.setdefault(item[0], [0])
                            finds[item[0]][0] += 1
                            botdata.data['landfill'][item[0]] -= 1
                            item[1] -= 1
                            count -= 1
                            break
                user = add_items(user, finds)
                find = parseInventory(ctx, finds, False)
                #user.data['inventory'] = {**user.data['inventory'], **finds}
                user.data['can dumpster dive'] = False
                out = f"After searching the dump for a few hours, you've found:\n{find[0]}{find[1]}\nBut now you're all filthy."
                save_user_data(user)
                save_user_data(botdata)
            else:
                out = "The landfill is empty."
        else:
            out = "You've already searched the dump today. Come back tomorrow!"
        message_return = finalize(ctx, 'dumpdive', out, "OK")
        await ctx.send(message_return)
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'dumpdive', out, out)
        await ctx.send(message_return)

@bot.command()
async def shop(ctx, *args):
    """Shows the things that you can buy. Parameters: <Page #>"""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy']:
        return
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    if len(args) == 0:
        args = ["1"]
    if args[0] not in "10112013141516171819":
        itemname = args[0]
        for arg in args:
            if arg != args[0]:
                itemname += ' ' + arg
        await Purchases.show_cost(ctx, user_data, str.lower(itemname), False)
        message_return = finalize(ctx, 'shop', None, "OK", itemname)
    else:
        await Purchases.shop(ctx, user_data, args, False)
        save_user_data(user_data)
        if len(args) > 0:
            message_return = finalize(ctx, 'shop', None, "OK", args[0])
        else:
            message_return = finalize(ctx, 'shop', None, "OK")

@bot.command()
async def buy(ctx, *, args):
    """Buys an object from the shop. Parameters: <Item ID>"""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy']:
        return
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    quantity = 1
    passin = ''
    if len(args) > 0:
        for arg in args:
            args = str.lower(args)
        if args[-1] in '0123456789' and args[-2] in ' ':
            quantity = int(args[-1])
            if quantity < 1:
                out = 'You cannot buy any less than one item!'
                message_return = finalize(ctx, 'buy', out, "OK", args)
                await ctx.send(message_return)
                return
            cursor = 0
            while cursor < len(args)-1:
                passin = args[:-2]
                cursor += 1
        else:
            passin = args
    while quantity > 0:
        await Purchases.buy(ctx, user_data, passin, False)
        quantity -= 1
    save_user_data(user_data)
    if len(args) > 0:
        message_return = finalize(ctx, 'buy', None, "OK", args[0])
    else:
        message_return = finalize(ctx, 'buy', None, "OK")

@bot.command(aliases=['xchg', 'exchg', 'exch'])
async def exchange(ctx, currency):
    """Exchange rupees and coins! Can only be used once daily.
    /exchange <coin/rupee>
    Alternative arguments:
    coin, coins, arg, args, silver, Ag, SP, c
    rupee, rupees, rup, r
    omnicredit, omnicredits, omnicorecredit, omnicorecredits, oc, occ"""
    g_data = get_guild_data(ctx)
    if not g_data.data['economy']:
        return
    identity = testfor_alt(ctx.message.author.id)
    user = get_user_data(identity)
    name = username(ctx.message.author, identity)[0]
    level = user.lv()
    rank = user.rank() + 1
    cooldown = user.data.setdefault('exchange_cooldown',False)
    if cooldown == True:
        out = 'You have already used the exchange today! Come back tomorrow!'
        message_return = finalize(ctx, 'exchange', out, "OK", currency)
        await ctx.send(message_return)
        return
    else:
        user.data['exchange_cooldown'] = True
    rupees = level * 10
    coins = level * rank * 1000
    occ = rank
    rate = coins/rupees
    rout = ResourceParse.compress_rup_clov(rupees, 'rupee', identity)
    cout = ResourceParse.compress_coin(coins, identity)
    cointype = 'copper'
    if rate >= 1000:
        cointype = 'silver'
    if currency in ['coin', 'coins', 'arg', 'args', 'silver', 'Ag', 'SP', 'c', 'ag', 'sp']:
        if user.rupees()-rupees < 0:
            out = 'You cannot afford to complete this transaction!'
            message_return = finalize(ctx, 'exchange', out, "OK", currency)
            await ctx.send(message_return)
            return
        out = name + ' exchanged ' + rout + ' for ' + cout + ' at a rate of {0} {1} pieces per rupee.'.format(rate, cointype)
        rupees = 0-rupees
    elif currency in ['rupee', 'rupees', 'gems', 'rup', 'r']:
        if rank >= 3:
            if user.silver()-coins < 0:
                out = 'You cannot afford to complete this transaction!'
                message_return = finalize(ctx, 'exchange', out, "OK", currency)
                await ctx.send(message_return)
                return
            out = name + ' exchanged ' + cout + ' for ' + rout + ' at a rate of {0} {1} pieces per rupee.'.format(rate, cointype)
        else:
            out = 'This feature is reserved for VIP+ and above!'
            message_return = finalize(ctx, 'exchange', out, "OK", currency)
            await ctx.send(message_return)
            return
    elif currency in ['omnicredit', 'omnicredits', 'omnicorecredits', 'omnicorecredit', 'oc', 'occ', 'omni']:
        rate = int(get_all_user_sum('wallet', 'Rupees')/5000)*rank
        if user.rupees()-rate < 0:
            out = 'You cannot afford to complete this transaction!'
            message_return = finalize(ctx, 'exchange', out, "OK", currency)
            await ctx.send(message_return)
            return
        ocout = ResourceParse.compress_rup_clov(rank, 'oc2_occ', identity)
        rupees = -rate
        user.add_omnicredits(occ)
        rout = ResourceParse.compress_rup_clov(abs(rupees), 'rupee', identity)
        out = name + ' exchanged ' + rout + ' for ' + ocout + ' at a rate of 1 omnicredit per {} rupees.'.format(int(rate/rank))
    else:
        out = 'Invalid currency type!'
        message_return = finalize(ctx, 'exchange', out, "OK", currency)
        await ctx.send(message_return)
        return
    user.add_resources(rupees, coins, 0, 0)
    save_user_data(user)
    message_return = finalize(ctx, 'exchange', out, "OK", currency)
    await ctx.send(message_return)

#class Crafting(commands.cog):

    #def __init__(self, bot):
    #    self.bot = bot
    #    self._last_member = None


@bot.command()  # Bot determines how many rupees a user gets by rolling "pickaxe" d20s, then opening a chest for each nat20 rolled. Spaghet warning!
async def mine(ctx, *args):
    """Mine ore. You can only do so once per day. Clovers get you a bit more ore, if used.
    /mine (clovers)"""
    try:
        g_data = get_guild_data(ctx)
        if not g_data.data['crafting']:
            return
        if len(args) == 0:
            clover = 0
            moararg = False
        else:
            clover = int(args[0])
            moararg = True
        # --- User Data --- #
        user_data = get_user_data(testfor_alt(ctx.message.author.id))
        multi = user_data.get_money_multiplier()
        user_clovers = user_data.clovers()
        user_data.inventory()
        user_data.event()
        name = username(ctx.message.author, testfor_alt(ctx.message.author.id))[0]
        meow_var = 0
        lucky_day = 0
        if user_data.haz_pet_meow():
            meow_var = 1
        if user_data.event()['Lucky Day']:
            lucky_day = 1
        meteor = user_data.event()['Meteor Impact']
        picktier = user_data.data['pick']
        pickaxe = user_data.get_pickaxe_power() - (picktier+2)*meteor + (7 * (meow_var + lucky_day + clover))
        # --- Error Codes --- #
        if user_data.get_inv_volume() + pickaxe > user_data.inv_size():
            errout = "Your inventory is too full to do this!"
            message_return = finalize(ctx, 'mine', errout, "OK")
            await ctx.send(message_return)
            return
        if not user_data.data.setdefault('can_mine',True):
            errout = 'You have already mined today!'
            if moararg == True:
                message_return = finalize(ctx, 'mine', errout, "OK", args[0])
            if moararg == False:
                message_return = finalize(ctx, 'mine', errout, "OK")
            await ctx.send(message_return)
            return
        if user_clovers < clover:
            errout = 'Not enough clovers!'
            message_return = finalize(ctx, 'mine', errout, "OK", args[0])
            await ctx.send(message_return)
            return
        if mining_clover_event == False and clover > 1:
            errout = 'You cannot use more than one clover!'
            message_return = finalize(ctx, 'mine', errout, "OK", args[0])
            await ctx.send(message_return)
            return
        if mining_clover_event == True and clover > 3:
            errout = 'You cannot use more than three clovers!'
            message_return = finalize(ctx, 'mine', errout, "OK", args[0])
            await ctx.send(message_return)
            return
        if user_data.data['pick'] == -1:
            errout = name + user_data.break_pickaxe()
            if moararg == True:
                message_return = finalize(ctx, 'mine', errout, "OK", args[0])
            if moararg == False:
                message_return = finalize(ctx, 'mine', errout, "OK")
            await ctx.send(message_return)
            return
        # --- Variable Initialization --- #
        out, treas = 0, 0
        ore_list = ['Stone', 'Coal', 'Tetrahedrite', 'Cassiterite', 'Hematite', 'Native Silver',
                   'Native Gold', 'Diamond', 'Ringwoodite', 'Obsidian', 'Carmeltazite',
                   'Native Platinum', 'Rutile', 'Oil', 'Aetheric', 'Franciscite',
                   'Magnesite', 'Quartz', 'Sphalerite', 'Pegmatite', 'Wolframite', 'Cobaltite',
                   'Vanadinite', 'Chlorophyte', 'Luminite', 'Mobius Fuel', 'Plutonite', 'Treasure']
        invGain = {}
        oredrops = {
            40: 'Stone', 45: 'Sphalerite', 60: 'Coal', 85: 'Tetrahedrite', 90: 'Treasure',
            110: 'Cassiterite', 130: 'Hematite', 135: 'Native Silver', 140: 'Native Gold',
            145: 'Rupee Ore', 160: 'Diamond', 170: 'Obsidian', 175: 'Plutonite',
            185: 'Buried Hoard', 195: 'Ringwoodite', 210: 'Carmeltazite', 215: 'Oil',
            225: '2 Treasure', 240: 'Rutile', 245: 'Red Rupee Ore', 250: 'Franciscite',
            260: 'Large Hoard', 270: 'Dense Stone', 275: 'Rutile', 290: 'Magnesite',
            295: '5 Treasure', 310: 'Quartz', 315: 'Orange Rupee Ore', 330: 'Sphalerite',
            340: 'Aetheric', 355: 'Pegmatite', 365: 'Wolframite', 375: 'Massive Hoard', 390: 'Cobaltite',
            410: 'Vanadinite', 435: 'Chlorophyte', 455: 'Aetheric', 465: 'Mobius Fuel', 470: 'Native Platinum',
            485: 'Luminite', 500: 'Massive Hoard'}
        for ore in ore_list:
            invGain[ore] = [0]
        rupeeMessage, coinMessage, cloverMessage = '', '', ''
        remaining_deeds = remaining_land(ctx)
        overflow_multi = 1
        item = ''
        # --- Efficiency --- #
        if pickaxe > 10000:
            overflow_multi = float(pickaxe)/float(10000)  # overflow multiplier is 1/10k-th the pickaxe's power
            # float() division to ensure precision
            pickaxe = 10000  # 1/10k-th power x 10k uses = 1x power
            overflow_multi = round(overflow_multi)
        # --- Rolling Dice and Counting Treasures --- #
        while pickaxe > 0:
            oreHandle = random.randrange((picktier+2+meteor)*25)
            orequant = 1
            for key in oredrops:
                if oreHandle <= key:
                    item = oredrops[key]
                    break
            if item == 'Hematite':
                orequant = 2
            if item == 'Treasure':
                treas += 1
                item = ''
            if item == '2 Treasure':
                treas += 2
                item = ''
            if item == '5 Treasure':
                treas += 5
                item = 'Stone'
                orequant = 5
            if item == 'Rupee Ore':
                out += 1
                item = ''
            if item == 'Red Rupee Ore':
                out += 20
                item = ''
            if item == 'Orange Rupee Ore':
                out += 100
                item = ''
            if item == 'Buried Hoard':
                out += 5
                treas += 1
                item = ''
            if item == 'Large Hoard':
                out += 50
                treas += 5
                item = ''
            if item == 'Massive Hoard':
                out += 200
                treas += 10
                item = ''
            if item == 'Dense Stone':
                item = 'Stone'
                orequant = 5
            if item != '':
                invGain[item][0] += orequant*overflow_multi
            invGain['Stone'][0] += overflow_multi
            pickaxe -= 1
        # --- Parsing Output --- #
        out *= 1/(10/(clover+meow_var+lucky_day+1)) * multi
        out = int(out)
        clov = 0 - clover
        coin = 0
        invGain['Treasure'][0] += treas
        # --- Rounding, Saving, and Preparing Output --- #
        coin = round(coin)
        out = round(out)
        clov = round(clov)  # deed and clov need to be rounded because of overflow_multi
        user_data = add_items(user_data, invGain)
        inv, inv2 = parseInventory(ctx, invGain, False)
        invMessage = 'Ore Found:\n' + inv + inv2
        user_data.data['can_mine'] = False
        user_data.add_resources(out, coin, clov, 0)
        resourceMessage = ResourceParse.compress(out, coin, clov, 0, testfor_alt(ctx.message.author.id))
        treasMessage = ''
        if treas > 0:
            treasMessage = '{0} Treasure'.format(treas)
        # --- Finalization --- #
        breakmsg = user_data.break_pickaxe()
        outMessage = resourceMessage + '\n' + invMessage
        save_user_data(user_data)
        embed = discord.Embed(title="__**" + name + "'s Mining Results**__", color=0x8000FF)
        embed.add_field(name=name + breakmsg, value=outMessage, inline=False)
        if moararg == True:
            message_return = finalize(ctx, 'mine', None, "OK", args[0])
        elif moararg == False:
            message_return = finalize(ctx, 'mine', None, "OK")
        await ctx.send(embed=embed)
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'mine', out, out, str(args))

@bot.command(aliases=['open', 'box'])
async def boxes(ctx, crate: str, quantity: int):
    """Open treasure chests and crates!"""
    g_data = get_guild_data(ctx)
    if not g_data.data['crafting'] and not g_data.data['economy']:
        return
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    remaining_deeds = remaining_land(ctx)
    crate = str.lower(crate)
    multi = user_data.get_money_multiplier()
    name = username(ctx.message.author, testfor_alt(ctx.message.author.id))[0]
    if crate == 'treasure':
        if user_data.inventory()['Treasure'][0] < quantity:
            out = 'You don\'t have enough of this crate type!'
            message_return = finalize(ctx, 'open', out, "OK", crate + ' {}'.format(quantity))
            await ctx.send(message_return)
            return
        user_data.inventory()['Treasure'][0] -= quantity
        overflow_multi = 1
        if quantity > 10000:
            overflow_multi = float(quantity)/float(10000)  # overflow multiplier is 1/10k-th the pickaxe's power
            # float() division to ensure precision
            quantity = 10000  # 1/10k-th power x 10k uses = 1x power
            overflow_multi = round(overflow_multi)
        loots = treasure(remaining_deeds, quantity)
        rupees = int(loots[0] * multi * overflow_multi)
        coin = int(loots[1] * multi * overflow_multi)
        clov = int(loots[2] * overflow_multi)
        deed = int(loots[3] * overflow_multi)
        if deed >= remaining_deeds:
            deed = remaining_deeds
            remaining_deeds = 0
        user_data.add_resources(rupees, coin, clov, deed)
        save_user_data(user_data)
        resourceMessage = ResourceParse.compress(rupees, coin, clov, deed, testfor_alt(ctx.message.author.id))
        out = '**' + name + '** opened {0} treasure chest(s) and found '.format(quantity) + resourceMessage + '!\n\n' + check_land(ctx)
        embed = discord.Embed(title="__**" + name + "\'s Treasure Opening Results**__", color=0x8000FF)
        embed.add_field(name='Treasure chests are found in crates or from mining.', value=out, inline=False)
        message_return = finalize(ctx, 'boxes', None, "OK", crate + ' {}'.format(quantity))
        await ctx.send(embed=embed)
        

@bot.command()  # Bot determines how many rupees a user gets by rolling "pickaxe" d20s, then opening a chest for each nat20 rolled. Spaghet warning!
async def chop(ctx, *args):
    """Chop down trees. You can only do so once per day."""
    g_data = get_guild_data(ctx)
    if not g_data.data['crafting']:
        return
    # --- User Data --- #
    user_data = get_user_data(testfor_alt(ctx.message.author.id))
    multi = user_data.get_money_multiplier()
    user_data.inventory()
    inventory = user_data.data['inventory']
    if len(args) == 0:
        clover = 0
    else:
        clover = int(args[0])
    user_clovers = user_data.clovers()
    meow_var = 0
    lucky_day = 0
    if user_data.haz_pet_meow():
        meow_var = 1
    if user_data.event()['Lucky Day']:
        lucky_day = 1
    axetier = user_data.data['axe']
    axe = user_data.get_axe_power() + (7 * (meow_var + lucky_day + clover))
    # --- Error Codes --- #
    if user_data.get_inv_volume() + axe + axe//15 > user_data.inv_size():
        errout = "Your inventory is too full to do this!"
        message_return = finalize(ctx, 'chop', errout, "OK")
        await ctx.send(message_return)
        return
    if not user_data.data.setdefault('can_chop',True):
        errout = 'You have already chopped today!'
        message_return = finalize(ctx, 'chop', errout, "OK")
        await ctx.send(message_return)
        return
    if user_clovers < clover:
        errout = 'Not enough clovers!'
        message_return = finalize(ctx, 'chop', errout, "OK", args[0])
        await ctx.send(message_return)
        return
    if mining_clover_event == False and clover > 1:
        errout = 'You cannot use more than one clover!'
        message_return = finalize(ctx, 'chop', errout, "OK", args[0])
        await ctx.send(message_return)
        return
    if mining_clover_event == True and clover > 3:
        errout = 'You cannot use more than three clovers!'
        message_return = finalize(ctx, 'chop', errout, "OK", args[0])
        await ctx.send(message_return)
        return
    # --- Variable Initialization --- #
    user_data.add_clovers(-clover)
    invGain = {'Wood Log' : [0], 'Fruit' : [0], 'Nuts' : [0], 'Syrup' : [0]}
    overflow_multi = 1
    item = ''
    # --- Efficiency --- #
    if axe > 10000:
        overflow_multi = float(axe)/float(10000)  # overflow multiplier is 1/10k-th the pickaxe's power
        # float() division to ensure precision
        axe = 10000  # 1/10k-th power x 10k uses = 1x power
        overflow_multi = round(overflow_multi)
    # --- Rolling Dice --- #
    while axe > 0:
        hasfruit = random.randrange(15)
        hasnut = random.randrange(15)
        hassyrup = random.randrange(15)
        tree_height = random.randrange(5)
        invGain['Wood Log'][0] += tree_height * overflow_multi
        if hasfruit == 1:
            invGain['Fruit'][0] += 1
        if hasnut == 1:
            invGain['Nuts'][0] += 1
        if hassyrup == 1:
            invGain['Syrup'][0] += 1
        axe -= 1
    # --- Rounding, Saving, and Preparing Output --- #
    user_data = add_items(user_data, invGain)
    inv, inv2 = parseInventory(ctx, invGain, False)
    invMessage = 'Wood Obtained:\n' + inv + inv2
    user_data.data['can_chop'] = False
    # --- Finalization --- #
    name = username(ctx.message.author, testfor_alt(ctx.message.author.id))[0]
    breakmsg = user_data.break_axe()
    outMessage = name + breakmsg + '\n\n__**' + name + '\'s Chopping Results**__\n>>> ' + invMessage
    save_user_data(user_data)
    message_return = finalize(ctx, 'chop', outMessage, "OK")
    await ctx.send(message_return)

@bot.command(aliases=['recipe', 'bp', 'blp', 'blueprint', 'blueprints'])
async def recipes(ctx, *args):
    """Shows the things that you can craft. Parameters: <Page #>
    /blueprints <list type>
    List types: ingots, blocks, other, civ, util, picks, axes, sawmills, trees, granary, hardware
    /blueprints all will show you all the craftable items, but careful! It's spammy."""
    try:
        g_data = get_guild_data(ctx)
        if not g_data.data['crafting']:
            return
        user_data = get_user_data(testfor_alt(ctx.message.author.id))
        ingots = '__**Ingots**__\n\
Copper Ingot: 2×Tetrahedrite + 1×Coal (req Furnace)\n\
Tin Ingot: 2×Cassiterite + 1×Coal (req Furnace)\n\
Zinc Ingot: 2×Sphalerite + 1×Coal (req Furnace)\n\
Lithium Ingot: 2×Pegmatite + 1×Coal (req Furnace)\n\
3×Bronze Ingot: 2×Copper Ingot + 1×Tin Ingot + 1×Coal (req Furnace)\n\
3×Brass Ingot: 2×Copper Ingot + 1×Zinc Ingot + 1×Coal (req Furnace)\n\
Iron Ingot: 2×Hematite + 1×Coal (req Furnace)\n\
Magnesium Ingot: 2×Magnesite + 1×Coal (req Furnace)\n\
Silicon Ingot: 2×Quartz + 1×Coal (req Furnace)\n\
Silver Ingot: 2×Native Silver + 1×Coal (req Furnace)\n\
Gold Ingot: 2×Native Gold + 1×Coal (req Furnace)\n\
Californium Ingot: 2×Franciscite + 1×Coal (req Furnace)\n\
Cobalt Ingot: 2×Cobaltite + 1×Coal (req Furnace)\n\
Lithium Cobalt Oxide Ingot: 1×Cobalt Ingot + 1×Lithium Ingot + 1×Coal (req Furnace)\n\
Carbon Ingot: 3×Coal (req Blast Furnace)\n\
Carbon Ingot: 1×Oil (req Blast Furnace)\n\
3×Carbon Ingot: 1×Diamond (req Blast Furnace)\n\
3×Steel Ingot: 3×Iron Ingot + 2×Carbon Ingot (req Blast Furnace)\n\
Hellstone Ingot: 1×Ringwoodite + 1×Obsidian + 1×Carbon Ingot (req Blast Furnace)\n\
Titanium Ingot: 2×Rutile + 1×Carbon Ingot (req Blast Furnace)\n\
Tungsten Ingot: 2×Wolframite + 1×Carbon Ingot (req Blast Furnace)\n\
Platinum Ingot: 2×Native Platinum + 1×Carbon Ingot (req Blast Furnace)\n\
Plutonium Ingot: 2×Plutonite + 1×Carbon Ingot (req Blast Furnace)\n'
        ingots2 = 'Titanium Carbide Ingot: 3×Titanium Ingot + 3×Carbon Ingot (req Blast Furnace)\n\
Magnesium Carborundium Ingot: 1×Magnesium Ingot + 1×Silicon Ingot + 3×Carbon Ingot (req Blast Furnace)\n\
Majestic Ingot: 1×Magnesium Carborundium Ingot + 1×Titanium Carbide Ingot + 5×Carbon Ingot (req Blast Furnace)\n\
2×Mithril Ingot: 2×Silver Ingot + 1×Aetheric + 5×Carbon Ingot (req Blast Furnace)\n\
2×Adamantium Ingot: 1×Steel Ingot + 1×Tungsten Ingot + 2×Aetheric + 5×Carbon Ingot (req Blast Furnace)\n\
Vanadium Ingot: 2×Vanadinite + 1×Carbon Ingot\n\
2×Titanium Vanadate Ingot: 1×Titanium Ingot + 1×Vanadium Ingot + 3×Carbon Ingot (req Blast Furnace)\n\
Mobius Fuel: 6×Carbon Ingot + 1×Aetheric (req Adamant Furnace)\n\
2×Vibranium Ingot: 1×Adamantium Ingot + 1×Titanium Vanadate Ingot + 1×Mobius Fuel (req Adamant Furnace)\n\
Chlorophyte Ingot: 2×Chlorophyte + 1×Mobius Fuel (req Adamant Furnace)\n\
Uru Ingot: 2×Adamantium Ingot + 3×Vibranium Ingot + 5×Steel Ingot + 7×Aetheric + 2×Mobius Fuel (req Adamant Furnace)\n\
Luminite Ingot: 2×Luminite + 1×Mobius Fuel (req Adamant Furnace)\n\
Megasteel Ingot: 5×Adamantium Ingot + 2×Luminite Ingot + 2×Uru Ingot + 3×Majestic Ingot + 1×Mobius Block (req Adamant Furnace)\n\n'
        blocks = '__**Blocks**__\n\
Copper Block: 10×Copper Ingot\n\
Tin Block: 10×Tin Ingot\n\
Bronze Block: 10×Bronze Ingot\n\
Iron Block: 10×Iron Ingot\n\
Magnesium Block: 10×Magnesium Ingot\n\
Silicon Block: 10×Silicon Ingot\n\
Silver Block: 10×Silver Ingot\n\
Gold Block: 10×Gold Ingot\n\
Californium Block: 10×Californium Ingot\n\
Cobalt Block: 10×Cobalt Ingot\n\
Lithium Cobalt Oxide Block: 10×Lithium Cobalt Oxide Ingot\n\
Carbon Block: 10×Carbon Ingot\n\
Steel Block: 10×Steel Ingot\n\
Hellstone Block: 10×Hellstone Ingot\n\
Titanium Block: 10×Titanium Ingot\n\
Platinum Block: 10×Platinum Ingot\n\
Titanium Carbide Block: 10×Titanium Carbide Ingot\n\
Magnesium Carborundium Block: 10×Magnesium Carborundium Ingot\n\
Majestic Block: 10×Majestic Ingot\n\
Mithril Block: 10×Mithril Ingot\n\
Barrel of Oil: 10×Oil\n\
Lithium Block: 10×Lithium Ingot\n\
Tungsten Block: 10×Tungsten Ingot\n\
Zinc Block: 10×Zinc Ingot\n\
Bronze Block: 10×Bronze Ingot\n\
Adamantium Block: 10×Adamantium Ingot\n\
Vanadium Block: 10×Vanadium Ingot\n\
Titanium Vanadate Block: 10×Titanium Vanadate Ingot\n\
Mobius Block: 10×Mobius Fuel\n\
Vibranium Block: 10×Vibranium Ingot\n\
Chlorophyte Block: 10×Chlorophyte Ingot\n\
Uru Block: 10×Uru Ingot\n\
Luminite Block: 10×Luminite Ingot\n\
Megasteel Block: 10×Megasteel Ingot\n\n'
        other = '__**Resources**__\n\
4×Charcoal: 1×Wood Log\n\
4×Wood Plank: 1×Wood Log\n\
4×Stick: 1×Wood Plank\n\
4×Stone Brick: 4×Stone\n\
Pickaxe Wriststrap: 10×Clover\n\
Axe Wriststrap: 10×Clover\n\n'
        civ = '__**Civiliztion**__\n\
Simple Hut: 100×Wood Log + 2×Food + 1×Land\n\
Hut: 250×Wood Log + 5×Food + 2×Land\n\
Small Cottage: 1k×Wood Plank + 250×Stone + 10×Food + 3×Land\n\
Cottage: 2.5k×Wood Plank + 500×Stone Brick + 20×Food + 5×Land\n\
Small Village: 2×Small Farm + 5×Simple Hut + 2×Hut + 1×Well + 20×Land + 200×Food\n\
Large Village: 2×Medium Farm + 4×Small Village + 20×Simple Hut + 10×Hut + 5×Small Cottage + 1×Well + 50×Land + 1k×Food\n\
Logging Hut: 1×Hut + 20×Food + 100×Wood Plank\n\
Small Farm: 10×Land + 100×Wood Log + 1×Hut + 1×Well + 10×Food\n\
Medium Farm: 4×Small Farm + 1×Small Cottage + 1×Well + 1×Silo + 2.5k×Food\n\
Clover Garden: 20×Clover + 1×Land\n\
Beehive: 1×Clover Garden + 1k×Rupee\n\n'
        util = '__**Utility Buildings**__\n\
Furnace: 20×Stone\n\
Blast Furnace: 150×Stone Brick + 10×Iron Ingot + 1×Furnace\n\
Adamant Furnace: 1k×Stone Brick + 10×Adamantium Ingot + 1×Blast Furnace\n\
Factory: 20×Steel Ingot + 1k×Stone Brick\n\
Furnace (Factory): 1×Furnace + 10×Gears (req Factory)\n\
Blast Furnace (Factory): 1×Blast Furnace + 10×Gears (req Factory)\n\
Adamant Furnace (Factory): 1×Adamant Furnace + 10×Gears (req Factory)\n\
Well: 1×Iron Pickaxe + 500×Stone Brick + 100×Wood Plank\n\
Silo: 50×Tin Ingot + 350×Wood Plank + 100×Food\n\n'
        picks = '__**Pickaxes**__\n\
Wood Pickaxe: 3×Wood Plank + 2×Stick\n\
Stone Pickaxe: 3×Stone + 2×Stick\n\
Copper Pickaxe: 3×Copper Ingot + 2×Stick\n\
Bronze Pickaxe: 3×Bronze Ingot + 2×Stick\n\
Iron Pickaxe: 3×Iron Ingot + 2×Stick\n\
Diamond Pickaxe: 3×Diamond + 2×Stick\n\
Steel Pickaxe: 3×Steel Ingot + 2×Stick\n\
Hellstone Pickaxe: 3×Hellstone Ingot + 2×Stick\n\
Carmeltazite Pickaxe: 3×Carmeltazite + 2×Stick\n\
Titanium Pickaxe: 3×Titanium Ingot + 2×Stick\n\
Titanium Carbide Pickaxe: 3×Titanium Carbide Ingot + 2×Stick\n\
Magnesium Carborundium Pickaxe: 3×Magnesium Carborundium Ingot + 2×Stick\n\
Majestic Pickaxe: 3×Majestic Ingot + 2×Stick\n\
Mithril Pickaxe: 3×Mithril Ingot + 2×Stick\n\
Adamantium Pickaxe: 3×Adamantium Ingot + 2×Stick\n\n'
        axes = '__**Axes**__\n\
Wood Axe: 3×Wood Plank + 2×Stick\n\
Stone Axe: 3×Stone + 2×Stick\n\
Copper Axe: 3×Copper Ingot + 2×Stick\n\
Bronze Axe: 3×Bronze Ingot + 2×Stick\n\
Iron Axe: 3×Iron Ingot + 2×Stick\n\
Diamond Axe: 3×Diamond + 2×Stick\n\
Steel Axe: 3×Steel Ingot + 2×Stick\n\
Hellstone Axe: 3×Hellstone Ingot + 2×Stick\n\
Carmeltazite Axe: 3×Carmeltazite + 2×Stick\n\
Titanium Axe: 3×Titanium Ingot + 2×Stick\n\
Titanium Carbide Axe: 3×Titanium Carbide Ingot + 2×Stick\n\
Magnesium Carborundium Axe: 3×Magnesium Carborundium Ingot + 2×Stick\n\
Majestic Axe: 3×Majestic Ingot + 2×Stick\n\
Mithril Axe: 3×Mithril Ingot + 2×Stick\n\
Adamantium Axe: 3×Adamantium Ingot + 2×Stick\n\n'
        sawmills = '__**Sawmills**__\n\
Stone-bladed Sawmill: 1×Stone + 2×Stick + 5×Wood Plank\n\
Copper-bladed Sawmill: 1×Copper Ingot + 2×Stick + 5×Wood Plank\n\
Bronze-bladed Sawmill: 1×Bronze Ingot + 2×Stick + 5×Wood Plank\n\
Iron-bladed Sawmill: 1×Iron Ingot + 2×Stick + 5×Wood Plank\n\
Diamond-bladed Sawmill: 1×Diamond + 2×Stick + 5×Wood Plank\n\
Steel-bladed Sawmill: 1×Steel Ingot + 2×Stick + 5×Wood Plank\n\
Hellstone-bladed Sawmill: 1×Hellstone Ingot + 2×Stick\ + 5×Wood Plank\n\
Carmeltazite-bladed Sawmill: 1×Carmeltazite + 2×Stick + 5×Wood Plank\n\
Titanium-bladed Sawmill: 1×Titanium Ingot + 2×Stick + 5×Wood Plank\n\
Titanium-Carbide-bladed Sawmill: 1×Titanium Carbide Ingot + 2×Stick + 5×Wood Plank\n\
Magnesium Carborundium-bladed Sawmill: 1×Magnesium Carborundium Ingot + 2×Stick + 5×Wood Plank\n\
Majestic-bladed Sawmill: 1×Majestic Ingot + 2×Stick + 5×Wood Plank\n\
Mithril-bladed Sawmill: 1×Mithril Ingot + 2×Stick + 5×Wood Plank\n\
Adamantium-bladed Sawmill: 1×Adamantium Ingot + 2×Stick + 5×Wood Plank\n\n'
        trees = '__**Orchard Trees**__\n\
Oak Tree: 1×Land + 8×Nuts + 4×Stick\n\
Maple Tree: 1×Land + 6×Nuts + 2×Syrup + 4×Stick\n\
Spruce Tree: 1×Land + 4×Nuts + 4×Stick\n\
Apple Tree: 1×Land + 6×Fruit + 4×Stick\n\
Rupee Tree: 1×Land + 1k×Rupee + 2×Oak Tree + 4×Stick\n\
Coin Tree: 1×Land + 100×Arg + 2×Maple Tree + 4×Stick\n\
Oak Grove: 10×Oak Tree\n\
Maple Grove: 10×Maple Tree\n\
Spruce Grove: 10×Spruce Tree\n\
Apple Grove: 10×Apple Tree\n\
Rupee Grove: 10×Rupee Tree\n\
Coin Grove: 10×Coin Tree\n\
Oak Forest: 10×Oak Grove\n\
Maple Forest: 10×Maple Grove\n\
Spruce Forest: 10×Spruce Grove\n\
Apple Forest: 10×Apple Grove\n\
Rupee Forest: 10×Rupee Grove\n\
Coin Forest: 10×Coin Grove\n\n'
        granary = '__**Granary**__\n\
Bread: 3×Grain\n\
Golden Fruit: 1×Fruit, 8×Gold Ingot\n\
2×Food: 1×Fruit\n\
1×Food: 1×Nuts\n\
1×Food: 1×Syrup\n\
3×Food: 1×Grain\n\
3×Food: 1×Honey\n\
10×Food: 1×Bread\n\
25×Food: 1×Golden Fruit\n\n'
        hardware = '__**Hardware**__\n\
Gear: 4×Brass Ingot\n\
Copper Pipe: 4×Copper Ingot\n\
Tin Pipe: 4×Tin Ingot\n\
Zinc Pipe: 4×Zinc Ingot\n\
Bronze Pipe: 4×Bronze Ingot\n\
Brass Pipe: 4×Brass Ingot\n\
Iron Pipe: 4×Iron Ingot\n\
Steel Pipe: 4×Steel Ingot'
        if len(args) > 0:
            out = ''
            if str.lower(args[0]) == 'all':
                await ctx.send(ingots)
                await ctx.send(ingots2 + other)
                await ctx.send(blocks + picks)
                await ctx.send(axes + sawmills)
                await ctx.send(civ + util)
                await ctx.send(trees + granary + hardware)
                message_return = finalize(ctx, 'recipes', None, "OK", args[0])
                return
            elif str.lower(args[0]) == 'ingot' or str.lower(args[0]) == 'ingots':
                await ctx.send(ingots)
                out = ingots2
            elif str.lower(args[0]) == 'other' or str.lower(args[0]) == 'misc':
                out = other
            elif str.lower(args[0]) == 'blocks' or str.lower(args[0]) == 'block':
                out = blocks
            elif str.lower(args[0]) in ['picks', 'pickaxes', 'pick', 'pickaxe']:
                out = picks
            elif str.lower(args[0]) == 'axe' or str.lower(args[0]) == 'axes':
                out = axe
            elif str.lower(args[0]) == 'sawmill' or str.lower(args[0]) == 'sawmills':
                out = sawmills
            elif str.lower(args[0]) == 'civ' or str.lower(args[0]) == 'civilization':
                out = civ
            elif str.lower(args[0]) in ['util', 'utility', 'utilities']:
                out = util
            elif str.lower(args[0]) == 'tree' or str.lower(args[0]) == 'trees':
                out = trees
            elif str.lower(args[0]) == 'granary' or str.lower(args[0]) == 'food':
                out = granary
            elif str.lower(args[0]) in ['hardware', 'component', 'components']:
                out = hardware
            elif args[0] not in "2210112013141516171819":
                itemname = args[0]
                for arg in args:
                    if arg != args[0]:
                        itemname += ' ' + arg
                await Purchases.show_cost(ctx, user_data, str.lower(itemname), True)
                message_return = finalize(ctx, 'recipes', None, "OK", itemname)
            if out != "":
                message_return = finalize(ctx, 'recipes', out, "OK", args[0])
                await ctx.send(message_return)
        else:
            args = ['1']
        if args[0] in "2210112013141516171819":
            user_data = get_user_data(testfor_alt(ctx.message.author.id))
            user_data.test_smelt()
            user_data.loadall()
            await Purchases.shop(ctx, user_data, args, True)
            save_user_data(user_data)
            message_return = finalize(ctx, 'recipes', None, "OK", args[0])
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'recipes', out, out)
        await ctx.send(message_return)

@bot.command(aliases=['crafting'])
async def craft(ctx, *, args):
    """Crafts an object from the blueprint library. Parameters: <Item ID> <quantity>"""
    try:
        g_data = get_guild_data(ctx)
        if not g_data.data['crafting']:
            return
        user_data = get_user_data(testfor_alt(ctx.message.author.id))
        user_data.test_smelt()
        user_data.testfor_max_chests()
        user_data.loadall()
        passin = ''
        if len(args) > 0:
            for arg in args:
                args = str.lower(args)
            if len(args) >= 3:
                if args[-3] in ' ' and args[-2] in '123456789' and args[-1] in '0123456789':
                    quantity = int(args[-2:])
                    if quantity > 10:
                        out = 'You cannot craft any more than 10 items!'
                        message_return = finalize(ctx, 'craft', out, "OK", args)
                        await ctx.send(message_return)
                        return
                    cursor = 0
                    while cursor < len(args)-1:
                        passin = args[:-3]
                        cursor += 1
                elif args[-1] in '0123456789' and args[-2] in ' ':
                    quantity = int(args[-1])
                    if quantity < 1:
                        out = 'You cannot craft any less than one item!'
                        message_return = finalize(ctx, 'craft', out, "OK", args)
                        await ctx.send(message_return)
                        return
                    cursor = 0
                    while cursor < len(args)-1:
                        passin = args[:-2]
                        cursor += 1
                else:
                    quantity = 1
                    passin = args
            elif len(args) >= 2:
                if args[-1] in '0123456789' and args[-2] in ' ':
                    quantity = int(args[-1])
                    if quantity < 1:
                        out = 'You cannot craft any less than one item!'
                        message_return = finalize(ctx, 'craft', out, "OK", args)
                        await ctx.send(message_return)
                        return
                    cursor = 0
                    while cursor < len(args)-1:
                        passin = args[:-2]
                        cursor += 1
                else:
                    quantity = 1
                    passin = args
        code = "OK"
        while quantity > 0 and code == "OK":
            if user_data.get_inv_volume() > user_data.inv_size():
                errout = "Your inventory is too full to do this!"
                message_return = finalize(ctx, 'craft', errout, "OK")
                await ctx.send(message_return)
                code = "HALT"
            else:
                code = await Purchases.buy(ctx, user_data, passin, True)
                quantity -= 1
        save_user_data(user_data)
        if len(args) > 0:
            message_return = finalize(ctx, 'craft', None, "OK", args)
        else:
            message_return = finalize(ctx, 'craft', None, "OK")
    except Exception as e:
        out = f"Error: {e}"
        message_return = finalize(ctx, 'craft', out, out)
        await ctx.send(message_return)

@bot.command(aliases=['ac', 'autocrafting'])
async def autocraft(ctx, *args):
    """Allows autocrafting of items. Requires a factory to be built.
    /autocraft list <page number>
    /autocraft add <resource> <blueprint to make> <quantity of resource>
    If the amount of <resource> is less than the threshold set by <quantity>, then <blueprint> is automatically crafted.
    If <quantity> is 'Infinity', then <blueprint> will be crafted so long as you have the resources.
    Examples:
    /autocraft add "Wood Planks" plank0 100
    > Crafts more wood planks four at a time per autocraft tick when you have less than 100 planks
    /autocraft add Tetrahedrite cui Infinity
    > Crafts a copper ingot whenever you have enough tetrahedrite and coal to do so"""
    g_data = get_guild_data(ctx)
    if not g_data.data['crafting']:
        return
    if len(args) == 0:
        state = 'list'
    else:
        state = args[0]
    ShopItems.add_items = add_items
    identity = testfor_alt(ctx.message.author.id)
    user = get_user_data(identity)
    embed = discord.Embed(color=0x8000FF)
    if state == 'list':
        embed.title = "Autocrafted Items"
        if len(args) <= 1:
            page = 1
        else:
            page = int(args[1])
        embed.description = "Page {0}".format(str(page))
        items = user.autocrafted_items()
        if page < 1:
            embed.title = "Invalid Page!"
        else:
            to_print = []
            keys = list(items.keys())
            for i in range(page * 10 - 10, page * 10):
                if i < len(keys):
                    key = keys[i]
                    data = (key, items[key][0], items[key][1])
                    to_print.append(data)
                else:
                    break
            if len(to_print) == 0:
                embed.add_field(name="Error!", value="You do not autocraft anything [on this page]!")
            else:
                for item in to_print:
                    embed.add_field(name="Crafted at {0} items.".format(number_cronch(item[2], testfor_alt(ctx.message.author.id))),
                                    value="Craft ID {0} when you are low on {1}".format(item[1], item[0]),
                                    inline=False)
    elif state == 'add':
        embed.title = "Adding autocrafted item"
        embed.add_field(name="Note:",
                        value="If you don't have the valid auto-crafter items then autocrafting will not happen, " +
                              "even if you queue it.",
                        inline=False)
        embed.add_field(name="**WARNING:**",
                        value="If the recipe does not produce the item," +
                              "then the autocraft will run until you run out of resources!")
        if len(args) < 4:
            embed.add_field(name="Error!",
                            value="Input format: ``" + prefix + "autocraft add <Item> <crafting_ID> <number of items to autocraft at>``\n\
If the amount of `<resource>` is less than the threshold set by `<quantity>`, then `<blueprint>` is automatically crafted.\n\
If `<quantity>` is 'Infinity', then `<blueprint>` will be crafted so long as you have the resources.",
                            inline=False)
        else:
            if len(args) == 6:
                args = [args[0], args[1] + ' ' + args[2] + ' ' + args[3], args[4], args[5]]
            elif len(args) == 5:
                args = [args[0], args[1] + ' ' + args[2], args[3], args[4]]
            valid = True
            item = args[1]
            craft_id = args[2]
            num = args[3]
            try:
                num = int(num)
            except ValueError:
                if num == 'Infinity':
                    num = 1000**1000
                else:
                    valid = False
                    embed.add_field(name="Error!", value="{0} is not a valid number!".format(num), inline=False)
            if valid:
                # aka if no errors were thrown
                data = user.add_autocrafted_item(item, craft_id, num)
                embed.add_field(name=". . .", value=data, inline=False)
    elif state == "remove":
        if len(args) < 2:
            embed.add_field(name="Error!", value="Input format: ``" + prefix + "autocraft remove <Item to autocraft>``",
                inline=False)
        else:
            item = args[1]
            if user.remove_autocrafted_item(item):
                embed.add_field(name="Success!",
                    value="Successfully removed {0} from your autocraft list.".format(item),
                    inline=False)
            else:
                embed.add_field(name="Error!",
                    value="Item {0} is not in your autocraft list!".format(item),
                    inline=False)
    else:
        embed.add_field(name="Error!",
            value="{0} is an invalid action.".format(state))
    await ctx.send(embed=embed)
    save_user_data(user)
    if len(args) > 0:
        message_return = finalize(ctx, 'autocraft', None, "OK", args[0])
    else:
        message_return = finalize(ctx, 'autocraft', None, "OK")

@bot.event
async def on_message(message):
    g_data = get_guild_data(message)
    if message.guild == 251185305955205121 and developer_mode == 2:
        return
    author = message.author
    if author.bot:
        return
    #if data.data['xp_cooldown'] = True
    #   return
    data = get_user_data(testfor_alt(author.id))
    if type(data) is dict:
        data.add_exp(random.randrange(4)*experience_rate)
        lvup = data.lvup(username(author, testfor_alt(author.id))[0])
        if lvup != '' and not data.muteLevelup() and g_data.data['levels'] and g_data.data['lv_msg']:
            channel = message.channel
            await channel.send(lvup)
        #data.data['xp_cooldown'] = True
        save_user_data(data)
    
    gate = message.guild.name + ':#' + message.channel.name
    if gate in connections.keys() and message.content[:len(g_data.data['prefix'])] != g_data.data['prefix']:
        destination = connections[gate]
        dest_ctx = portals[destination]
        await dest_ctx.send(f"`[{str.upper(author.name)}]:` {scan(message.content)}")
    if gate in secure_connections.keys() and message.content[:len(g_data.data['prefix'])] != g_data.data['prefix']:
        destination = secure_connections[gate]
        dest_ctx = private[destination]
        await dest_ctx.send(f"`[{str.upper(author.name)}]:` {scan(message.content)}")
    retstr = ""
    act = 0
    for i in range(len(message.content)):
        if (message.content[i] in 'Aa'):
            act = act + 1
    if act == len(message.content):
        retstr += "🅱"*act

    if retstr != "":
        await message.channel.send(retstr)

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
        await ctx.send('Not a command. Do z!cmd or z!help for a list of commands.')
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
        await ctx.send("Args are either too short or otherwise wrong for this command. Check z!help <command> and try again.")
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
print('Backing up save files...')
backup()
print('Loading shops...') # So that all shop items are loaded.
print("\r> Loading shop items..." + " "*20, end="")
ShopItems.load_shop_items()
print("\r> Loading craft items..." + " "*20, end="")
CraftItems.load_craft_items()
print("\r> Adding item counters..." + " "*20, end="")
ShopHandler.set_function(add_items)
print('\rGetting item prices...' + " "*20)
get_item_prices()
print('\rLoading userdatas...' + " "*100)
load_all_users()
print('Inserting key...')
devmode = config.devmode
bot.run(devmode[dev_info['developer_mode']])
print('Running!')
