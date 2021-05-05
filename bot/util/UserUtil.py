from bot import ResourceParse
from data.FileHandler import *

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

def username(ctx, userid, *discord_data): #ctx = the unfiltered userdata, could be alt; userid = filtred user id
    player_data = get_user_data(userid)
    try:
        # find real name
        if player_data.realname() == '':
            try:
                player_data.data['realname'] = user_name[int(userid)]
            except Exception: # userdata realname is blank
                player_data.data['realname'] = ctx.name
        realname = player_data.realname()
        # find nickname
        if player_data.nick() == '':
            name = realname
        else:
            name = '\*' + player_data.nick() + '\*'
        name = player_data.data['displayed badge'] + name
    except Exception: # userdata does not exist
        realname = ctx.name
        name = realname
    return name, realname

def testfor_alt(user):
    user = int(user)
    for key in alts.keys():
        if key == user:
            user = alts[key]
    user = str(user)
    return user

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
