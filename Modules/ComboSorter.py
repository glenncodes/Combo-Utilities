from Modules.Utilities import Utilities
from colorama import Fore, Style
import random
import shutil
import time
import json
import re
import os

class ComboSorter():

    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None

    def startup(self):
        self.to_write.clear()
        self.utilities.clear()
        print(self.utilities.custom_color() + "[1]" + Fore.LIGHTWHITE_EX + " | Sort by lines length")
        print(self.utilities.custom_color() + "[2]" + Fore.LIGHTWHITE_EX + " | Sort by lines length [Reversed, longest first]")
        print(self.utilities.custom_color() + "[3]" + Fore.LIGHTWHITE_EX + " | Sort alphabetically ")
        print(self.utilities.custom_color() + "[4]" + Fore.LIGHTWHITE_EX + " | Comma adder + remover")
        print(self.utilities.custom_color() + "[5]" + Fore.LIGHTWHITE_EX + " | Add prefix or suffix")
        print(self.utilities.custom_color() + "[6]" + Fore.LIGHTWHITE_EX + " | Add domains to user:pass combos")
        print(self.utilities.custom_color() + "\nPress enter to go back to the main menu.")
        try:
            select = input("\n" + self.utilities.custom_color() + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

            self.modules = {
                "1": "self.module_1()",
                "2": "self.module_2()",
                "3": "self.module_3()",
                "4": "self.module_4()",
                "5": "self.module_5()",
                "6": "self.module_6()"
            }

            if select in self.modules:
                eval(self.modules[select])

        except Exception as e:
            print(e)
            self.utilities.pleasewait()
            self.startup()

    def module_1(self):
        with open(Utilities().openfile(), 'r', errors="ignore") as file:
            total_lines = Utilities().rawbigcount(file.name)
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
            start = time.time()
            lines = sorted(file.readlines(), key=len)
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(lines)
        self.utilities.pleasewait()
        self.startup()
    
    def module_2(self):
        with open(Utilities().openfile(), 'r', errors="ignore") as file:
            total_lines = Utilities().rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            lines = sorted(file.readlines(), key=len, reverse=True)

        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(Utilities().savelocation("Combo Sorter") + "/" + Utilities().files("ComboSorter") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(lines)
        self.utilities.pleasewait()
        self.startup()

    def module_3(self):
        with open(Utilities().openfile(), 'r', errors="ignore") as file:
            total_lines = Utilities().rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
            lines = sorted(file.readlines())
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(lines)
        self.utilities.pleasewait()
        self.startup()
    
    def module_4(self):
        with open(Utilities().openfile(), 'r', errors="ignore") as file:
            pick = input(self.utilities.custom_color() + "[?] Do you want to add or remove commas? - [add/remove]: ".center(self.width).split(':')[0] + ': ')
            total_lines = Utilities().rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            for lines in Utilities().progressbar(file, total_lines):
                if pick == "remove":
                    lines = re.sub('(,)[^,]*$', "\r", lines.rstrip())
                    self.to_write.append(lines)
                else:
                    lines = lines.rstrip()
                    result = "".join(lines) + ",\n"
                    self.to_write.append(result)
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()

    def module_5(self):
        with open(Utilities().openfile(), 'r', errors="ignore") as file:
            total_lines = Utilities().rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            pick = input("[?] Do you want to add a prefix or a suffix? - [prefix/suffix]: ".center(self.width).split(':')[0] + ': ')
            prefixorsuffix = input("[?] What would you like to add?: ".center(self.width).split(":")[0] + ': ')
            done = []
            for lines in Utilities().progressbar(file, total_lines):
                if pick == "prefix":
                    done.append(prefixorsuffix + f"{lines}")
                else:
                    done = (["".join([x.strip(), prefixorsuffix, "\n"]) for x in file.readlines()])
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        output = Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter")
        with open(output + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(done)
        self.utilities.pleasewait()
        self.startup()

    def module_6(self):
        with open(Utilities().openfile(), 'r', errors="ignore") as file:
            total_lines = Utilities().rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            email = input(self.utilities.custom_color() + "[?] What email would you like to add? [Domain [Example: gmail.com]/Random]".center(self.width).split("Random]")[0] + 'Random]: ').lower()
            with open("Settings/Email Providers.json") as json_file:
                emails = json.load(json_file)
            for lines in Utilities().progressbar(file, total_lines):
                if email == "random":
                    slines = lines.split(":")
                    username = slines[0]
                    self.to_write.append(username + "@" + random.choice(emails) + ":" + slines[1])
                else:
                    slines = lines.split(":")
                    username = slines[0]
                    self.to_write.append(username + "@" + email + ":" + slines[1])
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        output = Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter")
        with open(output + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()