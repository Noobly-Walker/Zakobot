from os.path import splitext
from sqlite3 import connect as sqlConnect
# Zako source code ©2022 Noobly Walker, ©2022 OmniCoreStudios
from util.cmdutil import cmdutil
text = cmdutil()

def addInventoryTable():
    dataInv = sqlConnect(f".\\playerdata\\inventory.db")
    dataInv.execute("""
CREATE TABLE inventory (
    userID TEXT,
    itemName TEXT,
    quantity TEXT,
    isFavorite BOOLEAN DEFAULT false,
    canBuy BOOLEAN DEFAULT false
    )
""")
    dataInv.commit() # saves
    dataInv.close() # closes file

def addItem(user, item, quantity):
    if not exists(f".\\playerdata\\inventory.db"): addInventoryTable()
    dataInv = sqlConnect(f".\\playerdata\\inventory.db")
    if quantity != 0: #items can be removed by having quantity be negative
        invQuan = dataInv.execute(f"""SELECT quantity FROM inventory WHERE (userID, itemName) VALUES ({user.id}, {item})""")
        if invQuan == None: #that entry doesn't exist
            dataInv.execute(f"""INSERT INTO inventory (userID, itemName, quantity) VALUES ({user.id}, {item}, {quantity})""")
            invQuan = 0
        else: 
            dataInv.execute(f"""INSERT INTO inventory quantity VALUE {invQuan+quantity}""")
        if invQuan+quantity > 3:
            dataInv.execute(f"""INSERT INTO inventory canBuy VALUE true""")
    dataInv.commit() # saves
    dataInv.close() # closes file
