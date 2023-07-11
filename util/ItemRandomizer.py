from random import randrange, choice
from os import system
from time import sleep
# Zako source code ©2023 Noobly Walker, ©2023 OmniCoreStudios
from util.SLHandle import *
from util.expol import expol
from util.cmdutil import cmdutil
from util.PotionRandomizer import potion_randomizer, comboCount

text = cmdutil()

#define materials
text.log("[ITEMGEN] Gathering standard material library...")

valueMats = ["copper", "silver", "gold", "platinum", "glass"]
rareValueMats = ["nickel", "ruthenium", "rhodium", "palladium", "osmium", "iridium"]
valueAlloys = ["billon", "electrum", "sandia", "corinthian bronze", "hepatizon",
               "sterling silver", "platinum sterling"]

ancientToolMats = ["oak wood", "birch wood", "maple wood", "pine wood", "spruce wood",
                   "acacia wood", "mahogany wood", "mangrove wood", "bone", "granite",
                   "andesite", "dacite", "diorite", "basalt", "sandstone", "shale",
                   "slate", "serpentine", "tuff", "rhyolite", "dolomite"
                   "copper", "tin", "bronze", "iron", "cast iron", "steel"]
modernToolMats = ["titanium", "vanadium", "titanium carbide", "tungsten", "tungsten carbide",
                  "carbon fiber", "aluminium"]

gems = ["[COLOR] quartz", "amethyst", "ruby", "emerald", "topaz", "[COLOR] sapphire",
        "[COLOR] diamond", "lapis lazuli", "[COLOR] agate", "amber", "garnet", "opal",
        "carmelite", "amazonite", "tiger eye", "aventurine",
        "obsidian", "aquamarine", "onyx", "pearl", "citrine",
        "peridot", "turquoise", "tanzanite", "jade", "fluorite", "iolite",
        "moonstone", "malachite", "rose quartz", "smoky quartz", "spinel",
        "[COLOR] zircon", "[COLOR] tourmaline", "aragonite"]

text.log("[ITEMGEN] Extending library...")
text.log("[ITEMGEN] Bending physics...")

metalsMinusHalides = ["lithium", "beryllium", "boron", "carbon", "sodium", "magnesium",
                      "aluminium", "silicon", "phosphorus", "sulphur",
                      "potassium", "calcium", "scandium", "titanium", "vanadium", "chromium",
                      "manganese", "iron", "cobalt", "nickel", "copper", "zinc",
                      "gallium", "germanium", "arsenic", "selenium", "rubidium", "strontium",
                      "yttrium", "zirconium", "niobium", "molybdenum", "technetium",
                      "ruthenium", "rhodium", "palladium", "silver", "cadmium", "indium",
                      "tin", "antimony", "tellurium", "caesium", 
                      "barium", "lanthanum", "cerium", "praseodymium", "neodymium",
                      "promethium", "samarium", "europium", "gadolinium", "terbium",
                      "dysprosium", "holmium", "erbium", "thulium", "ytterbium", "lutetium",
                      "hafnium", "tantalum", "tungsten", "rhenium", "osmium", "iridium",
                      "platinum", "gold", "mercury", "thallium", "lead", "bismuth",
                      "polonium", "francium", "radium", "actinium", "thorium",
                      "protactinium", "uranium", "neptunium", "plutonium", "americium",
                      "curium", "berkelium", "californium", "einsteinium", "fermium",
                      "mendelevium", "nobelium", "lawrencium", "rutherfordium", "dubnium",
                      "seaborgium", "bohrium", "hassium", "meitnerium", "darmstadtium",
                      "roentgenium", "copernicium", "nihonium", "flerovium", "moscovium", "livermorium",
                      "ununennium", "unbinilium", "unbiunium", "unbibium"]

metalsMinusChalcides = ["lithium", "beryllium", "boron", "carbon", "sodium", "magnesium",
                          "aluminium", "silicon", "phosphorus",
                          "potassium", "calcium", "scandium", "titanium", "vanadium", "chromium",
                          "manganese", "iron", "cobalt", "nickel", "copper", "zinc",
                          "gallium", "germanium", "arsenic", "rubidium", "strontium",
                          "yttrium", "zirconium", "niobium", "molybdenum", "technetium",
                          "ruthenium", "rhodium", "palladium", "silver", "cadmium", "indium",
                          "tin", "antimony", "caesium", 
                          "barium", "lanthanum", "cerium", "praseodymium", "neodymium",
                          "promethium", "samarium", "europium", "gadolinium", "terbium",
                          "dysprosium", "holmium", "erbium", "thulium", "ytterbium", "lutetium",
                          "hafnium", "tantalum", "tungsten", "rhenium", "osmium", "iridium",
                          "platinum", "gold", "mercury", "thallium", "lead", "bismuth",
                          "francium", "radium", "actinium", "thorium",
                          "protactinium", "uranium", "neptunium", "plutonium", "americium",
                          "curium", "berkelium", "californium", "einsteinium", "fermium",
                          "mendelevium", "nobelium", "lawrencium", "rutherfordium", "dubnium",
                          "seaborgium", "bohrium", "hassium", "meitnerium", "darmstadtium",
                          "roentgenium", "copernicium", "nihonium", "flerovium", "moscovium",
                          "ununennium", "unbinilium", "unbiunium", "unbibium"]

chalcides = ["oxide", "sulphide", "selenide", "telluride", "polonide", "livermoride"]
halides = ["hydride", "fluoride", "chloride", "bromide", "iodide", "astatide", "tennesside"]

elementsExt = ["lithium", "beryllium", "boron", "carbon", "sodium", "magnesium",
               "aluminium", "silicon", "red phosphorus", "white phosphorus", "black phosphorus",
               "sulphur", "potassium", "calcium", "scandium", "titanium", "vanadium", "chromium",
               "manganese", "iron", "cobalt", "nickel", "copper", "zinc",
               "gallium", "germanium", "arsenic", "selenium", "rubidium", "strontium",
               "yttrium", "zirconium", "niobium", "molybdenum", "technetium",
               "ruthenium", "rhodium", "palladium", "silver", "cadmium", "indium",
               "tin", "antimony", "tellurium", "iodine", "caesium", 
               "barium", "lanthanum", "cerium", "praseodymium", "neodymium",
               "promethium", "samarium", "europium", "gadolinium", "terbium",
               "dysprosium", "holmium", "erbium", "thulium", "ytterbium", "lutetium",
               "hafnium", "tantalum", "tungsten", "rhenium", "osmium", "iridium",
               "platinum", "gold", "thallium", "lead", "bismuth",
               "polonium", "astatine", "francium", "radium", "actinium", "thorium",
               "protactinium", "uranium", "neptunium", "plutonium", "americium",
               "curium", "berkelium", "californium", "einsteinium", "fermium",
               "mendelevium", "nobelium", "lawrencium", "rutherfordium", "dubnium",
               "seaborgium", "bohrium", "hassium", "meitnerium", "darmstadtium",
               "roentgenium", "nihonium", "moscovium", "livermorium", "tennessine",
               "oganesson", "unbinilium", "unbiunium", "unbibium"]

elementsExt2 = ["hydrogen metal", "solid mercury", "solid copernicium", "solid flerovium",
                "solid ununennium"]

text.log("[ITEMGEN] Putting gasses in the freezer...")

icesExt = ["hydrogen ice", "helium ice", "nitrogen ice", "oxygen ice",
           "ozone ice", "fluorine ice", "neon ice", "chlorine ice", "argon ice",
           "bromine ice", "krypton ice", "xenon ice", "radon ice", "methane ice",
           "ethane ice", "propane ice", "butane ice", "ammonia ice", "hydrazine ice",
           "water ice", "dry ice", "deuterium ice", "heavy water ice", "tritium ice"]

text.log("[ITEMGEN] Digging deeper...")

oresExt = ["acanthite", "barite", "bauxite", "[COLOR] beryl", "bornite", "cassiterite",
           "chalcocite", "chalcopyrite", "chromite", "cinnabar", "cobaltite",
           "coltan", "galena", "hematite", "ilmenite", "magnetite", "malachite",
           "molybdenite", "pentlandite", "pollucite", "pyrolusite", "scheelite",
           "smithsonite", "sperrylite", "sphalerite", "uraninite", "wolframite",
           "selenite", "plutonite", "franciscite", "ringwoodite", "rutile", "stibnite",
           "stannite", "bismuthinite", "lepidolite", "smaltite", "carrolite",
           "linnaeite", "covellite", "chalcocite", "cuprite", "azurite",
           "goethite", "limonite", "banded iron", "cerussite", "spodumene",
           "manganite", "braunite", "powellite", "garnierite", "niccolite",
           "pyrochlore", "columbite", "sperrylite", "bastnasite", "monazite",
           "xenotime", "eudialyte", "allanite", "argentite", "pitchblende",
           "carnotite", "patronite", "roscoelite", "smithsonite", "fluorospar",
           "gypsum", "feldspar", "franciscite"]

text.log("[ITEMGEN] Collecting random materials...")

alloysExt = ["brass", "meteoric iron", "amalgam", "pewter", "teflon", "duralumin",
             "magnalium", "magthor", "lockalloy", "rose metal", "nichrome", "ferrochrome",
             "megallium", "stellite", "constantan", "nordic gold", "invar", "german silver",
             "pig iron", "solder", "elektron", "britannium", "staballoy", "rolled gold",
             "dutch metal", "delta metal", "munz metal", "monel metal", "type metal",
             "stainless steel", "nickel steel"]

randomMatsExt = ["paper", "graphite", "anthracite", "bitumen", "lignite", "peat",
                 "polytetrafluoroethylene", "depleted uranium", "enriched uranium",
                 "polyvinyl chloride", "low density polyethylene", "high density polyethylene",
                 "polypropylene", "polystyrene", "polyethylene terephthalate", "polyurethane",
                 "isoprene", "styrene-butadiene", "butyl rubber", "nitrile", "neoprene",
                 "ethylene propylene diene monomer", "silicone", "viton", "latex",
                 "cardboard", "putty", "clay", "teracotta", "concrete", "silk", "leather",
                 "keratin", "ivory", "polyester", "cotton", "denim", "jute", "grass", "hemp"]

bioMatsExt = ["cystine", "cysteine", "phenylalanine", "tyrosine", "tryptophan", "aspartic acid",
              "isoleucine", "leucine", "alanine", "methionine", "glutamic acid", "serine",
              "valine", "proline", "arginine", "asparagine", "lysine", "hystidine", "glutamine",
              "threonine", "hydroxyproline", "glucose", "fructose", "sucrose", "galactose",
              "high density lipoprotein", "low density lipoprotein", "very low density lipoprotein",
              "retinol ice", "thiamine", "riboflavin", "niacin", "pantothenic acid", "pyridoxine",
              "biotin", "folic acid", "cobalamin", "ascorbic acid", "cholecalciferol",
              "tocopherol ice", "phylloquinone", "phosphatidylcholine", "phosphatidylethanolamine",
              "phosphatidylserine", "phosphatidylinositol", "adenine", "cytosine", "thymine",
              "guanine", "uracil", "acetylcholine", "dopamine", "serotonin", "gamma-aminobutyric acid",
              "glutamate", "epinephrine", "norepinephrine", "histamine", "insulin", "cortisol",
              "testosterone", "estrogen", "progesterone", "thyroxine", "triiodothyronine", "melatonin",
              "somatotrophin", "prolactin", "follitropin", "thyrotropin"]

text.log("[ITEMGEN] Escaping into the hyperverse...")

mythicalExt = ["mithril", "adamantite", "orichalcum", "uru", "eridium"]

terrariaExt = ["chlorophyte", "spectre", "luminite", "shroomite", "crimtane", "demonite",
               "hellstone"]

minecraftExt = ["crimson wood", "warped wood", "netherite", "prismarine", "endstone", "netherrack",
                "soulstone"]

starboundExt = ["aegisalt", "violium", "rubium", "solarium", "durasteel", "erchius", "core fragment"]

marvelExt = ["vibranium"]

dcExt = ["kryptonite"]

startrekExt = ["dilithium", "trilithium", "tritanium", "duranium"]

starwarsExt = ["[COLOR] kyber crystal"]

tf2Ext = ["australium", "moustachium"]

stargateExt = ["naquedah"]

scpExt = ["telekill alloy"]

starmadeExt = ["tekt", "larimar", "lukrah", "varis", "sugil", "chabaz", "macet", "sapsun", "zercaner",
               "hylat", "threns", "fertikeen", "sertise", "jisper"]

starmadeGemsExt = ["nocx", "parseen", "mattise", "varat", "hattel", "bastyn", "rammet", "sintyr"]

snrpExt = ["magsic", "majestic", "drakonite", "megasteel",
           "gigasteel", "terasteel", "petasteel", "exasteel", "zetasteel",
           "yottasteel", "aethersteel", "neutronium", "dark matter", "red matter",
           "meta alloy", "infinity alloy", "eternity alloy", "revivtia", "torpitia",
           "sectria", "veiltia", "foritia", "astria", "metia", "mulltria", "sievertia",
           "becquetria", "necrophyte"]

snrpIcesExt = ["kelvon ice", "ghaline ice", "soltia ice", "appoltia ice",
               "phoebtia ice", "raytia ice", "moderntia ice", "novetia ice",
               "mintia ice", "slotia ice", "indolentia ice", "loaftia ice",
               "scartia ice", "waldtia ice", "exotia ice", "geigtia ice"]

#Ender has given permission to use these materials.
enderfanExt = ["ghaliston", "ghalaqua", "ghaelström", "ghytriea", "ghestgon",
               "ghastroniue", "ghargent", "ghabold", "ghalice", "ghalflora positive",
               "ghalflora negative", "ghahogeny", "ghagika", "ghalinferno", "ghacid",
               "ghastrite"]

#waferExt = ["camo alloy"]

compositable = [*set([*elementsExt2, *oresExt, *gems, *enderfanExt, *starwarsExt,
                 *dcExt, *bioMatsExt, *randomMatsExt, *mythicalExt, *tf2Ext,
                 *terrariaExt, *minecraftExt, *marvelExt, *snrpExt, *snrpIcesExt,
                 *startrekExt, *icesExt, *scpExt, *stargateExt, *starmadeExt,
                 *starmadeGemsExt])]

text.log("[ITEMGEN] Applying salt...")

def salt():
    i = choice(halides)
    j = choice(metalsMinusHalides)
    return f"{j} {i}"

text.log("[ITEMGEN] Rusting metal...")

def oxide():
    i = choice(chalcides)
    j = choice(metalsMinusChalcides)
    return f"{j} {i}"

text.log("[ITEMGEN] Mixing alloys...")

def alloy():
    i = choice(metalsMinusChalcides)
    j = choice(metalsMinusChalcides)
    return f"{j}-{i} alloy"

text.log("[ITEMGEN] Fabricating composites...")

def comp():
    i = choice(compositable)
    j = choice(compositable)
    return f"{j}-{i} composite"

text.log("[ITEMGEN] Categorizing rock collection...")

gemMats = [*gems, *oresExt, *icesExt, *snrpIcesExt, *enderfanExt, *starwarsExt, *dcExt, *bioMatsExt,
           *starmadeGemsExt, salt()]
functionArray = [alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(),
                 alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp(), alloy(), salt(), oxide(), comp()]

chaosModeMats = [*set([*valueMats, *rareValueMats, *valueAlloys, *ancientToolMats, *modernToolMats,
                 *elementsExt, *elementsExt2, *oresExt, *gemMats, *bioMatsExt, *starmadeExt,
                 *randomMatsExt, *mythicalExt, *terrariaExt, *minecraftExt, *marvelExt, *starmadeGemsExt,
                 *snrpExt, *snrpIcesExt, *enderfanExt, *startrekExt,
                 *icesExt, *scpExt, *stargateExt, *tf2Ext]), *functionArray]

#define enchantments and curses
text.log("[ITEMGEN] Applying magical runes...")

genericEnchants = ["unbreaking", "mending"]
weaponMeleeEnchants = ["sharp", "smiting", "arthropodicidal", "efficient", "lucky",
                       "flaming", "impaling", "punching", "sweeping", "channeling",
                       "loyal", "piercing", "powerful", "vorpal", *genericEnchants]
weaponRangedEnchants = ["ammo conserving", "accurate", *weaponMeleeEnchants]
armorEnchants = ["amphibious", "blast resistant", "depth striding", "feather falling",
                 "fire resistant", "frost walking", "projectile resistant", "sturdy",
                 "aerated", "thorny", "light", *genericEnchants]
toolEnchants = ["efficient", "lucky", "silky", *genericEnchants]

genericCurses = ["vanishing", "breaking"]
weaponMeleeCurses = ["arachnophobic", "inefficient", "self-igniting", "unlucky", "hydrophobic",
                "soft", "dull", "thanatophobic", "dragging", *genericCurses]
weaponRangedCurses = ["ammo wasting", "inaccurate", *weaponMeleeCurses]
armorCurses = ["hydrophobic", "explodable", "pressured", "heavy", "flammable",
               "holey", "drowning", "bulky", "leeching", "binding", *genericCurses]
toolCurses = ["inefficient", "unlucky", *genericCurses]

allEffects = [*set([*weaponMeleeEnchants, *weaponRangedEnchants, *armorEnchants, *toolEnchants,
                    *weaponMeleeCurses, *weaponRangedCurses, *armorCurses, *toolCurses])]

# define gem shapes
text.log("[ITEMGEN] Cutting gems...")

gemCuts = ["single", "swiss", "briolette", "drop", "scissor", "portugese rose", "trap",
           "fire rose", "zinnia", "bead", "sphere", "zircon", "marigold", "sunflower",
           "dahlia", "point", "french", "table", "lozenge", "trapeze", "long octagon",
           "shield", "keystone", "bevel", "triangle"]

gemColors = ["", "red", "orange", "yellow", "green", "cyan", "blue", "purple", "brown", "black"]

# define artworks
text.log("[ITEMGEN] Painting on the cave wall...")

nounsSingular = ["a man", "a woman", "a child", "a dragon", "a bird", "a dog", "a horse", "a dwarf", "an elf",
                 "a cat", "a lizard", "a fox", "a kitsune", "an eldritch being"]
nounsPlural = ["men", "women", "children", "dragons", "birds", "dogs", "horses", "dwarves", "elves", "cats",
               "lizards", "foxes", "kitsunes", "eldritch beings"]
pluralCounts = ["two ", "three ", "four ", "five ", "many "]
objectiveVerbs = ["fighting", "protecting", "watching", "feeding", "following", "trying to escape", "sitting with"]
subjectiveVerbs = ["sitting", "running", "striking a pose", "smiling", "frowning", "sleeping"]
adjectives = ["heroic", "defensive", "casual", "weak", "friendly", "bored", "tired", "weary", "hopeful",
              "scared"]
settings = ["in a town", "in a city", "in a forest", "in a cave", "in an open plain", "on a mountaintop"]
structs = ["[NOUN0] [OBJV] [NOUN1]", "[NOUN0] [SUBV]", "[NOUN0] [SUBV]. They appear [ADJ]",
           "[NOUN0] [OBJV] [NOUN1] [SET]", "[NOUN0] [SUBV] [SET]", "[NOUN0] [SUBV] [SET]. They appear [ADJ]"]

#define shapes

text.log("[ITEMGEN] Hiring a VERY crazy dwarf...")
sleep(1)

tools = ["hatchet", "axe", "pickaxe", "shovel", "hoe", "scythe", "hammer", "saw", "shears", "bolt cutters"]
weaponsMelee = ["sword", "halberd", "spear", "trident", "dagger", "pike", "warhammer", "waraxe", "protosaber",
                "lightsaber", "lightdagger", "lightpike", "cerimonial dagger", "bat'leth"]
weaponsRanged = ["bow", "longbow", "crossbow", "sling", "boomerang", "pistol", "carbine", "revolver",
                 "dragoon", "blunderbuss", "shotgun", "assault rifle", "sniper rifle", "gauss rifle",
                 "railgun", "machine gun", "submachine gun", "plasma pistol", "plasma rifle", "tesla gun",
                 "rocket-propelled grenade launcher", "proton beam", "bazooka", "laser pistol", "laser rifle"]
ammo = ["arrow", "crossbow bolt", "sling stone", "pistol ammo", "blunderbuss shot", "shotgun shell",
        "rifle ammo", "EM rod", "plasma cell", "battery", "rocket-propelled grenade", "grenade",
        "pipe bomb", "smoke grenade", "flashbang", "bazooka rocket"]
batteries = ["lead-acid battery", "nickel-cadmium battery", "alkali battery", "lithium battery",
             "lithium ion battery", "sodium ion battery", "nickel metal hydride battery",
             "zinc-carbon battery"]
armor = ["helmet", "chestplate", "pair of leggings", "pair of boots", "pair of gauntlets", "shield",
         "pair of pauldrons", "belt", "fabric hat", "fabric shirt", "fabric scarf", "fabric pants",
         "fabric underwear", "fabric socks", "fabric shoes", "fabric shorts", "fabric coat",
         "fabric gloves"]
jewelry = ["amulet", "pendant", "necklace", "charm", "bracelet", "ring", "circlet", "crown"]
trinkets = ["token", "key", "tetrahedral die", "hexahedral die", "octahedral die",
            "decahedral die", "icosahedral die", "coin", "doll", "goblet", "mug", "plate", "platter",
            "bowl", "fork", "spoon", "knife", "spork", "spatula", "whisk", "pot", "pan"]
potions = ["vial", "bottle", "flask"]
artworks = ["statue", "painting", "drawing", "photograph", "carving", "hologram"]
furnitures = ["table", "slab", "chair", "throne", "coffin", "coffer", "chest", "box",
              "bookshelf", "bench", "bed", "cot", "hutch", "coffee table", "end table",
              "hearth", "lamp", "lantern", "cabinet", "china cabinet", "display case",
              "dining table", "night stand", "chest of drawers"]

types = {"tool": tools, "melee": weaponsMelee, "ranged": weaponsRanged, "ammo": ammo,
         "armor": armor, "jewelry": jewelry,
         "trinket": trinkets, "potion": potions, "artwork": artworks, "furniture": furnitures}

allShapes = [*tools, *weaponsMelee, *weaponsRanged, *ammo, *armor, *jewelry, *trinkets,
             *potions, *artworks, *furnitures]

#define modifier adjectives

text.log("[ITEMGEN] Training craftsdwarf...")

craftMods = ["shoddy", "poor quality", "average", "fine", "masterwork"]
wearMods = ["brand new", "slightly used", "damaged", "broken"]
grimeMods = ["immaculate", "dusty", "dirty", "grimy", "eroded"]

text.log("[ITEMGEN] Cooking books...")

counts = ["no", "a", "two of", "three of", "four of", "five of", "six of", "seven of", "eight of", "nine of",
          "ten of", "eleven of", "twelve of", "thirteen of", "fourteen of", "fifteen of"]

simpleMatCount = len(chaosModeMats) - len(functionArray)
saltsCount = len(halides) * len(metalsMinusHalides)
oxidesCount = len(chalcides) * len(metalsMinusChalcides)
alloysCount = len(metalsMinusChalcides) * (len(metalsMinusChalcides)-1) // 2
compositesCount = len(compositable) * (len(compositable)-1) // 2
materialCount = expol(simpleMatCount + saltsCount + oxidesCount + alloysCount + compositesCount -36 -8 + 8*len(gemColors))
weaponMeleeStates = len(weaponsMelee) * (len(weaponMeleeCurses) + len(weaponMeleeEnchants)) ** 2
weaponRangedStates = len(weaponsRanged) * (len(weaponRangedCurses) + len(weaponRangedEnchants)) ** 2
toolStates = len(tools) * (len(toolCurses) + len(toolEnchants)) ** 2
armorStates = (len(armor) + len(jewelry)) * (len(armorCurses) + len(armorEnchants)) ** 2

artSubjects = len(nounsSingular) * (len(pluralCounts)+1)
artTwoParty = artSubjects**2 * len(objectiveVerbs) * (len(settings)+1)
artOneParty = artSubjects * len(subjectiveVerbs) * (len(settings)+1) * (len(adjectives)+1)

artStates = len(artworks) * (artTwoParty + artOneParty)
potionStates = len(potions) * comboCount()
otherStates = len(trinkets)*5 + len(furnitures) + (len(ammo)+len(batteries)-1)*15 + len(artworks)
gemStates = (len(gemMats)-8 + 8*len(gemColors)) * len(gemCuts) + 1
totalPossibleItems = expol(materialCount**2 * (weaponMeleeStates + weaponRangedStates + toolStates + armorStates + \
                     artStates + potionStates + otherStates) * len(craftMods) * len(wearMods) * len(grimeMods) * gemStates * \
                     (artTwoParty + artOneParty + 1))

text.log(f"[ITEMGEN] Loaded {materialCount:i.3} materials.")
text.log(f"[ITEMGEN] Loaded {len(allEffects)} effects.")
text.log(f"[ITEMGEN] Loaded {len(allShapes)} objects of {len(types.keys())} types.")
text.log(f"[ITEMGEN] This generator will be able to create {totalPossibleItems:i.3} unique items.")

listMode = False
insanityMode = True

def getMaterial(materialList):
    material = choice(materialList)
    if material == "salt": material = choice(saltsExt)
    if material == "alloy": material = choice(alloysExt)
    if material == "oxide": material = choice(oxidesExt)
    if material == "comp": material = choice(compositeExt)
    if material == "battery": material = choice(batteries)
    return material.replace("[COLOR]", choice(gemColors))

def itemGenerator(ctx, selectedType, potionMods):
    if selectedType not in types.keys() and selectedType not in ["any", "info"]:
        return "Invalid type."
        
    description = ""
    if selectedType == "any":
        selectedType = choice(list(types.keys()))
    if selectedType != "info":
        item = choice(types[selectedType])
        opulence = False
        gem = None
        effect = ""
        effectStatus = ""
        artDesc = ""
        trim = None
        contents = None

        #choose if opulent
        if selectedType != "jewelry" and randrange(5) == 0:
            if not insanityMode: materialList = valuableMats
            else: materialList = chaosModeMats
            material = getMaterial(materialList)
            opulence = True
        if selectedType == "jewelry" or opulence:
            if randrange(2) == 0:
                cut = choice(gemCuts) + "-cut "
                if insanityMode: gem = getMaterial(gemMats)
                else: gem = getMaterial(gems)
                gem = cut + gem
        if opulence: opulence = "opulent "
        if not opulence: opulence = ""

        # get another material for trim
        if randrange(5) == 0:
            if insanityMode: trim = getMaterial(chaosModeMats)
            else: trim = getMaterial(valuableMats)

        #is art
        if selectedType == "artwork" or (opulence and randrange(20) == 0):
            artDesc = choice(structs)
            if randrange(2) == 0: artDesc = artDesc.replace("[NOUN0]", choice(nounsSingular))
            else: artDesc = artDesc.replace("[NOUN0]", choice(pluralCounts)+choice(nounsPlural))
            if randrange(2) == 0: artDesc = artDesc.replace("[NOUN1]", choice(nounsSingular))
            else: artDesc = artDesc.replace("[NOUN1]", choice(pluralCounts)+choice(nounsPlural))
            artDesc = artDesc.replace("[OBJV]", choice(objectiveVerbs))
            artDesc = artDesc.replace("[SUBV]", choice(subjectiveVerbs))
            artDesc = artDesc.replace("[ADJ]", choice(adjectives))
            artDesc = artDesc.replace("[SET]", choice(settings))

        #is potion
        if selectedType == "potion":
            contents = potion_randomizer(ctx, potionMods)

        #fill out remaining modifiers
        craftwork = choice(craftMods)
        wearing = choice(wearMods)
        filthiness = choice(grimeMods)

        # Set material, if not already set
        if insanityMode: material = getMaterial(chaosModeMats)
        elif not opulence: material = getMaterial(toolMats)

        # Enchant item
        magic = randrange(8)
        if selectedType in ["tool", "armor", "melee", "ranged", "jewelry"]:
            if magic == 6:
                if selectedType == "tool": effect = choice(toolCurses) + " "
                elif selectedType in ["armor", "jewelry"]: effect = choice(armorCurses) + " "
                elif selectedType == "melee": effect = choice(weaponMeleeCurses) + " "
                elif selectedType == "ranged": effect = choice(weaponRangedCurses) + " "
                effectStatus = "cursed "
            if magic == 7:
                if selectedType == "tool": effect = choice(toolEnchants) + " "
                elif selectedType in ["armor", "jewelry"]: effect = choice(armorEnchants) + " "
                elif selectedType == "melee": effect = choice(weaponMeleeEnchants) + " "
                elif selectedType == "ranged": effect = choice(weaponRangedEnchants) + " "
                effectStatus = "blessed "
                
            magic2 = randrange(4)
            if magic2 == 3:
                effect2 = ""
                if effectStatus == "cursed ":
                    if selectedType == "tool": effect2 = choice(toolCurses) + " "
                    elif selectedType in ["armor", "jewelry"]: effect2 = choice(armorCurses) + " "
                    elif selectedType == "melee": effect2 = choice(weaponMeleeCurses) + " "
                    elif selectedType == "ranged": effect2 = choice(weaponRangedCurses) + " "
                if effectStatus == "blessed ":
                    if selectedType == "tool": effect2 = choice(toolEnchants) + " "
                    elif selectedType in ["armor", "jewelry"]: effect2 = choice(armorEnchants) + " "
                    elif selectedType == "melee": effect2 = choice(weaponMeleeEnchants) + " "
                    elif selectedType == "ranged": effect2 = choice(weaponRangedEnchants) + " "
                if effect != effect2: effect += effect2

        #Checking count
        if selectedType in ["ammo", "trinket"]:
            if selectedType == "ammo": count = counts[randrange(1,15)]
            else: count = counts[randrange(1,5)]
        else: count = counts[1]

        # Prepare description
        description = f"You found {count} {effectStatus}{filthiness}, {wearing}, {opulence}{craftwork} {effect}{material} {item}"
        if gem != None or trim != None:
            description += " with a "
            if trim != None: description += f"{trim} trim"
            if gem != None and trim != None: description += " and a "
            if gem != None: description += f"{gem} setting"
        if artDesc != "": description += f". The artwork depicts {artDesc}"
        if contents != None: description += f". It contains {contents[0].lower() + contents[1:]}"
            
    else:
        description = "Formatting: {count} {effectStatus}{filthiness}, {wearing}, {opulence}{craftwork} {effect}{material} {item} with a {trim} trim and a {cut}-cut {gem} setting. The artwork depicts {artDesc}. It contains {contents}."

        description += """
effectStatus - Whether an item is enchanted. Blessed items have good enchantments, and cursed items have bad enchantments.
filthiness - How dirty an item is, from immaculate to eroded.
wearing - How worn or damaged an item is, from brand new to broken.
opulence - Non-jewelry items have a chance to be generated as opulent. Opulent items are ornate in design, have gems inset into them, and are not designed to be functional. If insanity mode is disabled, opulent items will be made of valuable materials, such as gold or silver.
craftwork - How well-made the item is, from shoddy to masterwork.
effect - If blessed or cursed, this will tell what the enchantment is.
material - The primary material of the item. If insanity mode is disabled and the item is something such as a tool or armor, this may be something like iron or steel. If the type is jewelry, or if the piece is opulent, it will be something valuable, such as silver or gold. If insanity mode is enabled, it could be made of anything, as if some lunatic craftsdwarf got their hands on a futuristic lab and went crazy making artifacts out of whatever he could find.
item - What shape the item takes. This could be a pair of boots, or a flask, or a die, or a ring.
trim - Decorative chain, foil, or other ornament of a secondary material.
cut - If the object is opulent or jewelry, it may have a gem. This is the shape of the gem.
gem - If the object is opulent or jewelry, it may have a gem. This is the type of gem. Insanity mode will add additional gem types, but gems won't have as many variants as materials.
artDesc - If the object is an artwork, this will tell what the artwork's subject is about.
contents - If the object is a potion, this will describe the color, taste, and effect of the potion"""

    return description + "."
