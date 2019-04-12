from Modules.Utilities import Utilities
from colorama import Fore, Style
import shutil
import time
import os

class DuplicateRemover():
    
    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None

    def startup(self):
        self.to_write.clear()
        self.utilities.clear()
        self.module_1()

    def module_1(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
            uniquelines = set(file.readlines())

        if not len(uniquelines) == total_lines:
            output = self.utilities.savelocation("Duplicate Remover") + "/" + self.utilities.files("DuplicateRemover")
            with open(output + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(uniquelines)
            print("[+] Duplicates Removed: %s".center(self.width) % str(len(uniquelines) - total_lines))
        else:
            print("[-] No duplicates found".center(self.width))
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        self.utilities.pleasewait()
        self.startup()