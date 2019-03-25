import os
import sys
import time
import datetime
import shutil
import json
import ctypes
import random
from itertools import takewhile, repeat
from colorama import Fore, Style, init
from tkinter import Tk, filedialog
from tqdm import tqdm


class Utilities:
    def __init__(self):
        init()
        self.width = shutil.get_terminal_size().columns
        self.file_names = None
        self.yes_values = {"true", "yes", "1", "on"}
        self.no_values = {"false", "no", "0", "off"}
        with open("config.json", "r") as json_file:
            self.data = json.load(json_file)

    def savelocation(self, mode):
        if self.data["SaveLocation"].lower() == "default":
            return os.getcwd() + f"/Keepin' It Clean/{mode}"
        else:
            return str(self.data["SaveLocation"])
    
    def files(self, mode):
        if self.data["FileNameType"].lower() == "default":
            umode = {
                "ComboCleaner": "Combo Cleaner",
                "ComboCombiner": "Combo Combiner",
                "ComboParser": "Combo Parser",
                "ComboSorter": "Combo Sorter",
                "ComboSplitter": "Combo Splitter",
                "DomainSorter": "Domain Sorter",
                "DuplicateRemover": "Duplicate Remover",
                "EmailToUsername": "Email To Username",
                "EmptylinesRemover": "Empty Line Remover",
                "linesCounter": "Line Counter",
                "Randomizelines": "Randomize Lines",
                "ComboSplitter2Email": "Email-Usernames",
                "ComboSplitter2Password": "Passwords",
                "ComboSplitter3Email": "Emails",
                "ComboSplitter3Username": "Usernames",
                "ComboSplitter3Password": "Passwords",
                "PasswordFilterer": "Password Filterer",
                "RandomUtilities": "Random Utilities",
                "ComboParser1": "Combo Parser[Usernames]",
                "ComboParser2": "Combo Parser[Passwords]"
            }
            return umode[mode] + " "

        elif self.data["FileNameType"].lower() == "custom":
            if mode in ("DomainSorter", "Domain Sorter"):
                return "Domain Sorter "
            else:
                print(Fore.YELLOW + "[*] Adding '.txt' isn't needed.".center(self.width) + Style.RESET_ALL)
                umode = input(Fore.YELLOW + "Input the file name you'd like to use: ".center(self.width).split(": ")[0] + ": ")
                return umode + " "

        else:
            exit('Invalid option entered in config file. (File Name Type; Line 2)')
        
    def progressbar(self, file, amount): 
        if self.data["ProgressBar"].lower() in self.yes_values:
            return tqdm(file, desc="Cleaning", total=amount, smoothing=1, ascii=True, unit=" lines", position=0, leave=False)
        elif self.data["ProgressBar"].lower() in self.no_values:
            return tqdm(file, disable=True)
        else:
            exit('Invalid option entered in the config file. (Progress bar; Line 5)')
    
    def randomcolor(self):
        if self.data["RandomMenuColor"].lower() in self.yes_values:
            colors = (Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLUE_EX)
            return random.choice(colors)
        elif self.data["RandomMenuColor"].lower() in self.no_values:
            return Fore.YELLOW
        else:
            exit('Invalid option entered in the config file. (Random Menu Color; Line 3)')

    def rawbigcount(self, filename):
        f = open(filename, 'rb')
        bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
        return sum(buf.count(b'\n') for buf in bufgen if buf)
    
    def openfile(self):
        root = Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(title="Select combo file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))

        return root.filename
    
    def clear(self):
        return os.system("cls" if os.name == "nt" else "clear")
    
    def currenttime(self):
        return datetime.datetime.now().strftime("%b %d %Y %H-%M-%S")
    
    def pleasewait(self):
        for _ in range(1,4)[::-1]:
            print(Fore.YELLOW + f"[*] Returning to menu in {_} seconds".center(self.width), end="\r")
            time.sleep(1)

    def startup_setup(self):
        self.clear()
        
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW("Combo Utilities | Version 0.1a")
        else:
             sys.stdout.write("\x1b]2;Combo Utilities | Version 0.1a\x07")
        
        self.base_file = "Keepin' It Clean/"
        self.location = os.getcwd() + "/"
        self.file_names = {
            "Combo Cleaner", "Combo Combiner", "Combo Parser", 
            "Combo Sorter", "Combo Splitter", "Domain Sorter", 
            "Duplicate Remover", "Email To Username", "Empty Line Remover", 
            "Line Counter", "Randomize Lines", "Random Utilities", 
            "Password Filterer"
            }
        
        if not os.path.exists(self.location + self.base_file):
            os.makedirs(self.location + self.base_file)
        for folder_name in self.file_names:
            if not os.path.exists(self.location + self.base_file + folder_name):
                os.makedirs(self.location + self.base_file + folder_name)



