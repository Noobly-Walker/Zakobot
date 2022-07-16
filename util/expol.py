from math import log, ceil, floor
# Expol.PY is free to use.

MANTISSA = 0
EXPONENT = 1

class MemoryOverflowSafeguard(Exception):
    def __init__(self, length, message="this operation would require a dangerous amount of memory. This action has been cancelled."):
        self.length = length
        self.size = int(self.length*100//225)
        if self.size < 10**30:
            prefixes = ['', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa', 'zeta', 'yotta', 'bronto']
            index = min(int(log(self.size, 1000)), len(prefixes)-1)
            self.size /= 1000**index
            self.message = f"conversion from expol to int would require a dangerous amount of memory (est. {round(self.size,3)} {prefixes[index]}bytes). This action has been cancelled."
        else: self.message = message

        super().__init__(self.message)

class expol:
    def __init__(self, obj=None):
        """Converts variables into exponent lists.

expol(int) -> expol: expol(123)
expol(float) -> expol: expol(123.0)
expol(str) -> expol: expol("123"), expol("1.23e2"), expol("123.0"), expol("[123,0]"), expol("[1.23,0]")
expol([int|float, int]) -> expol: expol([123,0]), expol([1.23,0])
-------------------------------------------------------------------------------------------------------
String Formats:                 Examples:
e   - Engineering               1.23e45680
el  - Engineering Log-looped    1.23ee4.660
k   - Engineering K             123.000k15226
kl  - Engineering K Log-looped  123.000kk1.394
s   - Scientific                1.23×10^45680
sl  - Scientific Log-looped     1.23×10^10^4.660
sk  - Scientific K              123.000×1000^15226
skl - Scientific K Log-looped   123.000×1000^1000^1.394
i   - Illions                   123.000 QuinVigintDucent-QuinMyrMillillion
is  - Illions Shorthand         123.000 QiVgDc-QimMyMl
li  - Long Illions              <not implemented>
l   - Logarithmic               <not implemented>

.   - Round to Nth decimal place
,   - Insert thousands separators
%   - Append percent sign"""
        self.value = [0,0]
        if obj != None:
            if type(obj) == str:
                #Case 1: Stringified exponent
                values = obj.split('e')
                if len(values) == 2:
                    if values[0] == '': values[0] = 1 #e0 = 1
                    else: raise TypeError(f"Invalid string value '{values[0]}' passed in.")
                    if values[1] == '': values[1] = 0 #8e = 8
                    else: raise TypeError(f"Invalid string value '{values[1]}' passed in.")
                    self.value = [values[0], values[1]]
                else:
                    evaldStr = eval(obj)
                    #Case 2: Stringified list
                    if type(evaldStr) == list:
                        if len(evaldStr) == 2:
                            if type(evaldStr[0]) in [float, int] and type(evaldStr[1]) == int: self.value = evaldStr
                            else: #going to find out which one was the wrong type
                                if type(evaldStr[0]) not in [float, int]: raise TypeError(f"index 0: expected int or float, but got {type(evaldStr[0])}")
                                if type(evaldStr[1]) not in [int]: raise TypeError(f"index 1: expected int, but got {type(evaldStr[0])}")
                        else: raise IndexError(f"expol list takes 2 positional variables but {len(evaldStr)} were given")
                    #Cases 3 and 4: Stringified float or int
                    elif type(evaldStr) in [float, int]: self.value = self.expExtract(evaldStr)
                    else: raise ValueError(f"invalid literal for expol() with value '{obj}'")
            #Case 5: List
            elif type(obj) == list:
                if len(obj) == 2:
                    if type(obj[0]) in [float, int] and type(obj[1]) == int: self.value = obj
                    else: #going to find out which one was the wrong type
                        if type(obj[0]) not in [float, int]: raise TypeError(f"index 0: expected int or float, but got {type(obj[0])}")
                        if type(obj[1]) not in [int]: raise TypeError(f"index 1: expected int, but got {type(obj[0])}")
                else: raise IndexError(f"expol list takes 2 positional variables but {len(obj)} were given")
            #Cases 6 and 7: Float or int
            elif type(obj) in [float, int]: self.value = self.expExtract(obj)
            #Case 8: Expol
            elif type(obj) == expol: self.value = obj.value
            else: raise TypeError(f"expected int, float, list, or str, but got {type(obj[0])}")

    @property
    def mantissa(self):
        return self.value[MANTISSA]

    @property
    def exponent(self):
        return self.value[EXPONENT]
            
    def expExtract(self, variable): #Converts integers and double floating point numbers into exponent lists
        if type(variable) in [int, float]:
            if variable != 0:
                exponent = int(log(abs(variable),10))
                mantissa = variable / 10**exponent
                return self.expFixVar([mantissa, exponent])
            else: return [0,0]
        elif type(variable) == expol:
            return variable.value
        elif type(variable) == list:
            return variable

    def expFixVar(self, variable): #Corrals the mantissa between 1 and 10 and updates the exponent accordingly
        if variable[MANTISSA] != 0:
            while abs(variable[MANTISSA]) >= 10:
                variable[MANTISSA] /= 10
                variable[EXPONENT] += 1
            while abs(variable[0]) < 1:
                variable[MANTISSA] *= 10
                variable[EXPONENT] -= 1
        else:
            variable[EXPONENT] = 0
        return variable

    def __add__(self, addend): #Addition operation +
        var1 = self.value; var2 = self.expExtract(addend)
        expDiff = var1[EXPONENT] - var2[EXPONENT]
        if abs(expDiff) <= 50:
            if expDiff < 0: mantOut = var1[MANTISSA]*10**expDiff+var2[MANTISSA]
            elif expDiff >= 0: mantOut = var1[MANTISSA]+var2[MANTISSA]/10**expDiff
            expOut = max(var1[EXPONENT], var2[EXPONENT])
        #the following is to prevent float overflow due to attempting to add two numbers of incomparable size
        elif expDiff > 50: mantOut = var1[MANTISSA]; expOut = var1[EXPONENT]
        elif expDiff < -50: mantOut = var2[MANTISSA]; expOut = var2[EXPONENT]
        return expol(self.expFixVar([mantOut, expOut]))

    def __sub__(self, subtrahend): #Subtraction operation -
        var1 = self.value; var2 = self.expExtract(subtrahend)
        return self.__add__([var2[MANTISSA]*-1, var2[EXPONENT]])

    def __mul__(self, factor): #Multiplication operation *
        var1 = self.value; var2 = self.expExtract(factor)
        mantOut = var1[MANTISSA] * var2[MANTISSA]
        expOut = var1[EXPONENT] + var2[EXPONENT]
        return expol(self.expFixVar([mantOut, expOut]))

    def __truediv__(self, divisor): #Division operation /
        var1 = self.value; var2 = self.expExtract(divisor)
        return self.__mul__([1/var2[MANTISSA], -var2[EXPONENT]])

    def __floordiv__(self, divisor): #Floor division operation //
        quotient = self.__truediv__(self.expExtract(divisor))
        if abs(quotient.value[EXPONENT]) < 100: #if the number is too large, the ones place might not be saved anyway
            quotient.value[MANTISSA] = floor(quotient.value[MANTISSA]*10**quotient.value[EXPONENT])/10**quotient.value[EXPONENT]
        return expol(self.expFixVar(quotient.value))

    def __mod__(self, divisor): #Modulo division operation %
        quotient = self.__truediv__(self.expExtract(divisor))
        floor = self.__floordiv__(self.expExtract(divisor))
        return quotient - floor

    def __pow__(self, exponent): #Exponentiation operation **
        const = 13000000000
        var1 = self.value; var2 = expol(exponent)
        expOut = int(expol(var1).log10() * var2)
        mantOut = 10**((int(expol(var1).log10()*const * var2)%const)/const)
        return expol(self.expFixVar([mantOut, expOut]))

    def log10(self): #Log10 operation
        mant,exp = self.value
        return expol(log(mant, 10)+exp)

    def log(self, base:float): #Custom log operation
        mant,exp = self.value
        return expol(log(mant, base)+exp/log(base, 10))

    def __neg__(self): #Negate operation -expol
        return expol([self.value[MANTISSA]*-1,self.value[EXPONENT]])

    def __pos__(self): #Positive operation +expol
        return expol(self.value)

    def __abs__(self): #Absolute value operation
        if self.value[MANTISSA] < 0: return expol([self.value[MANTISSA]*-1,self.value[EXPONENT]])
        else: return expol(self.value)

    def compare(self, compared): #base function for comparisons
        try: compared = expol(compared)
        except (NameError, TypeError): return -2 #if it cannot be converted into expol, it cannot be compared, and thus cannot be equivalent
        val1, val2 = [x.value[EXPONENT] for x in (self, compared)]
        val3, val4 = [x.value[MANTISSA] for x in (self, compared)]
        if val1 > val2:
            if (val3 < 0 and val4 < 0) or (val3 > 0 and val4 > 0): return 0 #both are on the same side of 0, so the exponent was enough
            elif val3 <= 0 and val4 >= 0: return 2 #compared is negative, self is positive
            elif val3 >= 0 and val4 <= 0: return 0 #compared is positive, self is negative
        elif val1 < val2:
            if (val3 < 0 and val4 < 0) or (val3 > 0 and val4 > 0): return 2 #both are on the same side of 0, so the exponent was enough
            elif val3 <= 0 and val4 >= 0: return 2 #compared is negative, self is positive
            elif val3 >= 0 and val4 <= 0: return 0 #compared is positive, self is negative
        elif val1 == val2:
            if val3 > val4: return 0
            elif val3 == val4: return 1
            elif val3 < val4: return 2

    def __eq__(self, compared): #Equal comparison ==
        if self.compare(compared) == 1: return True
        else: return False

    def __ne__(self, compared): #Not equal comparison !=
        if self.compare(compared) != 1: return True
        else: return False

    def __gt__(self, compared): #Greater than comparison >
        if self.compare(compared) == 0: return True
        else: return False

    def __ge__(self, compared): #Greater or equal comparison >=
        if self.compare(compared) in [0,1]: return True
        else: return False

    def __lt__(self, compared): #Less than comparison <
        if self.compare(compared) == 2: return True
        else: return False

    def __le__(self, compared): #Less or equal comparison <=
        if self.compare(compared) in [1,2]: return True
        else: return False

    def __str__(self):#Conversion to string
        return f"{self.value[MANTISSA]}e{self.value[EXPONENT]}"

    def __format__(self, fmt): #String format codes
        mant = self.value[MANTISSA]; exp = self.value[EXPONENT]
        MANTISSA_ROUND = 10
        string = ""

        tier0long1 = ["Thousand","Million","Billion","Trillion","Quadrillion","Quintillion","Sextillion","Septillion","Octillion","Nonillion"]
        
        tier1long1 = ["","Un","Duo","Tre","Quattor","Quin","Sex","Septen","Octo","Novem"]
        tier1long2 = ["","Dec","Vigint","Trigint","Quadragint","Quinquagint","Sexagint","Septuagint","Octagint","Nonagint"]
        tier1long3 = ["","Cent","Ducent","Trecent","Quadringent","Quincent","Sescent","Septingent","Octingent","Nongent"]
        
        tier2long1 = ["","Mill","Dumill","Tremill","Quadrimill","Quinmill","Sextimill","Septimill","Octimill","Nonimill"]
        tier2long1b = ["","","Du","Tre","Quadri","Quin","Sexti","Septi","Octi","Noni"]
        tier2long2 = ["","Myr","Dumyr","Tremyr","Quadrimyr","Quinmyr","Sextimyr","Septimyr","Octimyr","Nonimyr"]
        tier2long3 = ["","Ce","Duce","Trece","Quadrice","Quince","Sextice","Septice","Octice","Nonice"]
        tier2long4 = ["","Mill","Micr","Nan","Pic","Femt","Att","Zept","Yoct","Xon"]
        tier2long4b = ["Ve","Me","Due","Trio","Tetre","Pente","Hexe","Hepte","Octe","Enne"]
        tier2long4c = ["","Me","Due","Trio","Tetre","Pente","Hexe","Hepte","Octe","Enne"]
        tier2long4d = ["","","Due","Trio","Tetre","Pente","Hexe","Hepte","Octe","Enne"]
        tier2long5 = ["","c","Icos","Triacont","Tetracont","Pentacont","Hexacont","Heptacont","Octacont","Ennacont"]
        tier2long6 = ["","Hect","Duehect","Triahect","Tetrahect","Pentahect","Hexahect","Heptahect","Octahect","Ennahect"]

        tier3long1 = ["","Kill","Meg","Gig","Ter","Pet","Ex","Zet","Yot","Xenn"]

        tier0short1 = ["k","M","B","T","Qa","Qi","Sx","Sp","O","N"]
        
        tier1short1 = ["","U","D","T","Qa","Qi","Sx","Sp","O","N"]
        tier1short2 = ["","Dc","Vg","Tg","Qag","Qig","Sxg","Spg","Og","Ng"]
        tier1short3 = ["","Ct","Dt","Tt","Qat","Qit","Sct","Spt","Ot","Nt"]
        
        tier2short1 = ["","Ml","Dl","Tl","Qal","Qil","Sxl","Spl","Ol","Nl"]
        tier2short1b = ["","","D","T","Qa","Qi","Sx","Sp","O","N"]
        tier2short2 = ["","My","Dy","Ty","Qay","Qiy","Sxy","Spy","Oy","Ny"]
        tier2short3 = ["","Ce","De","Te","Qae","Qie","Sxe","Spe","Oe","Ne"]
        tier2short4 = ["","Ml","Mc","Na","Pc","Fm","At","Zp","Yc","Xn"]
        tier2short4b = ["Ve","M","D","Tr","Te","P","Hx","Hp","O","E"]
        tier2short4c = ["","M","D","Tr","Te","P","Hx","Hp","O","E"]
        tier2short4d = ["","","D","Tr","Te","P","Hx","Hp","O","E"]
        tier2short5 = ["","","Ic","Trc","Tec","Pc","Hxc","Hpc","Oc","Ec"]
        tier2short6 = ["","Hct","Dct","Trct","Tect","Pct","Hxct","Hpct","Oct","Ect"]

        tier3short1 = ["","Kil","Meg","Gig","Ter","Pet","Ex","Zet","Yot","Xen"]

        illionsShortList = [
          [
            ["k","M","B","T","Qa","Qi","Sx","Sp","O","N"],
            ["","U","D","T","Qa","Qi","Sx","Sp","O","N"],
            ["","Dc","Vg","Tg","Qag","Qig","Sxg","Spg","Og","Ng"],
            ["","Ct","Dt","Tt","Qat","Qit","Sct","Spt","Ot","Nt"]
          ],
          [
            ["","Ml","Dl","Tl","Qal","Qil","Sxl","Spl","Ol","Nl"],
            ["","M","D","Tr","Te","P","Hx","Hp","O","E"],
            ["","Vc","Ic","Trc","Tec","Pc","Hxc","Hpc","Oc","Ec"],
            ["","Hct","Dct","Trct","Tect","Pct","Hxct","Hpct","Oct","Ect"]
          ],
          [
            ["","Kl","Mg","Gg","Tr","P","E","Z","Y","X"],
            ["","H","D","Tr","Te","P","E","Z","Y","N"],
            ["","Dk","Ik","Trk","Tek","Pk","Ek","Zk","Yk","Nk"],
            ["","Hot","Bot","Trot","Tot","Pot","Eot","Zot","Yot","Not"]
          ]
        ]

        def splitThou(number):
            number = f"{number:,}".split(",")
            return [int(n) for n in number]

        def parseIllionsShort(_tier, index, highest=True):
            out = ""
            revindex = str(index)[:: -1]
            for power in range(len(revindex)):
                if index < 10 and power == 0 and highest:
                    out += illionsShortList[_tier][power][int(revindex[power])]
                    print(f"triggered: '{out}' for {_tier}, {power}, {int(revindex[power])}")
                else:
                    out += illionsShortList[_tier][power+1][int(revindex[power])]
            return out

        def checkIndex(indexedList, index):
            try: return indexedList[index]
            except IndexError: return 0
        
        if "." in fmt: #rounding
            fmtChunks = fmt.split(".")
            try:
                if fmtChunks[1][0] in "0123456789" : MANTISSA_ROUND = int(fmtChunks[1][0])
                else: MANTISSA_ROUND = 0
            except IndexError: #clearly, there wasn't another character after the period.
                MANTISSA_ROUND = 0
        
        if "el" in fmt: #engineering log looped
            loops = 1
            while exp > 10:
                exp = round(log(exp, 10),MANTISSA_ROUND)
                loops += 1
            string = f"{round(mant,MANTISSA_ROUND)}" + "e" * loops + "{exp}"
        
        elif "e" in fmt or fmt == "": #engineering
            if "," in fmt: string = f"{round(mant,MANTISSA_ROUND)}e{exp:,}"
            else: string = f"{round(mant,MANTISSA_ROUND)}e{exp}"
        
        elif "skl" in fmt: #scientific k log looped
            if "," in fmt: k = "1,000"
            else: k = "1000"
            mant *= 10**(exp % 3)
            exp //= 3
            loops = 1
            while exp > 1000:
                exp = round(log(exp, 1000),MANTISSA_ROUND)
                loops += 1
            string = f"{round(mant,MANTISSA_ROUND)}×" + k * loops + "{exp}"
        
        elif "sk" in fmt: #scientific k
            mant *= 10**(exp % 3)
            exp //= 3
            if "," in fmt: string = f"{round(mant,MANTISSA_ROUND)}×1,000^{exp:,}"
            else: string = f"{round(mant,MANTISSA_ROUND)}×1000^{exp}"

        elif "is" in fmt: #illions shorthand
            mant *= 10**(exp % 3)
            if exp < 0: isFraction = True
            else: isFraction = False
            exp = (abs(exp)-isFraction) // 3 -1 + isFraction
            name = ""
            tier = 0
            oldExp = None
            while exp > 1000:
                oldExp = exp #save the last tier's exponent, in case it's needed
                exp = round(log(exp, 1000))
                tier += 1
            if exp < 10 and oldExp != None:
                oldExp = splitThou(oldExp)
                sections = []
                for e in range(exp, -1, -1):
                    if e == exp:
                        sections.insert(0, parseIllionsShort(tier-1, oldExp[-(e+1)]) + parseIllionsShort(tier, e, False))
                    else:
                        sections.insert(0, parseIllionsShort(tier-1, oldExp[-(e+1)], False) + parseIllionsShort(tier, e, False))
                if len(sections) > 1: name = "-".join(sections)
            else:
                name = parseIllionsShort(tier, exp)

            if isFraction: name += "þ"
            if len(name) > 80:
                name = "..." + name[-80:]
            if (tier <= 1 and exp < 10) or (tier == 0):
                string = f"{round(mant,MANTISSA_ROUND)} " + name
            else:
                string = name
##            mant *= 10**(exp % 3)
##            if exp < 0: isFraction = True
##            else: isFraction = False
##            exp = (abs(exp)-isFraction) // 3 -1 + isFraction
##            name = ""
##            if -1 < exp < 10: #the illions every school kid knows about
##                name = tier0short1[exp]
##            if 10 <= exp < 10**30: #the illions that are latin
##                places = [int(i) for i in str(exp)]
##                name += tier1short1[checkIndex(places,-1)] + tier1short2[checkIndex(places,-2)] + tier1short3[checkIndex(places,-3)]
##                if exp >= 1000:
##                    if name != "": name += "-"
##                    name += tier2short1[checkIndex(places,-4)] + tier2short2[checkIndex(places,-5)] + tier2short3[checkIndex(places,-6)]
##            if 1000000 <= exp < 10**30: # the illions that are descending SI prefixes. Transitional!
##                for block in range(round(log(exp,10)//3)):
##                    places = [int(i) for i in str(exp)]
##                    if block == 0: continue
##                    if name != "": name += "-"
##                    name += tier2short1b[checkIndex(places,-(block*3+4))] + tier2short2[checkIndex(places,-(block*3+5))] + tier2short3[checkIndex(places,-(block*3+6))] + tier2short4[block+1]
##            if 10**30 <= exp: #the illions that are greek
##                exp = round(log(exp,10))//3
##                name += "~"
##                for block in range(round(log(exp,1000)//1)+1):
##                    places = [int(i) for i in str(exp)]
##                    if name != "~": name += "-"
##                    if checkIndex(places,-(block*3+2)) == 0: 
##                        if block == 0:
##                            name += tier2short4[checkIndex(places,-(block*3+1))]
##                        else:
##                            name += tier2short4d[checkIndex(places,-(block*3+1))]
##                    elif checkIndex(places,-(block*3+2)) == 1: name += tier2short4b[checkIndex(places,-(block*3+1))]
##                    else: name += tier2short4c[checkIndex(places,-(block*3+1))]
##                    name += tier2short5[checkIndex(places,-(block*3+2))] + tier2short6[checkIndex(places,-(block*3+3))] + tier3short1[block]
##            if isFraction: name += "þ"
##            if len(name) > 80:
##                name = "..." + name[-80:]
##            string = f"{round(mant,MANTISSA_ROUND)} " + name

        elif "i" in fmt: #illions
            mant *= 10**(exp % 3)
            if exp < 0: isFraction = True
            else: isFraction = False
            exp = (abs(exp)-isFraction) // 3 -1 + isFraction
            name = ""
            if -1 < exp < 10: #the illions every school kid knows about
                name = tier0long1[exp]
            if 10 <= exp < 10**30: #the illions that are latin
                places = [int(i) for i in str(exp)]
                name += tier1long1[checkIndex(places,-1)] + tier1long2[checkIndex(places,-2)] + tier1long3[checkIndex(places,-3)]
                if exp >= 1000:
                    if name != "": name += "-"
                    name += tier2long1[checkIndex(places,-4)] + tier2long2[checkIndex(places,-5)] + tier2long3[checkIndex(places,-6)]
            if 1000000 <= exp < 10**30: # the illions that are descending SI prefixes. Transitional!
                for block in range(round(log(exp,10)//3)):
                    places = [int(i) for i in str(exp)]
                    if block == 0: continue
                    if name != "": name += "-"
                    name += tier2long1b[checkIndex(places,-(block*3+4))] + tier2long2[checkIndex(places,-(block*3+5))] + tier2long3[checkIndex(places,-(block*3+6))] + tier2long4[block+1]
            if 10**30 <= exp: #the illions that are greek
                exp = round(log(exp,10))//3
                name += "~"
                for block in range(round(log(exp,1000)//1)+1):
                    places = [int(i) for i in str(exp)]
                    if name != "~": name += "-"
                    if checkIndex(places,-(block*3+2)) == 0: 
                        if block == 0:
                            name += tier2long4[checkIndex(places,-(block*3+1))]
                        else:
                            name += tier2long4d[checkIndex(places,-(block*3+1))]
                    elif checkIndex(places,-(block*3+2)) == 1: name += tier2long4b[checkIndex(places,-(block*3+1))]
                    else: name += tier2long4c[checkIndex(places,-(block*3+1))]
                    name += tier2long5[checkIndex(places,-(block*3+2))] + tier2long6[checkIndex(places,-(block*3+3))] + tier3long1[block]
            if exp >= 10: name += "illion"
            if isFraction: name += "th"
            if len(name) > 80:
                name = "..." + name[-80:]
            string = f"{round(mant,MANTISSA_ROUND)} " + name
            
        elif "sl" in fmt: #scientific log looped
            loops = 1
            while exp > 10:
                exp = round(log(exp, 10),MANTISSA_ROUND)
                loops += 1
            string = f"{round(mant,MANTISSA_ROUND)}×" + "10^" * loops + "{exp}"
        
        elif "s" in fmt: #scientific
            if "," in fmt: string = f"{round(mant,MANTISSA_ROUND)}×10^{exp:,}"
            else: string = f"{round(mant,MANTISSA_ROUND)}×10^{exp}"
        
        elif "kl" in fmt: #engineering k log looped
            mant *= 10**(exp % 3)
            exp //= 3
            loops = 1
            while exp > 1000:
                exp = round(log(exp, 1000),MANTISSA_ROUND)
                loops += 1
            string = f"{round(mant,MANTISSA_ROUND)}" + "k" * loops + "{exp}"

        elif "k" in fmt: #engineering k
            mant *= 10**(exp % 3)
            exp //= 3
            if "," in fmt: string = f" = {round(mant,MANTISSA_ROUND)}k{exp:,}"
            else: string = f" = {round(mant,MANTISSA_ROUND)}k{exp}"

        if "%" in fmt: #percent sign
            string += "%"
        return string

    def __repl__(self): #Conversion to stringified list if normal printing doesn't work
        return str(self.value)

    def __int__(self): #Conversion to integer
        if self.value[EXPONENT] > 1000000: raise MemoryOverflowSafeguard(self.value[EXPONENT])
        elif self.value[EXPONENT] > 100: #must carefully step down to int to prevent float overflow
            x = int(self.value[MANTISSA]*10**100)
            expon = self.value[EXPONENT]-100
            return x*10**expon
        elif self.value[EXPONENT] < 0:
            return 0
        else: return int(self.value[MANTISSA]*10**self.value[EXPONENT])

    def __float__(self): #Conversion to double floating point
        if abs(self.value[EXPONENT]) > 308: raise OverflowError("expol too large to convert to float") #will float overflow if too large, and could cause memory overflow.
        else: return float(self.value[MANTISSA]*10**self.value[EXPONENT])

    def __iter__(self): #Conversion to list
        return iter(self.value)
    
