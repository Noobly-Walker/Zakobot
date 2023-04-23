from PIL import Image, ImageFont, ImageDraw
from random import randrange, choice
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios

cards = {
     0: [(0,0), "testImg", "This is test text."],
     1: [(1,1), "Hydrogen", "A colorless gas.#Could be considered alkali or halogen.#Hydrogen ice is pale yellow."],
     2: [(1,2), "Helium", "A colorless noble gas.#Was discovered on Sol before it was found on Terra.#It cannot freeze at standard pressure, even at 0 kelvin.#Natural helium on Terra is generated from radioactive decay."],
     3: [(1,3), "Lithium", "A silvery alkali metal.#Can be cut with a butter knife.#Explodes in contact with water, creating a shower of red sparks and lithium hydride gas."],
     4: [(1,4), "Beryllium", "A dull brown-gray alkali earth metal.#One of the main components in emerald."],
     5: [(1,5), "Boron", "A dull brown or gray triel.#The image of the lumpy brown solid involves melting boron and dribbling it into liquid, in which it takes its amorphous allotrope."],
     6: [(1,6), "Carbon", "A crumbly black tetral.#The premier building block of Terran life."],
     7: [(1,7), "Nitrogen", "A colorless pnictogen gas.#The most plentiful element in the air.#Dinitrogen is extremely stable. Nitrogen-rich compounds will want to return to dinitrogen, explosively."],
     8: [(1,8), "Oxygen", "A pale blue chalcogen gas.#The most common element on Earth."],
     9: [(1,9), "Fluorine", "A pale yellow halogen gas.#The most electronegative element.#It is extremely difficult to keep, as it reacts with almost everything."],
    10: [(1,10), "Neon", "A colorless noble gas.#Name based on 'Neo', which means new."],
    11: [(1,11), "Sodium", "A silvery alkali metal.#Once called Natrium.#Sodium chloride, table salt, is often referred to as sodium on nutrition lists."],
    12: [(1,12), "Magnesium", "A dull gray alkali earth metal.#Highly flammable, will combust even in normally inert nitrogen atmospheres."],
    13: [(1,13), "Aluminium", "A silvery triel metal.#The first metal triel.#Used in construction of things that have to be light, where other metals are too heavy."],
    14: [(1,14), "Silicon", "A shiny black tetral.#The second most common element on Earth.#Along with Oxygen, produces the most common mineral family, silicates."],
    15: [(1,15), "Phosphorus", "A crumbly bright red, yellow-white, or black pnictogen.#The yellow-white allotrope ignites in sunlight, and is impossible to put out.#The red allotrope is used in matchboxes as the strike surface."],
    16: [(1,16), "Sulphur", "A yellow chalcogen crystal.#Is involved in a most smelly compounds."],
    17: [(1,17), "Chlorine", "A pale green halogen gas.#Was used as a chemical weapon in the first World War.#Has antibiotic properties.#Muriatic Acid, produced by the stomach, is hydrochloric acid dissolved into water."],
    18: [(1,18), "Argon", "A colorless noble gas.#Considered 'lazy', but in Greek, due to it not wanting to react to anything."],
    19: [(1,19), "Potassium", "A silvery alkali metal.#Once called Kalium. Still called Kalium in parts of Europe.#Oxygen potassium, boomer."],
    20: [(1,20), "Calcium", "A silvery alkali earth metal.#It, along with phosphorus, a couple halogens, and oxygen, make up a mineral called Apatite, which is found in teeth and bones, but also in rocks."],
    21: [(1,21), "Scandium", "A silvery rare earth metal.#Was discovered in Scandanavia."],
    22: [(1,22), "Titanium", "A silvery transition metal.#Alloyed with carbon to make a hard alloy."],
    23: [(1,23), "Vanadium", "A silvery transition metal.#Was named after the Norse goddess of fertility, Vanadís (Freyja)."],
    24: [(1,24), "Chromium", "A silvery transition metal.#Often electroplated onto things to make them 'chromed'.#Named after the many chromatic hues its ores have."],
    25: [(1,25), "Manganese", "A silvery transition metal.#Pronounced 'man-gan-ease'.#Named after magnetite (Fe3O4) and magnesia (MnO2), both called magnes in ancient Greek."],
    26: [(1,26), "Iron", "A silvery transition metal.#Once known as Ferrum.#The fourth most common element on Earth.#Used in many alloys, such as Steel (with carbon), and Invar (with nickel).#Known well for its red and black oxides."],
    27: [(1,27), "Cobalt", "A silvery transition metal.#Not actually blue. It has the same silvery gray that most transition elements have. Cobalt blue is actually a salt of cobalt and aluminium (CoAl2O4)."],
    28: [(1,28), "Nickel", "A silvery transition metal.#Used with iron in an alloy called Invar, but not used in nickels. Not anymore, anyway.#Meteoric Iron is a form of invar, which can be found in some asteroids."],
    29: [(1,29), "Copper", "An orange transition metal.#Once called Cuprium.#Used to make many alloys, notably with tin to make Bronze, or zinc to make Brass.#I smell pennies."],
    30: [(1,30), "Zinc", "A brittle silvery transition metal.#Zinc improves the health of your immune system.#Used with copper to make Brass."],
    31: [(1,31), "Gallium", "A silvery triel.#Melts in your hand.#Non-toxic, but don't eat it anyway."],
    32: [(1,32), "Germanium", "A silvery tetral crystal.#Was discovered in Germany.#Germanium dioxide is sometimes used in fiber optic cables."],
    33: [(1,33), "Arsenic", "A gray, yellow, or black pnictogen crystal.#It, and most of its compounds, are incredibly toxic and carcinogenic.#It has historically been used as a poison to assassinate people."],
    34: [(1,34), "Selenium", "A dark green-gray chalcogen crystal.#Known for its smelly compounds."],
    35: [(1,35), "Bromine", "A red-brown halogen liquid.#It evaporates at room temperature, forming a brown haze in its container. It doesn't boil at room temperature, however."],
    36: [(1,36), "Krypton", "A colorless noble gas.#Not to be confused with Kryptonite."],
    37: [(1,37), "Rubidium", "A silvery alkali metal.#Alkali metals explode in contact with water. This one explodes hot enough to ignite the hydrogen emitted in the reaction."],
    38: [(1,38), "Strontium", "A silvery alkali earth metal.#Named after Strontian, a village in Scotland where it was discovered."],
    39: [(1,39), "Yttrium", "A silvery rare earth metal.#One of many elements named after Ytterby, a town in Sweden.#Of all the elements discovered in Ytterby's quartz mine, this was the first."],
    40: [(1,40), "Zirconium", "A silvery transition metal.#Best known for the false diamond, Cubic Zirconia."],
    41: [(1,41), "Niobium", "A silvery transition metal.#Named after Niobe, daughter of Tantalus.#Once was named Columbium."],
    42: [(1,42), "Molybdenum", "A silvery transition metal.#Pronounced 'moe-lib-den-um'.#Molly be damned."],
    43: [(1,43), "Technetium", "A silvery transition metal.#Synthesized in a lab before it was discovered to be a trace element."],
    44: [(1,44), "Ruthenium", "A silvery pale-blue transition metal.#Platinum group elements tend to hang with each other.#Colored metals are so due to relativistic effects."],
    45: [(1,45), "Rhodium", "A silvery transition metal.#Platinum group elements tend to be considered 'noble', due to lack of reactivity in many cases."],
    46: [(1,46), "Palladium", "A silvery transition metal.#Named after the asteroid Pallas.#Used as a catylist."],
    47: [(1,47), "Silver", "A silvery transition metal.#Once called Argentium.#Some people consume silver and turn blue.#Alloyed with copper to make Billon, or gold to make Electrum."],
    48: [(1,48), "Cadmium", "A silvery transition metal.#Used to be used with nickel to make batteries.#Is quite toxic, and is falling out of use."],
    49: [(1,49), "Indium", "A silvery triel metal.#The softest natural non-alkali metal.#Named after the indigo spectral line it produces when burned."],
    50: [(1,50), "Tin", "A silvery tetral metal.#Once known as Stanium.#Alloyed with copper to make Bronze, or lead to make Solder.#Once used to make roofs, though it disentegrates after a while."],
    51: [(1,51), "Antimony", "A silvery pnictogen metal.#Once known as Stibium.#Often used for flameproofing."],
    52: [(1,52), "Tellurium", "A silvery chalcogen crystal.#Despite being a chalcogen like Oxygen, its helical crystalline structure doesn't oxidize."],
    53: [(1,53), "Iodine", "A purple halogen crystal.#It doesn't sublimate, that's a myth.#Most governments on Terra add iodine to table salt, as it's a necessary trace element."],
    54: [(1,54), "Xenon", "A colorless noble gas.#Named xeno, alien.#Despite being a noble gas, its electropositivity is high enough that fluorine and chlorine can steal a valence electron."],
    55: [(1,55), "Caesium", "A pale golden alkali metal.#The most electropositive element. Yes, even more electropositive than Francium.#The second is defined by the time it takes for its valence electron to interact 9.192 billion times."],
    56: [(1,56), "Barium", "A silvery alkali earth metal.#Named baryc, meaning heavy."],
    57: [(1,57), "Lanthanum", "A silvery rare earth metal.#The first of the Lanthanide series of rare earth metals."],
    58: [(1,58), "Cerium", "A silvery rare earth metal.#Named after the planet Ceres."],
    59: [(1,59), "Praseodymium", "A silvery rare earth metal.#Named Prasinos Didymos, leek-green twin."],
    60: [(1,60), "Neodymium", "A silvery rare earth metal.#Named Neo Didymos, new twin.#Alloys with iron and boron and is polarized to make a powerful magnet."],
    61: [(1,61), "Promethium", "A silvery rare earth metal.#Named after Prometheus, who brought the knowledge of fire to man, and was punished by being chained to a rock and having birds peck out his liver, for all eternity.#Is radioactive."],
    62: [(1,62), "Samarium", "A silvery rare earth metal.#Used to treat certain types of cancer."],
    63: [(1,63), "Europium", "A silvery rare earth metal.#Named after the continent of Europe.#Used in blue and red LEDs."],
    64: [(1,64), "Gadolinium", "A silvery rare earth metal.#Small amounts of gadolinium can soften alloys and increase oxidation resistance."],
    65: [(1,65), "Terbium", "A silvery rare earth metal.#One of many elements named after Ytterby, a town in Sweden.#Used in green LEDs."],
    66: [(1,66), "Dysprosium", "A silvery rare earth metal.#A thin sheet of it is used in some disks."],
    67: [(1,67), "Holmium", "A silvery rare earth metal.#Named after Stockholm in Sweden."],
    68: [(1,68), "Erbium", "A silvery rare earth metal.#One of many elements named after Ytterby, a town in Sweden."],
    69: [(1,69), "Thulium", "A silvery rare earth metal.#The sixty-ninth element. 'haha funny number xd' -someone, probably."],
    70: [(1,70), "Ytterbium", "A silvery rare earth metal.#One of many elements named after Ytterby, a town in Sweden.#Yttrium 2: Swedish Boogaloo."],
    71: [(1,71), "Lutetium", "A silvery rare earth metal.#The last of the Lanthanide series."],
    72: [(1,72), "Hafnium", "A silvery transition metal.#Used to soak up neutrons in nuclear reactors, as control rods."],
    73: [(1,73), "Tantalum", "A silvery transition metal.#Often used in capacitors and resistors."],
    74: [(1,74), "Tungsten", "A silvery transition metal.#Once known as Wolfram.#The densest natural element.#Has the highest melting point of the natural elements.#Used as incandescent bulb filaments."],
    75: [(1,75), "Rhenium", "A silvery transition metal.#Once known as Nipponium.#Ree."],
    76: [(1,76), "Osmium", "A silvery pale blue transition metal.#One of the rarest elements on Terra."],
    77: [(1,77), "Iridium", "A silvery transition metal.#Found on meteorites more often than in Terra rocks, as it is iron-loving, and sank into Terra's core."],
    78: [(1,78), "Platinum", "A silvery transition metal.#It has been used since ancient times, though it's not clear whether they knew that they had a OsIrPtAu alloy."],
    79: [(1,79), "Gold", "A yellow transition metal.#Once called Aurium.#Extremely malleable and pliable, it can be stretched into monatomic wire before snapping.#Commonly alloyed with silver to make Electrum."],
    80: [(1,80), "Mercury", "A silvery liquid transition metal.#Once called Hydrargyrum, meaning watery silver.#Most mercury compounds are neurotoxic.#A mercury alloy called Amalgam used to be used to fill cavities."],
    81: [(1,81), "Thallium", "A silvery triel metal.#Thallium was named 'green twig', but in Greek, for the green spectral line it produces when burned.#Thallium salts are tasteless and extremely toxic. They have been used to kill rats and humans."],
    82: [(1,82), "Lead", "A silvery tetral metal.#Once called Plumbium.#Used with tin to make an alloy called Solder.#Burning leaded gas in the 1950s caused a lead poisoning pandemic, which helped make two generations of agressive idiots."],
    83: [(1,83), "Bismuth", "A silvery pnictogen metal.#Bismuth subsalycilate will calm an upset stomach.#Known for the colorful crystals, the color is produced by a thin layer of oxide."],
    84: [(1,84), "Polonium", "A silvery chalcogen metal.#Named after Marie Curie's homeland, Poland."],
    85: [(1,85), "Astatine", "A dark purple halogen crystal.#The rarest element on Terra.#While solid at room temperature, it wouldn't stay at room temperature, quickly boiling off due to the heat produced from radioactivity."],
    86: [(1,86), "Radon", "A colorless noble gas.#Houses built over actinide deposits may have this leak into their basement. If not dealt with, could cause radiation poisoning."],
    87: [(1,87), "Francium", "A golden alkali metal.#One of the rarest elements on Terra. Only a few atoms exist at any one time.#Would melt in your hand, if it didn't explode first."],
    88: [(1,88), "Radium", "A silvery alkali earth metal.#It glows green.#People used to put radium compound on watch faces to get them to glow."],
    89: [(1,89), "Actinium", "A silvery rare earth metal.#The first of the Actinide series of rare earth metals.#Glows in the dark!"],
    90: [(1,90), "Thorium", "A silvery rare earth metal.#Named after Thor, Norse god of thunder.#Being explored as a possible replacement for uranium in fission plants."],
    91: [(1,91), "Protactinium", "A dull silvery rare earth metal.#Nuclear waste. Useless!"],
    92: [(1,92), "Uranium", "A dull silvery rare earth metal.#Named after Uranus.#The first radioactive element discovered.#The most common fission fuel.#Used to make most nuclear bombs."],
    93: [(1,93), "Neptunium", "A dull silvery rare earth metal.#Named after Neptune.#Used to breed Plutonium. That's it."],
    94: [(1,94), "Plutonium", "A dull silvery rare earth metal.#Named after Pluto.#Often used in nuclear research. And bombs, of course.#The heaviest natural element."],
    95: [(1,95), "Americium", "A dull silvery rare earth metal.#Named after the United States of America, the land of fat and McDonalds.#Used in some smoke detectors."],
    96: [(1,96), "Curium", "A dull silvery rare earth metal.#Named after Marie and Pierre Curie.#Glows in the dark!"],
    97: [(1,97), "Berkelium", "A dull silvery rare earth metal.#Named after the city of Berkely in California."],
    98: [(1,98), "Californium", "A dull silvery rare earth metal.#Named after the state of California."],
    99: [(1,99), "Einsteinium", "A dull silvery rare earth metal.#Named after Albert Einstein.#Period seven elements appear dull due electrons moving close to the speed of light.#The last element we've produced a visible sample of."],
   100: [(1,100), "Fermium", "A dull silvery rare earth metal.#Named after Enrico Fermi.#Discovered in the fallout of the first fusion bomb."],
   101: [(1,101), "Mendelevium", "A dull silvery rare earth metal.#Named after Dmitri Mendeleev."],
   102: [(1,102), "Nobelium", "A dull silvery rare earth metal.#Named after Alfred Nobel."],
   103: [(1,103), "Lawrencium", "A dull silvery rare earth metal.#Named after Ernest Lawrence."],
   104: [(1,104), "Rutherfordium", "A dull silvery transition metal.#Named after Ernest Rutherford."],
   105: [(1,105), "Dubnium", "A dull silvery transition metal.#Named after Dubna in Russia."],
   106: [(1,106), "Seaborgium", "A dull silvery transition metal.#Named after Glenn Seaborg.#The densest element without a G-shell, with the highest melting point."],
   107: [(1,107), "Bohrium", "A dull silvery transition metal.#Named after Niels Bohr."],
   108: [(1,108), "Hassium", "A dull silvery pale blue transition metal.#Named after the German state of Hesse."],
   109: [(1,109), "Meitnerium", "A dull silvery transition metal.#Named after Lise Meitner."],
   110: [(1,110), "Darmstadtium", "A dull silvery transition metal.#Named after Darmstadt, Germany."],
   111: [(1,111), "Roentgenium", "A silvery transition metal.#Named after Wilhelm Röntgen."],
   112: [(1,112), "Copernicium", "A dull silvery liquid transition metal.#Named after Nicolaus Copernicus."],
   113: [(1,113), "Nihonium", "A dull silvery triel metal.#Named after Japan."],
   114: [(1,114), "Flerovium", "A dull silvery liquid tetral metal.#Named after the Flerov Laboratory of Nuclear Reactions in Dubna, Russia."],
   115: [(1,115), "Moscovium", "A dull silvery pnictogen metal.#Named after Moscow, Russia."],
   116: [(1,116), "Livermorium", "A dull silvery chalcogen metal.#Named after Livermore, California."],
   117: [(1,117), "Tennessine", "A deep violet halogen metal.#Named after the state of Tennessee."],
   118: [(1,118), "Oganesson", "A white noble ice.#Named after Yuri Oganessian.#The last element discovered as of 2022."],
   119: [(1,119), "Ununennium", "A dull golden liquid alkali metal.#The provisional name means 'one hundred nineteen'.#The first liquid alkali.#Odd elements tend to be less stable.#Will likely be the 121st element to be discovered."],
   120: [(1,120), "Unbinilium", "A dull silvery alkali earth metal.#The provisional name means 'one hundred twenty'.#Even elements tend to be more stable.#Will likely be the 119th element to be discovered."],
   121: [(1,121), "Unbiunium", "A dull silvery rare earth metal.#The provisional name means 'one hundred twenty-one'.#Will likely be the 123rd element to be discovered.#An atom of Ubu is larger than Cs, and is easier to ionize."],
   122: [(1,122), "Unbibium", "A dull silvery rare earth metal.#The provisional name means 'one hundred twenty-two'.#Will likely be the 120th element to be discovered."]
    }

commonCards = [8, 11, 12, 13, 14, 19, 20, 26] #>10000ppm
uncommonCards = [1, 9, 6, 15, 16, 17, 22, 23, 24, 25, 38, 40, 50, 55, 56] #9999ppm - 100ppm
rareCards = [3, 4, 5, 7, 18, 21, 27, 28, 29, 30, 31, 32, 33, 35, 37, 39, 41, 42, 57, 58, 59, 60, 62, 63, 64, 65, 66, 67, 68, 70, 72, 73, 74, 82, 90, 92] #99ppm - 1ppm
epicCards = [2, 10, 34, 44, 45, 46, 47, 48, 49, 51, 52, 53, 69, 71, 76, 77, 78, 79, 80, 81, 83] #999ppb - 1ppb
legendaryCards = [36, 54, 75, 88, 91, 43, 61, 84, 85, 86, 87, 89, 93, 94] #<999ppt
mythicalCards = [95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122] #synthetic

def generateCard(ID=None):
    shinyDice = randrange(100)
    rarityDice = randrange(100)
    cardbase = "cardbase"
    if ID == None:
        card = None
        rarity = None
        if rarityDice <= 50:
            rarity = "common"
            if shinyDice < 2: cardbase += "-shiny"
            card = choice(commonCards)
        elif 50 < rarityDice <= 75:
            rarity = "uncommon"
            if shinyDice < 3: cardbase += "-shiny"
            card = choice(uncommonCards)
        elif 75 < rarityDice <= 88:
            rarity = "rare"
            if shinyDice < 5: cardbase += "-shiny"
            card = choice(rareCards)
        elif 88 < rarityDice <= 94:
            rarity = "epic"
            if shinyDice < 9: cardbase += "-shiny"
            card = choice(epicCards)
        elif 94 < rarityDice <= 98:
            rarity = "legendary"
            if shinyDice < 16: cardbase += "-shiny"
            card = choice(legendaryCards)
        elif 98 < rarityDice:
            rarity = "mythical"
            if shinyDice < 29: cardbase += "-shiny"
            card = choice(mythicalCards)
    else:
        rarity = "debug"
        card = int(ID)
    return [cardbase, rarity, card]

def getCard(args):
    nameFont = ImageFont.truetype('.\\assets\\fonts\\Nebula-Regular.otf', 18)
    rarityFont = ImageFont.truetype('.\\assets\\fonts\\Nebula-Regular.otf', 12)
    descFont = ImageFont.truetype('.\\assets\\fonts\\courbd.ttf', 12)
    rarityColors = {
        "debug": (128,0,255),
        "common": (0,0,0),
        "uncommon": (0,255,0),
        "rare": (0,0,255),
        "epic": (255,0,255),
        "legendary": (255,0,0),
        "mythical": (128,64,0)
        }

    descText = "* " + cards[args[2]][2].replace("#", "\n* ")
    lines = descText.split("\n")
    newText = []
    for line in lines:
        words = line.split()
        newlines = [""]
        index = 0
        for word in words:
            if len(newlines[index] + word + " ") <= 31:
                newlines[index] += word + " "
            else:
                newlines.append("  " + word + " ")
                index += 1
        newText.append("\n".join(newlines))
    descText = "\n".join(newText)
    with Image.open(".\\assets\\images\\cards\\" + args[0] + ".png") as card:
        image = Image.open(".\\assets\\images\\cards\\cardimgs\\" + cards[args[2]][1] + ".png")
        card.paste(image, (13,38))
        cardEditor = ImageDraw.Draw(card)
        cardEditor.text((8,8), cards[args[2]][1], (0, 0, 0), font=nameFont)
        cardEditor.text((8,164), args[1], rarityColors[args[1]], font=rarityFont)
        cardEditor.text((8,177), descText, (0, 0, 0), font=descFont)
        cardEditor.text((8,300), f"ID-{str(cards[args[2]][0][1]).rjust(6, '0')}", (0, 0, 0), font=rarityFont)
        cardEditor.text((170,300), f"S{cards[args[2]][0][0]} #{str(cards[args[2]][0][1]).rjust(3, '0')}", (0, 0, 0), font=rarityFont)
        card.save(".\\temp\\card.png")

def generatePack(cards=10):
    pack = []
    for i in range(cards):
        pack.append(generateCard())
    return pack

def getPack(args):
    rows = min(5, len(args)//-5*-1)
    packImg = Image.new(mode="RGBA", size=(240*5,320*rows))
    def sortKey(key):
        return int(key[2])
    args.sort(key=sortKey)
    for i in range(len(args)):
        getCard(args[i])
        card = Image.open(".\\temp\\card.png")
        packImg.paste(card, (240*(i%5), 320*(i//5)))
    packImg.save(".\\temp\\pack.png")
