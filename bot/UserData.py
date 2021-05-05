from datetime import *
from bot.util.ToolUtil import *
from bot import ResourceParse
from bot import NumberCronch
import random
import json

class UserData:
    ### variables and dicts
    material_tier_names = {
        -1 : 'Hand', # Hand has 5 power and mines up to 0 depth
        0 : 'Wooden', # The 0th pickaxe has 10 power and mines up to 50 depth
        1 : 'Stone', # The 1st pickaxe (stone) has 15 power and mines up to 75 depth
        2 : 'Copper', # The 2nd pickaxe (copper) has 20 power and mines up to 100 depth
        3 : 'Bronze', # The 3rd pickaxe (bronze) has 25 power and mines up to 125 depth
        4 : 'Iron', # The 4th pickaxe (iron) has 30 power and mines up to 150 depth
        5 : 'Diamond', # diamond, 175 depth
        6 : 'Steel', # steel, 200 depth
        7 : 'Hellstone', # hellstone, 225 depth
        8 : 'Carmeltazite', # carmeltazite, 250 depth
        9 : 'Titanium',  # titanium, 275 depth
        10 : 'Titanium Carbide', # titanium carbide, 300 depth
        11 : 'Magnesium Carborundium', # magnesium silicon carbide, 325 depth
        12 : 'Majestic', # magnesium silicon titanium carbide, 350 depth
        13 : 'Mithril', # mithril, 375 depth
        14 : 'Adamantium', # adamantium, 400 depth
        15 : 'Vibranium', # vibranium, 425 depth
        16 : 'Chlorophyte', # chlorophyte, 450 depth
        17 : 'Uru', # uru, 475 depth
        18 : 'Luminite', # luminite, 500 depth
        19 : 'Megasteel', # megasteel, 525 depth
        20 : 'Gigasteel', # gigasteel, 550 depth
        22 : 'Terasteel', # terasteel, 600 depth
        24 : 'Petasteel', # petasteel, 650 depth
        26 : 'Exasteel', # exasteel, 700 depth
        28 : 'Zetasteel', # zetasteel, 750 depth
        30 : 'Yottasteel', # yottasteel, 800 depth
        35 : 'Aethersteel', # 925 depth
    }

    rank_money_multipliers = {
        0.0: 1.0,  # base rank has a 1x multiplier
        1.0: 1.0,  # vip has a 1x multiplier
        2.0: 1.5,  # vip+ has a 1.5x multiplier
        3.0: 3.0,  # premium has a 3x multiplier, 2x from premium and 1.5x from vip+
        4.0: 6.0,  # elite has a 6x multiplier, 2x from elite, 2x from premium, and 1.5x from vip+
        5.0: 18.0, # supreme is elite×3
        6.0: 54.0, # ultimate is supreme×3
        7.0: 270.0 # ultimate+ is ultimate×5
    }

    levelupachievements = {1: 20, 2: 30, 5: 80, 10: 150, 15: 300, 20: 600, 25: 1000, 30: 1250, 35: 1500, 40: 1750,
                           45: 2000, 50: 2500, 60: 3000, 70: 4000, 80: 5000, 90: 7500, 100: 10000, 120: 12500,
                           140: 15000, 160: 20000, 180: 25000, 200: 30000, 225: 40000, 250: 50000}

    ### class init
    
    def __init__(self):
        # All the data about the user.
        # Use setdefault() when collecting data, to ensure you always get something (no [Exception]s from lack of data)
        self.data = {
            'id': float(0),  # these values are guaranteed to ALWAYS exist inside ALL users.
            'can trade': 0,
            'can_mine': True,
            'can_chop': True,
            'exchange_cooldown': False,
            'has_taxed': False,
            'count_iteration_upgrade': 0,
            'crate_purchases': 0,
            'description': '',
            'nickname': '',
            'exp': 0,
            'lv': 0,
            'prst': 0,
            'power': 100,
            'can see images': True,
            'mute levelup': False,
            'bonus slots': 0,
            'notation': 0,
            'color' : 0x8000FF,
            'drill' : 0,
            'can smelt' : False,
            'can blast' : False,
            'can adamantize': False,
            'haz meow' : False,
            'haz pet meow' : False,
            'can drink e-drink' : True,
            'can dumpster dive' : True,
            'can rate bot' : True,
            'realname' : '',
            'random event': 'None',
            'lootbox_counting_multi': [1.0, 1],
            'base inventory size': 500,
            'max_chests': 5,
            'is_max_chests': False,
            'developed land': 0,
            'badges': [''],
            'displayed badge': ''
        }
        self.loadall()

    ### important functions
        
    # add a ton of data at the same time using Dict
    def set_data(self, add: dict):
        for key in add.keys():
            self.data[key] = add[key]
        self.monthly_reset() # Dev reasons.
        self.daily_reset()  # Dev reasons.
        self.minute_reset()  # Dev reasons.

    def loadall(self):
        self.data.setdefault('collections', self.empty_collection)
        self.inventory()
        self.wallet()
        self.achievements()
        self.zfile()
        self.chests()
        self.township()
        self.testfor_max_chests()
        if self.data['id'] == "405968021337669632":
            self.landfill()



    ### pickaxes

    def reset_pickaxe_power(self):
        self.data['lootbox_pick_multi'] = 1
        self.data['pick'] = -1
        self.data['pick_sharpener'] = 0
        self.data['pick_weight'] = 0
        self.data['pick_handle'] = 0
        self.data['pickaxe_wriststrap'] = 0

    def break_pickaxe(self):
        pickaxe = self.data.setdefault('pick', -1)
        sharpener = self.data.setdefault('pick_sharpener', 0)
        weight = self.data.setdefault('pick_weight', 0)
        handle = self.data.setdefault('pick_handle', 0)
        wriststrap = self.data.setdefault('pickaxe_wriststrap', 0)
        if pickaxe == -1:
            out = ' tried punching a rock. Their hand is now mangled beyond recognition. Maybe they should craft a tool to help them.'
        else:
            out = '\'s ' + self.material_tier_names[pickaxe] + ' pickaxe broke!'
        self.data['pick'] = -1
        self.data['pick_sharpener'] = 0
        self.data['pick_weight'] = 0
        self.data['pick_handle'] = 0
        self.data['pickaxe_wriststrap'] = 0
        return out

    # Base pickaxe power.
    def base_pickaxe_power(self):
        pickaxe_num = self.pickaxe_num()
        return (pickaxe_num+2) * 5

    def pickaxe_num(self):
        return self.data.setdefault('pick', -1)

    # Pickaxe sharpener, Extra Weight, Reinforced Handle.
    def pickaxe_shop_multiplier(self):
        sharpener = self.data.setdefault('pick_sharpener', 0)
        weight = self.data.setdefault('pick_weight', 0)
        handle = self.data.setdefault('pick_handle', 0)
        out = 1
        if sharpener > 0:
            out *= 1.1
        if weight > 0:
            out *= 1.25
        if handle > 0:
            out *= 1.5
        return out

    def pickaxe_wriststrap_multiplier(self):
        if self.data.setdefault('pickaxe_wriststrap', 0) > 0:
            clovers = self.clovers()
            out = min((clovers/1000) + 1, 1+(1/self.pickaxe_num()+1))
            if out > 10:
                out = 10
            return out
        return 1

    def lootbox_pickaxe_multiplier(self):
        return self.data.setdefault('lootbox_pick_multi', 1.0)

    def mult_lootbox_pick_boost(self, to_multiply):
        self.data['lootbox_pick_multi'] = self.lootbox_pickaxe_multiplier() * to_multiply

    def get_pickaxe_power(self):
        base = self.base_pickaxe_power()
        power = base * self.pickaxe_shop_multiplier()
        power *= self.lootbox_pickaxe_multiplier()
        power *= self.pickaxe_wriststrap_multiplier()

        power += 0.5  # so that it's round(), instead of floor()
        return int(power)



    ### axes

    def reset_axe_power(self):
        self.data['lootbox_axe_multi'] = 1
        self.data['axe'] = -1
        self.data['axe_sharpener'] = 0
        self.data['axe_weight'] = 0
        self.data['axe_handle'] = 0
        self.data['axe_wriststrap'] = 0

    def break_axe(self):
        axe = self.data.setdefault('axe', -1)
        sharpener = self.data.setdefault('axe_sharpener', 0)
        weight = self.data.setdefault('axe_weight', 0)
        handle = self.data.setdefault('axe_handle', 0)
        wriststrap = self.data.setdefault('axe_wriststrap', 0)
        if axe == -1:
            out = ' tried punching a tree. Their fingers are now broken, but they fell a few trees.'
        else:
            out = '\'s ' + self.material_tier_names[axe] + ' axe broke!'
        self.data['axe'] = -1
        self.data['axe_sharpener'] = 0
        self.data['axe_weight'] = 0
        self.data['axe_handle'] = 0
        self.data['axe_wriststrap'] = 0
        return out

    # Base pickaxe power.
    def base_axe_power(self):
        axe_num = self.axe_num()
        return (axe_num+2) * 5

    def axe_num(self):
        return self.data.setdefault('axe', -1)

    # Pickaxe sharpener, Extra Weight, Reinforced Handle.
    def axe_shop_multiplier(self):
        sharpener = self.data.setdefault('axe_sharpener', 0)
        weight = self.data.setdefault('axe_weight', 0)
        handle = self.data.setdefault('axe_handle', 0)
        out = 1
        if sharpener > 0:
            out *= 1.1
        if weight > 0:
            out *= 1.25
        if handle > 0:
            out *= 1.5
        return out

    def axe_wriststrap_multiplier(self):
        if self.data.setdefault('axe_wriststrap', 0) > 0:
            clovers = self.clovers()
            out = (clovers/1000) + 1
            if out > 10:
                out = 10
            return out
        return 1

    def lootbox_axe_multiplier(self):
        return self.data.setdefault('lootbox_axe_multi', 1.0)

    def mult_lootbox_axe_boost(self, to_multiply):
        self.data['lootbox_axe_multi'] = self.lootbox_pickaxe_multiplier() * to_multiply

    def get_axe_power(self):
        base = self.base_axe_power()
        power = base * self.axe_shop_multiplier()
        power *= self.lootbox_axe_multiplier()
        power *= self.axe_wriststrap_multiplier()

        power += 0.5  # so that it's round(), instead of floor()
        return int(power)


    ### counting multiplier

    def get_shop_counting_multi(self):
        shop_bonus = self.count_upgrades()
        shop_levels = [0.2, 0.3, 0.5, 1, 2, 2.5, 3.5, 4, 6, 10, 20, 50,
                       1.2, 1.3, 1.5, 2, 3, 3.5, 4.5, 5, 7, 10, 20, 50,
                       1.2, 1.3, 1.5, 2, 3, 3.5, 4.5, 5, 7, 10, 20, 50]
        shop_add = 1
        shop_mult = 1
        shop_expon = 1
        while shop_bonus > 24:
            shop_expon **= shop_levels[shop_bonus-1]
            shop_bonus -= 1
        while 24 >= shop_bonus > 12:
            shop_mult *= shop_levels[shop_bonus-1]
            shop_bonus -= 1
        while 12 >= shop_bonus > 0:
            shop_add += shop_levels[shop_bonus-1]
            shop_bonus -= 1
        return [shop_add * shop_mult, shop_expon]

    def get_crafting_counting_multi(self):
        inv = self.inventory()
        cmr1 = inv['Stone Multiplier Rune'][0] * 0.01
        cmr2 = inv['Copper Multiplier Rune'][0] * 0.03
        cmr3 = inv['Billon Multiplier Rune'][0] * 0.09
        cmr4 = inv['Silver Multiplier Rune'][0] * 0.27
        cmr5 = inv['Electrum Multiplier Rune'][0] * 0.81
        cmr6 = inv['Gold Multiplier Rune'][0] * 2.43
        cmr7 = inv['Sandia Multiplier Rune'][0] * 7.29
        cmr8 = inv['Platinum Multiplier Rune'][0] * 21.87
        cmr9 = inv['Caltinum Multiplier Rune'][0] * 65.61
        cmr10 = inv['Californium Multiplier Rune'][0] * 196.83
        cmr11 = inv['Diamond Multiplier Rune'][0] * 590.49
        cmr12 = inv['Carmeltazite Multiplier Rune'][0] * 1771.47
        cmr13 = inv['Tourmaline Multiplier Rune'][0] * 5314.41
        runemulti = cmr1 + cmr2 + cmr3 + cmr4 + cmr5 + cmr6 + cmr7 + cmr8 + cmr9 + cmr10 + cmr11 + cmr12 + cmr13 + 1
        return runemulti

    def get_counting_multiplier(self, zako):
        base = zako
        prst = self.prst() + 1
        rank = self.rank() + 1
        level = self.lv() / 2 + 1
        if self.data['lootbox_counting_multi'][0] > 10:
            self.data['lootbox_counting_multi'][0] /= 10
            self.data['lootbox_counting_multi'][1] += 1
        bonus = self.lootbox_counting_multiplier()
        shop = self.get_shop_counting_multi()
        runemulti = self.get_crafting_counting_multi()
        multi = base[0] * prst * rank * level * bonus[0] * shop[0] * runemulti
        multi_e = 0
        while multi > 10:
            multi /= 10
            multi_e += 1
        multi **= shop[1]
        while multi > 10:
            multi /= 10
            multi_e += 1
        multi_e += (bonus[1] + base[1] - 2)*shop[1]
        multi_k = multi_e // 3
        multi_kbase = multi * 10**(multi_e - multi_k*3)
        return NumberCronch.number_cronch(multi_kbase, self.data['id'], multi_k), multi_kbase, multi_k

    def lootbox_counting_multiplier(self):
        return self.counting_multi()

    def counting_multi(self):
        return self.data.setdefault('lootbox_counting_multi', [1.0, 1])

    def mult_lootbox_count_boost(self, to_multiply):
        self.data['lootbox_counting_multi'][0] = self.counting_multi()[0] * to_multiply

##    def add_lootbox_count_boost(self, to_add):
##        self.data['lootbox_counting_multi'] = self.lootbox_counting_multiplier() + to_add
##
##    def expon_lootbox_count_boost(self, to_power):
##        self.data['lootbox_counting_multi'] = self.lootbox_counting_multiplier() ** to_power
  
    def count_iteration_upgrade(self):
        return self.data.setdefault('count_iteration_upgrade', 0)

    def count_upgrades(self):
        return self.data.setdefault('count_upgrades', 0)


    ### money multiplier

    def basic_money_multiplier(self):
        return self.data.setdefault('basic_money_multiplier', 1)

    def get_money_multiplier(self):
        rank = self.rank()
        if rank > 7:
            base = self.rank_money_multipliers[7]
        else:
            base = self.rank_money_multipliers[rank]
        # basic_money_multiplier and lootbox_money_multiplier are kept separate
        # so that basic_money_multiplier can be used to calculate how many more (doublers/triplers/etc.) can be bought
        base *= self.data.setdefault('basic_money_multiplier', 1)
        base *= self.data.setdefault('lootbox_money_multi', 1)
        base = round(base, 2)
        return base

    def reset_money_multiplier(self):
        self.data['basic_money_multiplier'] = 1
        self.data['lootbox_money_multi'] = 1

    def lootbox_money_multiplier(self):
        return self.data.setdefault('lootbox_money_multi', 1.0)

    def mult_lootbox_money_boost(self, to_multiply):
        self.data['lootbox_money_multi'] = self.lootbox_money_multiplier() * to_multiply




    ### profile

    def desc(self):
        return self.data.setdefault('description', '')

    def set_desc(self, string):
        self.data['description'] = string

    def profile_image(self):
        return self.data.setdefault('profile image', '')

    def canSeeImages(self):
        return self.data.setdefault('can see images', True)

    def muteLevelup(self):
        return self.data.setdefault('mute levelup', False)

    def rank(self):
        return self.data.setdefault('rank', 0)

    def add_rank(self, to_add: float):
        self.data['rank'] = self.rank() + to_add

    def notation(self):
        return self.data.setdefault('notation', 0)

    def set_notation(self, notation: int):
        self.data['notation'] = notation

    def nick(self):
        return self.data.setdefault('nickname', '')

    def realname(self):
        return self.data.setdefault('realname', '')

    def zfile(self):
        files = self.data.setdefault('zfiles', {})
        file0 = files.setdefault('0', '')
        file1 = files.setdefault('1', '')
        file2 = files.setdefault('2', '')
        file3 = files.setdefault('3', '')
        file4 = files.setdefault('4', '')
        file5 = files.setdefault('5', '')
        file6 = files.setdefault('6', '')
        file7 = files.setdefault('7', '')
        file8 = files.setdefault('8', '')
        file9 = files.setdefault('9', '')
        return files

    def bonus_slots(self):
        return self.data.setdefault('bonus slots', 0)

    def set_developed_land(self, new_value):
        self.data['developed land'] = new_value

    def add_badge(self, badge):
        if badge not in self.data['badges']:
            self.data['badges'].append(badge)

    def set_badge(self, badge_no):
        if 0 <= badge_no+1 <= len(self.data['badges']):
            self.data['displayed badge'] = self.data['badges'][badge_no]
            return True
        else:
            return False


    ### rupees, coins, clovers, and land
        
    def rupees(self):
        return self.data['wallet']['Rupees']

    def add_rupees(self, to_add: int):
        self.data['wallet']['Rupees'] = self.rupees() + to_add

    def silver(self):
        return self.data['wallet']['Kups']

    def add_silver(self, to_add: float):
        self.data['wallet']['Kups'] = self.silver() + to_add

    def clovers(self):
        return self.data['wallet']['Clovers']

    def add_clovers(self, to_add: int):
        self.data['wallet']['Clovers'] = self.clovers() + to_add

    def land(self):
        return self.data['wallet']['Land']

    def add_land(self, to_add: int):
        self.data['wallet']['Land'] = self.land() + to_add

    def add_resources(self, rupees, coins, clovers, land):
        self.add_rupees(rupees)
        self.add_silver(coins)
        self.add_clovers(clovers)
        self.add_land(land)

    def tickets(self):
        return self.data.setdefault('Tickets', 0)

    def omnicredits(self):
        return self.data['wallet']['OmniCoreCredits']

    def add_omnicredits(self, to_add: int):
        self.data['wallet']['OmniCoreCredits'] = self.omnicredits() + to_add



    ### exp, lv, prst, and power

    def exp(self):
        return self.data.setdefault('exp', 0)

    def add_exp(self, to_add: float):
        self.data['exp'] = self.exp() + to_add

    def lv(self):
        return self.data.setdefault('lv', 0)

    def add_lv(self, to_add: float):
        self.data['lv'] = self.lv() + to_add

    def prst(self):
        return self.data.setdefault('prst', 0)

    def add_prst(self, to_add: float):
        self.data['prst'] = self.prst() + to_add

    def power(self):
        return self.data.setdefault('power', 100)

    def haz_meow(self):
        return self.data.setdefault('haz meow', False)

    def haz_pet_meow(self):
        return self.data.setdefault('haz pet meow', False)

    def set_power(self):
        self.data['power'] = 100

    def lvup(self, username):
        text = ''
        rupAch = 0
        levelup, rupOut = 0, 0
        xpcap = 20+(self.lv()**2*20)
        achievementtext = ''
        while self.exp() > xpcap:
            levelup += 1
            xpcap = 20+((self.lv()+levelup)**2*20)
            rupOut += (self.lv()+levelup)
            for achievement in self.levelupachievements:
                if achievement == self.lv() + levelup:
                    achievementtext += '\n**Achievement get:** Level {0}\n> +{1}'.format(achievement, ResourceParse.compress_rup_clov(self.levelupachievements[achievement] * self.get_money_multiplier(), 'rupee', self.data['id']))
                    rupAch += self.levelupachievements[achievement]
                    self.achievements()['Level {}'.format(achievement)] += 1
        rupOut = round(rupOut*self.get_money_multiplier())
        rupAch = round(rupAch*self.get_money_multiplier())
        if levelup > 1:
            self.add_lv(levelup)
            text = '**LEVEL UP!** {0} has levelled up {1} times, and is now **Level {2}! (+{3})**'.format(username, levelup, self.lv(), ResourceParse.compress_rup_clov(rupOut, 'rupee', self.data['id']))
        elif levelup == 1:
            self.add_lv(levelup)
            text = '**LEVEL UP!** {0} is now **Level {1}! (+{2})**'.format(username, self.lv(), ResourceParse.compress_rup_clov(rupOut, 'rupee', self.data['id']))
        text += achievementtext
        self.add_rupees(rupOut + rupAch)
        return text

    def get_level(self):
        prst = self.prst()
        level = self.lv()
        exp = self.exp()
        return '**[Prst{0}]**    Lv{1}    ({2}/{3}XP)'.format(prst, level, exp, 20+(self.lv()**2*20))


    ### collections, achievements, and inventory
    
    empty_collection = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    achs = ['Level 1', 'Level 2', 'Level 5', 'Level 10', 'Level 15', 'Level 20', 'Level 25',
            'Level 30', 'Level 35', 'Level 40', 'Level 45', 'Level 50', 'Level 60', 'Level 70',
            'Level 80', 'Level 90', 'Level 100', 'Level 120', 'Level 140', 'Level 160', 'Level 180',
            'Level 200', 'Level 225', 'Level 250', 'Prestige 1', 'Prestige 2', 'Prestige 3',
            'Prestige 4', 'Prestige 5', 'Prestige 6', 'Prestige 8', 'Prestige 10', 'Prestige 12',
            'Prestige 15', 'Prestige 20', 'TNG Overcharge', 'Campers', 'Village Idiots',
            'Clan Encampment', 'Fort Rubble', 'Feudal Life', 'On The Map', 'Township']

    def achievements(self):
        ach = self.data.setdefault('achievements', {})
        for item in self.achs:
            ach.setdefault(item, 0)
        return ach

    def collections(self):
        return self.data.setdefault('collections', self.empty_collection)

    def collection_bonuses(self):
        return self.data.setdefault('collection_bonuses', [0, 0, 0, 0, 0, 0])
        # Six because "completion of all collections"

    def add_collections(self, to_add):
        collections = self.collections()
        if type(to_add[0]) == list:  # 2D array
            for i in range(0,5):
                for j in range(0,5):
                    collections[i][j] += to_add[i][j]
        else:  # 1D array
            for i in range(0, 5):
                for j in range(0, 5):
                    index = 5 * i + j
                    collections[i][j] += to_add[index]
        self.data['collections'] = collections
        bonuses = self.collection_bonuses()  # current completions
        new_completions = [0, 0, 0, 0, 0, 0]  # new completions
        reward = 0
        for i in range(0, 5):
            completions = min(collections[i])  # completions in that collection
            # using < instead of !=, to prevent selling collections then re-buying them for infinite rupees.
            while bonuses[i] < completions:
                new_completions[i] += 1
                bonuses[i] += 1
                reward += bonuses[i] * 1000

        # Super Completions (completion of all collections)
        super_completions = min_2d(collections)
        while bonuses[5] < super_completions:
            new_completions[5] += 1
            bonuses[5] += 1
            reward += 10000*bonuses[5]  # In case we ever decide finishing all collections is worth something.
        # Save
        self.data['collection_bonuses'] = bonuses

        return new_completions, reward

    events = [['Meteor Impact', 'Better ores accessible. Pickaxe acts as if it is a tier higher, while having less durability'],
              ['Lucky Day', 'Luck increased when mining and chopping'],
              ['Famine', 'Taxing is half as effective'],
              ['Spring Bloom', 'Beehives are twice as effective'],
              ['Discovered Lands', 'Effectiveness of town conquering is doubled'],
              ['Rounding Error', 'Counting Multiplier is 50% larger']]

    def event(self):
        event = self.data.setdefault('events', {})
        for item in self.events:
            event.setdefault(item[0], False)
        return event

    walletstuff = ['Rupees', 'Kups', 'Clovers', 'Land', 'OmniCoreCredits']
    
    items = [
        'Wood Log', 'Wood Plank', 'Wood Stick',
        'Stone', 'Stone Brick',
        'Coal', 'Coal Block',
        'Oil', 'Barrel of Oil',
        'Mobius Block',
        'Bronze Block',
        'Diamond', 'Diamond Block',
        'Steel Block',
        'Ringwoodite', 'Obsidian',
        'Hellstone Block',
        'Carmeltazite', 'Carmeltazite Block',
        'Titanium Carbide Block',
        'Magnesium Carborundium Block',
        'Majestic Block',
        'Aetheric',
        'Mithril Block',
        'Food', 'Fruit', 'Grain', 'Nuts', 'Syrup', 'Honey', 'Bread', 'Golden Fruit',
        'Common Crate', 'Uncommon Crate', 'Rare Crate', 'Multiplier Crate', 'Treasure',
        'Brass Block',
        'Lithium Cobalt Oxide Block',
        'Pipe', 'Joules', 'Canister',
        'Carbon Dioxide', 'Barrel of Carbon Dioxide',
        'Natural Gas', 'Barrel of Natural Gas',
        'Gasoline', 'Barrel of Gasoline',
        'Adamantium Block',
        'Titanium Vanadate Block',
        'Vibranium Block',
        'Chlorophyte', 'Chlorophyte Block',
        'Uru Block',
        'Luminite', 'Luminite Block',
        'Megasteel Block', 'Gigasteel Block',
        'Pegmatite', 'Lithium Block',
        'Tourmaline', 'Boron Block',
        'Carbon Block',
        'Sodium Nugget', 'Sodium Block',
        'Magnesite', 'Magnesium Block',
        'Quartz', 'Silicon Nugget', 'Silicon Block',
        'Argon', 'Barrel of Argon',
        'Potassium Nugget', 'Potassium Block',
        'Rutile', 'Titanium Block',
        'Vanadinite', 'Vanadium Block',
        'Hematite', 'Iron Block',
        'Cobaltite', 'Cobalt Block',
        'Tetrahedrite', 'Copper Block',
        'Sphalerite', 'Zinc Block',
        'Rubidium Nugget', 'Rubidium Block',
        'Native Silver', 'Silver Block',
        'Cassiterite', 'Tin Block',
        'Wolframite', 'Tungsten Block',
        'Osmium Nugget', 'Osmium Block',
        'Iridium Nugget', 'Iridium Block',
        'Native Platinum', 'Platinum Block',
        'Native Gold', 'Gold Block',
        'Uranium Nugget', 'Uranium Block',
        'Plutonite', 'Plutonium Nugget', 'Plutonium Block',
        'Curium Nugget', 'Curium Block',
        'Franciscite', 'Californium Block',
        'Galena', 'Lead Ingot', 'Lead Block',
        'Nitrogen Ingot', 'Oxygen Ingot', 'Neon Ingot',
        'Phosphorus Ingot', 'Sulphur Ingot',
        'Spacetime Compression Module']
    try:
        with open('.\\data\\item_list.txt', 'r') as file:
            itemlist = json.loads(file.read())
            for item in itemlist:
                if item in items:
                    print("Warning: Please remove " + item + " from the items list in UserData.py")
                    # z!debug inventory already does this... as does z!isell all
                if itemlist[item][1][0] in ["ITEM"] and item not in items:
                    items.append(item)

    except Exception:
        with open('C:\\B\\zako\\data\\item_list.txt', 'r') as file:
            itemlist = json.loads(file.read())
            for item in itemlist:
                if item in items:
                    print("Warning: Please remove " + item + " from the items list in UserData.py")
                if itemlist[item][1][0] in ["ITEM"] and item not in items:
                    items.append(item)

    townbuilds = [
        'Sawmill', 'Auto Sawmill',
        'Furnace', 'Auto Furnace',
        'Blast Furnace', 'Auto Blast Furnace',
        'Adamant Furnace', 'Auto Adamant Furnace',
        'Simple Hut', 'Hut', 'Small Cottage', 'Cottage',
        'Small Village', 'Large Village',
        'Small Farm', 'Medium Farm',
        'Driller Hut', 'Logging Hut',
        'Clover Field', 'Beehive',
        'Well', 'Silo', 'Blacksmith',
        'Factory', 'Storage Shed']

    def chests(self):
        chests = self.data.setdefault('chests', {})
        for material in self.material_tier_names:
            if material >= 0:
                chests.setdefault(self.material_tier_names[material] + " Chest", 0)
        return chests

    def max_chests(self):
        max_chests = 5 + self.data['civ']['Storage Shed']['count']*2
        self.data['max_chests'] = max_chests
        return max_chests

    def count_chests(self):
        count = 0
        for chest in self.chests():
            count += self.chests()[chest]
        return count

    def testfor_max_chests(self):
        return self.count_chests() >= self.max_chests()

    def chests_str(self):
        chests = self.chests()
        out = ''
        for chest in chests:
            if chests[chest] > 0:
                out += f"{ResourceParse.number_cronch(chests[chest], self.data['id'])} {chest}\n"
        if out == '':
            out = "<no chests>"
        return out

    def inv_size(self):
        inv_size = self.data.setdefault('base inventory size', 500)
        chests = self.chests()
        for chest in chests:
            i = -1
            for key in self.material_tier_names:
                if chest[:-6] == self.material_tier_names[key]:
                    i = key
            if i > -1:
                inv_size += chests[chest]*25*round(1.6**i)
        return inv_size

    def get_inv_volume(self):
        volume = 0
        for item in self.inventory():
            volume += self.inventory()[item][0]
        return volume

    def wallet(self):
        wal = self.data.setdefault('wallet', {})
        for item in self.walletstuff:
            wal.setdefault(item, 0)
        return wal

    def inventory(self):
        inv = self.data.setdefault('inventory', {})
        for item in self.items:
            inv.setdefault(item, [0, False, False])
            value = 0
            if type(inv[item]) is int:
                value = [inv[item], False, False]
                inv[item] = value
            if type(inv[item]) is list and len(inv[item]) < 3:
                value = [inv[item][0], inv[item][1], False]
                inv[item] = value
            else:
                inv.setdefault(item, [0, False, False])
        return inv

    def landfill(self):
        inv = self.data.setdefault('landfill', {})
        for item in self.items:
            inv.setdefault(item, 0)
        return inv

    def township(self):
        civ = self.data.setdefault('civ', {})
        for item in self.townbuilds:
            civ.setdefault(item, {'count': 0})
        return civ

    def is_valid_item(self, item_name: str):
        for item in self.items:
            if item == item_name:
                return True
        return False

    ### buildings

        #### furnaces and other crafting buildings
    
    def fixBuilding(self, oldName, newName):
        count = self.data.pop(oldName, 0)
        var_data = self.township().pop(oldName, {'count': 0})
        if type(var_data) is dict:
            if var_data.get("tier", 0) > 0:
                count = var_data.get("tier")
            else:
                count = var_data.get("count")
        elif type(var_data) is int:
            if var_data > 0:
                count = var_data
        if count is None:
            count = 0
        old_data = self.township().get(newName, {'count': 0})
        if type(old_data) is dict:
            if old_data["count"] > count: # without this, running debug_data() twice in a row deletes your buildings
                count = old_data["count"]
        self.township()[newName] = {'count': count}

    def updateBuildings(self):
        self.fixBuilding("sawmill", "Sawmill")
        self.fixBuilding("auto sawmill", "Auto Sawmill")
        self.fixBuilding("furnace", "Furnace")
        self.fixBuilding("auto furnace", "Auto Furnace")
        self.fixBuilding("blast furnace", "Blast Furnace")
        self.fixBuilding("auto blast furnace", "Auto Blast Furnace")
        self.fixBuilding("adamant furnace", "Adamant Furnace")
        self.fixBuilding("auto adamant furnace", "Auto Adamant Furnace")
        self.fixBuilding("hut_simple", "Simple Hut")
        self.fixBuilding("hut", "Hut")
        self.fixBuilding("small_cottage", "Small Cottage")
        self.fixBuilding("cottage", "Cottage")
        self.fixBuilding("small village", "Small Village")
        self.fixBuilding("large village", "Large Village")
        self.fixBuilding("small farm", "Small Farm")
        self.fixBuilding("medium farm", "Medium Farm")
        self.fixBuilding("logging hut", "Logging Hut")
        self.fixBuilding("drill hut", "Driller Hut")
        self.fixBuilding("auto crafting", "Auto Crafting")
        self.fixBuilding("clover field", "Clover Field")
        self.fixBuilding("beehives", "Beehive")
        self.fixBuilding("well", "Well")
        self.fixBuilding("silo", "Silo")
        self.fixBuilding("storage shed", "Storage Shed")

    # I made buildings use both count AND tier because i'm stupid.
    # and then i realized my mistake.
    def hasBuilding(self, building, count, exact):
        if self.township().get(building) is None:
            return False
        test_count = "count" in self.township()[building]
        test_tier = "tier" in self.township()[building]
        if test_tier:
            num = self.township()[building]["tier"]
            self.township()[building]["count"] = self.township()[building]["tier"]
            self.township()[building].pop("tier")
            test_count = True
        if test_count:
            if exact and self.township()[building]["count"] == count:
                return True
            if self.township()[building]["count"] <= count:
                return True
        return False

    def autochop(self):
        bloom = self.event()['Spring Bloom']
        famine = self.event()['Famine']
        oak = (self.trees()['Oak Tree'] + self.trees()['Oak Grove']*11 + self.trees()['Oak Forest']*121)//(famine+1)
        maple = (self.trees()['Maple Tree'] + self.trees()['Maple Grove']*11 + self.trees()['Maple Forest']*121)//(famine+1)
        spruce = (self.trees()['Spruce Tree'] + self.trees()['Spruce Grove']*11 + self.trees()['Spruce Forest']*121)//(famine+1)
        apple = (self.trees()['Apple Tree'] + self.trees()['Apple Grove']*11 + self.trees()['Apple Forest']*121)//(famine+1)
        rupee = (self.trees()['Rupee Tree'] + self.trees()['Rupee Grove']*11 + self.trees()['Rupee Forest']*121)//(famine+1)
        coin = (self.trees()['Coin Tree'] + self.trees()['Coin Grove']*11 + self.trees()['Coin Forest']*121)//(famine+1)
        clov = self.data['civ']['Clover Field']['count']//(famine+1)
        bees = int((self.data['civ']['Beehive']['count'] * (bloom + 1)//(famine+1)+1)**0.7)
        out = ''
        gain = [(oak + maple + spruce + apple + rupee + coin) * (1 + bees),
                rupee * (5 + bees),
                coin * (500 + bees*100),
                (oak + maple) * (1 + bees),
                maple * (3 + bees),
                apple * (2 + bees),
                int(round(clov * random.uniform(1, 1.3*bees))),
                bees]
        if gain[0] > 0:
            self.inventory()['Wood Log'][0] += gain[0]
            out += '{} Wood Logs\n'.format(ResourceParse.number_cronch(gain[0], self.data['id']))
        if gain[1] > 0:
            self.add_rupees(gain[1])
            out += ResourceParse.compress_rup_clov(gain[1], 'rupee', self.data['id']) + '\n'
        if gain[2] > 0:
            self.add_silver(gain[2])
            out += ResourceParse.compress_coin(gain[2], self.data['id']) + '\n'
        if gain[3] > 0:
            self.inventory()['Nuts'][0] += gain[3]
            out += '{} Nuts\n'.format(ResourceParse.number_cronch(gain[3], self.data['id']))
        if gain[4] > 0:
            self.inventory()['Syrup'][0] += gain[4]
            out += '{} Syrup\n'.format(ResourceParse.number_cronch(gain[4], self.data['id']))
        if gain[5] > 0:
            self.inventory()['Fruit'][0] += gain[5]
            out += '{} Fruit\n'.format(ResourceParse.number_cronch(gain[5], self.data['id']))
        if gain[6] > 0:
            self.add_clovers(gain[6])
            out += '{} Clovers\n'.format(ResourceParse.number_cronch(gain[6], self.data['id']))
        if gain[7] > 0:
            self.inventory()['Honey'][0] += gain[7]
            out += '{} Honey\n'.format(ResourceParse.number_cronch(gain[7], self.data['id']))
        return out

    def can_smelt(self):
        return self.data.setdefault('can smelt', False)

    def can_blast(self):
        return self.data.setdefault('can blast', False)

    def can_adamantize(self):
        return self.data.setdefault('can adamantize', False)

    def test_smelt(self):
        if self.data['civ']['Furnace']["count"] > 0:
            self.data['can smelt'] = True
        else:
            self.data['can smelt'] = False
        if self.data['civ']['Blast Furnace']["count"] > 0:
            self.data['can blast'] = True
        else:
            self.data['can blast'] = False
        if self.data['civ']['Adamant Furnace']["count"] > 0:
            self.data['can adamantize'] = True
        else:
            self.data['can adamantize'] = False
            

        #### utility structures

    def trees(self):
        trees = self.data.setdefault('trees', {})
        oakTree = trees.setdefault('Oak Tree', 0)
        mapleTree = trees.setdefault('Maple Tree', 0)
        spruceTree = trees.setdefault('Spruce Tree', 0)
        appleTree = trees.setdefault('Apple Tree', 0)
        rupeeTree = trees.setdefault('Rupee Tree', 0)
        coinTree = trees.setdefault('Coin Tree', 0)
        oakGrove = trees.setdefault('Oak Grove', 0)
        mapleGrove = trees.setdefault('Maple Grove', 0)
        spruceGrove = trees.setdefault('Spruce Grove', 0)
        appleGrove = trees.setdefault('Apple Grove', 0)
        rupeeGrove = trees.setdefault('Rupee Grove', 0)
        coinGrove = trees.setdefault('Coin Grove', 0)
        oakForest = trees.setdefault('Oak Forest', 0)
        mapleForest = trees.setdefault('Maple Forest', 0)
        spruceForest = trees.setdefault('Spruce Forest', 0)
        appleForest = trees.setdefault('Apple Forest', 0)
        rupeeForest = trees.setdefault('Rupee Forest', 0)
        coinForest = trees.setdefault('Coin Forest', 0)
        return trees

    

    ### autocraft

    def autocrafted_items(self) -> dict:
        return self.data.setdefault('autocraft', {})

    def add_autocrafted_item(self, item: str, craft_id: str, num: int):
        if num <= 0:
            # will never trigger the autocraft
            return "An autocraft that triggers when you have less than 0 items will never trigger!"
        if not self.is_valid_item(item):
            return "{0} is not a valid item!".format(item)  # not even a valid item to begin with
        autocrafted = self.autocrafted_items()
        autocrafted[item] = (craft_id, num)
        self.data['autocraft'] = autocrafted
        return "Successfully added autocrafted item!"

    def remove_autocrafted_item(self, item: str):
        autocrafted = self.autocrafted_items()
        if item in autocrafted:
            autocrafted.pop(item)
            self.data['autocraft'] = autocrafted
            return True
        return False

    ### time-based events

    def event_daily(self):
        self.data.setdefault('event_daily', False)

    def xp_cooldown(self):
        self.data.setdefault('xp_cooldown', False)

    def exchange_cooldown(self):
        self.data.setdefault('exchange_cooldown', False)

    def has_taxed(self):
        self.data.setdefault('has_taxed', False)

    def can_drink_edrink(self):
        self.data.setdefault('can drink e-drink', True)

    @staticmethod
    def date_to_string(date: date):
        day = date.day
        month = date.month
        year = date.year
        return "{0}-{1}-{2}".format(year, month, day)

    @staticmethod
    def string_to_yearmonthday(date: str):
        year, month, day = date.split("-")
        return int(year), int(month), int(day)

    @staticmethod
    def time_to_string(datetime: datetime):
        minute = datetime.minute
        hour = datetime.hour
        day = datetime.day
        month = datetime.month
        year = datetime.year
        return "{0}-{1}-{2}-{3}-{4}".format(year, month, day, hour, minute)

    @staticmethod
    def string_to_yrmodyhrmin(date: str):
        year, month, day, hour, minute = date.split("-")
        return int(year), int(month), int(day), int(hour), int(minute)

    # Reset all data that needs to be reset daily.
    def monthly_reset(self):
        if self.is_this_month('lastreset_date'):
            return
        
        self.data['can rate bot'] = True
        
    def daily_reset(self):
        if self.is_today('lastreset_date'):
            # do not reset anything.
            return

        if not self.is_today('lastmine_date'):
            if self.data.get('lastmine_date') is not None:
                self.data.pop('lastmine_date') # Removing usage of this variable.
        if not self.is_today('lastchop_date'):
            if self.data.get('lastchop_date') is not None:
                self.data.pop('lastchop_date') # Removing usage of this variable.
        if not self.is_today('lastcrate_date'):
            if self.data.get('lastcrate_date') is not None:
                self.data.pop('lastcrate_date') # Removing usage of this variable.

        if self.data.get('lastcrate_date') is None:
            self.data['crate_purchases'] = 0
        if self.data.get('lastmine_date') is None:
            self.data['can_mine'] = True
        if self.data.get('lastchop_date') is None:
            self.data['can_chop'] = True

        self.data['daily_shop_purchases'] = {}
        self.data['event_daily'] = False
        self.data['exchange_cooldown'] = False
        self.data['has_taxed'] = False
        self.data['haz pet meow'] = False
        self.data['can drink e-drink'] = True
        self.data['can dumpster dive'] = True

        for event_type in self.events:
            self.event()[event_type[0]] = False
        event_check = random.randrange(20)
        if event_check == 7:
            event_type = self.events[random.randrange(len(self.events))][0]
            self.data['random event'] = event_type
            self.event()[event_type] = True
        else:
            self.data['random event'] = 'None'

        self.data['lastreset_date'] = self.date_to_string(datetime.utcnow())

    def minute_reset(self):
        if self.is_now('lastreset_time'):
            # do not reset anything.
            return

        self.data['lastreset_time'] = self.time_to_string(datetime.utcnow())
            

    

    def is_this_month(self, name: str):
        date = self.data.get(name)
        if date is None:
            return False
        year, month, day = UserData.string_to_yearmonthday(date)
        today = datetime.utcnow()
        return year == today.year and month == today.month

    # Returns whether a specific date is today

    def is_today(self, name: str):
        date = self.data.get(name)
        if date is None:
            return False
        year, month, day = UserData.string_to_yearmonthday(date)
        today = datetime.utcnow()
        return year == today.year and month == today.month and day == today.day

    def is_now(self, name: str):
        time = self.data.get(name)
        if time is None:
            return False
        year, month, day, hour, minute = UserData.string_to_yrmodyhrmin(time)
        now = datetime.utcnow()
        return year == now.year and month == now.month and day == now.day and hour == now.hour and minute == now.minute



# Min value of 2D array
def min_2d(array):
    # I have no fucking clue how this works.
    # All I know is that Stack Overflow is a good source.
    return min([min(r) for r in array])
