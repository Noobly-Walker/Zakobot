import asyncio
from discord.ext import commands
import discord
import traceback
from os.path import isdir,exists
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import expol
from util.SLHandle import *
from util.PlayerDataHandler import *
from util.GuildDataHandler import *
from util.ColorUtil import rectColor
from util.cmdutil import cmdutil
text = cmdutil()


def bubbleSort(array:list):
    l=len(array)
    for i in range(l-1):
        for j in range(i+1,l):
            if array[i]>array[j]:
                t=array[i]
                array[i]=array[j]
                array[j]=t
    return array

def parenthesisFinder(funct:list, index, direction, symbols="()"):
    opened = direction
    offset = 0 + direction
    while True:
        if funct[index + offset] == symbols[0]:
            opened += 1
        if funct[index + offset] == symbols[1]:
            opened -= 1
        if opened == 0:
            break
        offset += direction
    new_index = index + offset
    return new_index

def calculatorFunct(user, funct:str):
    funct = list(funct) #converts tuple to string, then to list
    derivedFunct = []
    expectedStrings = ["//","**","floor","fdiv","ceil","ceiling","cdiv","log","ln","ld","mod","exp","pi","phi","tau"]
    for index in range(len(funct)): #splits string up for recombination into ints
        try:
            if funct[index] in "-0123456789.": #combining numbers
                try:
                    while funct[index+1] in "-0123456789.":
                        funct[index] += funct[index+1]
                        del funct[index+1]
                except IndexError: pass #reached end of list
                if funct[index] != "-":
                    derivedFunct.append(f"expol({funct[index]})")
                else:
                    derivedFunct.append(funct[index])
            elif funct[index] not in "0123456789.": #combining non-numbers
                derivedFunct.append(funct[index])
                for string in expectedStrings:
                    if funct[index] == string[0]:
                        try:
                            isMatch = True
                            for char in range(len(string)):
                                if funct[index+char] != string[char]:
                                    isMatch = False
                                    break
                            if isMatch:
                                for char in range(len(string)-1):
                                    derivedFunct[-1] += funct[index+1]
                                    del funct[index+1]
                                break
                        except IndexError: continue #reached end of list
            if isinstance(derivedFunct[-1], str):
                #normalizing built-in operations
                if derivedFunct[-1] in "×x": derivedFunct[-1] = "*"
                if derivedFunct[-1] == "÷": derivedFunct[-1] = "/"
                if derivedFunct[-1] in ["^","exp"]: derivedFunct[-1] = "**"
                if derivedFunct[-1] in ["floor","fdiv"]: derivedFunct[-1] = "//"
                if derivedFunct[-1] == "mod": derivedFunct[-1] = "%"
                #filtering out constants
                if derivedFunct[-1] in ["phi","φ","ϕ"]: derivedFunct[-1] = "expol(1.61803399)"
                if derivedFunct[-1] in ["pi","π"]: derivedFunct[-1] = "expol(3.14159265)"
                if derivedFunct[-1] in ["tau","τ"]: derivedFunct[-1] = "expol(6.28318530)"
                if derivedFunct[-1] == "e": derivedFunct[-1] = "expol(2.71828183)"
        except IndexError: break #reached end of list before expected
    for index in range(len(derivedFunct), -1, -1): #second pass, to apply functions that must look ahead
        try:
            if derivedFunct[index] in ["ln", "ld", "log"]: #logarithms
                if derivedFunct[index+1] == "(": #log must come after parenthesis
                    newIndex = parenthesisFinder(derivedFunct, index+1, 1)
                    if derivedFunct[index] == "ln": derivedFunct[newIndex] += ".log(2.71828183)"
                    if derivedFunct[index] == "ld": derivedFunct[newIndex] += ".log(10)"
                    if derivedFunct[index] == "log":
                        functFrag = "".join(derivedFunct[index+1:newIndex+1])
                        if derivedFunct[newIndex+1] == "(":
                            newNewIndex = parenthesisFinder(derivedFunct, newIndex+1, 1)
                            derivedFunct[newNewIndex] += f".log(expol({list(eval(functFrag))}))"
                        else: derivedFunct[newIndex+1] += f".log({float(eval(functFrag))})"
                        #remove already parsed region
                        derivedFunct = [derivedFunct[i] for i in range(len(derivedFunct)) if i not in range(index+1,newIndex+1)]
                else:
                    if derivedFunct[index] == "ln": derivedFunct[index+1] += ".log(2.71828183)"
                    elif derivedFunct[index] == "ld": derivedFunct[index+1] += ".log(10)"
                    elif derivedFunct[index] == "log":
                        if derivedFunct[index+2] == "(":
                            newIndex = parenthesisFinder(derivedFunct, index+2, 1)
                            derivedFunct[newIndex] += f".log({derivedFunct[index+1]})"
                        else: derivedFunct[index+2] += f".log({derivedFunct[index+1]})"
                        del derivedFunct[index+1] # remove log base
                del derivedFunct[index] #remove log argument
            elif derivedFunct[index] in ["E", "K"]:
                #converting derived operations
                if derivedFunct[index] == "E":
                    if derivedFunct[index-1] not in "+-**//%": derivedFunct[index] = '*'
                    derivedFunct.insert(index+1, "expol(10)")
                    if derivedFunct[index+2] == "*": derivedFunct[index+2] = '**'
                    else: derivedFunct.insert(index+2, '**')
                if derivedFunct[index] == "K":
                    if derivedFunct[index-1] not in "+-**//%": derivedFunct[index] = '*'
                    derivedFunct.insert(index+1, "expol(1000)")
                    if derivedFunct[index+2] == "*": derivedFunct[index+2] = '**'
                    else: derivedFunct.insert(index+2, '**')
        except IndexError: continue #list suddenly shrank, but the index will return to the list soon
    try:
        funct = eval("".join(derivedFunct))
        return f"{funct:{GetNotationCode(user)}}"
    except:
        return traceback.format_exc().splitlines()[-1]
