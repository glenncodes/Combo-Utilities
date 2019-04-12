from Modules.Utilities import Utilities
from colorama import Fore, Style
import shutil
import time
import os

class ComboSplitter():
    
    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None

    def startup(self):
        self.to_write.clear()
        self.utilities.clear()
        print(self.utilities.custom_color() + "[1]" + Fore.LIGHTWHITE_EX + " | Split combos into multiple smaller combos")
        print(self.utilities.custom_color() + "[2]" + Fore.LIGHTWHITE_EX + " | Split combo into 2 files, user/email + password")
        print(self.utilities.custom_color() + "[3]" + Fore.LIGHTWHITE_EX + " | Split Email:pass into 3 files, emails, passwords and usernames")
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
        except Exception as e:
            print(e)
            self.utilities.pleasewait()
            self.startup()


    def module_1(self):
        splitlen = int(input(self.utilities.custom_color() + "Input the amount of lines you'd like per file: ".center(self.width).split(':')[0] + ": "))
        with open(self.utilities.openfile(), "r", errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print("File contains {} lines.".format(total_lines).center(self.width))
            print("Estimated amount of files: {}".format(total_lines / splitlen).split(".")[0].center(self.width) + Style.RESET_ALL)
            at = 0
            count = 0
            output = self.utilities.savelocation("Combo Splitter") + "/" + self.utilities.files("ComboSplitter")
            for lines in file:
                if count % splitlen == 0:
                    dest = open(output + " - " + str(at) + " - " + self.utilities.currenttime() + ".txt", "a", errors="ignore")
                    at += 1
                dest.writelines(lines)
                count += 1

        dest.close()
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        self.utilities.pleasewait()
        self.startup()

    def module_2(self):
        to_write0 = []
        to_write1 = []

        with open(self.utilities.openfile(), "r", errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            output = self.utilities.savelocation("Combo Splitter") + "/" + self.utilities.files("ComboSplitter2Email")
            output2 = self.utilities.savelocation("Combo Splitter") + "/" + self.utilities.files("ComboSplitter2Password")

            for lines in file:
                try:
                    inputlines = lines.split(":")
                    to_write0.append("{}".format(inputlines[0]))
                    to_write1.append("{}\n".format(inputlines[1]))
                except Exception:
                    pass
        with open(output + self.utilities.currenttime() + ".txt", "a", errors="ignore") as file1:
            file1.writelines(to_write0)
        with open(output2 + self.utilities.currenttime() + ".txt", "a", errors="ignore") as file2:
            file2.writelines(to_write1)
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        self.utilities.pleasewait()
        self.startup()
    
    def module_3(self):
        emails = []
        usernames = []
        passwords = []

        with open(self.utilities.openfile(), "r", errors="ignore") as file:
            total_lines = self.utilities.rawbigcount(file.name)
            start = time.time()
            print(self.utilities.custom_color() + f"Loaded {os.path.basename(file.name)}".rstrip().center(self.width))
            print(self.utilities.custom_color() + "File contains {:,} lines.".rstrip().format(total_lines).center(self.width) + Style.RESET_ALL)

            output = self.utilities.savelocation("Combo Splitter") + "/" + self.utilities.files("ComboSplitter3Email")
            output2 = self.utilities.savelocation("Combo Splitter") + "/" + self.utilities.files("ComboSplitter3Username")
            output3 = self.utilities.savelocation("Combo Splitter") + "/" + self.utilities.files("ComboSplitter3Password")
            try:
                for lines in file:
                    emails.append(lines.split(":")[0] + '\n')
                    usernames.append(lines.split(":")[0].split('@')[0] + '\n')
                    passwords.append(lines.split(":")[1])
            except IndexError:
                pass
        with open(output + self.utilities.currenttime() + '.txt', 'a', errors="ignore") as outfile1:
            outfile1.writelines(emails)
        with open(output2 + self.utilities.currenttime() + ".txt", "a", errors="ignore") as outfile2:
            outfile2.writelines(usernames)
        with open(output3 + self.utilities.currenttime() + ".txt", "a", errors="ignore") as outfile3:
            outfile3.writelines(passwords)
        print(self.utilities.custom_color() + "[+] Time took: {}".rstrip().center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        self.utilities.pleasewait()
        self.startup()

