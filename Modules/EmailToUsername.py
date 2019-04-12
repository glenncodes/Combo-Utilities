from Modules.Utilities import Utilities
from colorama import Fore, Style
import shutil
import time
import os

class EmailToUsername():
    
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
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            output = self.utilities.savelocation("Email To Username") + "/" + self.utilities.files("EmailToUsername")

            for line in file:
                lines = line.split(":")
                self.to_write.append(lines[0].split("@")[0] + ":" + lines[1])

        print(self.utilities.custom_color() + "[+] lines Converted: %s".rstrip().center(self.width) % total_lines)
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(output + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()

