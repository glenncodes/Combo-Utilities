from Modules.Utilities import Utilities
from colorama import Fore, Style, init
import shutil
import time
import os

class ComboCleaner():
    
    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None
    
    def startup(self):
        self.utilities.clear()
        self.to_write.clear()
        print(self.utilities.custom_color() + "[1]" + Fore.LIGHTWHITE_EX + " | Replace all ;'s with :'s")
        print(self.utilities.custom_color() + "[2]" + Fore.LIGHTWHITE_EX + " | Remove all lines containing '{' or '}'")
        print(self.utilities.custom_color() + "[3]" + Fore.LIGHTWHITE_EX + " | Remove all lines not containing ':' or ';'")
        print(self.utilities.custom_color() + "[4]" + Fore.LIGHTWHITE_EX + " | Remove all lines not containing '@'")
        print(self.utilities.custom_color() + "[5]" + Fore.LIGHTWHITE_EX + " | Remove all lines containing '@'")
        print(self.utilities.custom_color() + "[6]" + Fore.LIGHTWHITE_EX + " | Remove all of the above (Except option 5)")
        print(self.utilities.custom_color() + "[7]" + Fore.LIGHTWHITE_EX + " | Remove all lines containing a certain string")
        print(self.utilities.custom_color() + "[8]" + Fore.LIGHTWHITE_EX + " | Invalid combo remover [example@example.com: ] or [ :example]")
        print(self.utilities.custom_color() + "[9]" + Fore.LIGHTWHITE_EX + " | Remove all lines longer than or shorter than x")
        print(self.utilities.custom_color() + "\nPress enter to go back to the main menu.")
        try:
            select = input("\n" + self.utilities.custom_color() + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)
            
            self.modules = {
                "1": "self.module_1()",
                "2": "self.module_2()",
                "3": "self.module_3()",
                "4": "self.module_4()",
                "5": "self.module_5()",
                "6": "self.module_6()",
                "7": "self.module_7()",
                "8": "self.module_8()",
                "9": "self.module_9()"
            }
            if select in self.modules:
                eval(self.modules[select])
        
        except Exception as e:
            print(e)
            self.utilities.pleasewait()
            self.startup()

    
    def module_1(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            self.total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(self.total_lines).center(self.width) + Style.RESET_ALL)

            for lines in self.utilities.progressbar(file, self.total_lines):
                if ';' in lines:
                    line = lines.replace(";", ":")
                    self.to_write.append(line)
                else:
                    self.to_write.append(lines)
        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Cleaner") + "/" + self.utilities.files("ComboCleaner") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

    def module_2(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            for lines in self.utilities.progressbar(file, total_lines):
                if "{" in lines or "}" in lines:
                    pass
                else:
                    self.to_write.append(lines)
        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Cleaner") + "/" + self.utilities.files("ComboCleaner") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
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
                if ":" in lines or ";" in lines:
                    self.to_write.append(lines)
                else:
                    pass
        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Cleaner") + "/" + self.utilities.files("ComboCleaner") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

    def module_4(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
            for lines in self.utilities.progressbar(file, total_lines):
                if "@" not in lines:
                    pass
                else:
                    self.to_write.append(lines)
        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Cleaner") + "/" + self.utilities.files("ComboCleaner") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

    def module_5(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)
            for lines in self.utilities.progressbar(file, total_lines):
                if "@" not in lines:
                    self.to_write.append(lines)
                else:
                    pass
        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Cleaner") + "/" + self.utilities.files("ComboCleaner") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

    def module_6(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines+1).center(self.width) + Style.RESET_ALL)
            for lines in self.utilities.progressbar(file, total_lines):
                if "{" in lines or "}" in lines or "@" not in lines:
                    pass
                else:
                    if ";" in lines:
                        line = lines.replace(';', ':')
                        self.to_write.append(line)
                    else:
                        if ":" not in lines:
                            pass
                        else:
                            self.to_write.append(lines)

        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Cleaner") + "/" + self.utilities.files("ComboCleaner") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

    def module_7(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            word = input(self.utilities.custom_color() + "[?] Input the word to search for: ".center(self.width).split(':')[0] + ': ' + Fore.LIGHTWHITE_EX)
            for lines in self.utilities.progressbar(file, total_lines):
                if word in lines:
                    pass
                else:
                    self.to_write.append(lines)
        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Cleaner") + "/" + self.utilities.files("ComboCleaner") + self.utilities.currenttime() + f'{[word]}.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

    def module_8(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            for lines in self.utilities.progressbar(file, total_lines):
                try:
                    line = lines.split(":")
                    if line[0] in ("\n", ""):
                        pass
                    elif line[1] in ("\n", ""):
                        pass
                    else:
                        self.to_write.append(lines)
                except Exception:
                    pass
        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Cleaner") + "/" + self.utilities.files("ComboCleaner") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

    def module_9(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as file:
            pick = input(self.utilities.custom_color() + "[?] Would you like to remove lines longer or shorter than x? | [longer/shorter]: ".center(self.width).split(':')[0] + ': ' + Fore.LIGHTWHITE_EX).lower()
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            if pick == "longer":
                longest = int(input(self.utilities.custom_color() + "[?] How long should the maximum be? ".center(self.width).split('? ')[0] + '? ' + Fore.LIGHTWHITE_EX))
                for lines in self.utilities.progressbar(file, total_lines):
                    if len(lines) > longest:
                        pass
                    else:
                        self.to_write.append(lines)

            elif pick == "shorter":
                shortest = int(input(self.utilities.custom_color() + "[?] How long should the shortest be? ".center(self.width).split('? ')[0] + '? ' + Fore.LIGHTWHITE_EX))
                for lines in self.utilities.progressbar(file, total_lines):
                    if len(lines) < shortest:
                        pass
                    else:
                        self.to_write.append(lines)
        if len(self.to_write) >= 1:
            print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(self.utilities.savelocation("Combo Cleaner") + "/" + self.utilities.files("ComboCleaner") + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(self.to_write)
        else:
            print(self.utilities.custom_color() + "No invalid lines were found.".center(self.width))
        self.utilities.pleasewait()
        self.startup()

