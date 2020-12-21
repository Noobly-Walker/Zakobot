import builtins
from data.FileHandler import *
from bot.UserData import UserData


def load_all_users():
    for root, dirs, files in os.walk("data/user"):
        for file in files:
            id = int(file[:-4])
            user = get_user_data(id)

def to_array(data: str):
    out = []
    to_append = ""
    while len(data) != 0:
        if data[:1] == "\t":
            out.append(to_append)
            to_append = ""
            data = data[1:]
        else:
            to_append += data[:1]
            data = data[1:]
    out.append(to_append)
    return out


def get_rank(rank: str):
    if rank == "Prem":
        return 3
    if rank == "VIP+":
        return 2
    if rank == "VIP":
        return 1
    return 0


def get_pickaxe(power: int):
    # get pickaxe # using inverted map
    inv_pickaxe_powers = {v: k for k, v in UserData.pickaxe_powers.items()}
    return inv_pickaxe_powers[power]


def get_pickaxe_multiplier(multi: float):
    sharp, weight, handle = 0, 0, 0
    if multi > 1.1:
        sharp = 1
        multi /= 1.1
    if multi > 1.25:
        weight = 1
        multi /= 1.25
    if multi > 1.5:
        handle = 1
        multi /= 1.5
    return sharp, weight, handle, multi


def float(num: str):  # Intentionally shadows builtins.int() because commas
    if num == "":
        return 0.0
    return builtins.float(num.replace(',', ''))


def int(num: str):  # Intentionally shadowing builtins.int() because this also takes care of commas.
    if num == "":
        return 0  # Just in case.
    return builtins.int(builtins.float(num.replace(',', '')))

