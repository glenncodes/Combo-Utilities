from Modules.Utilities import Utilities
from colorama import Fore, Style
import shutil
import time
import json
import os
import re

class PasswordFilterer():
    
    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None

    def startup(self):
        self.to_write.clear()
        self.utilities.clear()
        print(self.utilities.custom_color() + "[1]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 uppercase letter.")
        print(self.utilities.custom_color() + "[2]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 number.")
        print(self.utilities.custom_color() + "[3]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 symbol.")
        print(self.utilities.custom_color() + "[4]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 uppercase and 1 symbol.")
        print(self.utilities.custom_color() + "[5]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 number and 1 uppercase.")
        print(self.utilities.custom_color() + "[6]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 number, 1 uppercase and is shorter than x amount of characters.")
        print(self.utilities.custom_color() + "[7]" + Fore.LIGHTWHITE_EX + " | Remove all passwords shorter or longer than x amount of characters.")
        print(self.utilities.custom_color() + "[8]" + Fore.LIGHTWHITE_EX + " | Custom Presets")

        print(self.utilities.custom_color() + "\nPress enter to go back to the main menu.")
        try:
            select = input("\n" + self.utilities.custom_color() + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX).lower()

            self.modules = {
                "1": "self.module_1()",
                "2": "self.module_2()",
                "3": "self.module_3()",
                "4": "self.module_4()",
                "5": "self.module_5()",
                "6": "self.module_6()",
                "7": "self.module_7()",
                "8": "self.custom_presets()"
            }

            if select.lower() in self.modules:
                eval(self.modules[select])
        
        except Exception as e:
            print(e)
            self.utilities.pleasewait()
            self.startup()


    def module_1(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            for lines in self.utilities.progressbar(file, total_lines):
                try:
                    line = lines.split(':')[1]
                    reg = re.search(r".*[A-Z]+.*", line)
                    if reg:
                        self.to_write.append(lines)
                        pass
                    else:
                        pass
                except IndexError:
                    continue
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(self.utilities.savelocation('Password Filterer') + '/' + self.utilities.files("PasswordFilterer") + self.utilities.currenttime() + '.txt', 'w') as output:
            output.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()

    def module_2(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            for lines in self.utilities.progressbar(file, total_lines):
                try:
                    line = lines.split(':')[1]
                    reg = re.search(r".*[0-9]+.*", line)
                    if reg:
                        self.to_write.append(lines)
                    else:
                        pass
                except IndexError:
                    continue
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(self.utilities.savelocation('Password Filterer') + '/' + self.utilities.files("PasswordFilterer") + self.utilities.currenttime() + '.txt', 'w') as output:
            output.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()

    def module_3(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            for lines in self.utilities.progressbar(file, total_lines):
                try:
                    line = lines.split(':')[1]
                    reg = re.search(r".*[\\!$%^&*()_+|~\-=`{}[\]:\";'<>?,./@#]+.*", line)
                    if reg:
                        self.to_write.append(lines)
                    else:
                        pass
                except IndexError:
                    continue
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(self.utilities.savelocation('Password Filterer') + '/' + self.utilities.files("PasswordFilterer") + self.utilities.currenttime() + '.txt', 'w') as output:
            output.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()

    def module_4(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            for lines in self.utilities.progressbar(file, total_lines):
                try:
                    line = lines.split(':')[1]
                    reg = re.search(r"((.*[A-Z]+).*([\\!$%^&*()_+|~\-=`{}[\]:\";'<>?,./@#]+.*))", line)
                    if reg:
                        self.to_write.append(lines)
                    else:
                        pass
                except IndexError:
                    continue
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(self.utilities.savelocation('Password Filterer') + '/' + self.utilities.files("PasswordFilterer") + self.utilities.currenttime() + '.txt', 'w') as output:
            output.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()

    def module_5(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            for lines in self.utilities.progressbar(file, total_lines):
                try:
                    line = lines.split(':')[1]
                    reg = re.search(r"((.*[A-Z]+).*([0-9]+.*))", line)
                    if reg:
                        self.to_write.append(lines)
                    else:
                        pass
                except IndexError:
                    continue
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(self.utilities.savelocation('Password Filterer') + '/' + self.utilities.files("PasswordFilterer") + self.utilities.currenttime() + '.txt', 'w') as output:
            output.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()

    def module_6(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            amount = int(input("[?] How long should the password minimum be?: "))
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            for lines in self.utilities.progressbar(file, total_lines):
                try:
                    line = lines.split(':')[1]
                    if len(line) >= amount:
                        reg = re.search(r"((.*[A-Z]+).*([0-9]+.*))", line)
                        if reg:
                            self.to_write.append(lines)
                        else:
                            pass
                    else:
                        pass
                except IndexError:
                    continue
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(self.utilities.savelocation('Password Filterer') + '/' + self.utilities.files("PasswordFilterer") + self.utilities.currenttime() + '.txt', 'w') as output:
            output.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()

    def module_7(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            lonorsho = input(self.utilities.custom_color() + "[?] Would you like to remove passwords longer or shorter than x?: [Shorter/Longer] ".center(self.width).split("r] ")[0] + "r] ").lower()
            amount = int(input(self.utilities.custom_color() + "[?] How long should the password minimum be?: ".center(self.width).split("?: ")[0] + "?: " + Fore.LIGHTWHITE_EX))
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            for lines in self.utilities.progressbar(file, total_lines):
                try:
                    if lonorsho == "longer":
                        line = lines.split(':')[1]
                        if len(line) >= amount:
                            self.to_write.append(lines)
                        else:
                            pass
                    else:
                        line = lines.split(":")[1]
                        if len(line) <= amount:
                            self.to_write.append(lines)
                        else:
                            pass
                except IndexError:
                    continue
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(self.utilities.savelocation('Password Filterer') + '/' + self.utilities.files("PasswordFilterer") + self.utilities.currenttime() + '.txt', 'w') as output:
            output.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()
        
    def custom_presets(self):
        with open("Settings/Password Filterer Presets.json", "r") as file:
            file = json.load(file)
            for preset in file:
                print(preset)
            preset_selection = input(self.utilities.custom_color() + "\n[?] Select the preset you would like to use: " + Fore.LIGHTWHITE_EX)
            regex = file[preset_selection]['Regex']
            with open(self.utilities.openfile(), 'r', errors='ignore') as f:
                total_lines = self.utilities.rawbigcount(f.name)
                print(self.utilities.custom_color() + f"Loaded {os.path.basename(f.name)}".rstrip().center(self.width))
                print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
                for lines in self.utilities.progressbar(f, total_lines):
                    
                    if file[preset_selection]['Type'].lower() in ("pass", "password", "passw"):
                        line = lines.split(':')[1]
                    elif file[preset_selection]['Type'].lower() in ("email", "emailaddress"):
                        line = lines.split(":")[0]
                    elif file[preset_selection]['Type'].lower() == "line":
                        line = lines
                    
                    reg = re.search(regex, line)
                    if reg:
                        if file[preset_selection]['Group'].lower() != "none":
                            try:
                                reg_g = reg.group(file[preset_selection]['Group'])
                                self.to_write.append(reg_g)
                            except Exception:
                                continue
                        else:
                            self.to_write.append(lines)
                    else:
                        pass
        output = self.utilities.savelocation('Password Filterer') + "/" + self.utilities.files('PasswordFilterer')
        with open(output + f" [{preset_selection}] " + self.utilities.currenttime() + '.txt', 'a', errors="ignore") as output_files:
            output_files.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()


