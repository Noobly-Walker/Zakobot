from os import walk
from sys import exit
import json

class Config:
        def __init__(self):
                try:
                        try:
                                self.config = config = self.read_config('config.txt')
                        except Exception:
                                self.config = config = self.read_config('C:\\B\\zako\\config.txt')
                        self.dev_info = config['dev_info']
                        self.bot_info = config['bot_info']
                        self.devmode = config['devmode']
                except:
                        self.config = self.default_config()

        def read_config(self, filename:str):
                for root, dirs, files in walk('.'):
                        dirs[:] = []
                        if filename in files:
                                with open(filename) as f:
                                        config = json.load(f)
                                return config
                return None

        def write_config(self, filename:str):
                with open(filename, 'w+') as f:
                        f.write(json.dumps(self.config, indent=4))

        def default_config(self):
                alpha = "\u03b1"
                self.dev_info = {
                        'developer_mode': '0',
                        'version': f"{alpha}2.15.0"
                }
                version = self.dev_info['version']
                self.bot_info = {
                        'desc': f"OmniCore's bot boi v{version}, proudly serving OmniCore, BLZK, InfinityReverb, and Foxxo's RP Mansion since UNIX48!",
                        'prefix': 'z/'
                }
                self.devmode = {
                        0: '0',
                        1: '1'
                }

                self.config = {
                        'dev_info': self.dev_info,
                        'bot_info': self.bot_info,
                        'devmode': self.devmode
                }

                self.write_config('config.txt')
