expected = "0123456789πτφϕ∞izfptaue"

#Constants
π = pi = 3.14159265
τ = tau = 6.2831853
e = 2.71828183
phi = φ = ϕ = 1.61803399

def parenthesis_finder(string, index, direction):
    opened = direction
    offset = 0 + direction
    while True:
        if string[index + offset] == "(":
            opened += 1
        if string[index + offset] == ")":
            opened -= 1
        if opened == 0:
            break
        offset += direction
    new_index = index + offset
    return new_index

def replace_root(funct):
    srseek = True
    srtype = ["[-3]", "√", "root"]
    while srseek:
        sook = 0
        for type in srtype:
            seek = funct.find(type)
            if seek > -1:
                if funct[seek-1] in expected or funct[seek-2:seek] == "zf":
                    funct = funct[:seek] + "**(1/" + funct[seek+len(type):]
                    seek += 5
                else:
                    funct = funct[:seek] + "2**(1/" + funct[seek+len(type):]
                    seek += 6
                if funct[seek] == "(":
                    new_index = parenthesis_finder(funct, seek, 1)
                    try:
                        funct = funct[:new_index] + ")" + funct[new_index:]
                    except IndexError:
                        funct += ")"
                else:
                    try:
                        while funct[seek] in expected:
                            seek += 1
                        funct = funct[:seek] + ")" + funct[seek:]
                    except IndexError:
                        funct += ")"
            else:
                sook += 1
        if sook == len(srtype):
            srseek = not srseek
    return funct

def replace_ceilingdiv(funct):
    cdseek = True
    cdtype = ["cdiv"]
    while cdseek:
        sook = 0
        for type in cdtype:
            seek = funct.find(type)
            if seek > -1:
                offset = 0
                try:
                    if funct[seek-1] == ")":
                        new_index = parenthesis_finder(funct, seek-1, -1)
                        try:
                            funct = funct[:new_index] + "-(-" + funct[new_index:]
                        except IndexError:
                            funct = "-(-" + funct                
                    else:
                        try:
                            while funct[seek-(offset+1)] in expected:
                                offset += 1
                            funct = funct[:seek-(offset+1)] + "-(-" + funct[seek-(offset+1):]
                        except IndexError:
                            funct = "-(-" + funct
                except IndexError:
                    try:
                        while funct[seek-(offset+1)] in expected:
                            offset += 1
                        funct = funct[:seek-(offset+1)] + "-(-" + funct[seek-(offset+1):]
                    except IndexError:
                        funct = "-(-" + funct
                        
                funct = funct.replace(type, "//")
                seek -= len(type)-2
                if funct[seek+2] == "(":
                    new_index = parenthesis_finder(funct, seek, 1)
                    try:
                        funct = funct[:new_index] + "-(-" + funct[new_index:]
                    except IndexError:
                        funct += "-(-"
                else:
                    try:
                        while funct[seek]+funct[seek+1] != "//":
                            seek += 1
                        seek += 2
                        while funct[seek] in expected:
                            seek += 1
                        funct = funct[:seek] + ")" + funct[seek:]
                    except IndexError:
                        funct += ")"
            else:
                sook += 1
        if sook == len(cdtype):
            cdseek = not cdseek
    return funct

def calculate(funct):
    #Replace simple operators
    funct = funct.replace("[1]", "+")
    funct = funct.replace("[-1]", "-")
    funct = funct.replace("[2]", "*")
    funct = funct.replace("x", "*")
    funct = funct.replace("×", "*")
    funct = funct.replace("÷", "/")
    funct = funct.replace("[-2]", "/")
    funct = funct.replace("floor", "//")
    funct = funct.replace("fdiv", "//")
    funct = funct.replace("mod", "%")
    funct = funct.replace("exp", "**")
    funct = funct.replace("^", "**")
    funct = funct.replace("[3]", "**")
    funct = funct.replace("E", "*10**")
    funct = funct.replace("K", "*1000**")

    #Detect python code instead of function
    blacklist = ["if", "elif", "else", "for", "and", "or", "import", "def", "break", "return",
                 "exit", "eval", "exec", "True", "False", "os", "not", "system", "from", "in"]
    for i in blacklist:
        if i in funct:
            out = "Syntax Error"
            return out

    #Remove whitespace from function
    funct = str([char for char in funct if char != ' '])

    #Break function into characters and find parenthesis
    level = 0
    compilation = []
    character_index = 0
    for character in funct:
        if character  == "(":
            level += 1
        elif character  == ")":
            level -= 1
        else:
            compilation.append( (character, level) )
            character_index += 1

    #Combine adjacent characters in the same parenthesis level
    compilation_prime = []
    last_level = 0
    slot = 0
    max_level = 0
    for string, level in compilation:
        if slot > 0 and level == last_lv:
            compilation_prime[-1][0] += string
        else:
            compilation_prime.append( (string, level) )
        last_level = level
        if level > max_level:
            max_level = level
        slot += 1

    #Fast simplification
    for level in list(range(max_level+1))[::-1]:
        for string, tier in compilation_prime:
            if level == tier:
                try:
                    string = eval(string)
                    tier -= 1
                except Exception:
                    continue

    #catch for root
    funct = replace_root(funct)
        
    #catch for ceilingdiv
    funct = replace_ceilingdiv(funct)
    
    calculating = True
    while calculating:
            try:
                    try:
                            out = eval(funct)
                            calculating = not calculating
                    except SyntaxError:
                        out = "Syntax Error\nTODO: Catches for ∞, i, zf, and other non-ints"
                        #todo: catches for infinity, imaginary, zero fraction, and other non-ints
            except ZeroDivisionError:
                out = "Zero Fraction\nTODO: Replace /0 with imaginary variable 'zf' and manually continue calculations."
                    #funct = funct.replace("//0", "zf")
                    #funct = funct.replace("/0", "zf")
    return out

funct = ""
