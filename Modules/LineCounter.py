from Modules.Utilities import Utilities
from colorama import Fore, Style
import shutil
import time
import os
import re

class LineCounter():
    
    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None

    def startup(self):
        self.to_write.clear()
        self.utilities.clear()
        print(self.utilities.custom_color() + "[1]" + Fore.LIGHTWHITE_EX + " | Count all lines")
        print(self.utilities.custom_color() + "[2]" + Fore.LIGHTWHITE_EX + " | Count all lines containing a certain string")
        print(self.utilities.custom_color() + "\nPress enter to go back to the main menu.")
        try:
            select = input("\n" + self.utilities.custom_color() + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)
            
            self.modules = {
                "1": "self.module_1()",
                "2": "self.module_2()"
            }
            if select in self.modules:
                eval(self.modules[select])

        except Exception as e:
            print(e)
            self.utilities.pleasewait()
            self.startup()

    
    def module_1(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        self.utilities.pleasewait()
        self.startup()

    def module_2(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            word = input(self.utilities.custom_color() + "Input the word to search for: ".center(self.width).split(':')[0] + ': ' + Fore.LIGHTWHITE_EX)
            for lines in file:
                if word not in lines:
                    pass
                else:
                    self.to_write.append(lines)
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        output = self.utilities.savelocation("Line Counter") + "/" + self.utilities.files("linesCounter") + "[{}]".format(word)
        with open(output + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()
