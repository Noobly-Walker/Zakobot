from datetime import *
from bot import ResourceParse
from bot import NumberCronch
import random

class ServerData:

    ### class init
    
    def __init__(self):
        # All the data about the user.
        # Use setdefault() when collecting data, to ensure you always get something (no [Exception]s from lack of data)
        self.data = {
            'name': "undefined",
            'id': float(0),
            'users': 0,
            'bad users': [0,1], #[alt, bot]
            'economy': True,
            'crafting': True,
            'prefix': 'z!',
            'potions': {
                'debuff': True,
                'tf': True,
                'nsfw': False,
                'vore': False,
                'gore': False,
                'fetish': False
                },
            'levels': True,
            'lv_msg': True,
            'dice': True,
            'portal': True,
            'dedicated_portal': -1,
            'counting': True,
            'potion': True,
            'network data': {
                'acronym': '',
                'category': 'General',
                'allow ads': False,
                'server link': '',
                'description': ''
                },
            'show hints': True,
            'current count': [0.0,0]
            }

    ### important functions
    
    # add a ton of data at the same time using Dict
    def set_data(self, add: dict):
        for key in add.keys():
            self.data[key] = add[key]

# Min value of 2D array
def min_2d(array):
    # I have no fucking clue how this works.
    # All I know is that Stack Overflow is a good source.
    return min([min(r) for r in array])
