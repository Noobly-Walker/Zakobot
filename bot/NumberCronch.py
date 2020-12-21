import discord
from discord.ext import commands
import sys
from bot.UserData import *
from data import FileHandler
import math

ktext = [[
    ['k', 'Thousand', 'N'], ['M', 'M', 'I'], ['B', 'B', 'II'], ['T', 'Tr', 'III'], ['Qa', 'Quadr', 'IV'],
    ['Qi', 'Quint', 'V'], ['Sx', 'Sext', 'VI'], ['Sp', 'Sept', 'VII'], ['O', 'Oct', 'VIII'], ['N', 'Non', 'IX']
    ],
    [['', '', ''], ['U', 'Un', 'I'], ['D', 'Duo', 'II'], ['T', 'Tre', 'III'], ['Qa', 'Quattor', 'IV'],
     ['Qi', 'Quin', 'V'], ['Sx', 'Sex', 'VI'], ['Sp', 'Septen', 'VII'], ['O', 'Octo', 'VIII'], ['N', 'Novem', 'IX']
    ],
    [['', '', ''], ['Dc', 'Dec', 'X'], ['Vg', 'Vigint', 'XX'], ['Tg', 'Trigint', 'XXX'], ['Qag', 'Quadragint', 'XL'],
     ['Qig', 'Quinquagint', 'L'], ['Sxg', 'Sexagint', 'LX'], ['Spg', 'Septuagint', 'LXX'], ['Og', 'Octagint', 'LXXX'], ['Ng', 'Nonagint', 'XC']
    ],
    [['', '', ''], ['Ct', 'Cent', 'C'], ['Dt', 'Ducent', 'CC'], ['Tt', 'Trecent', 'CCC'], ['Qat', 'Quadringent', 'CD'],
     ['Qit', 'Quingent', 'D'], ['Sxt', 'Sescent', 'DC'], ['Spt', 'Septingent', 'DCC'], ['Ot', 'Octingent', 'DCCC'], ['Nt', 'Nongent', 'CIK']
    ],
    [['', '', ''], ['Ml', 'Mill', 'I'], ['Dl', 'Dumill', 'II'], ['Tl', 'Tremill', 'III'], ['Qal', 'Quadramill', 'IV'],
     ['Qil', 'Quinmill', 'V'], ['Sxl', 'Seximill', 'VI'], ['Spl', 'Septimill', 'VII'], ['Ol', 'Octimill', 'VIII'], ['Nl', 'Nonimill', 'IX']
    ],
    [['', '', ''], ['My', 'Myr', 'X'], ['Dy', 'Dumyr', 'XX'], ['Ty', 'Tremyr', 'XXX'], ['Qay', 'Quadramyr', 'XL'],
     ['Qiy', 'Quinmyr', 'L'], ['Sxy', 'Seximyr', 'LX'], ['Spy', 'Septimyr', 'LXX'], ['Oy', 'Octimyr', 'LXXX'], ['Ny', 'Nonimyr', 'XC']
    ],
    [['', '', ''], ['Lk', 'Lak', 'C'], ['Dk', 'Dulak', 'CC'], ['Tk', 'Trelak', 'CCC'], ['Qak', 'Quadralak', 'CD'],
     ['Qik', 'Quinlak', 'D'], ['Sxk', 'Sexilak', 'DC'], ['Spk', 'Septilak', 'DCC'], ['Ok', 'Octilak', 'DCCC'], ['Nk', 'Nonilak', 'CIM']
    ],
    [['', '', ''], ['Mi', 'Micr', 'M'], ['Dµ', 'Dumicr', 'II'], ['Tµ', 'Tremicr', 'III'], ['Qaµ', 'Quadrimicr', 'IV'],
     ['Qiµ', 'Quinmicr', 'V'], ['Sxµ', 'Seximicr', 'VI'], ['Spµ', 'Septimicr', 'VII'], ['Oµ', 'Octimicr', 'VIII'], ['Nµ', 'Nonimicr', 'IX']
    ],
    [['', '', ''], ['Myµ', 'Myrimicr', 'X'], ['Dyµ', 'Dumyrimicr', 'XX'], ['Tyµ', 'Trimyrimicr', 'XXX'], ['Qayµ', 'Quadrimyrimicr', 'XL'],
     ['Qiyµ', 'Quinmyrimicr', 'L'], ['Sxyµ', 'Seximyrimicr', 'LX'], ['Spyµ', 'Septimyrimicr', 'LXX'], ['Oyµ', 'Octimyrimicr', 'LXXX'], ['Nyµ', 'Nonimyrimicr', 'XC']
    ],
    [['', '', ''], ['Lkµ', 'Lakimicr', 'C'], ['Dkµ', 'Dulakimicr', 'CC'], ['Tkµ', 'Trelakimicr', 'CCC'], ['Qakµ', 'Quadralakimicr', 'CD'],
     ['Qikµ', 'Quinlakimicr', 'D'], ['Sxkµ', 'Sexilakimicr', 'DC'], ['Spkµ', 'Septilakimicr', 'DCC'], ['Okµ', 'Octilakimicr', 'DCCC'], ['Nkµ', 'Nonilakimicr', 'CIM']
    ]]

cubic = ['D', 'h', 'k', 'Dk', 'hk', 'M', 'DM', 'hM', 'G', 'DG', 'hG', 'T']

def numbuild(k, notation):
    text = []
    digit = []
    type2suffix = ['', 'K-', 'M-']
    notationTranslate = {1 : 0, 7 : 1, 11 : 2, 12 : 3, 13 : 4, -1 : 5}
    numtype = notationTranslate[notation]
    kpr = k
    num = numtype
    out = ''
    if numtype == 0 or numtype == 1 or numtype == 2 or numtype == 5:
        k -= 1
    if numtype == 3 or numtype == 4:
        k = k//2
        num -= 3
    if k < 10 and k >= 0:
        if numtype == 0 or numtype == 1 or numtype == 2:
            out = ktext[0][k][numtype]
            if numtype == 1:
                out = ' ' + out
                if k >= 1:
                    out = out + 'illion'
        elif numtype == 3 or numtype == 4:
            out = ktext[0][k][num] 
            if k - kpr/2 != 0 and k >= 1:
                if numtype == 4:
                    out = ' ' + out
                out = ktext[0][0][num] + out
            if numtype == 4:
                out = ' ' + out
                if k >= 1:
                    out = out + 'illion'
        elif numtype == 5:
            out = cubic[k]
    if k >= 10:
        limit = 0
        while k >= 10**limit: # breaks k exponent down into individual digits
            digit.append(get_digit(k, limit, 1))
            limit += 1
        limit = 0
        while k >= 10**limit: # translates digits into strings
            text.append(ktext[limit+1][digit[limit]][num])
            limit += 1
        if num == 0 or num == 1: # finalizes notations 1, 7, 12, and 13
            limit = 0
            while len(text) > limit:
                out = text[len(text)-limit-1] + out
                limit += 1
            if k - kpr/2 != 0 and (numtype == 3 or numtype == 4): # modifies output string based on notation decor
                if numtype == 4:
                    out = ' ' + out
                out = ktext[0][0][num] + out
            if num == 1:
                out = ' ' + out + 'illion'
        elif numtype == 2: #finalizes notation 11
            limit = 0
            while len(text) > limit:
                if (limit+1)%3 == 0:
                    out = text[limit] + type2suffix[(limit+1)//3] + out
                else:
                    out = text[limit] + out
                limit += 1
    return out
        
def get_digit(integer, digit, width):
    if width <= 0:
        print("Width must be a positive integer!")
        return
    return (integer // 10**digit) % 10**width # digit == 0 will return the ones place, width == 1 returns 1 digit.

def is_infinite(num):
    if num > sys.float_info.max: # The largest number floats can be, AKA 1e308
        return True
    else:
        return False

def infinityOverflowII(inp: list): #Used in tetration
    corrected_inp = []
    for variable in inp:
        arg1, arg2 = infinityOverflow(variable)
        corrected_inp.append([arg1, arg2])
    #index base expn exp2...
    #    0 arg1 arg2
    #    1      arg1 arg2
    #    2           arg1...
    #    .                .
    #    .                    .
    #    .                        .
    var = corrected_inp[0][0]
    vark = []
    for exponent in range(len(corrected_inp)):
        if exponent == 0:
            continue
        vark.append(corrected_inp[exponent-1][1] + corrected_inp[exponent][0])
        if exponent+1 == len(corrected_inp):
            vark.append(corrected_inp[exponent][1])
    print(vark)
    return var, vark
    
def infinityOverflow(inp: int):
    var = abs(inp)
    if var > 0:
        vard = int(math.log10(var))
        var = var / 10**vard * 10**(vard%3)
        vark = vard//3
    else:
        vark = 0
    if inp < 0:
        var *= -1
    if round(var, 6) % 1 == 0:
        var = int(var)
    return var, vark

def notatizeII(integer: int, intk: list, notation): #Used in tetration
    if notation == 0 or notation == 2 or notation == 3 or notation == 6 or notation == 9 or notation == 10:
        cursor = 0
        if notation == 0 or notation == 3 or notation == 9 or notation == 10:
            while integer >= 10:
                integer /= 10
                intk[0] += 1
            intk[cursor] *= 3
            while cursor <= len(intk)-1:
                while intk[cursor] >= 10:
                    intk[cursor] -= 10
                    try:
                        intk[cursor+1] += 1
                    except IndexError:
                        intk.append(1)
                cursor += 1
            output = str(integer)
            cursor = 0
            while cursor <= len(intk)-1:
                if notation == 0 or notation == 6:
                    if intk[cursor] != 0:
                        output += '×10^(' + str(round(intk[cursor], 3))
                    elif cursor != len(intk)-2:
                        output += '×10^('
                elif notation == 2 or notation == 3 or notation == 9:
                    if intk[cursor] != 0:
                        output += 'e' + str(round(intk[cursor], 3))
                    elif cursor != len(intk)-2:
                        output += 'e'
                elif notation == 10:
                    if intk[cursor] != 0:
                        output += 'e^' + str(round(intk[cursor], 3))
                    elif cursor != len(intk)-2:
                        output += 'e^'
                cursor += 1
            while cursor > 0 and notation == 0 or notation == 6:
                output += ')'
                cursor -= 1
    elif notation in [-1, 1, 4, 5, 7, 8, 11, 12, 13]:
        output = str(integer)
        cursor = 0
        while cursor <= len(intk)-1:
            if notation != 8:
                if intk[cursor] != 0:
                    output += ' k' + str(round(intk[cursor], 3))
                elif cursor != len(intk)-2:
                    output += ' k'
                cursor += 1
            else:
                if intk[cursor] != 0:
                    output += '×1000^(' + str(round(intk[cursor], 3))
                elif cursor != len(intk)-2:
                    output += '×1000^('
                cursor += 1
            if notation == 8:
                while cursor > 0:
                    output += ')'
                    cursor -= 1
    return output
                
def notatize(integer:int, intk:int, notation):
    intt = 0
    suffix = ''
    if intk >= 1:
        if notation == 0:
            while abs(integer) >= 10:
                integer /= 10
                intt += 1
            integer = round(integer, 3)
            suffix = '×10^' + str(intk*3 + intt)
        if notation == -1 or notation == 1 or notation == 7 or notation == 11 or notation == 12 or notation == 13:    
            suffix = numbuild(intk, notation)
        if notation == 2:
            suffix = 'e+' + str(intk*3)
        if notation == 3:
            while abs(integer) >= 10:
                integer /= 10
                intt += 1
            integer = round(integer, 3)
            suffix = 'e+' + str(intk*3 + intt)
        if notation == 4:
            suffix = 'k+' + str(intk)
        if notation == 5:
            if intk >= 2:
                suffix = ' ' + str(intk-1) + '-illion'
            else:
                integer *= 1000
        if notation == 6:
            suffix = '×10^' + str(intk*3)
        if notation == 8:
            suffix = '×1000^' + str(intk)
        if notation == 9 or notation == 14:
            suffix = 'e'
            significand = round(math.log10(integer) + intk * 3, 3)
            if notation == 14:
                hyper = 1
                while significand >= 10:
                    significand = round(math.log10(significand), 3)
                    hyper += 1
                if hyper > 1:
                    hyper = '#{}'.format(hyper)
                else:
                    hyper = ''
                suffix += str(significand) + hyper
            elif notation == 9:
                suffix += str(significand)
        if notation == 10:
            suffix = 'e^' + str(round(math.log(integer) + (intk * math.log(1000)), 3))
    if notation != 9 and notation != 10 and notation != 14:
        output = str(round(integer, 3)) + suffix
    if notation == 9 or notation == 10 or notation == 14:
        if suffix != '':
            output = suffix
        else:
            output = str(round(integer, 3))
    return output

def number_cronch(inp, userid, *inpk):
    if not isinstance(userid, tuple):
        userid = (userid,);
    if len(userid) == 0 or userid == None:
        notation = 0
    else:
        data = FileHandler.get_user_data(userid[0])
        notation = data.notation()
    if len(inpk) == 0 or inpk == None:
        inpk = 0
    else:
        inpk = inpk[0]
    if isinstance(inp, list):
        inf_crunch = infinityOverflowII(inp)
        notat = notatizeII(inf_crunch[0], inf_crunch[1], notation)
    else:
        inf_crunch = infinityOverflow(inp)
        notat = notatize(inf_crunch[0], inf_crunch[1]+inpk, notation)
    return notat
