import os
import shutil
import json
from colorama import Fore, Style, init
import time
from tkinter import Tk, filedialog
import time
import random
from tqdm import tqdm
import sys
import ctypes
import datetime
from itertools import takewhile, repeat

class Utilities:
    def __init__(self):
        init()
        self.width = shutil.get_terminal_size().columns
        self.file_names = None

    def savelocation(self, mode):
        with open("config.json") as json_file:
            data = json.load(json_file)

        if data["SaveLocation"] == "Default":
            return os.getcwd() + f"/Keepin' It Clean/{mode}"
        else:
            return str(data["SaveLocation"])
    
    def files(self, mode):
        with open("config.json") as f:
            data = json.load(f)

        if data["FileNameType"] == "Default":
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

        elif data["FileNameType"] == "Custom":
            if mode in ("DomainSorter", "Domain Sorter"):
                return "Domain Sorter "
            else:
                print(Fore.YELLOW + "[*] Adding '.txt' isn't needed.".center(self.width) + Style.RESET_ALL)
                umode = input(Fore.YELLOW + "Input the file name you'd like to use: ".center(self.width).split(": ")[0] + ": ")
                return umode + " "

        else:
            exit('Invalid config file option | File Name Type | Line 2')
        
    def progressbar(self, file, amount):
        with open("config.json") as f:
            data = json.load(f)

        if data["ProgressBar"] == "True":
            return tqdm(file, desc="Cleaning", total=amount, smoothing=1, ascii=True, unit=" lines", position=0, leave=False)
        elif data["ProgressBar"] == "False":
            return tqdm(file, disable=True)
        else:
            exit('Invalid config file option | Progress bar | Line 5')
    
    def randomcolor(self):
        with open("config.json") as f:
            data = json.load(f)

        if data["RandomMenuColor"] == "True":
            colors = (Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLUE_EX)
            return random.choice(colors)
        elif data["RandomMenuColor"] == "False":
            return Fore.YELLOW

        else:
            exit('Invalid config file option | Random Menu Color | Line 3')

    def rawbigcount(self, filename):
        f = open(filename, 'rb')
        bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
        return sum(buf.count(b'\n') for buf in bufgen if buf)
    
    def openfile(self):
        root = Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(title="Select combo file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))

        return root.filename
    
    def settitle(self):
            return (ctypes.windll.kernel32.SetConsoleTitleW("Combo Utilities | Version 0.1a") if os.name == "nt" else sys.stdout.write("\x1b]2;Combo Utilities | Version 0.1a\x07"))

    def createfiles(self):
        self.base_file = "Keepin' It Clean/"
        self.location = os.getcwd()
        self.file_names = {
            "Combo Cleaner", "Combo Combiner", "Combo Parser", 
            "Combo Sorter", "Combo Splitter", "Domain Sorter", 
            "Duplicate Remover", "Email To Username", "Empty Line Remover", 
            "Line Counter", "Randomize Lines", "Random Utilities", 
            "Password Filterer"
            }
        
        if not os.path.exists(self.location + "/" + self.base_file):
            os.makedirs(self.location + "/" + self.base_file)
        for folder_name in self.file_names:
            if not os.path.exists(self.location + "/" + self.base_file + folder_name):
                os.makedirs(self.location + "/" + self.base_file + folder_name)

    def clear(self):
        return os.system("cls" if os.name == "nt" else "clear")
    
    def currenttime(self):
        return datetime.datetime.now().strftime("%b %d %Y %H-%M-%S")
    
    def pleasewait(self):
        for _ in range(0,3)[::-1]:
            print(Fore.YELLOW + f"[*] Returning to menu in {_} seconds".center(self.width), end="\r")
            time.sleep(1)

