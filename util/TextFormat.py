# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.SLHandle import *
from util.cmdutil import cmdutil
text = cmdutil()

def returnEmoji(emoji):
    eml = loadJSON("emojis.json", "data")
    if emoji in eml: return eml[emoji]
    else: return "e!" + emoji

def formatText(text):
    if text in ["", " ", None]: return ""
    text += " "
    end = False
    while not end:
        for char in range(len(text)):
            try:
                if text[char] + text[char+1] == "e!":
                    startIndex = char
                    currentIndex = char
                    while text[currentIndex+1] != " ":
                        currentIndex += 1
                    endIndex = currentIndex+1
                    text = text[:startIndex] + returnEmoji(text[startIndex+2:endIndex]) + text[endIndex:-1]
            except Exception:
                end = True
                break
    text = text.strip()
    text = text.replace("\\n", "\n")
    return text
