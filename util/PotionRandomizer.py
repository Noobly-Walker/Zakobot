import random
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.cmdutil import cmdutil
text = cmdutil()

mainpots = ["user fully regenerates",
        "user regrows one lost limb",
        "user heals all ailments",
        "user heals all wounds",
        "user is healed of all minor ailments and wounds",
        "user is healed of all minor ailments",
        "user is healed of all minor wounds",
        "user can now only see radio waves",
        "user can now only see microwaves",
        "user can now only see infrared",
        "user can now only see RGB",
        "user can now only see ultraviolet",
        "user can now only see X waves",
        "user can now only see Y waves",
        "user's element changes to fire",
        "user's element changes to water",
        "user's element changes to grass",
        "user's element changes to rock",
        "user's element changes to ground",
        "user's element changes to steel",
        "user's element changes to ice",
        "user's element changes to psychic",
        "user's element changes to electric",
        "user's element changes to bug",
        "user's element changes to poison",
        "user's element changes to flying",
        "user's element changes to dragon",
        "user's element changes to ghost",
        "user's element changes to dark",
        "user's element changes to fighting",
        "user's element changes to normal",
        "user's element changes to fairy",
        "user's element changes to nuclear",
        "user's element changes to shield",
        "user's element changes to light",
        "user's element changes to sound",
        "user's element changes to magic",
        "user's element changes to virtual",
        "user's element changes to cosmic",
        "user's element changes to mutant",
        "user is faster than a bullet",
        "user is faster than a cheetah",
        "user is faster than a galloping horse",
        "user is slower than a tortise",
        "user is slower than an ant",
        "user is slower than a snail",
        "user now can spray irritating black dye when startled",
        "user is now leaking magical energy",
        "user is now extremely sleepy",
        "user is now laughing uncontrollably",
        "user is now completely paralyzed",
        "user can now see glimpses of the future",
        "user is now capable of slightly altering the past",
        "user is now their spirit animal",
        "user's breath can freeze anything",
        "user is now quite warm to the touch",
        "user is now cool to the touch",
        "user is unable to thirst",
        "user is unable to hunger",
        "user is now more alert",
        "user now has more energy",
        "user is filled with magical potential",
        "user has lost one addiction",
        "user is poison resistant",
        "user suddenly possesses a bunch of useful equipment",
        "user can now breathe fire",
        "user's hunger is sated",
        "user can no longer get drunk",
        "user's lungs can now cause hurricane force winds",
        "user is now invisible",
        "user can climb any vertical surface",
        "user is now extremely charismatic",
        "user is invulnerable",
        "user is capable of telekinesis",
        "user is inclined to say 'nice' every time they see something",
        "user is suddenly experienced in combat",
        "user's backpack/satchel/purse becomes two times larger on the inside",
        "user feels lucky today",
        "user's next wish becomes true",
        "user feels constructive",
        "user can create or repair any device without fail",
        "user feels nostalgic",
        "user now has impeccable focus and patience",
        "user has the ability to use telepathy",
        "user is immune to mind powers",
        "user is immune to everything",
        "user can be hurt, but is unkillable",
        "user can smell things in the ground",
        "user can phase through objects",
        "any non-living thing the user touches turns to gold",
        "the next door the user opens will take them to the world of their dreams",
        "user becomes drunk",
        "user's chemical balance is restored and metabolism returns to default",
        "user can jump higher",
        "user can steal souls",
        "user can teleport wherever they want in the universe",
        "user can open portals between two places with a thought",
        "user can open a permanent portal to a pocket dimension once",
        "user's kiss is paralyzing",
        "user is immune to acid",
        "user may switch locations with any other user",
        "user can tame any non-sentient animal, plant, fungus, virus, or bacterium once",
        "user swaps bodies with nearest neighbor"
        "user can speak and understand an additional language",
        "user can jump four times higher",
        "the dominant hand on user's index finger glows like a torch",
        "user forgets everything that’s happened over the last 2 days",
        "it's just water",
        "user finds out they just drank a slime, as it attempts to wriggle its way out",
        "user drank very refreshing water. A water elemental may reform from the user's sweat",
        "user drank a somewhat cherry flavored sugary soda. Is this cola?",
        "user's breath is now minty fresh. User's body is now 100% efficient, and doesn't produce any sort of waste",
        "user is capable of reading thoughts",
        "user now hovers 10cm off the ground",
        "user can now navigate slippry and sticky surfaces as if they were normal, but normal surfaces are sticky",
        "user can now navigate slippry and sticky surfaces as if they were normal, but normal surfaces are slippery",
        "user can see aura",
        "user must dance until they drop, and will resist all attempts to make them stop",
        "user's magic points are fully restored",
        "user has become addicted to drinking these potions",
        "this potion is actually empty, it just appears to have something inside it",
        "user hovers 2cm above the ground, but their speed is doubled",
        "user's bones start hurting. They drank bone hurting juice",
        "user is inclined to fart REALLY LOUDLY, and can do so once a minute",
        "user appears drunk, but is now much smarter",
        "user is capable of flying like Superman, but is unable to walk",
        "user can now see hidden traps and false walls and floors",
        "user can fly like Superman up to a height of 30m",
        "user's touch can cure others of any effect except parasitism",
        "user's health overcaps by 50%",
        "user's magic power overcaps by 50%",
        "user's saturation overcaps by 50%",
        "user's hydration overcaps by 50%",
        "user teleports to the moon",
        "user teleports to 0 latitude 0 longitude at ground or sea level",
        "user teleports to an empty pocket dimension",
        "user teleports to wherever they acquired this potion",
        "user teleports to the next planet out",
        "user teleports to the next planet in",
        "user teleports to the next closest habitable planet",
        "user teleports to the next closest civilized planet",
        "user teleports to the nearest source of freshwater. They feel as if they should refill the bottle",
        "user is now fully healed, their form returns to the one they were born with, and their stats increase across the board",
        "user will teleport out of danger next time they are in danger",
        "user finds da wae",
        "user now has a mage hand that only they can see, and can do anything the user wants like a hand so long as it is within 10 meters of the user"]

debuffpots = ["user suffers from bubonic plague",
        "user suffers from the flu",
        "user suffers from a common cold",
        "user is now covered in scrapes and scratches",
        "user is now on fire",
        "user's saliva is now glue",
        "user's throat is now burned by acid",
        "user is now insane",
        "user is now uncontrollably angry",
        "user is now stressed or anxious",
        "user is now rather dumb",
        "user is now feral",
        "user is now depressed",
        "user is now extremely hungry",
        "user is now extremely parched",
        "user is compelled to scream",
        "user is unable to open their mouth",
        "user is unable to concentrate",
        "user is now entirely uncharismatic",
        "user feels as though they are made of paper",
        "user feels bored",
        "user is unusually susceptible to telepathy and mind control",
        "user is now unusually susceptible to suggestion, to a point",
        "user is now petrified",
        "the next door the user opens will take them to the world of their nightmares",
        "user is effectively dead",
        "user drools uncontrollably",
        "user is now afraid of projectiles",
        "user's speech is incomprehensible to everyone but themselves",
        "the potion explodes",
        "user is blind",
        "user is deaf",
        "user is mute, and can only communicate through gestures or writing",
        "user's speech sounds like a dog barking to everyone but themselves",
        "the bitter potion causes the user to vomit profusely",
        "user's clothes are evil and they want to kill them",
        "user's next wish comes true, but the outcome is twisted",
        "user's next wish comes true, but the outcome is opposite of what the user wished for",
        "user's face causes those who gaze upon it, including the user, to become petrified",
        "user is now flammible",
        "user feels very cold",
        "user feels very hot"]

tfpots = ["user is now made of crystal",
        "user is now made of gas",
        "user is now made of iron",
        "user is now made of gold",
        "user is now made of mercury",
        "user is now made of water",
        "user can change material of their body",
        "user skin/coat color is now pale",
        "user skin/coat color is now brown",
        "user skin/coat color is now black",
        "user skin/coat color is now red",
        "user skin/coat color is now orange",
        "user skin/coat color is now yellow",
        "user skin/coat color is now green",
        "user skin/coat color is now blue",
        "user skin/coat color is now purple",
        "user skin/coat color is now white",
        "user eye color is now pale",
        "user eye color is now brown",
        "user eye color is now black",
        "user eye color is now red",
        "user eye color is now orange",
        "user eye color is now yellow",
        "user eye color is now green",
        "user eye color is now blue",
        "user eye color is now purple",
        "user eye color is now white",
        "user is 10× stronger",
        "user is now 500% stronger",
        "user is now 200% stronger",
        "user is now 100% stronger",
        "user is now 50% stronger",
        "user is now 50% weaker",
        "user is now 100% weaker",
        "user is now 200% weaker",
        "user is now 500% weaker",
        "user is now 10× weaker",
        "user is now 50% taller",
        "user is now 20% taller",
        "user is now 10% taller",
        "user is now 10% shorter",
        "user is now 20% shorter",
        "user is now 50% shorter",
        "user is now 10% heavier",
        "user is now 5% heavier",
        "user is now 2% heavier",
        "user is now 2% lighter",
        "user is now 5% lighter",
        "user is now 20% lighter",
        "user now has gills",
        "user body hair/coat is now very long",
        "user now has wings capable of carrying them into the air",
        "user is a slime",
        "user can shapeshift into anything at will",
        "user is now a vampire",
        "user is now a were",
        "user's bodily fluids are now toxic",
        "user now possesses a silk gland",
        "user's mane/hair grows very long",
        "user is slowly turned into a clockwork machine",
        "user's skin becomes wood",
        "user's skin becomes scaly",
        "user is made of liquid latex",
        "user's lower half becomes snake tail",
        "user's lower half becomes cow-taur",
        "user's body becomes biomechanical",
        "user's biology becomes insectoid",
        "user's biology becomes furry",
        "user's biology becomes scaly",
        "user's biology returns to default",
        "user can produce vines from their back",
        "user can shapeshift into whatever they desire once",
        "user evolves, if supported",
        "user devolves, if supported",
        "user gains a marsupial pouch",
        "user becomes like clay and can be easily reshaped by others",
        "user changes color based on surroundings",
        "user becomes a gaia dragon",
        "user becomes a plushie",
        "user becomes ugly",
        "user now has a beard",
        "user gains two additional arms",
        "user is capable of photosynthesis",
        "user grows a third eye in the middle of their forehead",
        "user grows an additional toe on each foot",
        "user's nose is topologically inverted and sinks into their head",
        "user is now a cabbage",
        "user's skin becomes thick, like armor. It's bulky and heavy like armor, too",
        "user's hemaglobin becomes iron-based, turning it red",
        "user's hemaglobin becomes sulphur-based, turning it green",
        "user's hemaglobin becomes copper-based, turning it blue",
        "water in the user's bodily fluids becomes liquid ammonia, dying their flesh pale-violet, and will boil in 30m if they are warmer than -33°C",
        "user's fluids glow bright blue, causing them to glow faintly",
        "user's blood becomes unnaturally thin, causing any wounds to bleed out",
        "user's blood becomes unnaturally thick. They can't bleed, but their chest hurts a lot",
        "user becomes a pony",
        "user becomes a unicorn",
        "user becomes a pegasus",
        "user becomes a alicorn",
        "user becomes an avali",
        "user becomes a naga",
        "user becomes a plant person"]

nsfwpots = ["user now possesses an extremely high libido",
            "user now emits lust-inducing pheromones",
            "user's saliva is now addicting to others",
            "user can be pleasured by just being touched",
            "user's personality is inverted. Dom becomes sub, sub becomes dom",
            "user is 50% more fertile",
            "user's cum and milk can form long tentacles that they control",
            "user has increased ejaculation speed",
            "user's excretions have higher surface tension",
            "user can orgasm at the slightest touch",
            "user's genitalia excrete glue from skin",
            "user becomes slave to their sexual drive",
            "user produces both sperm and eggs",
            "female user can lay eggs instead of birthing live young. Male user's cum causes females to lay eggs.",
            "male user's skin is capable of excreting cum/female's skin is capable of absorbing cum",
            "user is physically unable to orgasm",
            "user must consume cum or milk as nourishment",
            "user gains desire to push things into their holes",
            "user desires to be milked",
            "user becomes paralyzed and emits pheromones",
            "user's breasts/cocks glow with hypnotic symbols that captivate those that look at it",
            "user gets pregnant with her own species.If user doesn't have a womb, an egg will appear in the user's balls.",
            "user gets pregnant with a fox pup. If user doesn't have a womb, an egg will appear in the user's balls.",
            "user gets pregnant with a wolf pup. If user doesn't have a womb, an egg will appear in the user's balls.",
            "user gets pregnant with a neko kitten. If user doesn't have a womb, an egg will appear in the user's balls.",
            "user gets pregnant with a pony foal. If user doesn't have a womb, an egg will appear in the user's balls.",
            "user gets pregnant with a cow calf. If user doesn't have a womb, an egg will appear in the user's balls.",
            "user slowly becomes sluttier and less aware of their actions.",
            "user gets pregnant by touching an entity of the opposite gender",
            "a lewd mage hand appears that only the user can see. The mage hand has a mind of its own and will finger or stroke the user off."]

vorepots = ["user is larger on the inside",
            "user can melt and assimilate creatures they touch",
            "user is lonely and desires to be a part of someone/have someone be a part of them",
            "user can create magical orbs that absorb things inside them and return the nutrient",
            "user's gaze will convince anything that meets the gaze that they/the user is food",
            "user gains a tailmaw",
            "user's abdomen becomes slime",
            "user's jaw becomes split",
            "user's head becomes a mouth with four jaw bones",
            "user's belly grows a mouth",
            "user gains a zipper down their middle",
            "user's stomach lining is furry",
            "user's stomach lining is sticky",
            "user becomes a living fursuit"]

fetishpots = ["user's reproductive organs become plants",
              "user's reproductive organs become carnivorous plants",
              "user now possesses a large penis",
              "user gender is inverted",
              "user now has no genitalia",
              "user now possesses large breasts and ass",
              "user has cocks on breasts/nipples on balls",
              "female user grows an udder/male user grows horns",
              "user's cock knots/instantly absorbs cum to nearest fat or muscle",
              "user becomes a living inflatable",
              "user's flesh becomes un-tearable",
              "user's genitals and/or breasts can inflate at will",
              "user's nipples/cocks have faucets on them that will cause backup if shut off",
              "user's breasts/balls are replaced with rubber versions of themselves. Though they appear to be filled with air, when deflated, milk/cum will pour out."
              "user has larger genitalia and/or breasts",
              "user can cause hyperbreasts/hypercocks/hyperballs/etc with a touch",
              "user's eggs/sperm can absorb other eggs/sperm to grow larger",
              "user now has duplicated genitalia and/or breasts",
              "user can duplicate or merge genitalia and/or breasts at will",
              "user can enslave the minds of people they've bitten",
              "user becomes bimboified: strong, sexy, slutty, and stupid",
              "user's tongue becomes the length of their body and very dexterous.",
              "user has genitalia suction",
              "lining of user's breasts/balls/womb is furry",
              "lining of user's breasts/balls/womb is sticky",
              "user's limbs and tail becomes tentacles",
              "user becomes a living gasm drive, and has full control of the size, number, and function of their limbs, cocks, pussies, breasts, libido, orgasms, and heads. They can grow shaft snakes and lay eggs. If their eggs are consumed in any manner by another individual, they will also become a living gasm drive."]

gorepots = ["the potion tastes somewhat metallic. It's blood.",
            "user's pain sensitivity is inverted. User's entire body is filled with dull pain that doesn't stop until they are wounded. Wounds don't hurt, and the user is unkillable.",
            "user will think they've become inflatable, but will rupture if they attempt to inflate themselves",
            "user becomes a zombie",
            "user's flesh melts off their bones, becoming a living skeleton",
            "user's biology becomes parasitic, desires to seek host"]

nsfwvpots = ["user's breasts/balls churn consumed material into milk/cum",
             "user will merge with their next sexual partner",
             "user now has genitalia tongues",
             "user's breasts/balls open like flowers",
             "user's nipples/cock tips turn into mouths",
             "inside of user's breasts/balls/womb have tentacles/mouths/breasts inside them"]

flavors = ['sweet', 'tangy', 'spicy', 'salty', 'bitter', 'minty', 'tasteless', 'vile', 'metallic', 'sour', 'meaty', 'dry']

colors = ['red', 'vermillion', 'orange', 'amber', 'yellow', 'chartreuse', 'green', 'teal', 'cyan', 'turquoise', 'blue', 'indigo', 'violet', 'purple', 'magenta',
          'maroon', 'jasper', 'brown', 'butterscotch', 'gold', 'forest', 'navy',
          'pink', 'melon', 'peach', 'lemon', 'lime', 'sky', 'lavendar',
          'black', 'gray', 'silver', 'white', 'colorless']

durations = ['10s', '15s', '20s', '30s', '45s',
             '1m', '1m 20s', '1m 30s', '2m', '2m 30s' '3m', '5m', '7m', '8m',
             '10m', '15m', '20m', '30m', '45m',
             '1h', '1h 30m', '2h', '3h', '4h', '5h', '6h', '8h',
             '10h', '12h', '15h', '18h',
             '1d', '1d 12h', '2d', '3d', '4d', '5d', '6d', '7d']

def potion_randomizer(ctx, mods):
    potions = [main()]
    if mods['debuff']:
        potions.append(debuff())
    if mods['tf']:
        potions.append(tf())
    if mods['nsfw']:
        potions.append(nsfw())
    if mods['vore']:
        potions.append(vore())
    if mods['gore']:
        potions.append(gore())
    if mods['fetish']:
        potions.append(fetish())
    if mods['nsfw'] and mods['vore']:
        potions.append(nsfwvore())
    potclass = random.randrange(len(potions))
    output = 'A ' + flavor() + ', ' + color() + ' potion. When consumed, ' + potions[potclass] + '. Potion lasts for the next ' + duration()
    return output

def main():
    potion = random.randrange(1, len(mainpots))
    return mainpots[potion]

def debuff():
    potion = random.randrange(1, len(debuffpots))
    return debuffpots[potion]

def tf():
    potion = random.randrange(1, len(tfpots))
    return tfpots[potion]

def nsfw():
    potion = random.randrange(1, len(nsfwpots))
    return nsfwpots[potion]

def vore():
    potion = random.randrange(1, len(vorepots))
    return vorepots[potion]

def gore():
    potion = random.randrange(1, len(gorepots))
    return gorepots[potion]

def fetish():
    potion = random.randrange(1, len(fetishpots))
    return fetishpots[potion]

def nsfwvore():
    potion = random.randrange(1, len(nsfwvpots))
    return nsfwvpots[potion]

def flavor():
    potion = random.randrange(1, len(flavors))
    return flavors[potion]

def color():
    potion = random.randrange(1, len(colors))
    return colors[potion]

def duration():
    potion = random.randrange(1, len(durations))
    return durations[potion]

def comboCount():
    effects = len(mainpots) + len(debuffpots) + len(tfpots) + len(nsfwpots) + \
              len(vorepots) + len(fetishpots) + len(gorepots) + len(nsfwvpots)
    combos = effects * len(flavors) * len(colors) * len(durations)
    return combos
