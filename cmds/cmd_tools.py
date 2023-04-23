import asyncio
from discord.ext import commands
import discord
import traceback
from os.path import isdir,exists
from datetime import *
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.expol import expol
from util.SLHandle import *
from util.PlayerDataHandler import *
from util.GuildDataHandler import *
from util.ToolsUtil import *
from util.ColorUtil import rectColor
from util.cmdutil import cmdutil
text = cmdutil()

def commandList():
    return [calc, tempcalc, speedcalc, timecalc]

def categoryDescription():
    return "Useful, helpful commands."


@commands.command(aliases=['cal', 'calculate', 'calculator'])
async def calc(ctx, *funct):
    """Calculates equations.

Operations:
    Addition: +
    Subtraction: -
    Multiplication: ×, x, *
    Division: /, ÷
    Floor Div: //, floor, fdiv
    Ceiling Div: ceil, ceiling, cdiv
    Rounding: rnd, round
    Modulo: %, mod
    Exponent: ^, **, exp
    Root: root, √
    Square root: sqrt
    Log to arbitrary base: log(base)
    Natural Log: ln
    Log10: ld
    Multiplication by ten raised to a power: E, ×10^
    Multiplication by one thousand raised to a power: K, ×1000^
    Tetration: ^^, ***, tet

Variables:
    Golden Ratio: phi, φ, ϕ, Φ = 1.61803399
    Euler's Number: e          = 2.71828183
    Pi: pi, π, Π               = 3.14159265
    Tau: tau, τ, Τ, T          = 6.28318530

Fractions:
    One tenth: ⅒               = 0.1
    One ninth: ⅑               = 0.11111111
    One eighth: ⅛              = 0.125
    One seventh: ⅐             = 0.14285714
    One sixth: ⅙               = 0.16666667
    One fifth: ⅕               = 0.2
    One fourth: ¼              = 0.25
    One third: ⅓               = 0.33333333
    Three eighths: ⅜           = 0.375
    Two fifths: ⅖              = 0.4
    One half: ½                = 0.5
    Three fifths: ⅗            = 0.6
    Five eighths: ⅝            = 0.625
    Two thirds: ⅔              = 0.66666667
    Three fourths: ¾           = 0.75
    Four fifths: ⅘             = 0.8
    Five sixths: ⅚             = 0.83333333
    Seven eighths: ⅞           = 0.875
"""
    await ctx.send(calculatorFunct(ctx.author, "".join(funct)))

@commands.command()
async def tempcalc(ctx, value, scale="K"):
    """Translates temperatures!
Scales:
    Fahrenheit:         F, °F               68°F
    Celsius:            C, °C               20°C
    Kelvin:             K, °K              293K (I know °K is wrong, this is merely idiot-proofing)
    Delisle:            De, °De            120°De
    Newton:             N, °N                6.6°N
    Rankine:            R, °R              527.67°R
    Réaumur:            Re, Ré, °Re, °Ré    16°Ré
    Rømer:              Ro, Rø, °Ro, °Rø    18°Rø
    Urist:              U, °U           10,036°U
    Joule Point Energy: J, Jpe               4.045SxþJpe
    Electron Volt:      eV                   0.025eV"""

    scales = [["F", "°F"], ["C", "°C"], ["K", "°K"],
              ["De", "°De"], ["N", "°N"], ["R", "°R"],
              ["Re", "°Re", "Ré", "°Ré"], ["Ro", "°Ro", "Rø", "°Rø"],
              ["U", "°U"], ["J", "Jpe"], ["eV"]]
    stateChanges = { #ionizing point in eV instead of K
        "H": [14.01, 20.3, 13.598],
        "He": [0, 4.2, 24.587],
        "Li": [453.7, 1603, 5.391],
        "Be": [1570, 2742, 9.322],
        "B": [2348, 4200, 8.298],
        "C": [3823, 4300, 11.26],
        "N": [63.1, 77.4, 14.534],
        "O": [54.8, 90.2, 13.618],
        "F": [53.5, 85, 17.422],
        "Ne": [24.6, 27.1, 21.564],
        "Na": [370.9, 1156.1, 5.139],
        "Mg": [923, 1363, 7.646],
        "Al": [933.5, 2743, 5.985],
        "Si": [1687, 3538, 8.151],
        "P": [317.3, 553.7, 10.486],
        "S": [388.4, 717.8, 10.36],
        "Cl": [171.6, 239.1, 12.967],
        "Ar": [83.8, 87.3, 15.759],
        "K": [336.5, 1032, 4.34],
        "Ca": [1115, 1757, 6.113],
        "Sc": [1814, 3109, 6.561],
        "Ti": [1941, 3560, 6.828],
        "V": [2183, 3680, 6.746],
        "Cr": [2180, 2944, 6.766],
        "Mn": [1519, 2334, 7.434],
        "Fe": [1811, 3134, 7.902],
        "Co": [1768, 3200, 7.881],
        "Ni": [1728, 3003, 7.639],
        "Cu": [1357, 2835, 7.726],
        "Zn": [692.7, 1180, 9.394],
        "Ga": [302.9, 2673, 5.999],
        "Ge": [1211.4, 3106, 7.9],
        "As": [887, 1090, 9.815],
        "Se": [494, 958, 9.752],
        "Br": [265.8, 332, 11.813],
        "Kr": [115.8, 119.9, 13.999],
        "Rb": [312.5, 961, 4.177],
        "Sr": [1050, 1650, 5.694],
        "Y": [1799, 3203, 6.217],
        "Zr": [2128, 4650, 6.633],
        "Nb": [2750, 5017, 6.758],
        "Mo": [2896, 4912, 7.092],
        "Tc": [2430, 4538, 7.28],
        "Ru": [2607, 4423, 7.36],
        "Rh": [2237, 3968, 7.458],
        "Pd": [1828.1, 3236, 8.336],
        "Ag": [1234.9, 2435, 7.576],
        "Cd": [594.2, 1040, 8.993],
        "In": [429.8, 2345, 5.786],
        "Sn": [505.1, 2875, 7.343],
        "Sb": [903.8, 1908, 8.64],
        "Te": [722.6, 1261, 9.009],
        "I": [386, 457.4, 10.451],
        "Xe": [161.3, 165.1, 12.129],
        "Cs": [301.6, 944, 3.893],
        "Ba": [1000, 2118, 5.211],
        "La": [1193, 3737, 5.577],
        "Ce": [1071, 3716, 5.538],
        "Pr": [1204, 3403, 5.464],
        "Nd": [1294, 3347, 5.525],
        "Pm": [1373, 3273, 5.55],
        "Sm": [1345, 2173, 5.643],
        "Eu": [1095, 1802, 5.67],
        "Gd": [1568, 3273, 6.15],
        "Tb": [1629, 3396, 5.893],
        "Dy": [1685, 2840, 5.938],
        "Ho": [1747, 2873, 6.021],
        "Er": [1770, 3141, 6.107],
        "Tm": [1818, 2223, 6.184],
        "Yb": [1092, 1469, 6.254],
        "Lu": [1936, 3675, 5.425],
        "Hf": [2506, 4876, 6.825],
        "Ta": [3290, 5731, 7.89],
        "W": [3695, 6203, 7.98],
        "Re": [3459, 5903, 7.88],
        "Os": [3306, 5285, 8.7],
        "Ir": [2739, 4403, 9.1],
        "Pt": [2041.4, 4098, 9],
        "Au": [1337.3, 3243, 9.225],
        "Hg": [234.3, 629.9, 10.437],
        "Tl": [577, 1746, 6.108],
        "Pb": [600.6, 2022, 7.416],
        "Bi": [544.4, 1837, 7.289],
        "Po": [527, 1235, 8.416],
        "At": [575, 610.1, 9.5],
        "Rn": [202, 211.5, 10.748],
        "Fr": [300, 890, 3.94],
        "Ra": [973, 2010, 5.278],
        "Ac": [1323, 3500, 5.17],
        "Th": [2023, 5061, 6.08],
        "Pa": [1845, 4300, 5.89],
        "U": [1408, 4404, 6.194],
        "Np": [917, 4447, 6.265],
        "Pu": [913, 3505, 6.06],
        "Am": [1449, 2880, 5.993],
        "Cm": [1618, 3383, 6.02],
        "Bk": [1323, 2900, 6.23],
        "Cf": [1173, 1743, 6.3],
        "Es": [1133, 1269, 6.42],
        "Fm": [1800, 3000, 6.5], #poor estimation of BP
        "Md": [1100, 2000, 6.58], #poor estimation of BP
        "No": [1100, 2000, 6.65], #poor estimation of BP
        "Lr": [1900, 3000, 6.5], #poor estimation of BP, IP
        "Rf": [2400, 5800, 6.011],
        "Db": [3500, 6000, 6.892], #poor estimation of MP, BP
        "Sg": [4400, 6400, 7.845], #poor estimation of MP, BP
        "Bh": [4400, 5630, 7.669], #poor estimation of MP, BP
        "Hs": [3800, 5012, 7.565], #poor estimation of MP, BP
        "Mt": [3100, 4130, 8.291], #poor estimation of MP, BP
        "Ds": [2200, 3825, 9.949], #poor estimation of MP, BP
        "Rg": [1300, 2970, 10.571], #poor estimation of MP, BP
        "Cn": [283, 340, 11.97],
        "Nh": [700, 1430, 4.508],
        "Fl": [200, 380, 8.625],
        "Mc": [670, 1400, 5.579],
        "Lv": [708.5, 1085, 6.88],
        "Ts": [723, 883, 7.699],
        "Og": [325, 350, 8.914],
        "Uue": [288, 903, 4.799],
        "Ubn": [953, 1973, 5.838],
        "Ubu": [1600, 3300, 2.680], #poor estimation of MP, BP
        "Ubb": [3100, 6200, 3.401] #poor estimation of MP, BP
        }
    MELTING_POINT = 0
    BOILING_POINT = 1
    IONIZING_POINT = 2
    
    value = expol(value)

    #Account for variations
    devariated = False
    for s in scales:
        for t in s:
            if scale.lower() == t.lower():
                scale = s[0]
                devariated = True
                break
        if devariated: break

    #Convert to kelvins
    if scale == "F": kValue = (value + 459.67) * (5/9)
    elif scale == "C": kValue = value + 273.15
    elif scale == "K": kValue = value
    elif scale == "De": kValue = expol(373.15) - value * (2/3)
    elif scale == "N": kValue = value * (100/33) + 273.15
    elif scale == "R": kValue = value * (5/9)
    elif scale == "Re": kValue = value * (5/4) + 273.15
    elif scale == "Ro": kValue = (value - 7.5) * (40/21) + 273.15
    elif scale == "U": kValue = (value - 9508.33) * (5/9)
    elif scale == "J": kValue = value * expol([7.243,22])
    elif scale == "eV": kValue = value * 11604.525
    else: scale = "K"; kValue = value #if some invalid scale is passed in, default to Kelvin

    #Convert to all scales
    fValue = kValue * (9/5) - 459.67
    cValue = kValue - 273.15
    deValue = (expol(373.15) - kValue) * (3/2)
    nValue = (kValue - 273.15) * (33/100)
    rValue = kValue * (9/5)
    reValue = (kValue - 273.15) * (4/5)
    roValue = (kValue - 273.15) * (21/40) + 7.5
    uValue = kValue * (9/5) + 9508.33
    jValue = kValue / expol([7.243,22])
    evValue = kValue / 11604.525

    scaleConvStr = f"\
**`Fahrenheit:`**`          {fValue:{GetNotationCode(ctx.author)}}°F`\n\
**`Celsius:`**`             {cValue:{GetNotationCode(ctx.author)}}°C`\n\
**`Kelvin:`**`              {kValue:{GetNotationCode(ctx.author)}}K`\n\
**`Delisle:`**`             {deValue:{GetNotationCode(ctx.author)}}°De`\n\
**`Newton:`**`              {nValue:{GetNotationCode(ctx.author)}}°N`\n\
**`Rankine:`**`             {rValue:{GetNotationCode(ctx.author)}}°R`\n\
**`Réaumur:`**`             {reValue:{GetNotationCode(ctx.author)}}°Ré`\n\
**`Rømer:`**`               {roValue:{GetNotationCode(ctx.author)}}°Rø`\n\
**`Urist:`**`               {uValue:{GetNotationCode(ctx.author)}}°U`\n\
**`Joule Point Energy:`**`  {jValue:{GetNotationCode(ctx.author)}}Jpe`\n\
**`Electron Volt:`**`       {evValue:{GetNotationCode(ctx.author)}}eV`"

    #Periodic Table
    if kValue < 2000000000000:
        el = {}
        for element in stateChanges:
            if type(stateChanges[element][IONIZING_POINT]) in [int, float, expol]:
                stateChanges[element][IONIZING_POINT] *= 11604.525
            if kValue < stateChanges[element][MELTING_POINT]: el[element] = "sld "
            elif kValue == stateChanges[element][MELTING_POINT]: el[element] = "melt"
            elif stateChanges[element][MELTING_POINT] == kValue == stateChanges[element][BOILING_POINT]: el[element] = "subl"
            elif stateChanges[element][MELTING_POINT] < kValue < stateChanges[element][BOILING_POINT]: el[element] = "liq "
            elif kValue == stateChanges[element][BOILING_POINT]: el[element] = "boil"
            elif stateChanges[element][BOILING_POINT] < kValue < stateChanges[element][IONIZING_POINT]: el[element] = "gas "
            elif kValue == stateChanges[element][IONIZING_POINT]: el[element] = "ionz"
            elif stateChanges[element][IONIZING_POINT] < kValue: el[element] = "pls "
            elif stateChanges[element][MELTING_POINT] == "undef": el[element] = "??? "
            elif stateChanges[element][BOILING_POINT] == "undef": el[element] = "??? "
            elif stateChanges[element][IONIZING_POINT] == "undef": el[element] = "??? "

        pt1 = f"**` H                                                                   He \n\
{el['H']}                                                                {el['He']}\n\
 Li  Be                                          B   C   N   O   F   Ne \n\
{el['Li']}{el['Be']}                                        {el['B']}{el['C']}{el['N']}{el['O']}{el['F']}{el['Ne']}\n\
 Na  Mg                                          Al  Si  P   S   Cl  Ar \n\
{el['Na']}{el['Mg']}                                        {el['Al']}{el['Si']}{el['P']}{el['S']}{el['Cl']}{el['Ar']}\n\
 K   Ca  Sc  Ti  V   Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr \n\
{el['K']}{el['Ca']}{el['Sc']}{el['Ti']}{el['V']}{el['Cr']}{el['Mn']}{el['Fe']}{el['Co']}{el['Ni']}{el['Cu']}{el['Zn']}{el['Ga']}\
{el['Ge']}{el['As']}{el['Se']}{el['Br']}{el['Kr']}\n\
 Rb  Sr  Y   Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te  I   Xe \n\
{el['Rb']}{el['Sr']}{el['Y']}{el['Zr']}{el['Nb']}{el['Mo']}{el['Tc']}{el['Ru']}{el['Rh']}{el['Pd']}{el['Ag']}{el['Cd']}{el['In']}\
{el['Sn']}{el['Sb']}{el['Te']}{el['I']}{el['Xe']}`**"
        pt2 = f"` Cs  Ba  La  Hf  Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn `"
        pt3 = f"**`{el['Cs']}{el['Ba']}{el['La']}{el['Hf']}{el['Ta']}{el['W']}{el['Re']}{el['Os']}{el['Ir']}{el['Pt']}{el['Au']}{el['Hg']}\
{el['Tl']}{el['Pb']}{el['Bi']}{el['Po']}{el['At']}{el['Rn']}\n\
 Fr  Ra  Ac  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Nh  Fl  Mc  Lv  Ts  Og \n\
{el['Fr']}{el['Ra']}{el['Ac']}{el['Rf']}{el['Db']}{el['Sg']}{el['Bh']}{el['Hs']}{el['Mt']}{el['Ds']}{el['Rg']}{el['Cn']}{el['Nh']}\
{el['Fl']}{el['Mc']}{el['Lv']}{el['Ts']}{el['Og']}\n\
Uue Ubn Ubu \n\
{el['Uue']}{el['Ubn']}{el['Ubu']}\n\
         Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu \n\
        {el['Ce']}{el['Pr']}{el['Nd']}{el['Pm']}{el['Sm']}{el['Eu']}\
{el['Gd']}{el['Tb']}{el['Dy']}{el['Ho']}{el['Er']}{el['Tm']}{el['Yb']}{el['Lu']}\n\
         Th  Pa  U   Np  Pu  Am  Cm  Bk  Cf  Es  Fm  Md  No  Lr \n\
        {el['Th']}{el['Pa']}{el['U']}{el['Np']}{el['Pu']}{el['Am']}\
{el['Cm']}{el['Bk']}{el['Cf']}{el['Es']}{el['Fm']}{el['Md']}{el['No']}{el['Lr']}\n\
        Ubb \n\
        {el['Ubb']}`**"
    elif kValue == 2000000000000: pt1 = "**`            * Fermi melting point *              \nThe 'boiling point' of atomic nuclei into quarks.`**"
    elif 2000000000000 < kValue < expol([1.42,32]): pt1 = "**`* Quark-gluon plasma *`**"
    elif kValue == expol([1.42,32]): pt1 = "**`       * Planck Temperature *          \nThe maximum temperature that can exist.\n    Wavelength of one Planck Length.   `**"
    elif kValue > expol([1.42,32]): pt1 = "**`                    * Kugelblitz *                       \nBlack hole formed from extreme electromagnetic radiation.`**"

    embed = discord.Embed(title=f"Temperature Calculator: {value:{GetNotationCode(ctx.author)}}{scale}", color=rectColor(PlayerdataGetFileIndex(ctx.author, "settings.json", "Color")))
    embed.add_field(name="Scales", value=scaleConvStr, inline=False)
    embed.add_field(name="Elements", value=pt1, inline=False)
    if kValue < 2000000000000: embed.add_field(name=pt2, value=pt3, inline=False)
    await ctx.send(embed=embed)

@commands.command(aliases=['spdcalc', 'spdcalculate', 'spdcalculator', 'speedcalculate', 'speedcalculator'])
async def speedcalc(ctx, speed: float, mode="short"):
    """Calculates speed! Input m/s. Mode 'long' unabbreviates everything."""
    mode = str.lower(mode)
    metric = speed
    us = speed / 0.9144
    mach = speed / 340.3
    LIGHTSPEED = 299792458
    LIGHTYEAR = LIGHTSPEED * 86400 * 365.25
    c = speed / LIGHTSPEED
    wf = c**(1/3)
    perspective = {1: 'cross one meter', 24: 'cross a suburban lawn', 1100: 'travel one city block',
                   30000: 'cross a large city', 1400000: 'traverse the N/S length of the UK', 10800000: 'cross the width of Eurasia',
                   40000000: 'circumnavigate the Earth', 384500000: 'fly to Luna from Earth', 149500000000: 'fly to Sol from Earth',
                   778000000000: 'fly to Jupiter from Sol', 5000000000000: 'fly to Pluto from Sol', 9460*1000**4: 'travel one light year',
                   4.244*LIGHTYEAR: 'travel to Alpha Centauri C', 100000*LIGHTYEAR: 'travel across the Milky Way Galaxy',
                   2500000*LIGHTYEAR: 'travel to the Andromeda Galaxy', 53800000*LIGHTYEAR: 'travel to the Virgo Cluster',
                   500000000*LIGHTYEAR: 'travel across the Laniakea Supercluster', 1000**3*LIGHTYEAR: 'travel to the Sloan Great Wall',
                   440*1000**8: 'travel to the edge of the observable universe', 1000**9: 'travel to the edge of the universe',
                   6.25*1000**11: 'cross one multiverse', 22.456*1000**12: 'cross one metaverse', 512*1000**12: 'traverse the Core and reach the Inner Rim',
                   25.41*1000**13: 'reach the Middle Rim', 631.56*1000**13: 'reach the Outer Rim', 1000**14: 'cross from Red Reality into the eternal void'}
##    metric_name = ['dc', 'n', 'o', 'sp', 'sx', 'qi', 'qa', 't', 'b', 'm', 'þ', '', 'Þ', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'O', 'N', 'Dc',
##                   'UDc', 'DDc', 'TDc', 'QaDc', 'QiDc', 'SxDc', 'SpDc', 'ODc', 'NDc', 'Vg', ]
##    metric_name_long = ['Decia', 'Nonia', 'Octia', 'Septia', 'Sextia', 'Quintia', 'Quadria', 'Tria', 'Bia', 'Mia', 'Thousia', '',
##                        'Thousia', 'Mia', 'Bia', 'Tria', 'Quadria', 'Quintia', 'Sextia', 'Septia', 'Octia', 'Nonia', 'Decia',
##                        'Undecia', 'Duodecia', 'Tredecia', 'Quattordecia', 'Quindecia',
##                        'Sexdecia', 'Septendecia', 'Octodecia', 'Novemdecia', 'Vigintia']
    metric_name = ['v', 'q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'µ', 'm', '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q', 'V',
                   'UDc ', 'DDc ', 'TDc ', 'QaDc ', 'QiDc ', 'SxDc ', 'SpDc ', 'ODc ', 'NDc ', 'Vg ', ]
    metric_name_long = ['Vendeko', 'Quecto', 'Ronto', 'Yocto', 'Zepto', 'Atto', 'Femto', 'Pico', 'Nano', 'Micro', 'Milli', '',
                        'Kilo', 'Mega', 'Giga', 'Tera', 'Peta', 'Exa', 'Zetta', 'Yotta', 'Ronna', 'Quetta', 'Vendeka',
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
    if mode == "short":
        metric_out = 'Metric: {0} {1}m/sec\n'.format(round(metric, 3), metric_name[metric_name_marker])
    elif mode == "long":
        metric_out = 'Metric: {0} {1}Meters per Second\n'.format(round(metric, 3), metric_name_long[metric_name_marker])
    times = ['sec', 'min', 'hr', 'dy', 'mo', 'yr']
    times_long = ['Seconds', 'Minutes', 'Hours', 'Days', 'Months', 'Years']
    time_marker = 0
    time_out = ''
    clock_out = 2
    overflow = False
    #calculate perspective speed
    for length in perspective:
        if speed < length: #can cross in more than a second
            time = length / speed
            if time > 60: #more than a minute
                time /= 60
                time_marker = 1
                if time > 60: #more than an hour
                    time /= 60
                    time_marker = 2
                    if time > 24: #more than a day
                        time /= 24
                        time_marker = 3
                        if time > 30.4167: #more than the average month
                            time /= 30.4167
                            time_marker = 4
                            if time > 12: #more than a year
                                time /= 12
                                time_marker = 5
                                time_metric = met_orig
                                overflow = True
                                while time >= 1000 and time_metric <= len(metric_name)-2: #deep time
                                    time /= 1000
                                    time_metric += 1
                                time = round(time, 3)
                                if mode == "short":
                                    time_out += '\nAt this speed, an object could ' + perspective[length] + ' in {0}{1}{2}'.format(time, metric_name[time_metric], times[time_marker])
                                elif mode == "long":
                                    time_out += '\nAt this speed, an object could ' + perspective[length] + ' in {0} {1}{2}'.format(time, metric_name_long[time_metric], times_long[time_marker])
            time = round(time, 3)
            if overflow == False:
                if mode == "short":
                    time_out += '\nAt this speed, an object could ' + perspective[length] + ' in {0}{1}'.format(time, times[time_marker])
                elif mode == "long":
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
                                        if mode == 'short':
                                            us_out = 'US Custom: {0} {1}{2}/sec\n'.format(round(us, 3), metric_name[us_metric_marker], us_name[us_name_marker])
                                        elif mode == 'long':
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
        if mode == "short":
            us_out = 'US Custom: {0} {1}/sec\n'.format(round(us, 3), us_name[us_name_marker])
        elif mode == "long":
            us_out = 'US Custom: {0} {1} per Second\n'.format(round(us, 3), us_name_long[us_name_marker])

    #calculate mach speed
    mach_metric_marker = met_orig
    while mach >= 1000 and mach_metric_marker <= len(metric_name)-2:
        mach /= 1000
        mach_metric_marker += 1
    while mach < 1 and mach_metric_marker > 0:
        mach *= 1000
        mach_metric_marker -= 1
    if mode == 'short':
        mach_out = 'Machspeed: {0}Ma {1}\n'.format(metric_name[mach_metric_marker], round(mach, 3))
    elif mode == 'long':
        mach_out = 'Machspeed: {0}Mach {1}\n'.format(metric_name_long[mach_metric_marker], round(mach, 3))

    #calculate lightspeed
    c_metric_marker = met_orig
    while c >= 1000 and c_metric_marker <= len(metric_name)-2:
        c /= 1000
        c_metric_marker += 1
    while c < 1 and c_metric_marker > 0:
        c *= 1000
        c_metric_marker -= 1
    if mode == 'short':
        c_out = 'Lightspeed: {0} {1}c\n'.format(round(c, 3), metric_name[c_metric_marker])
    elif mode == 'long':
        c_out = 'Lightspeed: {0} {1}Celeritas\n'.format(round(c, 3), metric_name_long[c_metric_marker])

    #calculate warp factor
    wf_metric_marker = met_orig
    while wf >= 1000 and wf_metric_marker <= len(metric_name)-2:
        wf /= 1000
        wf_metric_marker += 1
    while wf < 1 and wf_metric_marker > 0:
        wf *= 1000
        wf_metric_marker -= 1
    if mode == 'short':
        wf_out = 'Warp Factor: {0}wf {1}\n'.format(metric_name[wf_metric_marker], round(wf, 3))
    elif mode == 'long':
        wf_out = 'Warp Factor: {0}Warp {1}\n'.format(metric_name_long[wf_metric_marker], round(wf, 3))

    out = metric_out + us_out + mach_out + c_out + wf_out + time_out
    await ctx.send(out)


@commands.command(aliases=['timecalculate', 'timecalculator'])
async def timecalc(ctx, mode: str, value: float, unit: str):
    """Add or subtract time from the current timestamp.
Due to limits with datetime, units smaller than the second cannot be parsed."""
    unitmap = {
        "s": 1,
        "sec": 1,
        "second": 1,
        "seconds": 1,
        "Ds": 10, # 10 seconds
        "Dsec": 10,
        "dekasecond": 10,
        "dekaseconds": 10,
        "min": 60,
        "minute": 60,
        "minutes": 60,
        "hs": 100, # 100 seconds, 1 min 40 s
        "hsec": 100,
        "hectosecond": 100,
        "hectoseconds": 100,
        "ks": 1000, # 1000 seconds, 16 min 40 s
        "ksec": 1000,
        "kilosecond": 1000,
        "kiloseconds": 1000,
        "hr": 3600,
        "hour": 3600,
        "hours": 3600,
        "dy": 86400,
        "day": 86400,
        "days": 86400,
        "sol": 88775, # martian day, 24 hr 39 min 35 s
        "sols": 88775,
        "wk": 604800, # 7 dy
        "week": 604800,
        "weeks": 604800,
        "Ms": 1000000, # 1 million seconds, 11 dy 13 hr
        "Msec": 1000000,
        "megasecond": 1000000,
        "megaseconds": 1000000,
        "fn": 1209600, # 2 wk or 14 d
        "fortnight": 1209600,
        "fortnights": 1209600,
        "fortnite": 1209600, #included because damn kids think the length of time is the name of that damn game
        "fortnites": 1209600,
        "lmo": 2419200, # lunar month, 4 wk or 28 dy
        "lune": 2419200,
        "lunes": 2419200,
        "mo": 2629746, # ideal month, 30 dy 10 hr
        "month": 2629746,
        "months": 2629746,
        "yr": 31556952, # ideal year, 365 dy 5 hr
        "year": 31556952,
        "years": 31556952,
        "decade": 315569520, # 10 years
        "decades": 315569520,
        "gen": 631139040, # 20 years
        "generation": 631139040,
        "generations": 631139040,
        "score": 631139040,
        "scores": 631139040,
        "Gs": 1000000000, # 1 billion seconds, 31 yr 8 mo 8 dy
        "Gsec": 1000000000,
        "gigasecond": 1000000000,
        "gigaseconds": 1000000000,
        "life": 2524556160, # 4 gen or 80 yr
        "lives": 2524556160,
        "lifetime": 2524556160,
        "lifetimes": 2524556160
        }
    if mode in "+addplus":
        mode = 1
        state = "adding"
    elif mode in "-subtractminus":
        mode = -1
        state = "subtracting"
    combinedVal = value * unitmap[unit] * mode
    ts = int(ctx.message.created_at.replace(tzinfo=timezone.utc).timestamp())
    newts = int(ts + combinedVal)
    if combinedVal > 28800: formatcode = ""
    else: formatcode = ":t"
    out = f"Current datetime is <t:{ts}{formatcode}>.\n\
After {state} {value} {unit}, the datetime is <t:{newts}{formatcode}>.\n\
This is <t:{newts}:R>."
    await ctx.send(out)
