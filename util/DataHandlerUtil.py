from os.path import splitext
from sqlite3 import connect as sqlConnect
from datetime import datetime
from math import floor
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import *
from util.SLHandle import *
from util.cmdutil import cmdutil
text = cmdutil()

def getAcctAge(dataStats):
    ts = datetime.timestamp(datetime.now())
    return int((ts - dataStats["Acct Creation"])//86400)+1

def getActivity(dataStats):
    acctAge = getAcctAge(dataStats)
    return dataStats["Messages Sent"] / acctAge

def get60DayActivity(dataStats):
    board = dataStats["Activity Board"]
    return sum(board) / len(board)

def updateStats(dataStats):
    age = getAcctAge(dataStats)
    while dataStats["Last Update"] < age:
        dataStats["Activity Board"].append(0)
        dataStats["Last Update"] += 1
    while len(dataStats) > 60:
        dataStats.pop(0)
    return dataStats
        
def getAcctAgeYMD(dataStats):
    age = getAcctAge(dataStats)
    years = round(age // 365.2425)
    age -= floor(years * 365.2425)
    months = round(age // 30.436875)
    days = age - floor(months * 30.436875)
    return (years, months, days)
        
def getAcctAgeYMDAsStr(dataStats):
    age = getAcctAgeYMD(dataStats)
    if age[0] > 0: string = f"{age[0]} year(s) {age[1]} month(s) {age[2]} day(s)"
    elif age[1] > 0: string = f"{age[1]} month(s) {age[2]} day(s)"
    else: string = f"{age[2]} day(s)"
    return string
    

def GSCToInt(gold, silver, copper):
    return gold*1000000 + silver*1000 + copper

def IntToGSC(integer):
    return(int(integer // 1000000),
           int(integer % 1000000 // 1000),
           int(integer % 1000))

def regularizeGSC(gold, silver, copper):
    return IntToGSC(GSCToInt(gold, silver, copper))

def levelToExp(level:int):
    level -= 1
    return (((2 * ((1+level)/2)**2 - ((1+level)/2)) * (4 * ((1+level)/2) - 1))/3+level+1) * 20

