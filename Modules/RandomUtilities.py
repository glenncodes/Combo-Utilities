from Modules.Utilities import Utilities
from colorama import Fore, Style
import random
import shutil
import string
import time
import os
import re

class RandomUtilities():

    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None
    
    def startup(self):
        self.to_write.clear()
        self.utilities.clear()
        print(self.utilities.custom_color() + "[1]" + Fore.LIGHTWHITE_EX + " | Random string generator")
        print(self.utilities.custom_color() + "[2]" + Fore.LIGHTWHITE_EX + " | Number generator")
        print(self.utilities.custom_color() + "[3]" + Fore.LIGHTWHITE_EX + " | Line break remover")
        print(self.utilities.custom_color() + "[4]" + Fore.LIGHTWHITE_EX + " | Line break adder")
        print(self.utilities.custom_color() + "\nPress enter to go back to the main menu.")
        try:
            select = input("\n" + self.utilities.custom_color() + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)
            
            self.modules = {
                "1": "self.module_1()",
                "2": "self.module_2()",
                "3": "self.module_3()",
                "4": "self.module_4()"
            }

            if select in self.modules:
                eval(self.modules[select])

        except Exception as e:
            print(e)
            self.utilities.pleasewait()
            self.startup()


    def module_1(self):
        print("[*] Generating over 25 keys will automatically get saved instead of getting printed.")
        amount = int(input(self.utilities.custom_color() + "[?] How many would you like to generate?: "))
        length = int(input(self.utilities.custom_color() + "[?] How long should the string be?: "))
        if amount >= 25:
            output = self.utilities.savelocation("Random Utilities") + "/" + self.utilities.files("RandomUtilities")
            with open(output + self.utilities.currenttime() + '[String].txt', 'w') as outfile:
                start = time.time()
                for _ in range(amount)[::-1]:
                    self.to_write.append(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length)) + '\n')
                print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
                outfile.writelines(self.to_write)
        else:
            start = time.time()
            for _ in range(amount)[::-1]:
                print(Style.RESET_ALL + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length)))
        self.utilities.pleasewait()
        self.startup()

    def module_2(self):
        output = self.utilities.savelocation("Random Utilities") + "/" + self.utilities.files("RandomUtilities")
        amount = int(input(self.utilities.custom_color() + "[?] Input how many numbers to generate: ".center(self.width).split(":")[0] + ":"))
        start = time.time()
        for i in range(amount+1):
            self.to_write.append(i)
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(output + self.utilities.currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(str((x))+'\n' for x in self.to_write)
        self.utilities.pleasewait()
        self.startup()


    def module_3(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as inputf:
            start = time.time()
            for lines in inputf:
                self.to_write.append(lines.replace("\n", " "))
        output = self.utilities.savelocation("Random Utilities") + "/" + self.utilities.files("RandomUtilities")
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(output + self.utilities.currenttime() + '.txt', 'w') as outfile:
            outfile.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()

    def module_4(self):
        with open(self.utilities.openfile(), 'r', errors="ignore") as inputf:
            start = time.time()
            delimiter = input(self.utilities.custom_color() + "[?] What delimiter should I split at to add the lines break?: ")
            for lines in inputf:
                try:
                    lines = lines.split(str(delimiter))
                    a = lines[0]
                    b = lines[1]
                    outputs = a + '\n' + delimiter + b
                    self.to_write.append(outputs)
                except IndexError:
                    print(f"Unable to split at given delimiter: '{delimiter}'")
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        output = self.utilities.savelocation("Random Utilities") + "/" + self.utilities.files("RandomUtilities")
        with open(output + self.utilities.currenttime() + '.txt', 'w') as outfile:
            outfile.writelines(self.to_write)
        self.utilities.pleasewait()
        self.startup()
