import os
from bot.ShopHandler import *
from bot.UserData import *
from bot.ResourceParse import *
from data.FileHandler import *
import discord
from discord.ext import commands

def load_shop_items():
##    ShopItem("p19").set_description("Gigasteel Pickaxe (105 Pick Power)")\
##        .set_money_cost({"Rupees": 200000})\
##        .set_text_price(compress(200000, 0, 0, 0))\
##        .set_action({"pick": 19})
##    ShopItem("p20").set_description("Terasteel Pickaxe (110 Pick Power)")\
##        .set_money_cost({"Rupees": 1000000})\
##        .set_text_price(compress(1000000, 0, 0, 0))\
##        .set_action({"pick": 20})
##    ShopItem("p21").set_description("Petasteel Pickaxe (120 Pick Power)")\
##        .set_money_cost({"Rupees": 10000000})\
##        .set_text_price(compress(10000000, 0, 0, 0))\
##        .set_action({"pick": 22})
##    ShopItem("p22").set_description("Exasteel Pickaxe (130 Pick Power)")\
##        .set_money_cost({"Rupees": 100000000})\
##        .set_text_price(compress(100000000, 0, 0, 0))\
##        .set_action({"pick": 24})
##    ShopItem("p23").set_description("Zetasteel Pickaxe (140 Pick Power)")\
##        .set_money_cost({"Rupees": 2000000000})\
##        .set_text_price(compress(2000000000, 0, 0, 0))\
##        .set_action({"pick": 26})
##    ShopItem("p24").set_description("Yottasteel Pickaxe (150 Pick Power)")\
##        .set_money_cost({"Rupees": 500000000000})\
##        .set_text_price(compress(500000000000, 0, 0, 0))\
##        .set_action({"pick": 28})
    ShopItem("edrink").set_description("Energy Drink")\
        .set_prereqs({"can drink e-drink": True})\
        .set_money_cost({"OmniCoreCredits": 15})\
        .set_text_price(compress_rup_clov(15, 'oc2_occ'))\
        .set_action({"can drink e-drink": False, "can_mine": True, "can_chop": True, "can dumpster dive": True})\
        .add_alt_id("energy drink")

    ShopItem("m1").set_description("Money Doubler")\
        .set_prereqs({"basic_money_multiplier": 1})\
        .set_money_cost({"Rupees": 2500})\
        .set_text_price(compress_rup_clov(2500, 'rupee'))\
        .add_alt_id("money doubler").add_alt_id("x2 money").add_alt_id("2x money").add_alt_id("money x2").add_alt_id("money 2x")\
        .add_alt_id("rupee doubler").add_alt_id("x2 rupee").add_alt_id("2x rupee").add_alt_id("rupee x2").add_alt_id("rupee 2x")\
        .add_alt_id("rupees doubler").add_alt_id("x2 rupees").add_alt_id("2x rupees").add_alt_id("rupees x2").add_alt_id("rupees 2x")\
        .add_alt_id("coin doubler").add_alt_id("x2 coin").add_alt_id("2x coin").add_alt_id("coin x2").add_alt_id("coin 2x")\
        .add_alt_id("arg doubler").add_alt_id("x2 arg").add_alt_id("2x arg").add_alt_id("arg x2").add_alt_id("arg 2x")\
        .add_alt_id("silver doubler").add_alt_id("x2 silver").add_alt_id("2x silver").add_alt_id("silver x2").add_alt_id("silver 2x")\
        .add_alt_id("coins doubler").add_alt_id("x2 coins").add_alt_id("2x coins").add_alt_id("coins x2").add_alt_id("coins 2x")\
        .set_action({"basic_money_multiplier": 2})
    ShopItem("m2").set_description("Money Tripler")\
        .set_prereqs({"basic_money_multiplier": 2})\
        .set_money_cost({"Rupees": 25000})\
        .set_text_price(compress_rup_clov(25000, 'rupee'))\
        .add_alt_id("money tripler").add_alt_id("x3 money").add_alt_id("3x money").add_alt_id("money x3").add_alt_id("money 3x")\
        .add_alt_id("rupee tripler").add_alt_id("x3 rupee").add_alt_id("3x rupee").add_alt_id("rupee x3").add_alt_id("rupee 3x")\
        .add_alt_id("rupees tripler").add_alt_id("x3 rupees").add_alt_id("3x rupees").add_alt_id("rupees x3").add_alt_id("rupees 3x")\
        .add_alt_id("coin tripler").add_alt_id("x3 coin").add_alt_id("3x coin").add_alt_id("coin x3").add_alt_id("coin 3x")\
        .add_alt_id("arg tripler").add_alt_id("x3 arg").add_alt_id("3x arg").add_alt_id("arg x3").add_alt_id("arg 3x")\
        .add_alt_id("silver tripler").add_alt_id("x3 silver").add_alt_id("3x silver").add_alt_id("silver x3").add_alt_id("silver 3x")\
        .add_alt_id("coins tripler").add_alt_id("x3 coins").add_alt_id("3x coins").add_alt_id("coins x3").add_alt_id("coins 3x")\
        .set_action({"basic_money_multiplier": 3})
    ShopItem("m3").set_description("Money Quadrupler")\
        .set_prereqs({"basic_money_multiplier": 3})\
        .set_money_cost({"Rupees": 250000})\
        .set_text_price(compress_rup_clov(250000, 'rupee'))\
        .add_alt_id("money quadrupler").add_alt_id("x4 money").add_alt_id("4x money").add_alt_id("money x4").add_alt_id("money 4x")\
        .add_alt_id("rupee quadrupler").add_alt_id("x4 rupee").add_alt_id("4x rupee").add_alt_id("rupee x4").add_alt_id("rupee 4x")\
        .add_alt_id("rupees quadrupler").add_alt_id("x4 rupees").add_alt_id("4x rupees").add_alt_id("rupees x4").add_alt_id("rupees 4x")\
        .add_alt_id("coin quadrupler").add_alt_id("x4 coin").add_alt_id("4x coin").add_alt_id("coin x4").add_alt_id("coin 4x")\
        .add_alt_id("arg quadrupler").add_alt_id("x4 arg").add_alt_id("4x arg").add_alt_id("arg x4").add_alt_id("arg 4x")\
        .add_alt_id("silver quadrupler").add_alt_id("x4 silver").add_alt_id("4x silver").add_alt_id("silver x4").add_alt_id("silver 4x")\
        .add_alt_id("coins quadrupler").add_alt_id("x4 coins").add_alt_id("4x coins").add_alt_id("coins x4").add_alt_id("coins 4x")\
        .set_action({"basic_money_multiplier": 4})
    ShopItem("m4").set_description("Money Quintupler")\
        .set_prereqs({"basic_money_multiplier": 4})\
        .set_money_cost({"Rupees": 2500000})\
        .set_text_price(compress_rup_clov(2500000, 'rupee'))\
        .add_alt_id("money quintupler").add_alt_id("x5 money").add_alt_id("5x money").add_alt_id("money x5").add_alt_id("money 5x")\
        .add_alt_id("rupee quintupler").add_alt_id("x5 rupee").add_alt_id("5x rupee").add_alt_id("rupee x5").add_alt_id("rupee 5x")\
        .add_alt_id("rupees quintupler").add_alt_id("x5 rupees").add_alt_id("5x rupees").add_alt_id("rupees x5").add_alt_id("rupees 5x")\
        .add_alt_id("coin quintupler").add_alt_id("x5 coin").add_alt_id("5x coin").add_alt_id("coin x5").add_alt_id("coin 5x")\
        .add_alt_id("arg quintupler").add_alt_id("x5 arg").add_alt_id("5x arg").add_alt_id("arg x5").add_alt_id("arg 5x")\
        .add_alt_id("silver quintupler").add_alt_id("x5 silver").add_alt_id("5x silver").add_alt_id("silver x5").add_alt_id("silver 5x")\
        .add_alt_id("coins quintupler").add_alt_id("x5 coins").add_alt_id("5x coins").add_alt_id("coins x5").add_alt_id("coins 5x")\
        .set_action({"basic_money_multiplier": 5})
    ShopItem("m5").set_description("Money Sextupler")\
        .set_prereqs({"basic_money_multiplier": 5})\
        .set_money_cost({"Rupees": 25000000})\
        .set_text_price(compress_rup_clov(25000000, 'rupee'))\
        .add_alt_id("money sextupler").add_alt_id("x6 money").add_alt_id("6x money").add_alt_id("money x6").add_alt_id("money 6x")\
        .add_alt_id("rupee sextupler").add_alt_id("x6 rupee").add_alt_id("6x rupee").add_alt_id("rupee x6").add_alt_id("rupee 6x")\
        .add_alt_id("rupees sextupler").add_alt_id("x6 rupees").add_alt_id("6x rupees").add_alt_id("rupees x6").add_alt_id("rupees 6x")\
        .add_alt_id("coin sextupler").add_alt_id("x6 coin").add_alt_id("6x coin").add_alt_id("coin x6").add_alt_id("coin 6x")\
        .add_alt_id("arg sextupler").add_alt_id("x6 arg").add_alt_id("6x arg").add_alt_id("arg x6").add_alt_id("arg 6x")\
        .add_alt_id("silver sextupler").add_alt_id("x6 silver").add_alt_id("6x silver").add_alt_id("silver x6").add_alt_id("silver 6x")\
        .add_alt_id("coins sextupler").add_alt_id("x6 coins").add_alt_id("6x coins").add_alt_id("coins x6").add_alt_id("coins 6x")\
        .set_action({"basic_money_multiplier": 6})
    ShopItem("m6").set_description("Money Octupler")\
        .set_prereqs({"basic_money_multiplier": 6})\
        .set_money_cost({"Rupees": 250000000})\
        .set_text_price(compress_rup_clov(250000000, 'rupee'))\
        .add_alt_id("money octupler").add_alt_id("x8 money").add_alt_id("8x money").add_alt_id("money x8").add_alt_id("money 8x")\
        .add_alt_id("rupee octupler").add_alt_id("x8 rupee").add_alt_id("8x rupee").add_alt_id("rupee x8").add_alt_id("rupee 8x")\
        .add_alt_id("rupees octupler").add_alt_id("x8 rupees").add_alt_id("8x rupees").add_alt_id("rupees x8").add_alt_id("rupees 8x")\
        .add_alt_id("coin octupler").add_alt_id("x8 coin").add_alt_id("8x coin").add_alt_id("coin x8").add_alt_id("coin 8x")\
        .add_alt_id("arg octupler").add_alt_id("x8 arg").add_alt_id("8x arg").add_alt_id("arg x8").add_alt_id("arg 8x")\
        .add_alt_id("silver octupler").add_alt_id("x8 silver").add_alt_id("8x silver").add_alt_id("silver x8").add_alt_id("silver 8x")\
        .add_alt_id("coins octupler").add_alt_id("x8 coins").add_alt_id("8x coins").add_alt_id("coins x8").add_alt_id("coins 8x")\
        .set_action({"basic_money_multiplier": 8})

    ShopItem("pu1").set_description("Pickaxe Sharpener (×1.1 Pick Power)")\
        .set_prereqs({"pick_sharpener": 0})\
        .set_money_cost({"Rupees": 100})\
        .set_text_price(compress_rup_clov(100, 'rupee'))\
        .add_alt_id("pickaxe sharpener").add_alt_id("sharpened pickaxe")\
        .add_alt_id("pick sharpener").add_alt_id("sharpened pick")\
        .set_action({"pick_sharpener": 1})
    ShopItem("pu2").set_description("Extra Pick Head Weight (×1.25 Pick Power)")\
        .set_prereqs({"pick_weight": 0})\
        .set_money_cost({"Rupees": 200})\
        .set_text_price(compress_rup_clov(200, 'rupee'))\
        .add_alt_id("pickaxe head weight").add_alt_id("weighted pickaxe").add_alt_id("extra pickaxe weight")\
        .add_alt_id("weighted pickaxe head").add_alt_id("extra pickaxe head weight")\
        .add_alt_id("pick head weight").add_alt_id("weighted pick").add_alt_id("extra pick weight")\
        .add_alt_id("weighted pick head").add_alt_id("extra pick head weight")\
        .set_action({"pick_weight": 1})
    ShopItem("pu3").set_description("Reinforced Pick Handle (×1.5 Pick Power)")\
        .set_prereqs({"pick_handle": 0})\
        .set_money_cost({"Rupees": 500})\
        .set_text_price(compress_rup_clov(500, 'rupee'))\
        .add_alt_id("pickaxe handle").add_alt_id("reinforced pickaxe").add_alt_id("reinforced pickaxe handle")\
        .add_alt_id("pick handle").add_alt_id("reinforced pick").add_alt_id("reinforced pick handle")\
        .set_action({"pick_handle": 1})
    ShopItem("pux").set_description("Pickaxe Upgrade Kit (×2.0625 Pick Power)")\
        .set_prereqs({"pick_sharpener": 0, "pick_weight": 0, "pick_handle": 0})\
        .set_money_cost({"Rupees": 800})\
        .set_text_price(compress_rup_clov(800, 'rupee'))\
        .add_alt_id("pickaxe upgrade kit").add_alt_id("pick upgrade kit").add_alt_id("pick kit")\
        .add_alt_id("pickaxe kit")\
        .set_action({"pick_sharpener": 1, "pick_weight": 1, "pick_handle": 1})

    ShopItem("au1").set_description("Axe Sharpener (×1.1 Axe Power)")\
        .set_prereqs({"axe_sharpener": 0})\
        .set_money_cost({"Rupees": 100})\
        .set_text_price(compress_rup_clov(100, 'rupee'))\
        .add_alt_id("axe sharpener").add_alt_id("sharpened axe")\
        .set_action({"axe_sharpener": 1})
    ShopItem("au2").set_description("Extra Axe Head Weight (×1.25 Axe Power)")\
        .set_prereqs({"axe_weight": 0})\
        .set_money_cost({"Rupees": 200})\
        .set_text_price(compress_rup_clov(200, 'rupee'))\
        .add_alt_id("axe head weight").add_alt_id("weighted axe").add_alt_id("extra axe weight")\
        .add_alt_id("weighted axe head").add_alt_id("extra axe head weight")\
        .set_action({"axe_weight": 1})
    ShopItem("au3").set_description("Reinforced Axe Handle (×1.5 Axe Power)")\
        .set_prereqs({"axe_handle": 0})\
        .set_money_cost({"Rupees": 500})\
        .set_text_price(compress_rup_clov(500, 'rupee'))\
        .add_alt_id("axe handle").add_alt_id("reinforced axe").add_alt_id("reinforced axe handle")\
        .set_action({"axe_handle": 1})
    ShopItem("aux").set_description("Axe Upgrade Kit (×2.0625 Axe Power)")\
        .set_prereqs({"axe_sharpener": 0, "axe_weight": 0, "axe_handle": 0})\
        .set_money_cost({"Rupees": 800})\
        .set_text_price(compress_rup_clov(800, 'rupee'))\
        .add_alt_id("axe upgrade kit").add_alt_id("axe kit")\
        .set_action({"axe_sharpener": 1, "axe_weight": 1, "axe_handle": 1})

    ShopItem("rnk1").set_description("VIP")\
        .set_prereqs({"rank": 0})\
        .set_money_cost({"Rupees": 50000})\
        .set_text_price(compress_rup_clov(50000, 'rupee'))\
        .add_alt_id("VIP")\
        .set_action({"rank": 1})
    ShopItem("rnk2").set_description("VIP+")\
        .set_prereqs({"rank": 1})\
        .set_money_cost({"Rupees": 500000})\
        .set_text_price(compress_rup_clov(500000, 'rupee'))\
        .add_alt_id("VIP+")\
        .set_action({"rank": 2})
    ShopItem("rnk3").set_description("Premium")\
        .set_prereqs({"rank": 2})\
        .set_money_cost({"Rupees": 5000000})\
        .set_text_price(compress_rup_clov(5000000, 'rupee'))\
        .add_alt_id("Prem").add_alt_id("Premium")\
        .set_action({"rank": 3})
    ShopItem("rnk4").set_description("Elite")\
        .set_prereqs({"rank": 3})\
        .set_money_cost({"Rupees": 50000000})\
        .set_text_price(compress_rup_clov(50000000, 'rupee'))\
        .add_alt_id("Elit").add_alt_id("Elite")\
        .set_action({"rank": 4})
    ShopItem("rnk5").set_description("Supreme")\
        .set_prereqs({"rank": 4})\
        .set_money_cost({"Rupees": 500000000})\
        .set_text_price(compress_rup_clov(500000000, 'rupee'))\
        .add_alt_id("Supr").add_alt_id("Super").add_alt_id("Supreme")\
        .set_action({"rank": 5})
    ShopItem("rnk6").set_description("Ultimate")\
        .set_prereqs({"rank": 5})\
        .set_money_cost({"Rupees": 5000000000})\
        .set_text_price(compress_rup_clov(5000000000, 'rupee'))\
        .add_alt_id("Ultimate").add_alt_id("Ulti").add_alt_id("Ult")\
        .set_action({"rank": 6})
    ShopItem("rnk7").set_description("Ultimate+")\
        .set_prereqs({"rank": 6})\
        .set_money_cost({"Rupees": 50000000000})\
        .set_text_price(compress_rup_clov(50000000000, 'rupee'))\
        .add_alt_id("Ultimate+").add_alt_id("Ulti+").add_alt_id("Ult+")\
        .set_action({"rank": 7})
    
    ShopItem("pb1").set_description("Page Booster Pack I")\
        .set_prereqs({"bonus slots": 0})\
        .set_money_cost({"Rupees": 1000})\
        .set_text_price(compress_rup_clov(1000, 'rupee'))\
        .add_alt_id("bonus slots 1").add_alt_id("page booster 1").add_alt_id("page booster pack 1").add_alt_id("paper booster pack 1")\
        .add_alt_id("bonus slots i").add_alt_id("page booster i").add_alt_id("page booster pack i").add_alt_id("paper booster pack i")\
        .add_alt_id("bonus slot 1").add_alt_id("page boost 1").add_alt_id("page boost pack 1").add_alt_id("paper boost pack 1")\
        .add_alt_id("bonus slot i").add_alt_id("page boost i").add_alt_id("page boost pack i").add_alt_id("paper boost pack i")\
        .add_alt_id("pbi")\
        .set_action({"bonus slots": 1})
    ShopItem("pb2").set_description("Page Booster Pack II")\
        .set_prereqs({"bonus slots": 1})\
        .set_money_cost({"Rupees": 5000})\
        .set_text_price(compress_rup_clov(5000, 'rupee'))\
        .add_alt_id("bonus slots 2").add_alt_id("page booster 2").add_alt_id("page booster pack 2").add_alt_id("paper booster pack 2")\
        .add_alt_id("bonus slots ii").add_alt_id("page booster ii").add_alt_id("page booster pack ii").add_alt_id("paper booster pack ii")\
        .add_alt_id("bonus slot 2").add_alt_id("page boost 2").add_alt_id("page boost pack 2").add_alt_id("paper boost pack 2")\
        .add_alt_id("bonus slot ii").add_alt_id("page boost ii").add_alt_id("page boost pack ii").add_alt_id("paper boost pack ii")\
        .add_alt_id("pbii")\
        .set_action({"bonus slots": 2})
    ShopItem("pb3").set_description("Page Booster Pack III")\
        .set_prereqs({"bonus slots": 2})\
        .set_money_cost({"Rupees": 25000})\
        .set_text_price(compress_rup_clov(25000, 'rupee'))\
        .add_alt_id("bonus slots 3").add_alt_id("page booster 3").add_alt_id("page booster pack 3").add_alt_id("paper booster pack 3")\
        .add_alt_id("bonus slots iii").add_alt_id("page booster iii").add_alt_id("page booster pack iii").add_alt_id("paper booster pack iii")\
        .add_alt_id("bonus slot 3").add_alt_id("page boost 3").add_alt_id("page boost pack 3").add_alt_id("paper boost pack 3")\
        .add_alt_id("bonus slot iii").add_alt_id("page boost iii").add_alt_id("page boost pack iii").add_alt_id("paper boost pack iii")\
        .add_alt_id("pbiii")\
        .set_action({"bonus slots": 3})
    ShopItem("pb4").set_description("Page Booster Pack IV")\
        .set_prereqs({"bonus slots": 3})\
        .set_money_cost({"Rupees": 125000})\
        .set_text_price(compress_rup_clov(125000, 'rupee'))\
        .add_alt_id("bonus slots 4").add_alt_id("page booster 4").add_alt_id("page booster pack 4").add_alt_id("paper booster pack 4")\
        .add_alt_id("bonus slots iv").add_alt_id("page booster iv").add_alt_id("page booster pack iv").add_alt_id("paper booster pack iv")\
        .add_alt_id("bonus slot 4").add_alt_id("page boost 4").add_alt_id("page boost pack 4").add_alt_id("paper boost pack 4")\
        .add_alt_id("bonus slot iv").add_alt_id("page boost iv").add_alt_id("page boost pack iv").add_alt_id("paper boost pack iv")\
        .add_alt_id("pbiv")\
        .set_action({"bonus slots": 4})
    ShopItem("pb5").set_description("Page Booster Pack V")\
        .set_prereqs({"bonus slots": 4})\
        .set_money_cost({"Rupees": 625000})\
        .set_text_price(compress_rup_clov(625000, 'rupee'))\
        .add_alt_id("bonus slots 5").add_alt_id("page booster 5").add_alt_id("page booster pack 5").add_alt_id("paper booster pack 5")\
        .add_alt_id("bonus slots v").add_alt_id("page booster v").add_alt_id("page booster pack v").add_alt_id("paper booster pack v")\
        .add_alt_id("bonus slot 5").add_alt_id("page boost 5").add_alt_id("page boost pack 5").add_alt_id("paper boost pack 5")\
        .add_alt_id("bonus slot v").add_alt_id("page boost v").add_alt_id("page boost pack v").add_alt_id("paper boost pack v")\
        .add_alt_id("pbv")\
        .set_action({"bonus slots": 5})
    ShopItem("pb6").set_description("Page Booster Pack VI")\
        .set_prereqs({"bonus slots": 5})\
        .set_money_cost({"Rupees": 3125000})\
        .set_text_price(compress_rup_clov(3125000, 'rupee'))\
        .add_alt_id("bonus slots 6").add_alt_id("page booster 6").add_alt_id("page booster pack 6").add_alt_id("paper booster pack 6")\
        .add_alt_id("bonus slots vi").add_alt_id("page booster vi").add_alt_id("page booster pack vi").add_alt_id("paper booster pack vi")\
        .add_alt_id("bonus slot 6").add_alt_id("page boost 6").add_alt_id("page boost pack 6").add_alt_id("paper boost pack 6")\
        .add_alt_id("bonus slot vi").add_alt_id("page boost vi").add_alt_id("page boost pack vi").add_alt_id("paper boost pack vi")\
        .add_alt_id("pbvi")\
        .set_action({"bonus slots": 6})

##    def increase_global_multi(boost, boost_type):
##        zako = get_user_data(405968021337669632)
##        if boost_type == 'add':
##            zako.add_lootbox_count_boost(zako.lootbox_counting_multiplier()*boost)
##        if boost_type == 'mult':
##            zako.mult_lootbox_count_boost(boost)
##        if boost_type == 'expon':
##            zako.expon_lootbox_count_boost(boost)
##        save_user(zako)
    ShopItem("ca1").set_description("Counting Multi +20%")\
        .set_prereqs({"count_upgrades": 0})\
        .set_money_cost({"Kups": 10000})\
        .set_text_price(compress_coin(10000))\
        .set_action({"count_upgrades": 1})
    ShopItem("ca2").set_description("Counting Multi +30%")\
        .set_prereqs({"count_upgrades": 1})\
        .set_money_cost({"Kups": 20000})\
        .set_text_price(compress_coin(20000))\
        .set_action({"count_upgrades": 2})
    ShopItem("ca3").set_description("Counting Multi +50%")\
        .set_prereqs({"count_upgrades": 2})\
        .set_action({"count_upgrades": 3})\
        .set_money_cost({"Kups": 50000})\
        .set_text_price(compress_coin(50000))
    ShopItem("ca4").set_description("Counting Multi +100%")\
        .set_prereqs({"count_upgrades": 3})\
        .set_action({"count_upgrades": 4})\
        .set_money_cost({"Kups": 120000})\
        .set_text_price(compress_coin(120000))
    ShopItem("ca5").set_description("Counting Multi +200%")\
        .set_prereqs({"count_upgrades": 4})\
        .set_action({"count_upgrades": 5})\
        .set_money_cost({"Kups": 250000})\
        .set_text_price(compress_coin(250000))
    ShopItem("ca6").set_description("Counting Multi +250%")\
        .set_prereqs({"count_upgrades": 5})\
        .set_action({"count_upgrades": 6})\
        .set_money_cost({"Kups": 310000})\
        .set_text_price(compress_coin(310000))
    ShopItem("ca7").set_description("Counting Multi +350%")\
        .set_prereqs({"count_upgrades": 6})\
        .set_action({"count_upgrades": 7})\
        .set_money_cost({"Kups": 500000})\
        .set_text_price(compress_coin(500000))
    ShopItem("ca8").set_description("Counting Multi +400%")\
        .set_prereqs({"count_upgrades": 7})\
        .set_action({"count_upgrades": 8})\
        .set_money_cost({"Kups": 700000})\
        .set_text_price(compress_coin(700000))
    ShopItem("ca9").set_description("Counting Multi +600%")\
        .set_prereqs({"count_upgrades": 8})\
        .set_action({"count_upgrades": 9})\
        .set_money_cost({"Kups": 1000000})\
        .set_text_price(compress_coin(1000000))
    ShopItem("ca10").set_description("Counting Multi +1000%")\
        .set_prereqs({"count_upgrades": 9})\
        .set_action({"count_upgrades": 10})\
        .set_money_cost({"Kups": 1600000})\
        .set_text_price(compress_coin(1600000))
    ShopItem("ca11").set_description("Counting Multi +2000%")\
        .set_prereqs({"count_upgrades": 10})\
        .set_action({"count_upgrades": 11})\
        .set_money_cost({"Kups": 3500000})\
        .set_text_price(compress_coin(3500000))
    ShopItem("ca12").set_description("Counting Multi +5000%")\
        .set_prereqs({"count_upgrades": 11})\
        .set_action({"count_upgrades": 12})\
        .set_money_cost({"Kups": 9000000})\
        .set_text_price(compress_coin(9000000))
    ShopItem("ciu1").set_description("Counting Iteration Upgrade I (Unlocks multiplicitave counting upgrades)")\
        .set_prereqs({"count_iteration_upgrade": 0, "count_upgrades": 12})\
        .set_money_cost({"Kups": 20000000})\
        .set_text_price(compress_coin(20000000))\
        .set_action({"count_iteration_upgrade": 1})
    ShopItem("cm1").set_description("Counting Multi ×1.2")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 12})\
        .set_action({"count_upgrades": 13})\
        .set_money_cost({"Kups": 1000000})\
        .set_text_price(compress_coin(1000000))
    ShopItem("cm2").set_description("Counting Multi ×1.3")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 13})\
        .set_action({"count_upgrades": 14})\
        .set_money_cost({"Kups": 2000000})\
        .set_text_price(compress_coin(2000000))
    ShopItem("cm3").set_description("Counting Multi ×1.5")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 14})\
        .set_action({"count_upgrades": 15})\
        .set_money_cost({"Kups": 5000000})\
        .set_text_price(compress_coin(5000000))
    ShopItem("cm4").set_description("Counting Multi ×2")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 15})\
        .set_action({"count_upgrades": 16})\
        .set_money_cost({"Kups": 12000000})\
        .set_text_price(compress_coin(12000000))
    ShopItem("cm5").set_description("Counting Multi ×3")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 16})\
        .set_action({"count_upgrades": 17})\
        .set_money_cost({"Kups": 25000000})\
        .set_text_price(compress_coin(25000000))
    ShopItem("cm6").set_description("Counting Multi ×3.5")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 17})\
        .set_action({"count_upgrades": 18})\
        .set_money_cost({"Kups": 31000000})\
        .set_text_price(compress_coin(31000000))
    ShopItem("cm7").set_description("Counting Multi ×4.5")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 18})\
        .set_action({"count_upgrades": 19})\
        .set_money_cost({"Kups": 50000000})\
        .set_text_price(compress_coin(50000000))
    ShopItem("cm8").set_description("Counting Multi ×5")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 19})\
        .set_action({"count_upgrades": 20})\
        .set_money_cost({"Kups": 70000000})\
        .set_text_price(compress_coin(70000000))
    ShopItem("cm9").set_description("Counting Multi ×7")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 20})\
        .set_action({"count_upgrades": 21})\
        .set_money_cost({"Kups": 100000000})\
        .set_text_price(compress_coin(100000000))
    ShopItem("cm10").set_description("Counting Multi ×10")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 21})\
        .set_action({"count_upgrades": 22})\
        .set_money_cost({"Kups": 160000000})\
        .set_text_price(compress_coin(160000000))
    ShopItem("cm11").set_description("Counting Multi ×20")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 22})\
        .set_action({"count_upgrades": 23})\
        .set_money_cost({"Kups": 350000000})\
        .set_text_price(compress_coin(350000000))
    ShopItem("cm12").set_description("Counting Multi ×50")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 23})\
        .set_action({"count_upgrades": 24})\
        .set_money_cost({"Kups": 900000000})\
        .set_text_price(compress_coin(900000000))
    ShopItem("ciu2").set_description("Counting Iteration Upgrade II (Unlocks exponential counting upgrades)")\
        .set_prereqs({"count_iteration_upgrade": 1, "count_upgrades": 24})\
        .set_money_cost({"Kups": 20000000000})\
        .set_text_price(compress_coin(20000000000))\
        .set_action({"count_iteration_upgrade": 2})
    ShopItem("ce1").set_description("Counting Multi ^1.2")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 24})\
        .set_action({"count_upgrades": 25})\
        .set_money_cost({"Kups": 1000000000})\
        .set_text_price(compress_coin(1000000000))
    ShopItem("ce2").set_description("Counting Multi ^1.3")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 25})\
        .set_action({"count_upgrades": 26})\
        .set_money_cost({"Kups": 2000000000})\
        .set_text_price(compress_coin(2000000000))
    ShopItem("ce3").set_description("Counting Multi ^1.5")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 26})\
        .set_action({"count_upgrades": 27})\
        .set_money_cost({"Kups": 5000000000})\
        .set_text_price(compress_coin(5000000000))
    ShopItem("ce4").set_description("Counting Multi ^2")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 27})\
        .set_action({"count_upgrades": 28})\
        .set_money_cost({"Kups": 12000000000})\
        .set_text_price(compress_coin(12000000000))
    ShopItem("ce5").set_description("Counting Multi ^3")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 28})\
        .set_action({"count_upgrades": 29})\
        .set_money_cost({"Kups": 25000000000})\
        .set_text_price(compress_coin(25000000000))
    ShopItem("ce6").set_description("Counting Multi ^3.5")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 29})\
        .set_action({"count_upgrades": 30})\
        .set_money_cost({"Kups": 31000000000})\
        .set_text_price(compress_coin(31000000000))
    ShopItem("ce7").set_description("Counting Multi ^4.5")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 30})\
        .set_action({"count_upgrades": 31})\
        .set_money_cost({"Kups": 50000000000})\
        .set_text_price(compress_coin(50000000000))
    ShopItem("ce8").set_description("Counting Multi ^5")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 31})\
        .set_action({"count_upgrades": 32})\
        .set_money_cost({"Kups": 70000000000})\
        .set_text_price(compress_coin(70000000000))
    ShopItem("ce9").set_description("Counting Multi ^7")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 32})\
        .set_action({"count_upgrades": 33})\
        .set_money_cost({"Kups": 100000000000})\
        .set_text_price(compress_coin(100000000000))
    ShopItem("ce10").set_description("Counting Multi ^10")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 33})\
        .set_action({"count_upgrades": 34})\
        .set_money_cost({"Kups": 160000000000})\
        .set_text_price(compress_coin(160000000000))
    ShopItem("ce11").set_description("Counting Multi ^20")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 34})\
        .set_action({"count_upgrades": 35})\
        .set_money_cost({"Kups": 350000000000})\
        .set_text_price(compress_coin(350000000000))
    ShopItem("ce12").set_description("Counting Multi ^50")\
        .set_prereqs({"count_iteration_upgrade": 2, "count_upgrades": 35})\
        .set_action({"count_upgrades": 36})\
        .set_money_cost({"Kups": 900000000000})\
        .set_text_price(compress_coin(900000000000))
