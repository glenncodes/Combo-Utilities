from Modules.Utilities import Utilities
from colorama import Fore, Style
import shutil
import time
import os
import re

class ComboParser():

    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None

    def startup(self):
        self.utilities.clear()
        self.to_write.clear()
        print(self.utilities.custom_color() + "[1]" + Fore.LIGHTWHITE_EX + " | Password:Email/Username -> Email/Username:Password [Works for reversing email:password too]")
        print(self.utilities.custom_color() + "[2]" + Fore.LIGHTWHITE_EX + " | Username/email:Password:Email/username -> 2 files [user:pass, email:pass]")
        print(self.utilities.custom_color() + "[3]" + Fore.LIGHTWHITE_EX + " | Email Extractor")
        print(self.utilities.custom_color() + "\nPress enter to go back to the main menu.")
        try:
            select = input("\n" + self.utilities.custom_color() + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

            self.modules = {
                "1": "self.module_1()",
                "2": "self.module_2()",
                "3": "self.module_3()"
            }
            if select in self.modules:
                eval(self.modules[select])
        except Exception:
            self.utilities.pleasewait()
            self.startup()


    def module_1(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            for lines in self.utilities.progressbar(file, total_lines):
                tmp = lines.split(":")
                self.to_write.append(tmp[0].rstrip() + ':' + tmp[1].rstrip() + '\n')
        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Parser") + '/' + self.utilities.files("ComboParser") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

    def module_2(self):
        dest = []
        dest2 = []
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            for lines in self.utilities.progressbar(file, total_lines):
                eachlines = lines.split()
                dest.append(eachlines[2] + ":" + eachlines[1] + "\n")
                dest2.append(eachlines[0] + ":" + eachlines[1] + "\n")
        if len(dest) >= 1 and len(dest2) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Parser") + '/' + self.utilities.files("ComboParser1") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(dest)
            with open(self.utilities.savelocation("Combo Parser") + '/' + self.utilities.files("ComboParser2") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile2:
                outfile2.writelines(dest2)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()
    
    def module_3(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            for lines in self.utilities.progressbar(file, total_lines):
                match = re.search(r"""(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-zA-Z0-9-]*[a-zA-Z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", lines)
                if match:
                    self.to_write.append(match.group(0) + "\n")

        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Parser") + '/' + self.utilities.files("ComboParser") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

