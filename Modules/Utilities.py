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
        self.colors = {
            "black": Fore.BLACK, "red": Fore.RED, "green": Fore.GREEN, "yellow": Fore.YELLOW,
            "blue": Fore.BLUE, "magenta": Fore.MAGENTA, "cyan": Fore.CYAN, "white": Fore.WHITE,
            "lightblack": Fore.LIGHTBLACK_EX, "lightred": Fore.LIGHTRED_EX, "lightgreen": Fore.LIGHTGREEN_EX,
            "lightyellow": Fore.LIGHTYELLOW_EX, "lightblue": Fore.LIGHTBLUE_EX, "lightmagenta": Fore.LIGHTMAGENTA_EX,
            "lightcyan": Fore.LIGHTCYAN_EX, "lightwhite": Fore.LIGHTWHITE_EX
            }
        
        with open(os.getcwd() + '/settings/Configuration.json', 'r') as json_file:
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
                print(self.custom_color() + "[*] Adding '.txt' isn't needed.".center(self.width) + Style.RESET_ALL)
                umode = input(self.custom_color() + "Input the file name you'd like to use: ".center(self.width).split(": ")[0] + ": ")
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
    
    def custom_color(self):
        if self.data['CustomColor']['Enabled'].lower() in self.yes_values:
            if self.data['CustomColor']['Color'].lower() in self.colors:
                return self.colors[self.data['CustomColor']['Color'].lower()]
            else:
                print(Fore.RED + "Invalid option entered in config file. (Custom Color; Color; Line 9)")
                print("Reverting to default color; Yellow.")
                return Fore.YELLOW
        
        elif self.data['CustomColor']['Enabled'].lower() in self.no_values:
            return Fore.YELLOW
        
        else:
            exit('Invalid option entered in config file. (Custom Color; Enabled; Line 8)')

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
            print(self.custom_color() + f"[*] Returning to menu in {_} seconds".center(self.width), end="\r")
            time.sleep(1)

    def startup_setup(self):
        try:
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

            
            if not os.path.isfile(os.getcwd() + "/settings/Configuration.json"):
                # Create the configuration file as it doesn't exist yet
                config = {
                    "FileNameType": None,
                    "RandomMenuColor": None,
                    "SaveLocation": None,
                    "ProgressBar": None
                    }

                # Add content to the file
                file_name_type = input("\nWould you like to use custom or default file names by default? [Custom/Default] ")
                random_menu_color = input("\nWould you like the program to randomly select the colors of 'Combo Utilities' on start up? [True/False] ")
                file_save_location = input("\nWould you like to save the output to a different location? [Path to save to/Default] ")
                progress_bar = input("\nWould you like to use a progress bar? [True/False] ")
                
                # Assign their contents into the configuration dict
                config["FileNameType"] = file_name_type
                config["RandomMenuColor"] = random_menu_color
                config["SaveLocation"] = file_save_location
                config["ProgressBar"] = progress_bar

                # Write the configuration
                with open("settings/Configuration.json", "w") as file:
                    json.dump(config, file, indent=2)
            return True
        except Exception:
            return False





