from Modules.Utilities import Utilities
from collections import defaultdict
from colorama import Fore, Style
import shutil
import time
import json
import os
import re


class DomainSorter():
    
    def __init__(self):
        self.to_write = defaultdict(list)
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None

    def startup(self):
        self.to_write.clear()
        self.utilities.clear()
        print(self.utilities.custom_color() + "[1]" + Fore.LIGHTWHITE_EX + " | Filter all email domain")
        print(self.utilities.custom_color() + "[2]" + Fore.LIGHTWHITE_EX + " | Filter all email extensions.")
        print(self.utilities.custom_color() + "[3]" + Fore.LIGHTWHITE_EX + " | Filter custom email domains.")
        print(self.utilities.custom_color() + "[4]" + Fore.LIGHTWHITE_EX + " | Custom Presets")
        print(self.utilities.custom_color() + "\nPress enter to go back to the main menu.\n")
        try:
            select = input(self.utilities.custom_color() + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

            self.modules = {
                "1": "self.module_1()",
                "2": "self.module_2()",
                "3": "self.module_3()",
                "4": "self.custom_presets()",
            }
            if select in self.modules:
                eval(self.modules[select])
        except Exception as e:
            print(e)
            self.utilities.pleasewait()
            self.startup()
        

    def module_1(self):
        with open(self.utilities.openfile(), 'r', encoding="iso-8859-1") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
            for lines in self.utilities.progressbar(file, total_lines):
                reg = re.search(r'@(.*):', lines)
                if ":" in reg.group(1):
                    reggy = reg.group(1).split(":")[0]
                else:
                    reggy = reg.group(1)

                self.to_write[reggy].append(lines)
        for key in self.to_write.keys():
            output = self.utilities.savelocation("Domain Sorter") + "/" + self.utilities.files("DomainSorter") + self.utilities.currenttime() + "[{}].txt".format(key.replace(":", "").lower())
            with open(output, 'a+', errors="ignore") as outfile:
                outfile.writelines(self.to_write.get(key))
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        self.utilities.pleasewait()
        self.startup()
    
    def module_2(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
            try:
                for lines in self.utilities.progressbar(file, total_lines):
                    reg = re.search(r"@[^.]*(\..*\..*|\..*):", lines)
                    if ':' in reg.group(1):
                        reggy = reg.group(1).split(":")[0]
                    else:
                        reggy = reg.group(1)
                    self.to_write[reggy].append(lines)
                for key in self.to_write.keys():
                    output = self.utilities.savelocation("Domain Sorter") + "/" + self.utilities.files("DomainSorter") + self.utilities.currenttime() + "[{}].txt".format(key.replace(":", "").lower())
                    with open(output, 'a+', errors="ignore") as outfile:
                        outfile.writelines(self.to_write.get(key))
            except Exception as e:
                print(e)
                pass
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        self.utilities.pleasewait()
        self.startup()

    def module_3(self):
        domains = [x for x in input("Select domains [Seperated with a space]: ").split(" ")]
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
            try:
                for lines in self.utilities.progressbar(file, total_lines):
                    for line in domains:
                        reg = re.search(f"@{line}:", lines)
                        if reg:
                            self.to_write[line].append(lines)
                        else:
                            pass
                for key in self.to_write.keys():
                    output = self.utilities.savelocation("Domain Sorter") + "/" + self.utilities.files("DomainSorter") + self.utilities.currenttime() + "[{}].txt".format(key.replace(":", "").lower())
                    with open(output, 'a+', errors="replace") as outfile:
                        outfile.writelines(self.to_write.get(key))
            except Exception as e:
                print(e)
                pass
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        self.utilities.pleasewait()
        self.startup()

    def custom_presets(self):
        with open('settings/Domain Sorter Presets.json', 'r') as file:
            file = json.load(file)
            for preset in file:
                print(f"{preset}: ({', '.join(file[preset]['domains'])})")
            preset_selection = input(self.utilities.custom_color() + "\n[?] Select the preset you would like to use: " + Fore.LIGHTWHITE_EX)
            domains = file[preset_selection]['domains']
            with open(self.utilities.openfile(), 'r', errors='ignore') as f:
                total_lines = self.utilities.rawbigcount(f.name)
                print(self.utilities.custom_color() + f"Loaded {os.path.basename(f.name)}".rstrip().center(self.width))
                print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
                for lines in f:
                    for domain in domains:
                        if file[preset_selection]['type'].lower() == "domain":
                            if f"@{domain.lower()}:" in lines.lower():
                                self.to_write[domain.lower()].append(lines)
                                break
                            else:
                                pass
                        if file[preset_selection]['type'].lower() == 'extension':
                            if f"{domain.lower()}:" in lines.lower():
                                self.to_write[domain.lower()].append(lines)
                                break
                            else:
                                pass
                    else:
                        self.to_write['Others'].append(lines)

        for key in self.to_write.keys():
            output = self.utilities.savelocation('Domain Sorter') + "/" + self.utilities.files('DomainSorter')
            with open(output + f" [{key}] " + self.utilities.currenttime() + '.txt', 'a', errors="ignore") as output_files:
                output_files.writelines(self.to_write.get(key))
        self.utilities.pleasewait()
        self.startup()

