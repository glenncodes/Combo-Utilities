from Modules.Utilities import Utilities
from colorama import Fore, Style
import random
import shutil
import time
import os

class RandomizeLines():
    
    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None

    def startup(self):
        self.utilities.clear()
        self.to_write.clear()
        self.module_1()
    
    def module_1(self):
        with open(Utilities().openfile(), 'r', errors="ignore") as file:
            lines = file.readlines()
            total_lines = Utilities().rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + "Loaded {} ".format(os.path.basename(file.name)).center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
            output = Utilities().savelocation("Randomize Lines") + "/" + Utilities().files("Randomizelines")
            amount = input(self.utilities.custom_color() + "[?] How many times would you like to randomize?: ".center(self.width).split(":")[0] + ": ")
            for _ in range(int(amount)):
                random.shuffle(lines)
                print(f"[+] Randomized {_} times.".center(self.width), end="\r")
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(output + Utilities().currenttime() + ".txt", "a", errors="ignore") as output:
                output.writelines(lines)
            self.utilities.pleasewait()
            self.startup()
