from Modules.Utilities import Utilities
from colorama import Fore, Style
import shutil
import time
import os
import re


class EmptyLineRemover():

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
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".format(total_lines).rstrip().center(self.width) + Style.RESET_ALL)

            cleaned = list(filter(lambda x: not re.match(r'^\s*$', x), file.readlines()))
            print(self.utilities.custom_color() + "[+] Time took: {}".rstrip().center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            if len(cleaned) >= 1 and len(cleaned) < total_lines:
                output = self.utilities.savelocation("Empty Line Remover") + "/" + self.utilities.files("EmptylinesRemover")
                with open(output + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(cleaned)
                print(self.utilities.custom_color() + "[+] Empty Lines Removed: %s".rstrip().center(self.width) % str(int(total_lines) - int(len(cleaned))))
            else:
                print(self.utilities.custom_color() + "No invalid lines were found.".rstrip().center(self.width))
        self.utilities.pleasewait()
        self.startup()
