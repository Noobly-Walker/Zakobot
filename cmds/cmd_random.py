import asyncio
import discord
from discord.ext import commands
import traceback
from os.path import isdir,exists
from math import factorial, log
from random import *
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.ItemRandomizer import itemGenerator
from util.SLHandle import *
from util.expol import expol
from util.cmdutil import cmdutil
from util.PlayerDataHandler import GetNotationCode
text = cmdutil()
PATH = load(".\\locals\\%PATH%")

def commandList():
    return [splash, joke, choose, generate, randomelement,
            roll, namegenerator, chuck, dndtreasure]

def categoryDescription():
    return "Random numbers and items from lists."

def get_rand_from_list(listName:str):
    file = load(listName + '.txt', PATH + '\\randlists\\')
    randStr = file.split("\n")
    randID = randrange(len(randStr))
    string = randStr[randID]
    return string.replace("\\n", "\n")

@commands.command()
async def splash(ctx):
    "Returns a random splash"
    await ctx.send(get_rand_from_list("splash"))

@commands.command()
async def joke(ctx):
    "Returns a random joke"
    await ctx.send(get_rand_from_list("jokes"))

@commands.command(aliases=['gen'])
async def generate(ctx, type_=None):
    """Returns a random item with random modifiers. For fun or roleplaying; has no bearing on anything else.
    Valid types: tool, melee, ranged, ammo, armor, jewelry, trinket, potion, furniture, any
    Type '[PREFIX]generate info' to learn more about formatting of items."""
    if type_ is None: type_ = "any"
    await ctx.send(itemGenerator(ctx, type_, {"debuff": True, "tf": True, "nsfw": False, "vore": False, "gore": False, "fetish": False}))

@commands.command()
async def chuck(ctx):
    "Returns a random Chuck Norris joke"
    await ctx.send(get_rand_from_list("chucks"))

@commands.command(aliases=['choice']) # Bot randomly chooses between the inputs.
async def choose(ctx, *, choices: str):
    """Lets me choose between a list of items. Separate items using commas."""
    vals = choices.split(",")
    options = [] # short for post-processed
    for val in vals:
      stripped = val.strip()
      if stripped: # Empty sequences are falsy.
        options.append(stripped)
    await ctx.send(choice(options))

@commands.command(aliases=['dice']) # Bot rolls X Y-sided dice. Not as nice as Tsumikibot's dice system, and that's okay.
async def roll(ctx, dice: str, *formating: str):
    """Rolls some dice.
    Example: [prefix]roll 2d6
    Returns: 6, 2"""
    try:
        if dice[0] == 'd': dice = '1' + dice
        try: rolls, limit = map(int, dice.split('d'))
        except Exception:
            out = 'Invalid dice! Proper syntax example: ' + prefix + 'roll 10d20'
            await ctx.send(out); return
        total = 0
        result = '('
        dieoutputs = {}
        singlerolls = True
        if rolls > 1000000:
            await ctx.send("Too many dice!")
            return
            #There may be a way to use statistics to write an algorithm that would turn large amounts of dice into
            #  one dice roll, to save processing time.
            #10000000000d4 would result from 10 billion if we get 10 billion 1s, up to 40 billion, but it's most
            #  likely to be around 25 billion.
            #I'm not good at statistics.
        if rolls > 1: singlerolls = False
        while rolls > 0:
            roll = randint(1, limit)
            total += roll
            if len(formating) > 0:
                if formating[0] in 'cs':
                    dieoutputs[roll] = dieoutputs.setdefault(roll, 1)
            else: 
                result += str(roll)
                if rolls > 1: result += ', '
            rolls -= 1
        if len(formating) > 0:
            if formating[0] == 'c':
                for num in dieoutputs.keys():
                    result += '[{0} × {1}s], '.format(dieoutputs[num], num)
                result = result[:-2]
        if not singlerolls: result += ') Total: ' + str(total)
        else: result += ')'
        if len(result) > 2000: result = "Total: " + str(total)
    except Exception as e: result = f"Error: {e}"
    await ctx.send(result)

@commands.command(aliases=['namegen'])
async def namegenerator(ctx, tries=1):
    """Generate random names from consonants and vowels!
Clamped number of tries to 1 <= n <= 100"""
    consonants = []
    vowels = []

    def addToBag(bag:list,string:str,count:int):
        for i in range(count):
            bag.append(string)
        return bag

    consonants = addToBag(consonants, "r", 38)
    consonants = addToBag(consonants, "t", 35)
    consonants = addToBag(consonants, "n", 33)
    consonants = addToBag(consonants, "s", 29)
    consonants = addToBag(consonants, "l", 27)
    consonants = addToBag(consonants, "c", 23)
    consonants = addToBag(consonants, "d", 17)
    consonants = addToBag(consonants, "p", 16)
    consonants = addToBag(consonants, "m", 15)
    consonants = addToBag(consonants, "h", 15)
    consonants = addToBag(consonants, "g", 12)
    consonants = addToBag(consonants, "b", 10)
    consonants = addToBag(consonants, "ch", 10)
    consonants = addToBag(consonants, "sh", 10)
    consonants = addToBag(consonants, "th", 10)
    consonants = addToBag(consonants, "f", 9)
    consonants = addToBag(consonants, "y", 9)
    consonants = addToBag(consonants, "w", 6)
    consonants = addToBag(consonants, "k", 5)
    consonants = addToBag(consonants, "v", 5)
    consonants = addToBag(consonants, "x", 1)
    consonants = addToBag(consonants, "z", 1)
    consonants = addToBag(consonants, "j", 1)
    consonants = addToBag(consonants, "qu", 1)

    vowels = addToBag(vowels, "a", 43)
    vowels = addToBag(vowels, "e", 56)
    vowels = addToBag(vowels, "i", 38)
    vowels = addToBag(vowels, "o", 36)
    vowels = addToBag(vowels, "u", 18)
    vowels = addToBag(vowels, "y", 9)
    vowels = addToBag(vowels, "ee", 3)
    vowels = addToBag(vowels, "oo", 3)
    vowels = addToBag(vowels, "ae", 2)
    vowels = addToBag(vowels, "ea", 2)
    vowels = addToBag(vowels, "ie", 1)
    vowels = addToBag(vowels, "ue", 1)
    vowels = addToBag(vowels, "ei", 1)
    vowels = addToBag(vowels, "ai", 1)

    def wordGenerator(minBlocks,randAddedBlocks):
        boolean = choice([True, False])
        newName = ""
        if boolean: newName += choice(consonants) # start name with consonant
        newName += choice(vowels) # start name with vowel or finish first block
        minBlocks -= 1
        blocks = randrange(randAddedBlocks)+minBlocks
        for i in range(blocks):
            coin = randrange(2)
            if coin == 1:
                newName += choice(consonants) + choice(vowels)
            else:
                newName += choice(consonants) + choice(consonants) + choice(vowels)
        boolean = choice([True, False])
        if boolean: newName += choice(consonants)
        return newName

    tries = max(1, min(tries, 100))
    out = ""
    for i in range(tries):
        out += wordGenerator(2,2).title() + " " + wordGenerator(3,2).title() + "\n"
    await ctx.send(out)

@commands.command(aliases=["lmn"])
async def randomelement(ctx):
    """Draw a random atom from the Earth."""
    elementAbundance = {
        'Oxygen': 82979999999999994243515927468969116115166478467072,
        'Silicon': 50760000000000004205178170284470811098475984322560,
        'Aluminium': 14813999999999998999355473516658881919200417284096,
        'Iron': 10133999999999999670357022943454440614034329829376,
        'Calcium': 7470000000000000351867339071101198747853037502464,
        'Sodium': 4248000000000000439381613109056533253347130474496,
        'Magnesium': 4194000000000000172531316353004636267924735131648,
        'Potassium': 3761999999999999984840264255149821083481695846400,
        'Titanium': 1017000000000000103815858419505370347588800217088,
        'Hydrogen': 252000000000000001313595837606399929873099390976,
        'Phosphorus': 252000000000000001313595837606399929873099390976,
        'Manganese': 171000000000000026968752380213633354631783383040,
        'Fluorine': 105300000000000001128392820818436268524037996544,
        'Barium': 76499999999999996052539535633727745008494182400,
        'Strontium': 66599999999999997159928819365000343417608208384,
        'Sulfur': 63000000000000000328398959401599982468274847744,
        'Carbon': 35999999999999998738913005111509245414210535424,
        'Zirconium': 29699999999999996677832148806182204772657922048,
        'Chlorine': 26100000000000004916904689755699449810137382912,
        'Vanadium': 21600000000000001271588763432072589643251449856,
        'Chromium': 18359999999999999052609488552094658802038603776,
        'Rubidium': 16200000000000000953691572574054442232438587392,
        'Nickel': 15119999999999999368931414128575530954232168448,
        'Zinc': 12600000000000001586860512154195278289698816000,
        'Cerium': 11970000000000000873692186432370813626862272512,
        'Copper': 10800000000000000635794381716036294821625724928,
        'Neodymium': 7470000000000001031328060793432157950085955584,
        'Lanthanum': 7020000000000000159736228069777711334716080128,
        'Yttrium': 5939999999999999842626669852528201553212866560,
        'Cobalt': 4499999999999999842364125638938655676776316928,
        'Scandium': 3960000000000000317634646644428601534376312832,
        'Lithium': 3600000000000000000656360533973864691091374080,
        'Niobium': 3600000000000000000656360533973864691091374080,
        'Nitrogen': 3420000000000000159079867535803846643624706048,
        'Gallium': 3420000000000000159079867535803846643624706048,
        'Lead': 2520000000000000000459452373781705283763961856,
        'Boron': 1800000000000000000328180266986932345545687040,
        'Thorium': 1728000000000000127080113079130395201394180096,
        'Praseodymium': 1655999999999999936919395834216507683066871808,
        'Samarium': 1269000000000000182456140871033763768760795136,
        'Gadolinium': 1116000000000000095277266782649103166491066368,
        'Dysprosium': 936000000000000095244448755950409931936497664,
        'Erbium': 630000000000000079343025607709763914484940800,
        'Argon': 630000000000000079343025607709763914484940800,
        'Ytterbium': 576000000000000095178812702553023462827360256,
        'Hafnium': 540000000000000000098454080096079703663706112,
        'Caesium': 540000000000000000098454080096079703663706112,
        'Beryllium': 504000000000000063474420486167811131587952640,
        'Uranium': 486000000000000095162403689203676845550075904,
        'Bromine': 432000000000000031770028269782598800348545024,
        'Tin': 413999999999999984229848958554126920766717952,
        'Tantalum': 360000000000000079293798567661724062653087744,
        'Europium': 360000000000000079293798567661724062653087744,
        'Arsenic': 324000000000000063441602459469117897033383936,
        'Germanium': 270000000000000039663308297180208648603828224,
        'Holmium': 234000000000000023811112188987602482984124416,
        'Tungsten': 225000000000000039655103790505535339965186048,
        'Molybdenum': 216000000000000015885014134891299400174272512,
        'Terbium': 216000000000000015885014134891299400174272512,
        'Thallium': 153000000000000007950711574120323008725778432,
        'Lutetium': 144000000000000023794703175638255865706840064,
        'Thulium': 93600000000000017447261127021474752548044800,
        'Iodine': 81000000000000015860400614867279474258345984,
        'Indium': 45000000000000009911724820957715507831635968,
        'Antimony': 36000000000000005948675793909563966426710016,
        'Cadmium': 27000000000000001985626766861412425021784064,
        'Mercury': 15300000000000002280599204554488630751526912,
        'Silver': 13500000000000000992813383430706212510892032,
        'Selenium': 9000000000000001487168948477390991606677504,
        'Palladium': 2700000000000000384253682578948283737047040,
        'Bismuth': 1530000000000000166162918491179849330196480,
        'Helium': 1440000000000000411258637256335797142945792,
        'Neon': 900000000000000024922890919201071670755328,
        'Platinum': 900000000000000024922890919201071670755328,
        'Gold': 720000000000000205629318628167898571472896,
        'Osmium': 270000000000000038425368257894828373704704,
        'Tellurium': 180000000000000051407329657041974642868224,
        'Ruthenium': 180000000000000051407329657041974642868224,
        'Iridium': 180000000000000051407329657041974642868224,
        'Rhodium': 180000000000000051407329657041974642868224,
        'Rhenium': 126000000000000020510880268862128813768704,
        'Krypton': 18000000000000002239310998629087444992000,
        'Xenon': 5400000000000001276256209396040820850688,
        'Protactinium': 251999999999999993571422117850062520320,
        'Radium': 162000000000000020153798987661787004928,
        'Actinium': 99000000000000000953016143054897152,
        'Polonium': 36000000000000004958237343174623232,
        'Radon': 72000000000000008187092429438976,
        'Promethium': 2284260288275862052143104,
        'Francium': 75000000000000002097152,
        'Astatine': 71692151904761904761900,
        'Plutonium': 49361809508196713234432 + 449000000000000000000000000,
        'Neptunium': 2540987662447257059328 + 41000000000000000000000,
        'Technetium': 434587477525773221888,
        'Americium': 24988135933609955328 + 1820000000000000000000000,
        'Curium': 2488487917 + 33600000000000000000,
        'Berkelium': 0 + 39600000000000000000,
        'Californium': 0 + 36000000000000000000,
        'Einsteinium': 0 + 1
    } # Added atom count due to fallout from nuclear testing

    totalAtomCount = sum(elementAbundance.values())

    diceMap = {}
    value = 0
    for element in elementAbundance:
        diceMap[element] = elementAbundance[element] + value
        value += elementAbundance[element]

    dice = randint(1,totalAtomCount)
    rolledElement = "None"
    for element in diceMap:
        if diceMap[element] >= dice:
            rolledElement = element
            break
    denominator = int(totalAtomCount/elementAbundance[rolledElement])
    notation = GetNotationCode(ctx.author)
    text = f"Rolled {rolledElement} (1/{expol(denominator):{notation}})"

    rarity = [(128,128,128,255),
              (255,255,255,255),
              (0,255,0,255),
              (0,255,128,255),
              (0,255,255,255),
              (0,128,255,255),
              (0,0,255,255),
              (128,0,255,255),
              (255,0,255,255),
              (255,0,128,255),
              (255,0,0,255),
              (255,128,0,255),
              (255,255,0,255)]
    color = rarity[ min( int(log(denominator, 10)), len(rarity)-1 ) ]
    
    img = Image.new('RGBA', (1000, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 24)
    bbox = draw.textbbox((0,0), text, font=font, stroke_width=1)
    padding = 2
    crop_box = (bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding)

    draw.text(
        (0,0),
        text,
        fill=color,
        font=font,
        stroke_width=1,
        stroke_fill='black'
    )
    cropped_img = img.crop(crop_box)
    
    # Create in-memory buffer (no disk save!)
    buffer = BytesIO()
    cropped_img.save(buffer, format='PNG')
    buffer.seek(0)  # Reset to start

    # Create discord.File from buffer
    file = discord.File(fp=buffer, filename='cropped_text.png')

    # Send the file
    await ctx.send(file=file)

@commands.command(aliases=["d&dtreasure"])
async def dndtreasure(ctx, treas_type, *args):
    """Roll from D&D treasure tables.
[PREFIX]dnd_treasure single <cr>
  Values for <cr>: x where 0<=x 
[PREFIX]dnd_treasure hoard <cr>
  Values for <cr>: x where 0<=x
[PREFIX]dnd_treasure gems <value> <quantity>
  Values for <value>: 10, 50, 100, 500, 1000, 5000
[PREFIX]dnd_treasure arts <value> <quantity>
  Values for <value>: 25, 250, 750, 2500, 7500
[PREFIX]dnd_treasure item <table> <quantity>
  Values for <table>: a, b, c, d, e, f, g, h, i"""
    try:
        def dice(dice_num, dice_size, multiplier):
            total = 0
            while dice_num > 0:
                roll = randint(1, dice_size)
                total += roll
                dice_num -= 1
            return total*multiplier

        def parseInventory(ctx, inventory, submenu):
            def dict_split2(dictin):
                d1 = dict(list(dictin.items())[:-(len(dictin)//-2)])
                d2 = dict(list(dictin.items())[-(len(dictin)//-2):])
                return d1, d2
            out = ""
            out2 = ""
            subm = ""
            filtered = {}
            if submenu:
                subm = "> "
            for item in inventory:
                if type(inventory[item]) is int:
                    if inventory[item] == 0:
                        continue
                    else:
                        filtered[item] = inventory[item]
                elif type(inventory[item]) is list:
                    if inventory[item][0] == 0:
                        continue
                    else:
                        if len(inventory[item]) >= 2:
                            if inventory[item][1] == True:
                                filtered[item + ':star:'] = inventory[item][0]
                            else:
                                filtered[item] = inventory[item][0]
                        else:
                            filtered[item] = inventory[item][0]
            d1, d2 = dict_split2(filtered)
            for item in d1.keys():
                out += subm + str(d1[item]) + "× " + item + '\n'
            for item in d2.keys():
                out2 += subm + str(d2[item]) + "× " + item + '\n'
            if out == '' and out2 == '':
                out = '*<empty>*'
            if out != '' and out2 == '':
                out1 = out2
            return out, out2

        arg = [0, 1]
        if treas_type != 'item':
            arg[0] = int(args[0])
        else:
            arg[0] = args[0]
        if len(args) == 2:
            arg[1] = int(args[1])
        
        CP = "Copper Pieces"
        SP = "Silver Pieces"
        EP = "Electrum Pieces"
        GP = "Gold Pieces"
        PP = "Platinum Pieces"
        
        mitA = []
        mitB = []
        mitC = []
        mitD = []
        mitE = []
        mitF = []
        mitG = []
        mitH = []
        mitI = []
        
        it0 = [[[dice(5,6,1), CP]],
               [[dice(4,6,1), SP]],
               [[dice(3,6,1), EP]],
               [[dice(2,6,1), GP]],
               [[dice(1,6,1), PP]]]
        
        it5 = [[[dice(4,6,100), CP], [dice(1,6,10), EP]],
               [[dice(6,6,10), SP], [dice(2,6,10), GP]],
               [[dice(3,6,10), EP], [dice(2,6,10), GP]],
               [[dice(4,6,10), GP]],
               [[dice(2,6,10), GP], [dice(3,6,1), PP]]]
        
        it11 = [[[dice(4,6,100), SP], [dice(1,6,100), GP]],
               [[dice(1,6,100), EP], [dice(1,6,100), GP]],
               [[dice(2,6,100), GP], [dice(1,6,10), PP]],
               [[dice(2,6,100), GP], [dice(2,6,10), PP]]]
        
        it17 = [[[dice(2,6,1000), EP], [dice(8,6,100), GP]],
               [[dice(1,6,1000), GP], [dice(1,6,100), PP]],
               [[dice(1,6,1000), GP], [dice(2,6,100), PP]]]
        gem10 = [["Azurite",[""]], ["Banded Agate",["Brown ", "Blue ", "White ", "Red "]], ["Blue Quartz",[""]],
                 ["Eye Agate",["Gray ", "White ", "Brown ", "Blue ", "Green "]], ["Hematite",[""]], ["Lapis Lazuli",[""]],
                 ["Malachite",[""]], ["Moss Agate",[""]], ["Obsidian",[""]], ["Rhodochrosite",[""]], ["Tiger Eye",[""]],
                 ["Turquoise",[""]]]
        gem50 = [["Bloodstone",[""]], ["Carnelian",[""]], ["Chalcedony",[""]], ["Chrysoprase",[""]], ["Citrine",[""]],
                 ["Jasper",["Blue ", "Black ", "Brown "]], ["Moonstone",[""]], ["Onyx",[""]], ["Quartz",["Clear ", "Smoky ", "Yellow "]],
                 ["Sardonyx",[""]], ["Star Rose Quartz",[""]], ["Zircon",[""]]]
        gem100 = [["Amber",[""]], ["Amethyst",[""]], ["Chrysoberyl",[""]], ["Coral",[""]], ["Garnet",["Red ", "Brown-Green ", "Violet "]],
                  ["Jade",["Light Green ", "Deep Green ", "White "]], ["Jet",[""]], ["Pearl",["White ", "Yellow ", "Pink "]],
                  ["Spinel",["Red ", "Red-Brown ", "Deep Green "]], ["Tourmaline",["Pale Green ", "Blue ", "Brown ", "Red "]]]
        gem500 = [["Alexandrite",[""]], ["Aquamarine",[""]], ["Black Pearl",[""]], ["Blue Spinel",[""]], ["Peridot",[""]], ["Topaz",[""]]]
        gem1k = [["Black Opal",[""]], ["Blue Sapphire",[""]], ["Emerald",[""]], ["Fire Opal",[""]], ["Opal",[""]], ["Star Ruby",[""]],
                 ["Star Sapphire",[""]], ["Sapphire",["Yellow ", "Yellow-Green "]]]
        gem5k = [["Black Sapphire",[""]], ["Diamond",["Blue-White ", "Canary ", "Pink ", "Brown ", "Blue "]], ["Jacinth",[""]],
                 ["Ruby",["Red ", "Deep Crimson "]]]

        def gem_identify(quantity, value):
            values = {10:gem10, 50:gem50, 100:gem100, 500:gem500, 1000:gem1k, 5000:gem5k}
            table = values[value]
            gems = {}
            while quantity > 0:
                gem = table[dice(1, len(table), 1)-1]
                gem = choice(gem[1]) + gem[0] + f" ({value}GP)\n"
                gems.setdefault(gem, 0)
                gems[gem] += 1
                quantity -= 1
            if len(gems) > 1:
                out1, out2 = parseInventory(ctx,gems,True)
                out = "Gems:\n" + out1 + out2
            else:
                for key in gems:
                    out = key
            return out
        
        art25 = ["Silver Ewer", "Carved Bone Statuette", "Small Gold Bracelet", "Cloth-of-gold Vestments",
                 "Black Velvet Mask stitched with Silver Thread", "Copper Clalice with Silver Filigree",
                 "Pair of Engraved Bone Dice", "Small Mirror set in a Painted Wooden Frame", "Embroidered Silk Handkerchief",
                 "Gold Locket with a Painted Portrait"]
        art250 = [f"Gold Ring set with {gem_identify(1, 50)}s", "Carved Ivory Statuette", "Large Gold Bracelet",
                  f"Silver Necklace with a {gem_identify(1, 50)} Pendant", "Bronze Crown", "Silk Robe with Gold Embroidery",
                  "Large well-made Tapestry", "Brass Mug with Jade Inlay", "Box of Turquoise Animal Figurines",
                  "Gold Bird Cage with Electrum Filigree"]
        art750 = [f"Silver Chalice set with {gem_identify(1, 50)}", f"Silver-plated Longsword with {gem_identify(1, 100)} set in Hilt",
                  f"Carved Harp of Exotic Wood with Ivory Inlay and {gem_identify(1, 50)} Gems", "Small Gold Idol",
                  f"Gold Dragon Comb set with {gem_identify(1, 100)}s as Eyes", f"Bottle Stopper Cork embossed with Gold Leaf and set with {gem_identify(1, 100)}",
                  f"Ceremonial Electrum Dagger with a {gem_identify(1, 500)} in the Pommel", "Silver and Gold Brooch",
                  "Obsidian Statuette with Gold Fittings and Inlay", "Painted Gold War Mask"]
        art2500 = [f"Fine Gold Chain set with a {gem_identify(1, 1000)}", "Old Masterpiece Painting",
                   f"Embroidered Silk and Velvet Mantle set with numerous {gem_identify(1, 50)}s", f"Platinum Bracelet set with a {gem_identify(1, 1000)}",
                   f"Embroidered Glove set with {gem_identify(1, 1000)} and {gem_identify(1, 500)} chips",
                   f"{gem_identify(1, 1000)} and {gem_identify(1, 500)}-jeweled Anklet",
                   f"Gold Music Box", f"Gold Circlet set with four {gem_identify(1, 500)}",
                   f"Eye Patch with a Mock Eye set in {gem_identify(1, 1000)} and Moonstone", "A Necklace String of Small Pink Pearls"]
        art7500 = [f"{gem_identify(1, 5000)} and {gem_identify(1, 1000)}-jeweled Gold Crown",
                   f"{gem_identify(1, 5000)} and {gem_identify(1, 1000)}-jeweled Platinum Ring",
                   f"Small Gold Statuette set with {gem_identify(1, 5000)}s", f"Gold Cup set with {gem_identify(1, 1000)}s",
                   "Gold Jewelry Box with Platinum Filigree", "Painted Gold Child's Sarcophagus", "Jade Board Game with Solid Gold Playing Pieces",
                   f"{gem_identify(1, 5000)} and {gem_identify(1, 1000)}-bejeweled Ivory Drinking Horn with Gold Filigree"]
        
        def art_identify(quantity, value):
            values = {25:art25, 250:art250, 750:art750, 2500:art2500, 7500:art7500}
            table = values[value]
            arts = {}
            while quantity > 0:
                art = table[dice(1, len(table), 1)-1] + f" ({value}GP)\n"
                arts.setdefault(art, 0)
                arts[art] += 1
                quantity -= 1
            out1, out2 = parseInventory(ctx,arts,True)
            out = "Arts:\n" + out1 + out2
            return out

        mia = [[[1,50], "Potion of Healing"],
               [[51,60], "Spell Scroll (Cantrip)"],
               [[61,70], "Potion of Climbing"],
               [[71,90], "Spell Scroll (Lv1)"],
               [[91,94], "Spell Scroll (Lv2)"],
               [[95,98], "Potion of Greater Healing"],
               [[99], "Bag of Holding"],
               [[100], "Driftglobe"]]
        mib = [[[1,15], "Potion of Greater Healing"],
               [[16,22], "Potion of Fire Breath"],
               [[23,29], "Potion of Resistance"],
               [[30,34], "Ammunition, +1"],
               [[35,39], "Potion of Animal Friendship"],
               [[40,44], "Potion of Hill Giant Strength"],
               [[45,49], "Potion of Growth"],
               [[50,54], "Potion of Water Breathing"],
               [[55,59], "Spell Scroll (Lv2)"],
               [[60,64], "Spell Scroll (Lv3)"],
               [[65,67], "Bag of Holding"],
               [[68,70], "Keoghtom's Ointment"],
               [[71,73], "Oil of Slipperiness"],
               [[74,75], "Dust of Disappearance"],
               [[76,77], "Dust of Dryness"],
               [[78,79], "Dust of Sneezing and Choking"],
               [[80,81], "Elemental Gem"],
               [[82,83], "Philter of Love"],
               [[84], "Alchemy Jug"],
               [[85], "Cap of Water Breathing"],
               [[86], "Cloak of the Manta Ray"],
               [[87], "Driftglobe"],
               [[88], "Goggles of Night"],
               [[89], "Helm of Comprehending Languages"],
               [[90], "Immovable Rod"],
               [[91], "Lantern of Revealing"],
               [[92], "Mariner's Armor"],
               [[93], "Mithral Armor"],
               [[94], "Potion of Poison"],
               [[95], "Ring of Swimming"],
               [[96], "Robe of Useful Items"],
               [[97], "Rope of Climbing"],
               [[98], "Saddle of the Cavalier"],
               [[99], "Wand of Magic Detection"],
               [[100], "Wand of Secrets"]]
        mic = [[[1,15], "Potion of Superior Healing"],
               [[16,22], "Spell Scroll (Lv4)"],
               [[23,27], "Ammunition, +2"],
               [[28,32], "Potion of Clairvoyance"],
               [[33,37], "Potion of Diminution"],
               [[38,42], "Potion of Gaseous Form"],
               [[43,47], "Potion of Frost Giant Strength"],
               [[48,52], "Potion of Stone Giant Strength"],
               [[53,57], "Potion of Heroism"],
               [[58,62], "Potion of Invulnerability"],
               [[63,67], "Potion of Mind Reading"],
               [[68,72], "Spell Scroll (Lv5)"],
               [[73,75], "Elixir of Health"],
               [[76,78], "Oil of Etherealness"],
               [[79,81], "Potion of Fire Giant Strength"],
               [[82,84], "Quaal's Feather Token"],
               [[85,87], "Scroll of Protection"],
               [[88,89], "Bag of Beans"],
               [[90,91], "Bead of Force"],
               [[92], "Chime of Opening"],
               [[93], "Decanter of Endless Water"],
               [[94], "Eyes of Minute Seeing"],
               [[95], "Folding Boat"],
               [[96], "Heward's Handy Haversack"],
               [[97], "Horseshoes of Speed"],
               [[98], "Necklace of Fireballs"],
               [[99], "Periapt of Health"],
               [[100], "Sending Stones"]]
        mid = [[[1,20], "Potion of Supreme Healing"],
               [[21,30], "Potion of Invisibility"],
               [[31,40], "Potion of Speed"],
               [[41,50], "Spell Scroll (Lv6)"],
               [[51,57], "Spell Scroll (Lv7)"],
               [[58,62], "Ammunition, +3"],
               [[63,67], "Oil of Sharpness"],
               [[68,72], "Potion of Flying"],
               [[73,77], "Potion of Cloud Giant Strength"],
               [[78,82], "Potion of Longevity"],
               [[83,87], "Potion of Vitality"],
               [[88,92], "Spell Scroll (Lv8)"],
               [[93,95], "Horseshoes of a Zephyr"],
               [[96,98], "Nolzur's Marvelous Pigments"],
               [[99], "Bag of Devouring"],
               [[100], "Portable Hole"]]
        mie = [[[1,30], "Spell Scroll (Lv8)"],
               [[31,55], "Potion of Storm Giant Strength"],
               [[56,70], "Potion of Supreme Healing"],
               [[71,85], "Spell Scroll (Lv9)"],
               [[86,93], "Universal Solvent"],
               [[94,98], "Arrow of Slaying"],
               [[99,100], "Sovereign Glue"]]
        mif = [[[1,15], "Weapon, +1"], [[16,18], "Shield, +1"],
               [[19,21], "Sentinel Shield"], [[22,23], "Amulet of Proof Against Detection and Location"],
               [[24,25], "Boots of Elvenkind"], [[26,27], "Boots of Striding and Springing"],
               [[28,29], "Bracers of Archery"], [[30,31], "Brooch of Shielding"],
               [[32,33], "Broom of Flying"], [[34,35], "Cloak of Elvenkind"],
               [[36,37], "Cloak of Protection"], [[38,39], "Gauntlets of Ogre Power"],
               [[40,41], "Hat of Disguise"], [[42,43], "Javelin of Lightning"],
               [[44,45], "Pearl of Power"], [[46,47], "Rod of the Pact Keeper, +1"],
               [[48,49], "Slippers of Spider Climbing"], [[50,51], "Staff of the Adder"],
               [[52,53], "Staff of the Python"], [[54,55], "Sword of Vengeance"],
               [[56,57], "Trident of Fish Command"], [[58,59], "Wand of Magic Missiles"],
               [[60,61], "Wand of the War Mage, +1"], [[62,63], "Wand of Web"],
               [[64,65], "Weapon of Warning"], [[66], "Adamantine Armor (Chain Mail)"],
               [[67], "Adamantine Armor (Chain Shirt)"], [[68], "Adamantine Armor (Scale Mail)"],
               [[69], "Bag of Tricks (Gray)"], [[70], "Bag of Tricks (Rust)"],
               [[71], "Bag of Tricks (Tan)"], [[72], "Boots of the Winterlands"],
               [[73], "Circlet of Blasting"], [[74], "Deck of Illusions"],
               [[75], "Eversmoking Bottle"], [[76], "Eyes of Charming"],
               [[77], "Eyes of the Eagle"], [[78], "Figurine of Wondrous Power (Silver Raven)"],
               [[79], "Gem of Brightness"], [[80], "Gloves of Missile Snaring"],
               [[81], "Gloves of Swimming and Climbing"], [[82], "Gloves of Thievery"],
               [[83], "Headband of Intellect"], [[84], "Helm of Telepathy"],
               [[85], "Instrument of the Bards (Doss Lute)"], [[86], "Instrument of the Bards (Fochlucan Bandore)"],
               [[87], "Instrument of the Bards (Mac-Fuimidh Cittern)"], [[88], "Medallion of Thoughts"],
               [[89], "Necklace of Adaptation"], [[90], "Periapt of Wound Closure"],
               [[91], "Pipes of Haunting"], [[92], "Pipes of the Sewers"],
               [[93], "Ring of Jumping"], [[94], "Ring of Mind Shielding"],
               [[95], "Ring of Warmth"], [[96], "Ring of Water Walking"],
               [[97], "Quiver of Ehlonna"], [[98], "Stone of Good Luck"],
               [[99], "Wind Fan"], [[100], "Winged Boots"]]
        FWP = ["Bronze Griffon", "Ebony Fly", "Golden Lions", "Ivory Goats", "Marble Elephant", "Onyx Dog", "Onyx Dog", "Serpentine Owl"]
        HoV = ["Silver", "Brass"]
        BoGS = ["Frost", "Stone"]
        MAT = ["Armor, +2 (Half Plate)", "Armor, +2 (Half Plate)", "Armor, +2 (Plate)", "Armor, +2 (Plate)",
               "Armor, +3 (Studded Leather)", "Armor, +3 (Studded Leather)", "Armor, +3 (Breastplate)", "Armor, +3 (Breastplate)",
               "Armor, +3 (Splint)", "Armor, +3 (Splint)", "Armor, +3 (Half Plate)", "Armor, +3 (Plate)"]

        def subtable(item):
            table = {0:FWP,1:HoV,2:BoGS,3:MAT}[item]
            out = table[dice(1, len(table), 1)-1]
            return out
        
        mig = [[[1,11], "Weapon, +2"], [[12,14], f"Figurine of Wondrous Power ({subtable(0)})"],
               [[15], "Adamantine Armor (Breastplate)"], [[16], "Adamantine Armor (Splint)"],
               [[17], "Amulet of Health"], [[18], "Armor of Vulnerability"],
               [[19], "Arrow-catching Shield"], [[20], "Belt of Dwarvenkind"],
               [[21], "Belt of Hill Giant Strength"], [[22], "Berserker Axe"],
               [[23], "Boots of Levitation"], [[24], "Boots of Speed"],
               [[25], "Bowl of Commanding Water Elementals"], [[26], "Bracers of Defense"],
               [[27], "Braizer of Commanding Fire Elementals"], [[28], "Cape of the Mountebank"],
               [[29], "Censer of Controlling Air Elementals"], [[30], "Armor, +1 (Chain Mail)"],
               [[31], "Armor of Resistance (Chain Mail)"], [[32], "Armor, +1 (Chain Shirt)"],
               [[33], "Armor of Resistance (Chain Shirt)"], [[34], "Cloak of Displacement"],
               [[35], "Cloak of the Bat"], [[36], "Cube of Force"],
               [[37], "Daern's Instant Darkness"], [[38], "Dagger of Venom"],
               [[39], "Dimensional Shackles"], [[40], "Dragon Slayer"],
               [[41], "Elven Chain"], [[42], "Flame Tongue"],
               [[43], "Gem of Seeing"], [[44], "Giant Slayer"],
               [[45], "Glamoured Studded Leather"], [[46], "Helm of Teleportation"],
               [[47], "Horn of Blasting"], [[48], f"Horn of Valhalla ({subtable(1)})"],
               [[49], "Instrument of the Bards (Canaith Mandolin)"], [[50], "Instrument of the Bards (Cli Lyre)"],
               [[51], "Ioun Stone (Awareness)"], [[52], "Ioun Stone (Protection)"],
               [[53], "Ioun Stone (Reserve)"], [[54], "Ioun Stone (Sustenance)"],
               [[55], "Iron Bands of Bilarro"], [[56], "Armor, +1 (Leather)"],
               [[57], "Armor of Resistance (Leather)"], [[58], "Mace of Disruption"],
               [[59], "Mace of Smiting"], [[60], "Mace of Terror"],
               [[61], "Mantle of Spell Resistance"], [[62], "Necklace of Prayer Beads"],
               [[63], "Periapt of Proof Against Poison"], [[64], "Ring of Animal Influence"],
               [[65], "Ring of Evasion"], [[66], "Ring of Feather Falling"],
               [[67], "Ring of Free Action"], [[68], "Ring of Protection"],
               [[69], "Ring of Resistance"], [[70], "Ring of Spell Storing"],
               [[71], "Ring of the Ram"], [[72], "Ring of X-ray Vision"],
               [[73], "Robe of Eyes"], [[74], "Rod of Rulership"],
               [[75], "Rod of the Pact Keeper, +2"], [[76], "Rope of Entanglement"],
               [[77], "Armor, +1 (Scale Mail)"], [[78], "Armor of Resistance (Scale Mail)"],
               [[79], "Shield, +2"], [[80], "Shield of Missile Attraction"],
               [[81], "Staff of Charming"], [[82], "Staff of Healing"],
               [[83], "Staff of Swarming Insects"], [[84], "Staff of the Woodlands"],
               [[85], "Staff of Withering"], [[86], "Stone of Controlling Earth Elementals"],
               [[87], "Sun Blade"], [[88], "Sword of Life Stealing"],
               [[89], "Sword of Wounding"], [[90], "Tentacle Rod"],
               [[91], "Vicious Weapon"], [[92], "Wand of Binding"],
               [[93], "Wand of Enemy Detection"], [[94], "Wand of Fear"],
               [[95], "Wand of Fireballs"], [[96], "Wand of Lightning Bolts"],
               [[97], "Wand of Paralysis"], [[98], "Wand of the War Mage, +2"],
               [[99], "Wand of Wonder"], [[100], "Wings of Flying"]]
        mih = [[[1,10], "Weapon, +3"], [[11,12], "Amulet of the Planes"],
               [[13,14], "Carpet of Flying"], [[15,16], "Crystal Ball (Very Rare)"],
               [[17,18], "Ring of Regeneration"], [[19,20], "Ring of Shooting Stars"],
               [[21,22], "Ring of Telekinesis"], [[23,24], "Robe of Scintillating Colors"],
               [[25,26], "Robe of Stars"], [[27,28], "Rod of Absorption"],
               [[29,30], "Rod of Alertness"], [[31,32], "Rod of Security"],
               [[33,34], "Rod of the Pact Keeper, +3"], [[35,36], "Scimitar of Speed"],
               [[37,38], "Shield, +3"], [[39,40], "Staff of Fire"],
               [[41,42], "Staff of Frost"], [[43,44], "Staff of Power"],
               [[45,46], "Staff of Striking"], [[47,48], "Staff of Thunder and Lightning"],
               [[49,50], "Sword of Sharpness"], [[51,52], "Wand of Polymorph"],
               [[53,54], "Wand of the War Mage, +3"], [[55], "Adamantine Armor (Half Plate)"],
               [[56], "Adamantine Armor (Plate)"], [[57], "Animated Shield"],
               [[58], "Belt of Fire Strength"], [[59], f"Belt of {subtable(2)} Giant Strength"],
               [[60], "Armor, +1 (Breastplate)"], [[61], "Armor of Resistance (Breastplate)"],
               [[62], "Candle of Invocation"], [[63], "Armor, +2 (Chain Mail)"],
               [[64], "Armor, +2 (Chain Shirt)"], [[65], "Cloak of Arachnida"],
               [[66], "Dancing Sword"], [[67], "Demon Armor"],
               [[68], "Dragon Scale Mail"], [[69], "Dwarven Plate"],
               [[70], "Dwarven Thrower"], [[71], "Efreeti Bottle"],
               [[72], "Figurine of Wondrous Power (Obsidian Steed)"], [[73], "Frost Brand"],
               [[74], "Helm of Brilliance"], [[75], "Horn of Valhalla (Bronze)"],
               [[76], "Instrument of the Bards (Anstruth Harp)"], [[77], "Ioun Stone (Absorption)"],
               [[78], "Ioun Stone (Agility)"], [[79], "Ioun Stone (Fortitude)"],
               [[80], "Ioun Stone (Insight)"], [[81], "Ioun Stone (Intellect)"],
               [[82], "Ioun Stone (Leadership)"], [[83], "Ioun Stone (Strength)"],
               [[84], "Armor, +2 (Leather)"], [[85], "Manual of Bodily Health"],
               [[86], "Manual of Gainful Exercise"], [[87], "Manual of Golems"],
               [[88], "Manual of Quickness of Action"], [[89], "Manual of Life Tapping"],
               [[90], "Nine Lives Stealer"], [[91], "Oathbow"],
               [[92], "Armor, +2 (Scale Mail)"], [[93], "Spellguard Shield"],
               [[94], "Armor, +1 (Splint)"], [[95], "Armor of Resistance (Splint)"],
               [[96], "Armor, +1 (Studded Leather)"], [[97], "Armor of Resistance (Studded Leather)"],
               [[98], "Tome of Clear Thought"], [[99], "Tome of Leadership and Influence"], [[100], "Tome of Understanding"]]
        mii = [[[1,5], "Defender"], [[6,10], "Hammer of Thunderbolts"],
               [[11,15], "Luck Blade"], [[16,20], "Sword of Answering"],
               [[21,23], "Holy Avenger"], [[24,26], "Ring of Djinni Summoning"],
               [[27,29], "Ring of Invisibility"], [[30,32], "Ring of Spell Turning"],
               [[33,35], "Rod of Lordly Might"], [[36,38], "Staff of the Magi"],
               [[39,41], "Vorpal Sword"], [[42,43], "Belt of Cloud Giant Strength"],
               [[44,45], "Armor, +2 (Breastplate)"], [[46,47], "Armor, +3 (Chain Mail)"],
               [[48,49], "Armor, +3 (Chain Shirt)"], [[50,51], "Cloak of Invisibility"],
               [[52,53], "Crystal Ball (Legendary)"], [[54,55], "Armor, +1 (Half Plate)"],
               [[56,57], "Iron Flask"], [[58,59], "Armor, +3 (Leather)"],
               [[60,61], "Armor, +1 (Plate)"], [[62,63], "Robe of the Archmagi"],
               [[64,65], "Rod of Resurrection"], [[66,67], "Armor, +1 (Scale Mail)"],
               [[68,69], "Scarab of Protection"], [[70,71], "Armor, +2 (Splint)"],
               [[72,73], "Armor, +2 (Studded Leather)"], [[74,75], "Well of Many Worlds"],
               [[76], f"{subtable(3)}"], [[77], "Apparatus of Kwalish"],
               [[78], "Armor of Invulnerability"], [[79], "Belt of Storm Giant Strength"],
               [[80], "Cubic Gate"], [[81], "Deck of Many Things"],
               [[82], "Efreeti Chain"], [[83], "Armor of Resistance (Half Plate)"], 
               [[84], "Horn of Valhalla (Iron)"], [[85], "Instrument of the Bards (Ollamh Harp)"],
               [[86], "Ioun Stone (Greater Absorption)"], [[87], "Ioun Stone (Mastery)"],
               [[88], "Ioun Stone (Regeneration)"], [[89], "Plate Armor of Etherealness"],
               [[90], "Plate Armor of Resistance"], [[91], "Ring of Air Elemental Command"],
               [[92], "Ring of Earth Elemental Command"], [[93], "Ring of Fire Elemental Command"],
               [[94], "Ring of Three Wishes"], [[95], "Ring of Water Elemental Command"],
               [[96], "Sphere of Annihilation"], [[97], "Talisman of Pure Good"],
               [[98], "Talisman of the Sphere"], [[99], "Talisman of Ultimate Evil"],
               [[100], "Tome of the Stilled Tongue"]]

        def magic_identify(quantity, table_letter):
            table_letter = str.lower(table_letter)
            values = {'a':mia, 'b':mib, 'c':mic, 'd':mid, 'e':mie, 'f':mif, 'g':mig, 'h':mih, 'i':mii}
            table = values[table_letter]
            magic_items = {}
            while quantity > 0:
                die = dice(1, 100, 1)
                for item in table:
                    if len(item[0]) == 1:
                        if item[0][0] == die:
                            magic_items.setdefault(item[1], 0)
                            magic_items[item[1]] += 1
                            quantity -= 1
                    elif len(item[0]) == 2:
                        if item[0][0] <= die <= item[0][1]:
                            magic_items.setdefault(item[1], 0)
                            magic_items[item[1]] += 1
                            quantity -= 1
            out1, out2 = parseInventory(ctx,magic_items,False)
            out = out1 + out2
            return out

        hcoin0 = f"{dice(6,6,100)} {CP}, {dice(3,6,100)} {SP}, {dice(2,6,100)} {GP}\n"
        hcoin5 = f"{dice(2,6,100)} {CP}, {dice(2,6,1000)} {SP}, {dice(6,6,100)} {GP}, {dice(3,6,10)} {PP}\n"
        hcoin11 = f"{dice(4,6,1000)} {GP}, {dice(5,6,100)} {PP}\n"
        hcoin17 = f"{dice(12,6,1000)} {GP}, {dice(8,6,100)} {PP}\n"
        
        th0 = [[[1,6], hcoin0],
               [[7,16], hcoin0 + gem_identify(dice(2,6,1), 10)],
               [[17,26], hcoin0 + art_identify(dice(2,4,1), 25)],
               [[27,36], hcoin0 + gem_identify(dice(2,6,1), 50)],
               [[37,44], hcoin0 + gem_identify(dice(2,6,1), 10) + magic_identify(dice(1,6,1), 'a')],
               [[45,52], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,6,1), 'a')],
               [[53,60], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(dice(1,6,1), 'a')],
               [[61,65], hcoin0 + gem_identify(dice(2,6,1), 10) + magic_identify(dice(1,4,1), 'b')],
               [[66,70], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'b')],
               [[71,75], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(dice(1,4,1), 'b')],
               [[76,78], hcoin0 + gem_identify(dice(2,6,1), 10) + magic_identify(dice(1,4,1), 'c')],
               [[79,80], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'c')],
               [[81,85], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(dice(1,4,1), 'c')],
               [[86,92], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'f')],
               [[93,97], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(dice(1,4,1), 'f')],
               [[98,99], hcoin0 + art_identify(dice(2,4,1), 25) + magic_identify(1, 'g')],
               [[100], hcoin0 + gem_identify(dice(2,6,1), 50) + magic_identify(1, 'g')]]
        th5 = [[[1,4], hcoin5],
               [[5,10], hcoin5 + art_identify(dice(2,4,1), 25)],
               [[11,16], hcoin5 + gem_identify(dice(3,6,1), 50)],
               [[17,22], hcoin5 + gem_identify(dice(3,6,1), 100)],
               [[23,28], hcoin5 + art_identify(dice(2,4,1), 250)],
               [[29,32], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,6,1), 'a')],
               [[33,36], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(dice(1,6,1), 'a')],
               [[37,40], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,6,1), 'a')],
               [[41,44], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,6,1), 'a')],
               [[45,49], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'b')],
               [[50,54], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(dice(1,4,1), 'b')],
               [[55,59], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,4,1), 'b')],
               [[60,63], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'b')],
               [[64,66], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'c')],
               [[67,69], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(dice(1,4,1), 'c')],
               [[70,72], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,4,1), 'c')],
               [[73,74], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'c')],
               [[75,76], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(1, 'd')],
               [[77,78], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(1, 'd')],
               [[79], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(1, 'd')],
               [[80], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(1, 'd')],
               [[81,84], hcoin5 + art_identify(dice(2,4,1), 25) + magic_identify(dice(1,4,1), 'f')],
               [[85,88], hcoin5 + gem_identify(dice(3,6,1), 50) + magic_identify(dice(1,4,1), 'f')],
               [[89,91], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,4,1), 'f')],
               [[92,94], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'f')],
               [[95,96], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(dice(1,4,1), 'g')],
               [[97,98], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'g')],
               [[99], hcoin5 + gem_identify(dice(3,6,1), 100) + magic_identify(1, 'h')],
               [[100], hcoin5 + art_identify(dice(2,4,1), 250) + magic_identify(1, 'h')]]
        th11 = [[[1,3], hcoin11],
                [[4,6], hcoin11 + art_identify(dice(2,4,1), 250)],
                [[7,9], hcoin11 + art_identify(dice(2,4,1), 750)],
                [[10,12], hcoin11 + gem_identify(dice(3,6,1), 500)],
                [[13,15], hcoin11 + gem_identify(dice(3,6,1), 1000)],
                [[16,19], hcoin11 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'a') + magic_identify(dice(1,6,1), 'b')],
                [[20,23], hcoin11 + art_identify(dice(2,4,1), 750) + magic_identify(dice(1,4,1), 'a') + magic_identify(dice(1,6,1), 'b')],
                [[24,26], hcoin11 + gem_identify(dice(3,6,1), 500) + magic_identify(dice(1,4,1), 'a') + magic_identify(dice(1,6,1), 'b')],
                [[27,29], hcoin11 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,4,1), 'a') + magic_identify(dice(1,6,1), 'b')],
                [[30,35], hcoin11 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,6,1), 'c')],
                [[36,40], hcoin11 + art_identify(dice(2,4,1), 750) + magic_identify(dice(1,6,1), 'c')],
                [[41,45], hcoin11 + gem_identify(dice(3,6,1), 500) + magic_identify(dice(1,6,1), 'c')],
                [[46,50], hcoin11 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,6,1), 'c')],
                [[51,54], hcoin11 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'd')],
                [[55,58], hcoin11 + art_identify(dice(2,4,1), 750) + magic_identify(dice(1,4,1), 'd')],
                [[59,62], hcoin11 + gem_identify(dice(3,6,1), 500) + magic_identify(dice(1,4,1), 'd')],
                [[63,66], hcoin11 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,4,1), 'd')],
                [[67,68], hcoin11 + art_identify(dice(2,4,1), 250) + magic_identify(1, 'e')],
                [[69,70], hcoin11 + art_identify(dice(2,4,1), 750) + magic_identify(1, 'e')],
                [[71,72], hcoin11 + gem_identify(dice(3,6,1), 500) + magic_identify(1, 'e')],
                [[73,74], hcoin11 + gem_identify(dice(3,6,1), 1000) + magic_identify(1, 'e')],
                [[75,76], hcoin11 + art_identify(dice(2,4,1), 250) + magic_identify(1, 'f') + magic_identify(dice(1,4,1), 'g')],
                [[77,78], hcoin11 + art_identify(dice(2,4,1), 750) + magic_identify(1, 'f') + magic_identify(dice(1,4,1), 'g')],
                [[79,80], hcoin11 + gem_identify(dice(3,6,1), 500) + magic_identify(1, 'f') + magic_identify(dice(1,4,1), 'g')],
                [[81,82], hcoin11 + gem_identify(dice(3,6,1), 1000) + magic_identify(1, 'f') + magic_identify(dice(1,4,1), 'g')],
                [[83,85], hcoin11 + art_identify(dice(2,4,1), 250) + magic_identify(dice(1,4,1), 'h')],
                [[86,88], hcoin11 + art_identify(dice(2,4,1), 750) + magic_identify(dice(1,4,1), 'h')],
                [[89,90], hcoin11 + gem_identify(dice(3,6,1), 500) + magic_identify(dice(1,4,1), 'h')],
                [[91,92], hcoin11 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,4,1), 'h')],
                [[93,94], hcoin11 + art_identify(dice(2,4,1), 250) + magic_identify(1, 'i')],
                [[95,96], hcoin11 + art_identify(dice(2,4,1), 750) + magic_identify(1, 'i')],
                [[97,98], hcoin11 + gem_identify(dice(3,6,1), 500) + magic_identify(1, 'i')],
                [[99,100], hcoin11 + gem_identify(dice(3,6,1), 1000) + magic_identify(1, 'i')]]
        th17 = [[[1,2], hcoin17],
                [[3,5], hcoin17 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,8,1), 'c')],
                [[6,8], hcoin17 + art_identify(dice(1,10,1), 2500) + magic_identify(dice(1,8,1), 'c')],
                [[9,11], hcoin17 + art_identify(dice(1,4,1), 7500) + magic_identify(dice(1,8,1), 'c')],
                [[12,14], hcoin17 + gem_identify(dice(1,8,1), 5000) + magic_identify(dice(1,8,1), 'c')],
                [[15,22], hcoin17 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,6,1), 'd')],
                [[23,30], hcoin17 + art_identify(dice(1,10,1), 2500) + magic_identify(dice(1,6,1), 'd')],
                [[31,38], hcoin17 + art_identify(dice(1,4,1), 7500) + magic_identify(dice(1,6,1), 'd')],
                [[39,46], hcoin17 + gem_identify(dice(1,8,1), 5000) + magic_identify(dice(1,6,1), 'd')],
                [[47,52], hcoin17 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,6,1), 'e')],
                [[53,58], hcoin17 + art_identify(dice(1,10,1), 2500) + magic_identify(dice(1,6,1), 'e')],
                [[59,63], hcoin17 + art_identify(dice(1,4,1), 7500) + magic_identify(dice(1,6,1), 'e')],
                [[64,68], hcoin17 + gem_identify(dice(1,8,1), 5000) + magic_identify(dice(1,6,1), 'e')],
                [[69], hcoin17 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,4,1), 'g')],
                [[70], hcoin17 + art_identify(dice(1,10,1), 2500) + magic_identify(dice(1,4,1), 'g')],
                [[71], hcoin17 + art_identify(dice(1,4,1), 7500) + magic_identify(dice(1,4,1), 'g')],
                [[72], hcoin17 + gem_identify(dice(1,8,1), 5000) + magic_identify(dice(1,4,1), 'g')],
                [[73,74], hcoin17 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,4,1), 'h')],
                [[75,76], hcoin17 + art_identify(dice(1,10,1), 2500) + magic_identify(dice(1,4,1), 'h')],
                [[77,78], hcoin17 + art_identify(dice(1,4,1), 7500) + magic_identify(dice(1,4,1), 'h')],
                [[79,80], hcoin17 + gem_identify(dice(1,8,1), 5000) + magic_identify(dice(1,4,1), 'h')],
                [[81,85], hcoin17 + gem_identify(dice(3,6,1), 1000) + magic_identify(dice(1,4,1), 'i')],
                [[86,90], hcoin17 + art_identify(dice(1,10,1), 2500) + magic_identify(dice(1,4,1), 'i')],
                [[91,95], hcoin17 + art_identify(dice(1,4,1), 7500) + magic_identify(dice(1,4,1), 'i')],
                [[96,100], hcoin17 + gem_identify(dice(1,8,1), 5000) + magic_identify(dice(1,4,1), 'i')]]

        def hoard_loot(cr):
            if 0 <= cr <= 4:
                table = th0
            if 5 <= cr <= 10:
                table = th5
            if 11 <= cr <= 16:
                table = th11
            if 17 <= cr:
                table = th17
            outcome = dice(1,100,1)
            for item in table:
                if len(item[0]) == 1:
                    if item[0][0] == outcome:
                        out = item[1]
                elif len(item[0]) == 2:
                    if item[0][0] <= outcome <= item[0][1]:
                        out = item[1]
            return out
        
        if treas_type == "single":
            outcome = dice(1,100,1)
            if 0 <= arg[0] <= 4:
                if 1 <= outcome <= 30:
                    loot = it0[0]
                if 31 <= outcome <= 60:
                    loot = it0[1]
                if 61 <= outcome <= 70:
                    loot = it0[2]
                if 71 <= outcome <= 95:
                    loot = it0[3]
                if 96 <= outcome <= 100:
                    loot = it0[4]
            if 5 <= arg[0] <= 10:
                if 1 <= outcome <= 30:
                    loot = it5[0]
                if 31 <= outcome <= 60:
                    loot = it5[1]
                if 61 <= outcome <= 70:
                    loot = it5[2]
                if 71 <= outcome <= 95:
                    loot = it5[3]
                if 96 <= outcome <= 100:
                    loot = it5[4]
            if 11 <= arg[0] <= 16:
                if 1 <= outcome <= 20:
                    loot = it11[0]
                if 21 <= outcome <= 35:
                    loot = it11[1]
                if 36 <= outcome <= 75:
                    loot = it11[2]
                if 76 <= outcome <= 100:
                    loot = it11[3]
            if 17 <= arg[0]:
                if 1 <= outcome <= 15:
                    loot = it17[0]
                if 16 <= outcome <= 55:
                    loot = it17[1]
                if 56 <= outcome <= 100:
                    loot = it17[2]
            output = {}
            for item in loot:
                output[item[1]] = item[0]
            out1, out2 = parseInventory(ctx,output,False)
            out = out1 + out2
        if treas_type == "hoard":
            out = hoard_loot(arg[0])
        if treas_type == "gems":
            if len(arg) == 1:
                arg.append(1)
            out = gem_identify(arg[1], arg[0])
        if treas_type == "arts":
            if len(arg) == 1:
                arg.append(1)
            out = art_identify(arg[1], arg[0])
        if treas_type == "item":
            if len(arg) == 1:
                arg.append(1)
            out = magic_identify(arg[1], arg[0])
    except Exception as e:
        out = f"Error: {e}"
    await ctx.send(out)
