# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.cmdutil import cmdutil
text = cmdutil()

def rectColor(color):
    if set(color) <= set("0123456789"): #Stringified color integer
        return int(color)
    if set(color) <= set("0123456789,"): #Stringified RGB decimal
        color = color.split(",")
        for i in range(len(color)):
            color[i] = int(color[i])
    elif set(color) <= set("0123456789ABCDEFabcdefx,"): #Stringified RGB hex
        color = color.split(",")
        for i in range(len(color)):
            color[i] = int(color[i], 16)
    else: #Might be a color name
        color = color.lower()
        if color == "red": color = (255,0,0)
        if color == "vermillion": color = (255,64,0)
        if color == "orange": color = (255,128,0)
        if color == "amber": color = (255,192,0)
        if color == "yellow": color = (255,255,0)
        if color == "chartreuse": color = (128,255,0)
        if color == "green": color = (0,255,0)
        if color == "cyan": color = (0,255,255)
        if color == "cornflower": color = (0,128,255)
        if color == "blue": color = (0,0,255)
        if color == "indigo": color = (64,0,255)
        if color == "purple": color = (128,0,255)
        if color == "magenta": color = (255,0,255)
        if color in ["darkred", "maroon"]: color = (128,0,0)
        if color in ["darkvermillion", "brick", "copper"]: color = (128,32,0)
        if color in ["darkorange", "brown"]: color = (128,64,0)
        if color in ["darkamber", "brass"]: color = (128,96,0)
        if color in ["darkyellow", "gold"]: color = (128,128,0)
        if color in ["darkchartreuse", "swamp"]: color = (64,128,0)
        if color in ["darkgreen", "forest"]: color = (0,128,0)
        if color in ["darkcyan", "teal"]: color = (0,128,128)
        if color == "darkcornflower": color = (0,64,128)
        if color in ["darkblue", "navy"]: color = (0,0,128)
        if color in ["darkviolet", "midnight"]: color = (32,0,128)
        if color in ["plum", "darkpurple"]: color = (64,0,128)
        if color in ["darkmagenta", "eggplant"]: color = (128,0,128)
        if color in ["lightred", "pink"]: color = (255,128,128)
        if color in ["lightvermillion", "peach"]: color = (255,160,128)
        if color == "lightorange": color = (255,192,128)
        if color == "lightamber": color = (255,224,128)
        if color in ["lightyellow", "lemon"]: color = (255,255,128)
        if color in ["lightchartreuse", "avocado"]: color = (192,255,128)
        if color in ["lightgreen", "lime"]: color = (128,255,128)
        if color in ["lightcyan", "sky"]: color = (128,255,255)
        if color == "lightcornflower": color = (128,192,255)
        if color in ["lightblue", "slate"]: color = (128,128,255)
        if color == "lightindigo": color = (160,128,255)
        if color in ["lightpurple", "lavender"]: color = (192,128,255)
        if color in ["lightmagenta", "rose"]: color = (255,128,255)
        if color == "black": color = (0,0,0)
        if color in ["darkgray", "darkgrey"]: color = (64,64,64)
        if color in ["gray", "grey"]: color = (128,128,128)
        if color in ["lightgray", "lightgrey", "silver"]: color = (192,192,192)
        if color == "white": color = (255,255,255)
    return color[0]*256*256+color[1]*256+color[2]