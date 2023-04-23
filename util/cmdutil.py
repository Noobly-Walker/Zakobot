import sys
from datetime import datetime, timezone
from traceback import format_exc, format_tb
import os
os.system("")

class cmdutil:
    def __init__(self):
        try:           
            self.color = sys.stdout.shell.write
            self.source = "idle"
            
            self.colormap = {
                "red": "COMMENT",
                "yellow": "KEYWORD",
                "green": "STRING",
                "blue": "stdout",
                "purple": "BUILTIN",
                "white": "SYNC",
                "brown": "console",
                "default": "SYNC"
                }
        except AttributeError:
            self.source = "cmd"
            self.colormap = {
                "red": "\033[91m",
                "yellow": "\033[93m",
                "green": "\033[92m",
                "blue": "\033[94m",
                "purple": "\033[95m",
                "white": "\033[97m",
                "brown": "\033[31m",
                "default": "\033[0m"
                }
        self.num = [0]

    def print(self, text, color="default", endswith="\n"):
        if self.source == "idle": self.color(text + endswith, self.colormap[color])
        if self.source == "cmd": print(self.colormap[color] + text, end=self.colormap["default"] + endswith)

    def ts(self):
        time = datetime.now(timezone.utc)
        stamp = datetime.timestamp(time) #I did this on purpose, leave me alone.
        timeText = time.strftime("%Y-%m-%d %H:%M:%S UTC")
        return timeText

    def log(self, text, endswith="\n"):
        self.print(f"[{self.ts()}][LOG] " + text, "default", endswith)

    def warn(self, text, endswith="\n"):
        self.print(f"[{self.ts()}][WARN] " + text, "yellow", endswith)

    def error(self, text, endswith="\n"):
        errortype = "error"
        if issubclass(type(text), Exception):
            errortype = str(type(text)).replace("<class '", "").replace("'>", "")
            text = str(text) + "\nTraceback (most recent call last):\n" + "\n".join(format_tb(text.__traceback__))
            endswith = ""
        errortype = str(errortype).upper()
        #if traceback != "": traceback = "\n" + "\nTraceback (most recent call last):\n".join(format_tb(traceback))
        self.print(f"[{self.ts()}][{errortype}] {text}", "brown", endswith)

    def debug(self, text="", endswith="\n"):
        self.print(f"[{self.ts()}][DEBUG][{self.num[0]}] " + str(text), "blue", endswith)
        self.num[0] += 1

    def test(self):
        self.log(f"Running on {self.source}.")
        self.log(f"Testing colortext...")
        for i in list(self.colormap.keys()):
            self.print(f"This is {i}.", i)
        self.log(f"Testing log methods...")
        self.log("This is a log. Like print(), but with a timestamp.")
        self.warn("This is a warning. Something's gone wrong, but it's okay.")
        self.error("This is an error. Something broke.")
        self.debug("This is a breakpoint. Probably testing something.")
        self.debug("This is a breakpoint. Probably testing something.")
        self.debug("This is a breakpoint. Probably testing something.")
        self.debug("This is a breakpoint. Probably testing something.")
        self.debug("This is a breakpoint. Probably testing something.")
        self.num = [0]
        
#cmd = cmdutil()
#cmd.test()
