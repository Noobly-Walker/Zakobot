import os
from bot.ShopHandler import *
from bot.UserData import *
from bot.ResourceParse import *
from data.FileHandler import *
import discord
from discord.ext import commands

def load_craft_items():
    try:
        with open('.\\data\\item_list.txt', 'r') as file:
            shop_item_list = json.loads(file.read())
    except Exception:
        with open('C:\\B\\zako\\data\\item_list.txt', 'r') as file:
            shop_item_list = json.loads(file.read())

    #Os, Ir, and Pt are often found together!
    #Pu-244 decays into U-240 by alpha emission.
    #Cf-251 decays into Cu-247 by alpha emission, and Cu-247 further decays into Pu-243 by alpha emission.

    for item in shop_item_list:
        if shop_item_list[item][1][0] not in ["ITEM", "ITEMBR", "BUILDING"]:
            continue
        smelt, blast, adamant, action = False, False, False, False
        if shop_item_list[item][1][1] == 'FURNACE':
            smelt = True
        elif shop_item_list[item][1][1] == 'BLAST_FURNACE':
            blast = True
        elif shop_item_list[item][1][1] == 'ADAMANT_FURNACE':
            adamant = True
        elif shop_item_list[item][1][1] == "ACTION":
            action = True
        if len(shop_item_list[item][0]) > 1: # there are many recipes for this item, and they should be indexed.
            recipeno = 0
            for recipe in shop_item_list[item][0]:
                recipeno += 1
                if recipeno == 1:
                    recipeindex = ""
                else:
                    recipeindex = str(recipeno)
                #print("id: " + shop_item_list[item][2][0] + str(recipeno) + ", desc = " + item + f" Recipe #{recipeno}")
                shop_item = ShopItem(shop_item_list[item][2][0] + str(recipeindex)).set_description(item + f" Recipe #{recipeno}")
                if smelt:
                    shop_item.set_prereqs({"can smelt": True})
                if blast:
                    shop_item.set_prereqs({"can blast": True})
                if adamant:
                    shop_item.set_prereqs({"can adamantize": True})
                if action:
                    shop_item.set_action(shop_item_list[item][1][2])
                    try:
                        if len(shop_item_list[item][1][3]) != 0:
                            shop_item.set_prereqs(shop_item_list[item][1][3])
                    except Exception:
                        pass
                #print("main cost: " + str({**recipe[0], **recipe[2]}))
                #print("inv cost: " + str(recipe[1]))
                if recipe[0] != {}:
                    shop_item.set_cost(recipe[0])
                if recipe[1] != {}:
                    shop_item.set_inventory_cost(recipe[1])
                if recipe[2] != {}:
                    shop_item.set_money_cost(recipe[2])
                text_price = ''
                ingredientnumber = 0
                output_offset = 0
                ingredient_list = {**recipe[0], **recipe[1], **recipe[2]}
                sorted_ingredients = {k: v for k, v in sorted(ingredient_list.items(), key=lambda item: item[1], reverse=True)}
                #print("ingredient list: " + str(sorted_ingredients))
                for ingredient in sorted_ingredients:
                    if sorted_ingredients[ingredient] < 0:
                        output_offset += 1
                for ingredient in sorted_ingredients:
                    ingredientnumber += 1
                    if ingredientnumber <= len(sorted_ingredients) -(output_offset):
                        text_price += f"{sorted_ingredients[ingredient]}×{ingredient}"
                    if ingredientnumber >= len(sorted_ingredients)-(output_offset-1):
                        text_price += f"{sorted_ingredients[ingredient]*-1}×{ingredient}"
                    if ingredientnumber <= len(sorted_ingredients)-1:
                        if ingredientnumber == len(sorted_ingredients)-(output_offset):
                            text_price += " => "
                        else:
                            text_price += " + "
                #print("text price: " + text_price)
                shop_item.set_text_price(text_price)
                alt_ids = shop_item_list[item][2][:]
                #print("alt ids pre-numerated: " + str(alt_ids))
                for i in range(len(alt_ids)):
                    alt_ids[i] = alt_ids[i] + str(recipeno)
                #print("alt ids: " + str(alt_ids))
                shop_item.set_alt_ids(alt_ids)
                shop_item.is_crafted()
        else: # there is just one recipe for this item, no index needed.
            #print("id: " + shop_item_list[item][2][0] + ", desc = " + item)
            shop_item = ShopItem(shop_item_list[item][2][0]).set_description(item)
            if smelt:
                shop_item.add_prereqs({"can smelt": True})
            if blast:
                shop_item.add_prereqs({"can blast": True})
            if adamant:
                shop_item.add_prereqs({"can adamantize": True})
            if action:
                shop_item.set_action(shop_item_list[item][1][2])
                try:
                    if len(shop_item_list[item][1][3]) != 0:
                        shop_item.set_prereqs(shop_item_list[item][1][3])
                except Exception:
                    pass
            #print("main cost: " + str({**shop_item_list[item][0][0][0], **shop_item_list[item][0][0][2]}))
            #print("inv cost: " + str(shop_item_list[item][0][0][1]))
            if shop_item_list[item][0][0][0] != {}:
                shop_item.set_cost(shop_item_list[item][0][0][0])
            if shop_item_list[item][0][0][1] != {}:
                shop_item.set_inventory_cost(shop_item_list[item][0][0][1])
            if shop_item_list[item][0][0][2] != {}:
                shop_item.set_money_cost(shop_item_list[item][0][0][2])
            text_price = ''
            ingredientnumber = 0
            output_offset = 0
            ingredient_list = {**shop_item_list[item][0][0][0], **shop_item_list[item][0][0][1], **shop_item_list[item][0][0][2]}
            sorted_ingredients = {k: v for k, v in sorted(ingredient_list.items(), key=lambda item: item[1], reverse=True)}
            #print("ingredient list: " + str(sorted_ingredients))
            for ingredient in sorted_ingredients:
                if sorted_ingredients[ingredient] < 0:
                    output_offset += 1
            for ingredient in sorted_ingredients:
                ingredientnumber += 1
                if ingredientnumber <= len(sorted_ingredients) -(output_offset):
                    text_price += f"{sorted_ingredients[ingredient]}×{ingredient}"
                if ingredientnumber >= len(sorted_ingredients)-(output_offset-1):
                    text_price += f"{sorted_ingredients[ingredient]*-1}×{ingredient}"
                if ingredientnumber <= len(sorted_ingredients)-1:
                    if ingredientnumber == len(sorted_ingredients)-(output_offset):
                        text_price += " => "
                    else:
                        text_price += " + "
            #print("text price: " + text_price)
            #print("alt ids: " + str(shop_item_list[item][2]))
            shop_item.set_text_price(text_price)
            shop_item.set_alt_ids(shop_item_list[item][2])
            shop_item.is_crafted()

    ShopItem('meow').set_description("Lucky Meow Pet")\
        .set_prereqs({"haz meow": False})\
        .set_inventory_cost({'Mithril Block': 1, 'Aetheric': 25})\
        .set_money_cost({"Kups": 1000000, "Clovers": 25})\
        .set_text_price("1×Mithril Block + 25×Aetheric + 1×Auru + 25×Clover")\
        .set_action({"haz meow": True})\
        .add_alt_id("meow pet").add_alt_id("cat pet")\
        .add_alt_id("cat").add_alt_id("lucky meow pet")\
        .add_alt_id("lucky cat pet").add_alt_id("lucky meow")\
        .add_alt_id("lucky cat")\
        .is_crafted()

    ShopItem('oilb').set_description('Barrel of Oil')\
        .set_inventory_cost({'Oil': 10, 'Barrel of Oil': -1})\
        .set_text_price("10×Oil")\
        .add_alt_id('oil barrel').add_alt_id('barrel of oil')\
        .add_alt_id('crude barrel').add_alt_id('barrel of crude')\
        .is_crafted()
    ShopItem('oilb br').set_description('Breaking Barrel of Oil')\
        .set_inventory_cost({'Oil': -10, 'Barrel of Oil': 1})\
        .set_text_price("1×Barrel of Oil")\
        .add_alt_id('breaking oil barrel').add_alt_id('breaking barrel of oil')\
        .add_alt_id('breaking crude barrel').add_alt_id('breaking barrel of crude')\
        .add_alt_id('break oil barrel').add_alt_id('break barrel of oil')\
        .add_alt_id('break crude barrel').add_alt_id('break barrel of crude')\
        .is_crafted()

    matlib = [["Coal", "coal"], ["Copper Ingot", 'cu'], ["Bronze Ingot", 'bz', 'cusn'], ["Silver Ingot", 'ag'], ["Gold Ingot", 'au'],
              ["Iron Ingot", 'fe'], ["Diamond", 'dia'], ["Steel Ingot", 'st', 'fec'], ["Hellstone Ingot", 'hs'],
              ["Carmeltazite", 'carmelite'], ["Titanium Ingot", 'ti'], ["Titanium Carbide Ingot", 'tic'],  ["Tin Ingot", 'sn'],
              ["Platinum Ingot", 'pt'], ["Plutonium Ingot", 'pu'], ["Californium Ingot", 'cf'], ["Magnesium Carborundium Ingot", 'mgsic', 'megasick'],
              ["Majestic Ingot", 'mgsitic', 'magnesium titanium carborundium'], ["Mithril Ingot", 'mithrol', 'agaeth'],
              ["Magnesium Ingot", 'mg'], ["Silicon Ingot", 'si'], ["Carbon Ingot", 'c'], ["Zinc Ingot", 'zn'], ["Lithium Ingot", 'li'],
              ['Tungsten Ingot', 'w'], ['Brass Ingot', 'bs'], ['Adamantium Ingot', 'adm'], ['Cobalt Ingot', 'co'],
              ['Lithium Cobalt Oxide Ingot', 'licoo', 'lco'], ['Vanadium Ingot', 'v'], ['Titanium Vanadate Ingot', 'tiv'],
              ['Chlorophyte Ingot', 'cph'], ['Uru Ingot', 'ur'],['Luminite Ingot', 'lum'], ['Megasteel Ingot', 'mega'], ['Gigasteel Ingot', 'giga'],
              ['Mobius Fuel', 'mob'], ["Vibranium Ingot", 'vib'], ["Osmium Ingot", 'os'], ["Iridium Ingot", 'ir'],
              ["Uranium Ingot", 'u'], ["Curium Ingot", 'cm'], ["Boron Ingot", 'b'], ['Sodium Ingot', 'na'], ['Potassium Ingot', 'k'],
              ['Rubidium Ingot', 'rb'], ['Billon Ingot', 'bn'], ['Electrum Ingot', 'ec'], ['Sandia Ingot', 'sd'], ['Caltinum Ingot', 'ct']]
    matnum = 0
    for material in matlib:
        lower = str.lower(material[0])
        mat = material[0]
        if mat.endswith(" Ingot"):
            mat = mat[:-6]
        if mat.endswith(" Fuel"):
            mat = mat[:-5]
        lowermat = str.lower(mat)
        if len(material) == 2:
            ShopItem('{}b'.format(material[1])).set_description(mat + ' Block')\
                .set_inventory_cost({material[0]: 10, mat + ' Block': -1})\
                .set_text_price("10×" + material[0])\
                .add_alt_id(lowermat + ' block').add_alt_id('block of ' + lowermat)\
                .add_alt_id(material[1] + ' block').add_alt_id('block of ' + material[1])\
                .is_crafted()
            ShopItem('{}b br'.format(material[1])).set_description(mat + ' Block Breaking')\
                .set_inventory_cost({material[0]: -10, mat + ' Block': 1})\
                .set_text_price("1×" + mat + ' Block')\
                .add_alt_id(lowermat + ' block breaking').add_alt_id('breaking block of ' + lowermat)\
                .add_alt_id(material[1] + ' block breaking').add_alt_id('breaking block of ' + material[1])\
                .add_alt_id(lowermat + ' block break').add_alt_id('break block of ' + lowermat)\
                .add_alt_id(material[1] + ' block break').add_alt_id('break block of ' + material[1])\
                .is_crafted()
        elif len(material) == 3:
            ShopItem('{}b'.format(material[1])).set_description(mat + ' Block')\
                .set_inventory_cost({material[0]: 10, mat + ' Block': -1})\
                .set_text_price("10×" + material[0])\
                .add_alt_id(lowermat + ' block').add_alt_id('block of ' + lowermat)\
                .add_alt_id(material[1] + ' block').add_alt_id('block of ' + material[1])\
                .add_alt_id(material[2] + ' block').add_alt_id('block of ' + material[2])\
                .is_crafted()
            ShopItem('{}b br'.format(material[1])).set_description(mat + ' Block Breaking')\
                .set_inventory_cost({material[0]: -10, mat + ' Block': 1})\
                .set_text_price("1×" + mat + ' Block')\
                .add_alt_id(lowermat + ' block breaking').add_alt_id('breaking block of ' + lowermat)\
                .add_alt_id(material[1] + ' block breaking').add_alt_id('breaking block of ' + material[1])\
                .add_alt_id(material[2] + ' block breaking').add_alt_id('breaking block of ' + material[2])\
                .add_alt_id(lowermat + ' block break').add_alt_id('break block of ' + lowermat)\
                .add_alt_id(material[1] + ' block break').add_alt_id('break block of ' + material[1])\
                .add_alt_id(material[2] + ' block break').add_alt_id('break block of ' + material[2])\
                .is_crafted()

    sawmill_type = 0
    while sawmill_type <= 31:
        saw = sawmill_type + 1
        s = str(sawmill_type)
        ShopItem('plk'+s)\
            .set_min_prereqs({"Sawmill": sawmill_type})\
            .set_visible_prereqs({"Sawmill": sawmill_type})\
            .set_description("{}×Wood Plank".format(4 * saw))\
            .set_inventory_cost({'Wood Log': saw, 'Wood Plank': -4 * saw})\
            .set_text_price("{}×Wood Log".format(saw))\
            .add_alt_id("plank"+s).add_alt_id("wood plank"+s).add_alt_id("wooden plank"+s)\
            .add_alt_id("board"+s).add_alt_id("wood board"+s).add_alt_id("wooden board"+s)\
            .add_alt_id("planks"+s).add_alt_id("wood planks"+s).add_alt_id("wooden planks"+s)\
            .add_alt_id("boards"+s).add_alt_id("wood boards"+s).add_alt_id("wooden boards"+s)\
            .is_crafted()
        ShopItem('stbr'+s)\
            .set_min_prereqs({"Sawmill": sawmill_type})\
            .set_visible_prereqs({"Sawmill": sawmill_type})\
            .set_description("{}×Stone Brick".format(4 * saw))\
            .set_inventory_cost({'Stone': 4 * saw, 'Stone Brick': -4 * saw})\
            .set_text_price("{}×Stone".format(4*saw))\
            .add_alt_id("stone brick"+s).add_alt_id("stone bricks"+s)\
            .add_alt_id("rock brick"+s).add_alt_id("rock bricks"+s)\
            .is_crafted()
        ShopItem('stc'+s)\
            .set_min_prereqs({"Sawmill": sawmill_type})\
            .set_visible_prereqs({"Sawmill": sawmill_type})\
            .set_description("{}×Wood Stick".format(4 * saw))\
            .set_inventory_cost({'Wood Plank': saw, 'Wood Stick': -4 * saw})\
            .set_text_price("{}×Wood Plank".format(4 * saw))\
            .add_alt_id("stick"+s).add_alt_id("wood stick"+s).add_alt_id("wooden stick"+s)\
            .add_alt_id("rod"+s).add_alt_id("wood rod"+s).add_alt_id("wooden rod"+s)\
            .is_crafted()
        sawmill_type += 1

    pipelib = [["Copper Ingot", 'cu'], ["Tin Ingot", 'sn'], ["Bronze Ingot", 'bz', 'cusn'], ["Zinc Ingot", 'zn'],
               ['Brass Ingot', 'bs'], ["Iron Ingot", 'fe'], ["Steel Ingot", 'st', 'fec']]
    for material in pipelib:
        lower = str.lower(material[0])
        mat = material[0]
        if mat.endswith(" Ingot"):
            mat = mat[:-6]
        lowermat = str.lower(mat)
        if len(material) == 2:
            ShopItem('{}p'.format(material[1])).set_description(mat + ' Pipe')\
                .set_inventory_cost({material[0]: 4, 'Pipe': -1})\
                .set_text_price("4×" + material[0])\
                .add_alt_id(lowermat + ' pipe').add_alt_id(lowermat + ' tube').add_alt_id(lowermat + ' plumbing')\
                .add_alt_id(material[1] + ' pipe').add_alt_id(material[1] + ' tube').add_alt_id(material[1] + ' plumbing')\
                .is_crafted()
        elif len(material) == 3:
            ShopItem('{}p'.format(material[1])).set_description(mat + ' Pipe')\
                .set_inventory_cost({material[0]: 4, 'Pipe': -1})\
                .set_text_price("4×" + material[0])\
                .add_alt_id(lowermat + ' pipe').add_alt_id(lowermat + ' tube').add_alt_id(lowermat + ' plumbing')\
                .add_alt_id(material[1] + ' pipe').add_alt_id(material[1] + ' tube').add_alt_id(material[1] + ' plumbing')\
                .add_alt_id(material[2] + ' pipe').add_alt_id(material[2] + ' tube').add_alt_id(material[2] + ' plumbing')\
                .is_crafted()

    ShopItem('logh')\
        .set_prereqs({"Logging hut": 0})\
        .set_description("Logging Hut")\
        .set_inventory_cost({'Food': 20, 'Wood Plank': 100})\
        .set_cost({'Hut' : 1, 'Logging Hut' : -1})\
        .set_text_price("100×Wood Plank + 20×Food + 1×Hut")\
        .add_alt_id("logging hut").add_alt_id("woodcutting hut").add_alt_id("woodcutter's hut")\
        .add_alt_id("logging house").add_alt_id("woodcutting house").add_alt_id("woodcutter's house")\
        .is_crafted()

    ShopItem('tree1')\
        .set_description("Oak Tree")\
        .set_money_cost({"Land": 1})\
        .set_inventory_cost({'Nuts': 8, 'Wood Stick': 4})\
        .set_tree_cost({'Oak Tree' : -1})\
        .set_text_price("1×Land + 8×Nuts + 4×Stick")\
        .add_alt_id("oak tree").add_alt_id("oak sapling")\
        .is_crafted()
    ShopItem('tree2')\
        .set_description("Maple Tree")\
        .set_money_cost({"Land": 1})\
        .set_inventory_cost({'Nuts': 6, 'Syrup':2, 'Wood Stick': 4})\
        .set_tree_cost({'Maple Tree' : -1})\
        .set_text_price("1×Land + 6×Nuts + 2×Syrup + 4×Stick")\
        .add_alt_id("maple tree").add_alt_id("maple sapling")\
        .is_crafted()
    ShopItem('tree3')\
        .set_description("Spruce Tree")\
        .set_money_cost({"Land": 1})\
        .set_inventory_cost({'Nuts': 4, 'Wood Stick': 4})\
        .set_tree_cost({'Spruce Tree' : -1})\
        .set_text_price("1×Land + 4×Nuts + 4×Stick")\
        .add_alt_id("spruce tree").add_alt_id("spruce sapling")\
        .add_alt_id("pine tree").add_alt_id("pine sapling")\
        .is_crafted()
    ShopItem('tree4')\
        .set_description("Apple Tree")\
        .set_money_cost({"Land": 1})\
        .set_inventory_cost({'Fruit': 6, 'Wood Stick': 4})\
        .set_tree_cost({'Apple Tree' : -1})\
        .set_text_price("1×Land + 6×Fruit + 4×Stick")\
        .add_alt_id("apple tree").add_alt_id("apple sapling")\
        .add_alt_id("fruit tree").add_alt_id("fruit sapling")\
        .is_crafted()
    ShopItem('tree5')\
        .set_description("Rupee Tree")\
        .set_money_cost({"Land": 1, "Rupees": 1000})\
        .set_inventory_cost({'Wood Stick': 4})\
        .set_tree_cost({'Oak Tree' : 2, 'Rupee Tree' : -1})\
        .set_text_price("1×Land + 1k×Rupee + 2×Oak Tree + 4×Stick")\
        .add_alt_id("rupee tree").add_alt_id("rupee sapling")\
        .is_crafted()
    ShopItem('tree6')\
        .set_description("Coin Tree")\
        .set_money_cost({"Land": 1, "Kups" : 100})\
        .set_inventory_cost({'Wood Stick': 4})\
        .set_tree_cost({'Maple Tree' : 2, 'Coin Tree' : -1})\
        .set_text_price("1×Land + 100×Arg + 2×Maple Tree + 4×Stick")\
        .add_alt_id("coin tree").add_alt_id("coin sapling")\
        .is_crafted()
    ShopItem('clov')\
        .set_description("Clover Garden")\
        .set_cost({'Clover Field' : -1})\
        .set_money_cost({"Land": 1, "Clovers" : 20})\
        .set_text_price("1×Land + 20×Clover")\
        .add_alt_id("clover field").add_alt_id("clover garden")\
        .add_alt_id("clov field").add_alt_id("clov garden")\
        .is_crafted()
    ShopItem('bees')\
        .set_description("Beehive")\
        .set_cost({'Clover Field' : 1, 'Beehive': -1})\
        .set_money_cost({"Rupees": 1000})\
        .set_text_price("1×Clover Field + 1k×Rupee")\
        .add_alt_id("beehive").add_alt_id("bee nest")\
        .add_alt_id("bee hive").add_alt_id("bee box")\
        .is_crafted()

    treenum = 0
    treelib = ['Oak', 'Maple', 'Spruce', 'Apple', 'Rupee', 'Coin']
    for tree in treelib:
        lower = str.lower(tree)
        ShopItem('grove' + str(treenum))\
            .set_description(tree + " Grove")\
            .set_tree_cost({tree + ' Tree' : 10, tree + ' Grove' : -1})\
            .set_text_price("10×" + tree + " Tree")\
            .add_alt_id(lower + " grove").add_alt_id(lower + " orchard")\
            .is_crafted()
        ShopItem('forest' + str(treenum))\
            .set_description(tree + " Forest")\
            .set_tree_cost({tree + ' Grove' : 10, tree + ' Forest' : -1})\
            .set_text_price("10×" + tree + " Grove")\
            .add_alt_id(lower + " forest").add_alt_id(lower + " woods")\
            .is_crafted()
        
    
    ShopItem('chcl')\
        .set_description("4×Charcoal")\
        .set_inventory_cost({'Wood Log': 1, 'Coal': -4})\
        .set_text_price("1×Wood Log")\
        .add_alt_id("coal").add_alt_id("charcoal").add_alt_id("wood coal")\
        .add_alt_id("char").add_alt_id("wood char").add_alt_id("burned wood")\
        .is_crafted()

    ShopItem('food1')\
        .set_description("Granary: Fruit (+2 Food)")\
        .set_inventory_cost({'Fruit': 1, 'Food': -2})\
        .set_text_price("1×Fruit")\
        .is_crafted()
    ShopItem('food2')\
        .set_description("Granary: Nuts (+1 Food)")\
        .set_inventory_cost({'Nuts': 1, 'Food': -1})\
        .set_text_price("1×Nuts")\
        .is_crafted()
    ShopItem('food3')\
        .set_description("Granary: Syrup (+1 Food)")\
        .set_inventory_cost({'Syrup': 1, 'Food': -1})\
        .set_text_price("1×Syrup")\
        .is_crafted()
    ShopItem('food4')\
        .set_description("Granary: Grain (+3 Food)")\
        .set_inventory_cost({'Grain': 1, 'Food': -3})\
        .set_text_price("1×Grain")\
        .is_crafted()
    ShopItem('food5')\
        .set_description("Granary: Honey (+3 Food)")\
        .set_inventory_cost({'Honey': 1, 'Food': -3})\
        .set_text_price("1×Honey")\
        .is_crafted()
    ShopItem('food6')\
        .set_description("Granary: Bread (+10 Food)")\
        .set_inventory_cost({'Bread': 1, 'Food': -10})\
        .set_text_price("1×Bread")\
        .is_crafted()
    ShopItem('food7')\
        .set_description("Granary: Golden Fruit (+25 Food)")\
        .set_inventory_cost({'Golden Fruit': 1, 'Food': -25})\
        .set_text_price("1×Golden Fruit")\
        .is_crafted()

    ShopItem('bread')\
        .set_description("Loaf of Bread")\
        .set_inventory_cost({'Grain': 3, 'Bread': -1})\
        .set_text_price("3×Grain")\
        .add_alt_id("loaf of bread")\
        .is_crafted()
    ShopItem('gapple')\
        .set_description("Golden Fruit")\
        .set_inventory_cost({'Gold Ingot': 8, 'Fruit': 1, 'Golden Fruit': -1})\
        .set_text_price("1×Fruit, 8×Gold Ingot")\
        .add_alt_id("golden apple").add_alt_id("gold apple")\
        .add_alt_id("golden fruit").add_alt_id("gold fruit")\
        .add_alt_id("notch apple")\
        .is_crafted()

    ShopItem('well')\
        .set_description("Well")\
        .set_prereqs({"pick": 4})\
        .set_inventory_cost({'Stone Brick': 500, 'Wood Plank': 100})\
        .set_action({'pick': -1})\
        .set_cost({"Well": -1})\
        .set_text_price('500×Stone Brick + 100×Wood Plank + 1×Iron Pickaxe')\
        .is_crafted()
    ShopItem('silo')\
        .set_description("Silo")\
        .set_inventory_cost({'Tin Ingot': 50, 'Wood Plank': 350, 'Food': 100})\
        .set_cost({"Silo": -1})\
        .set_text_price('50×Tin Ingot + 350×Wood Plank + 100×Food')\
        .is_crafted()
    ShopItem('farm1')\
        .set_description("Small Farm")\
        .set_inventory_cost({'Food': 10, 'Wood Log': 100})\
        .set_cost({'Hut': 1, 'Well': 1, 'Small Farm': -1})\
        .set_money_cost({"Land": 10})\
        .set_text_price('10×Land + 100×Wood Log + 1×Hut + 1×Well + 10×Food')\
        .add_alt_id('small farm').add_alt_id('simple farm').add_alt_id('small plot').add_alt_id('simple plot')\
        .is_crafted()
    ShopItem('farm2')\
        .set_description("Medium Farm")\
        .set_inventory_cost({'Food': 2500})\
        .set_cost({"Small Farm": 4, 'Small Cottage': 1, 'Well': 1, 'Silo': 1, 'Medium Farm': -1})\
        .set_text_price('4×Small Farm + 1×Small Cottage + 1×Well + 1×Silo + 2.5k×Food')\
        .add_alt_id('medium farm').add_alt_id('middle farm').add_alt_id('medium plot').add_alt_id('middle plot')\
        .is_crafted()
    
    ShopItem('ch0').set_description('Wooden Chest')\
        .set_prereqs({'is_max_chests': False})\
        .set_inventory_cost({"Wood Plank": 20})\
        .set_chest_cost({"Wooden Chest": -1})\
        .set_text_price("20×Wood Plank")\
        .add_alt_id("wood chest").add_alt_id("wooden chest")\
        .is_crafted()
    ShopItem('ch1').set_description('Stone Chest')\
        .set_inventory_cost({"Stone": 20})\
        .set_chest_cost({"Wooden Chest": 1, "Stone Chest": -1})\
        .set_text_price("20×Stone, 1×Wooden Chest")\
        .add_alt_id("stone chest").add_alt_id("stone chest")\
        .is_crafted()
    ShopItem('ch2').set_description('Copper Chest')\
        .set_inventory_cost({"Copper Ingot": 20})\
        .set_chest_cost({"Stone Chest": 1, "Copper Chest": -1})\
        .set_text_price("20×Copper Ingot, 1×Stone Chest")\
        .add_alt_id("copper chest").add_alt_id("cu chest")\
        .is_crafted()

    matlib = [['Wood Plank', 'wooden'], ["Stone", 'rock'], ["Copper Ingot", 'cu'], ["Bronze Ingot", 'bz', 'cusn'],
              ["Iron Ingot", 'fe'], ["Diamond", 'dia'], ["Steel Ingot", 'st', 'fec'], ["Hellstone Ingot", 'hs'],
              ["Carmeltazite", 'carmelite'], ["Titanium Ingot", 'ti'], ["Titanium Carbide Ingot", 'tic'],
              ["Magnesium Carborundium Ingot", 'mgsic', 'megasick'],
              ["Majestic Ingot", 'mgsitic', 'magnesium titanium carborundium'], ["Mithril Ingot", 'mithrol', 'agaeth'],
              ["Adamantium Ingot", 'adamant', 'adm'], ["Vibranium Ingot", 'vib'], ["Chlorophyte Ingot", 'cph'],
              ["Uru Ingot", 'ur'], ["Luminite Ingot", 'lum'], ["Megasteel Ingot", 'mega'], ["Gigasteel Ingot", 'giga']]
    matnum = 0
    for material in matlib:
        lower = str.lower(material[0])
        mat = material[0]
        if mat.endswith(" Ingot") or mat.endswith(" Plank"):
            mat = mat[:-6]
        mat1 = matlib[matnum-1][0]
        if mat1.endswith(" Ingot") or mat1.endswith(" Plank"):
            mat1 = mat1[:-6]
        lowermat = str.lower(mat)
        lowermat1 = str.lower(mat1)
        if len(material) == 2:
            ShopItem('p{0}'.format(matnum)).set_description(mat + ' Pickaxe')\
                .set_inventory_cost({material[0]: 3, 'Wood Stick':2})\
                .set_text_price("3×" + material[0] + ' + 2×Stick')\
                .set_action({'pick': matnum})\
                .add_alt_id(lowermat + " pickaxe").add_alt_id(lowermat + " pick")\
                .add_alt_id(material[1] + " pickaxe").add_alt_id(material[1] + " pick")\
                .is_crafted()
            ShopItem('a{0}'.format(matnum)).set_description(mat + ' Axe')\
                .set_inventory_cost({material[0]: 3, 'Wood Stick':2})\
                .set_text_price("3×" + material[0] + ' + 2×Stick')\
                .set_action({'axe': matnum})\
                .add_alt_id(lowermat + " axe").add_alt_id(material[1] + " axe")\
                .is_crafted()
            if matnum > 0:
                ShopItem('sm{0}'.format(matnum)).set_description(mat + '-bladed Sawmill')\
                    .set_inventory_cost({material[0]: 1, 'Wood Stick':2, 'Wood Plank':5})\
                    .set_text_price("1×" + material[0] + ' + 2×Stick + 5×Wood Plank')\
                    .set_action({'Sawmill': matnum})\
                    .add_alt_id(lowermat + "-bladed sawmill").add_alt_id(material[1] + "-bladed sawmill")\
                    .add_alt_id(lowermat + "-blade sawmill").add_alt_id(material[1] + "-blade sawmill")\
                    .add_alt_id(lowermat + " bladed sawmill").add_alt_id(material[1] + " bladed sawmill")\
                    .add_alt_id(lowermat + " blade sawmill").add_alt_id(material[1] + " blade sawmill")\
                    .add_alt_id(lowermat + " sawmill").add_alt_id(material[1] + " sawmill")\
                    .is_crafted()
            if matnum > 2:
                ShopItem('ch{0}'.format(matnum)).set_description(mat + ' Chest')\
                    .set_inventory_cost({material[0]: 20})\
                    .set_chest_cost({mat1 + " Chest": 1, mat + " Chest": -1})\
                    .set_text_price("20×" + material[0] + ' + 1×' + mat1 + " Chest")\
                    .add_alt_id(lowermat + " chest").add_alt_id(material[1] + " chest")\
                    .is_crafted()
        elif len(material) == 3:
            ShopItem('p{0}'.format(matnum)).set_description(mat + ' Pickaxe')\
                .set_inventory_cost({material[0]: 3, 'Wood Stick':2})\
                .set_text_price("3×" + material[0] + ' + 2×Stick')\
                .set_action({'pick': matnum})\
                .add_alt_id(lowermat + " pickaxe").add_alt_id(lowermat + " pick")\
                .add_alt_id(material[1] + " pickaxe").add_alt_id(material[1] + " pick")\
                .add_alt_id(material[2] + " pickaxe").add_alt_id(material[2] + " pick")\
                .is_crafted()
            ShopItem('a{0}'.format(matnum)).set_description(mat + ' Axe')\
                .set_inventory_cost({material[0]: 3, 'Wood Stick':2})\
                .set_text_price("3×" + material[0] + ' + 2×Stick')\
                .set_action({'axe': matnum})\
                .add_alt_id(lowermat + " axe").add_alt_id(material[1] + " axe").add_alt_id(material[2] + " axe")\
                .is_crafted()
            if matnum > 0:
                ShopItem('sm{0}'.format(matnum)).set_description(mat + '-bladed Sawmill')\
                    .set_inventory_cost({material[0]: 1, 'Wood Stick':2, 'Wood Plank':5})\
                    .set_text_price("1×" + material[0] + ' + 2×Stick + 5×Wood Plank')\
                    .set_action({'Sawmill': matnum})\
                    .add_alt_id(lowermat + "-bladed sawmill").add_alt_id(material[1] + "-bladed sawmill").add_alt_id(material[2] + "-bladed sawmill")\
                    .add_alt_id(lowermat + "-blade sawmill").add_alt_id(material[1] + "-blade sawmill").add_alt_id(material[2] + "-blade sawmill")\
                    .add_alt_id(lowermat + " bladed sawmill").add_alt_id(material[1] + " bladed sawmill").add_alt_id(material[2] + " bladed sawmill")\
                    .add_alt_id(lowermat + " blade sawmill").add_alt_id(material[1] + " blade sawmill").add_alt_id(material[2] + " blade sawmill")\
                    .add_alt_id(lowermat + " sawmill").add_alt_id(material[1] + " sawmill").add_alt_id(material[2] + " sawmill")\
                    .is_crafted()
            if matnum > 2:
                ShopItem('ch{0}'.format(matnum)).set_description(mat + ' Chest')\
                    .set_inventory_cost({material[0]: 20})\
                    .set_chest_cost({mat1 + " Chest": 1, mat + " Chest": -1})\
                    .set_text_price("20×" + material[0] + ' + 1×' + mat1 + " Chest")\
                    .add_alt_id(lowermat + " chest").add_alt_id(material[1] + " chest").add_alt_id(material[2] + " chest")\
                    .is_crafted()
        matnum += 1

    ShopItem('shed0').set_description('Small Storage Shed')\
        .set_inventory_cost({"Wood Plank": 1000, "Stone Brick": 500})\
        .set_text_price("1k×Wood Plank + 500×Stone Brick")\
        .set_prereqs({'Storage Shed': 0})\
        .set_action({'Storage Shed': 1})\
        .add_alt_id("storage shed").add_alt_id("shed").add_alt_id("small storage shed").add_alt_id("small shed")\
        .is_crafted()
    ShopItem('shed1').set_description('Medium Storage Shed')\
        .set_inventory_cost({"Wood Plank": 10000, "Stone Brick": 5000})\
        .set_text_price("10k×Wood Plank + 5k×Stone Brick")\
        .set_prereqs({'Storage Shed': 1})\
        .set_action({'Storage Shed': 2})\
        .add_alt_id("medium storage shed").add_alt_id("medium shed")\
        .is_crafted()
    ShopItem('shed2').set_description('Large Storage Shed')\
        .set_inventory_cost({"Wood Plank": 100000, "Stone Brick": 50000})\
        .set_text_price("100k×Wood Plank + 50k×Stone Brick")\
        .set_prereqs({'Storage Shed': 2})\
        .set_action({'Storage Shed': 3})\
        .add_alt_id("large storage shed").add_alt_id("large shed")\
        .is_crafted()

    ShopItem('pu4')\
        .set_prereqs({"pickaxe_wriststrap": 0})\
        .set_description('Pickaxe Wriststrap')\
        .set_money_cost({"Clovers":10})\
        .set_text_price("10×Clover")\
        .set_action({"pickaxe_wriststrap": 1})\
        .add_alt_id('pick wriststrap').add_alt_id('pickaxe wriststrap')\
        .add_alt_id('lucky pick wriststrap').add_alt_id('lucky pickaxe wriststrap')\
        .add_alt_id('charmed pick wriststrap').add_alt_id('charmed pickaxe wriststrap')\
        .is_crafted()
    ShopItem('au4')\
        .set_prereqs({"axe_wriststrap": 0})\
        .set_description('Axe Wriststrap')\
        .set_money_cost({"Clovers":10})\
        .set_text_price("10×Clover")\
        .set_action({"axe_wriststrap": 1})\
        .add_alt_id('axe wriststrap').add_alt_id('lucky axe wriststrap').add_alt_id('charmed axe wriststrap')\
        .is_crafted()

    ShopItem.finalize()
