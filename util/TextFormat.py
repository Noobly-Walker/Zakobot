# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.SLHandle import *
from util.cmdutil import cmdutil
from datetime import datetime
from util.TimeUtil import *
text_ = cmdutil()

def returnEmoji(emoji):
    eml = loadJSON("emojis.json", "data")
    if emoji in eml: return eml[emoji]
    elif emoji + "~0" in eml: return eml[emoji+"~0"]
    else: return "e!" + emoji

def formatText(text):
    if text in ["", " ", None]: return ""
    text += " "
    end = False
    form = "normal"
    loops = 0
    formStart = []
    formEnd = []
    carry = []
    while not end:
        for char in range(len(text)):
            try:
                if text[char] + text[char+1] == "e!": #replace e!test with <test:123456789012>
                    startIndex = char
                    currentIndex = char
                    while text[currentIndex+1] != " ":
                        currentIndex += 1
                    endIndex = currentIndex+1
                    text = text[:startIndex] + returnEmoji(text[startIndex+2:endIndex]) + text[endIndex:]
                if text[char] + text[char+1] == "e[": #switch mode to emojitext, remove e[
                    form = "emojitext"
                    text = text[:char] + text[char+2:]
                    formStart.append(char)
                    formEnd.append(char)
                    carry.append("")
                if text[char] + text[char+1] + text[char+2] == "<t>": #replace <t> with <t:timestamp>
                    timestamp = int(datetime.now().timestamp())
                    text = text[:char] + f"<t:{timestamp}>" + text[char+3:]
                if form != "normal": #remove square bracket
                    if text[char] == "]" and text[char-1] != "\\":
                        form = "normal"
                        text = text[:char] + text[char+1:]
                if form == "emojitext": #replace string in square brackets with emojis
                    value = format(ord(text[char]), "x").upper().rjust(4, "0")
                    carry[-1] += returnEmoji(value)
                    formEnd[-1] += 1
                loops += 1
                if loops >= 10000: #catch to prevent it from running forever
                    text = "TextFormatError: Format failed."
                    text_.warn("[TEXTFORMATERROR] Format failed.")
            except Exception as e:
                end = True
                break
    if carry != []: #if something is in this string, it needs to be injected back into text
        for i in range(len(formStart)-1, -1, -1):
            text = text[:formStart[i]] + carry[i] + text[formEnd[i]:]
    text = text.strip() #strip leading and trailing whitespace
    text = text.replace("\\n", "\n") #put newline characters back
    if carry != [] and text[-1] == "]" and text[-2] != "\\": text = text[:-1] #patch to remove ] when it is the last character
    return text
