from bot.UserData import UserData
from bot.util.ToolUtil import *


class ShopItem:
    # Ensures that specific variables are ALWAYS a specific type.
    id: str
    alt_ids: list
    name: str
    text_price: str
    prereq: dict
    cost: dict
    money_cost: dict
    inventory_cost: dict
    chest_cost: dict
    tree_cost: dict
    action: dict
    daily_uses: int
    crafted: bool
    add_items: object

    # Because of a line in __init__, shop_items will ALWAYS have every shop item, whether or not it is valid.
    shop_items = []

    def __init__(self, id: str):
        self.id = id
        self.alt_ids = []
        self.name = ""
        self.text_price = ""  # The price of the object, expressed in WORDS. (5r, 100s)
        self.prereq = {}  # User prerequisites before buying. These are EXACTs, not MINIMUMs
        self.min_prereq = {}  # User prerequisites before buying. These are MINIMUMs, like cost
        # However, unlike cost, min_prereq does NOT spend the material
        self.cost = {} # Cost from base.
        self.money_cost = {} # Cost to purchase. Use negative values when giving user money, e.g. 1 rupee = 100 coins trade
        self.action = {}  # Changes to user after buying
        self.shop_items.append(self)  # Because of this, shop_items will ALWAYS have every shop item, valid or not.
        self.daily_uses = -1  # Number of times this can be used per day. -1 means infinite uses per day.
        self.crafted = False  # whether or not this item is crafted or bought in shop

        # ---- INVENTORY STUFFS ---- #

        self.inventory_cost = {}  # inventory cost, like Stone. Format for key/value pair is Name: Value
        # So if you want something to cost 5 Stone and 1 Coal, use: {'Stone': 5, 'Coal': 1}
        self.tree_cost = {}
        self.chest_cost = {}
        self.autocraft_prereqs = {}  # prerequisites specifically for autocrafting
        self.autocraft_min_prereqs = {}  # minimum-prerequisites specifically for autocrafting

        # ---- VISIBILITY STUFFS ---- #
        self.visible_prereqs = {}

        def blank_post_buy(user: UserData):
            pass

        self.post_buy = blank_post_buy

    @staticmethod
    def set_function(function:object):
        for item in ShopItem.shop_items:
            item.add_items = function

    def set_alt_ids(self, alt_ids: list):
        self.alt_ids = alt_ids
        return self

    def add_alt_id(self, alt_id: str):
        self.alt_ids.append(alt_id)
        return self

    def set_description(self, desc: str):
        self.name = desc
        return self

    def set_prereqs(self, prereqs: dict):
        self.prereq = prereqs
        return self

    def set_min_prereqs(self, min_prereqs: dict):
        self.min_prereq = min_prereqs
        return self

    def add_prereqs(self, prereqs: dict):
        for key in prereqs.keys():
            self.prereq[key] = prereqs[key]
        return self

    def add_min_prereqs(self, min_prereqs: dict):
        for key in min_prereqs.keys():
            self.min_prereq[key] = min_prereqs[key]
        return self

    def generate_auto_prereqs(self):
        # generates the auto-prereqs from regular prereqs
        # mostly just simplifies stuff for us
        for key in self.prereq.keys():
            if self.prereq[key] == True:  # as in, regular crafting.
                # stations which have a "1 for regular crafting, 2 for auto crafting"
                if key == 'can smelt':
                    self.add_auto_prereqs({'auto furnace': 1})
                if key == 'can blast':
                    self.add_auto_prereqs({'auto blast furnace': 1})
                if key == 'can adamantize':
                    self.add_auto_prereqs({'auto adamant furnace': 1})
        for key in self.min_prereq.keys():
            pass  # If we ever need to, this is here. But right now, we don't.
        if self.crafted:
            self.add_auto_prereqs({'auto crafting': 1})

    def set_auto_prereqs(self, auto_prereqs: dict):
        self.autocraft_prereqs = auto_prereqs
        return self

    def set_auto_min_prereqs(self, auto_min_prereqs: dict):
        self.autocraft_min_prereqs = auto_min_prereqs
        return self

    def add_auto_prereqs(self, auto_prereqs: dict):
        for key in auto_prereqs.keys():
            self.autocraft_prereqs[key] = auto_prereqs[key]
        return self

    def add_auto_min_prereqs(self, auto_min_prereqs: dict):
        for key in auto_min_prereqs.keys():
            self.autocraft_min_prereqs[key] = auto_min_prereqs[key]
        return self

    def set_cost(self, cost: dict):
        self.cost = cost
        return self

    def set_money_cost(self, cost: dict):
        self.money_cost = cost
        return self

    def set_inventory_cost(self, cost: dict):
        self.inventory_cost = cost
        return self

    def set_tree_cost(self, cost: dict):
        self.tree_cost = cost
        return self

    def set_chest_cost(self, cost:dict):
        self.chest_cost = cost
        return self

    def set_text_price(self, textprice: str):
        self.text_price = textprice
        return self

    def set_action(self, action: dict):
        self.action = action
        return self

    def set_daily_uses(self, uses: int):
        self.daily_uses = uses
        return self

    def set_post_buy(self, post_buy: callable):
        self.post_buy = post_buy
        return self

    def set_crafted(self, crafted: bool):
        self.crafted = crafted
        return self

    def is_crafted(self):
        return self.set_crafted(True)

    def same_id(self, compare: str):
        if self.id == compare:
            return True
        else:
            for id in self.alt_ids:
                if id == compare:
                    return True
        return False

    def prereqs_met(self, user: UserData):
        for key in self.prereq.keys():
            if not user.hasBuilding(key, self.prereq[key], True):
                if user.data.get(key) is None:
                    return False
                if user.data[key] != self.prereq[key]:
                    # User does not exactly meet prerequisites.
                    return False
        for key in self.min_prereq.keys():
            if not user.hasBuilding(key, self.min_prereq[key], False):
                if user.data.get(key) is None:
                    return False
                if user.data.get(key) < self.min_prereq[key]:
                    # User does not fulfill minimum
                    return False
        return True  # prereqs are good

    def can_afford(self, user: UserData):
        try:
            for key in self.cost.keys():
                if user.township()[key]["count"] < self.cost[key]:
                    # User has less base var than the cost.
                    return False
            for key in self.money_cost.keys():
                if user.wallet()[key] < self.money_cost[key]:
                    # User has less money than the cost.
                    return False
            for key in self.inventory_cost.keys():
                if user.inventory()[key][0] < self.inventory_cost[key]:
                    # User has less of item than cost.
                    return False
            for key in self.tree_cost.keys():
                if user.trees()[key] < self.tree_cost[key]:
                    # User has less of tree than cost.
                    return False
            for key in self.chest_cost.keys():
                if user.chests()[key] < self.chest_cost[key]:
                    return False
            return True
        except Exception:
            return False

    def can_purchase_daytimer(self, user: UserData):
        if self.daily_uses == -1:
            return True
        # Not infinite uses per day.
        user.data.setdefault('daily_shop_purchases', {})
        purchases = user.data['daily_shop_purchases'].setdefault(self.id, 0)
        if purchases >= self.daily_uses:
            # More uses per day than allowed!
            return False
        return True

    def can_buy(self, user: UserData, crafted: bool):
        if not self.crafted and crafted:
            # requesting only crafted items, this is not!
            return False
        if self.crafted and not crafted:
            # requesting only bought items, this is not!
            return False

        if not self.prereqs_met(user):
            return False  # prereqs not met

        if not self.can_afford(user):
            return False  # cannot afford this item

        if not self.can_purchase_daytimer(user):
            return False  # max purchases per day

        return True

    def buy(self, user: UserData, crafted: bool):  # DOES **NOT** SAVE!
        if self.can_buy(user, crafted):
            user.set_data(self.action)
            for key in self.cost.keys():
                # These all exist, because if they didn't, can_buy would return False.
                user.township()[key]["count"] -= self.cost[key]
            for key in self.money_cost.keys():
                user.wallet()[key] -= self.money_cost[key]
            for key in self.inventory_cost.keys():
                user = self.add_items(user, {key: [-self.inventory_cost[key]]})
            for key in self.tree_cost.keys():
                user.trees()[key] -= self.tree_cost[key]
            for key in self.chest_cost.keys():
                user.chests()[key] -= self.chest_cost[key]
            if self.daily_uses != -1:
                # Known to exist due to can_buy using setdefault()
                user.data['daily_shop_purchases'][self.id] += 1
            self.post_buy(user)
            return True  # successful purchase
        return False  # no purchase

    @staticmethod
    def infinite_autocraft_all(user: UserData):
        run = True
        executions = 100
        while run and executions > 0:
            run = False
            for item in ShopItem.shop_items:
                if item.autocraft(user):
                    print(f"Successfully autocrafted {item.name}")
                    run = True  # autocrafted something, try again
                    executions -= 1
                else:
                    print(f"Failed to autocraft {item.name}")

    # Autocrafting shit, had to go right after making this
    def autocraft(self, user: UserData):
        if not self.should_autocraft(user):
            return False  # should not autocraft, did not autocraft anything, end.
        else:
            return self.buy(user, self.crafted)

    def should_autocraft(self, user: UserData):
        autocrafteds = user.autocrafted_items()
        if len(autocrafteds.keys()) == 0:
            return False  # user doesn't want anything autocrafted anyway
        for item in autocrafteds.keys():  # "item" is item that wants to be autocrafted
            craft_id = autocrafteds[item][0]  # id of the item that needs to be autocrafted
            num = autocrafteds[item][1]  # number of items to stop autocrafting at
            if not self.same_id(craft_id):
                continue  # not this item, check next autocraft
            if user.inventory()[item][0] >= num:
                continue  # User already has enough items, check next autocraft
            for key in self.autocraft_prereqs.keys():
                print("Checking prereq \"", key, "\" Note: \"", "a", "\"")
                if not user.hasBuilding(key, self.autocraft_prereqs[key], True):
                    if user.data.get(key) is None:
                        return False
                    if user.data.get(key) != self.autocraft_prereqs[key]:
                        # User does not exactly meet prerequisites.
                        return False  # and won't, even in the next cycles.
            for key in self.autocraft_min_prereqs.keys():
                if not user.hasBuilding(key, self.autocraft_min_prereqs[key], False):
                    if user.data[key] < self.autocraft_min_prereqs[key]:
                        # User does not exactly meet minimum prerequisites
                        return False  # and won't, even in the next cycles.
            return True  # autocraft!
        return False  # nothing needs to be autocrafted

    def get_id(self):
        # What the user should see as the ID
        return "ID {0}".format(self.id)

    def get_text(self):
        # What the user should see this as.
        return "**{0}**\n{1}".format(self.name, self.text_price)

    def set_visible_prereqs(self, prereqs: dict):
        self.visible_prereqs = prereqs
        return self

    def is_visible(self, user: UserData, crafted):
        for key in self.visible_prereqs.keys():
            try:
                if user.data[key] != self.visible_prereqs[key]:
                    # Does not exactly meet requirements, so they can't see it!
                    return False
            except Exception:
                return False
        return self.can_buy(user, crafted)

    @staticmethod
    def finalize():
        for item in ShopItem.shop_items:
            item.generate_auto_prereqs()
