import ctypes
import datetime
import fileinput
import hashlib
import os
import platform
import random
import re
import shutil
import string
import subprocess
import sys
import time
from collections import defaultdict
from itertools import takewhile, repeat
from tkinter import filedialog, Tk
import json

def install_modules(module):
    if platform.system() == "Windows":
        return subprocess.call(f"pip install {module}")
    else:
        return subprocess.call(f"pip3 install {module}")

try:
    import colorama
    from colorama import Style, Fore
    colorama.init()
except ModuleNotFoundError:
    print("Colorama not found, Installing..")
    install_modules("colorama")
    try:
        import colorama
        from colorama import Style, Fore
        colorama.init()
    except Exception:
        exit("Unable to install colorama, exiting.")
try:
    import requests
except ModuleNotFoundError:
    print("Requests not found, Installing..")
    install_modules("requests")
    try:
        import requests
    except Exception:
        exit("Unable to install requests, exiting.")
try:
    from pypresence import Presence
except ModuleNotFoundError:
    print("PyPresence not found, Installing..")
    install_modules("pypresence")
    try:
        from pypresence import Presence
    except Exception:
        exit("Unable to install pypresence, exiting.")
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print("Tqdm not found, Installing..")
    install_modules("tqdm")
    try:
        from tqdm import tqdm
    except Exception:
        exit("Unable to install tqdm, exiting.")

RPC = Presence("446884598165536788")
to_write = []
width = shutil.get_terminal_size().columns
PYTHONDONTWRITEBYTECODE = 1

if not os.path.isfile("config.json"):
    # Create the configuration file as it doesn't exist yet
    config = {"DiscordRichPresence": None,"FileNameType": None, "RandomMenuColor": None, "SaveLocation": None, "ProgressBar": None}
    # Add content to the file
    drpyn = input("Would you like to enable discord rich presence by default? [True/False] ")
    docfiles = input("\nWould you like to use custom or default file names by default? [Custom/Default] ")
    rmc = input("\nWould you like the program to randomly select the colors of 'Combo Utilities' on start up? [True/False] ")
    dsl = input("\nWould you like to save the output to a different location? [Full file path to save to/Default] ")
    pbar = input("\nWould you like to use a progress bar? [True/False] ")
    config["DiscordRichPresence"] = drpyn
    config["FileNameType"] = docfiles
    config["RandomMenuColor"] = rmc
    config["SaveLocation"] = dsl
    config["ProgressBar"] = pbar

    with open("config.json", "w") as file:
        json.dump(config, file, indent=2)


def savelocation(mode):
    with open("config.json") as json_file:
        data = json.load(json_file)

    if data["SaveLocation"] == "Default":
        return os.getcwd() + f"/Keepin' It Clean/{mode}"
    else:
        return str(data["SaveLocation"])
    
def files(mode):
    with open("config.json") as f:
        data = json.load(f)

    if data["FileNameType"] == "Default":
        umode = dict(ComboCleaner="Combo Cleaner ",
                     ComboCombiner="Combo Combiner ",
                     ComboParser="Combo Parser ",
                     ComboSorter="Combo Sorter ",
                     ComboSplitter="Combo Splitter ",
                     DomainSorter="Domain Sorter ",
                     DuplicateRemover="Duplicate Remover ",
                     EmailToUsername="Email To Username ",
                     EmptylinesRemover="Empty Line Remover ",
                     linesCounter="Line Counter ",
                     Randomizelines="Randomize Lines ",
                     ComboSplitter2Email="Email-Usernames ",
                     ComboSplitter2Password="Passwords ",
                     ComboSplitter3Email="Emails ",
                     ComboSplitter3Username="Usernames ",
                     ComboSplitter3Password="Passwords ",
                     PasswordFilterer="Password Filterer ",
                     RandomUtilities="Random Utilities ",
                     ComboParser1="Combo Parser[Usernames] ",
                     ComboParser2="Combo Parser[Passwords] ")
        return umode.get(mode)

    elif data["FileNameType"] == "Custom":
        if mode in ("DomainSorter", "Domain Sorter"):
            return "Domain Sorter "
        else:
            print(Fore.YELLOW + "[*] Adding '.txt' isn't needed.".center(width) + Style.RESET_ALL)
            umode = input(Fore.YELLOW + "Input the file name you'd like to use: ".center(width).split(": ")[0] + ": ")
            return umode

    else:
        exit('Invalid config file option | File Name Type | Line 2')


def progressbar(file, amount):
    with open("config.json") as f:
        data = json.load(f)

    if data["ProgressBar"] == "True":
        return tqdm(file, desc="Cleaning", total=amount, smoothing=1, ascii=True, unit=" lines", position=0, leave=False)
    elif data["ProgressBar"] == "False":
        return tqdm(file, disable=True)
    else:
        exit('Invalid config file option | Progress bar | Line 5')


def randomcolor():
    with open("config.json") as f:
        data = json.load(f)

    if data["RandomMenuColor"] == "True":
        colors = (Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTBLUE_EX)
        return random.choice(colors)
    elif data["RandomMenuColor"] == "False":
        return Fore.YELLOW

    else:
        exit('Invalid config file option | Random Menu Color | Line 3')


def rawbigcount(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
    return sum(buf.count(b'\n') for buf in bufgen if buf)


def lines_checker(text):
    regex = re.compile(r':\s*\S')
    regex2 = re.compile(r'\s*\S:')
    if regex.search(text):
        if regex2.search(text):
            return True
        else:
            return False
    else:
        return False


def openfile():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir=os.path.expanduser("~/Desktop"), title="Select combo file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))

    return root.filename


def settitle():
    if platform.system() == "Windows":
        return ctypes.windll.kernel32.SetConsoleTitleW("Combo Utilities | Version 0.1a")
    elif platform.system() == "Linux":
        return sys.stdout.write("\x1b]2;Combo Utilities | Version 0.1a\x07")


def createfiles():
    if not os.path.exists("Keepin' It Clean"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean")

    if not os.path.exists("Keepin' It Clean/Combo Cleaner"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Combo Cleaner")

    if not os.path.exists("Keepin' It Clean/Combo Combiner"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Combo Combiner")

    if not os.path.exists("Keepin' It Clean/Combo Parser"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Combo Parser")

    if not os.path.exists("Keepin' It Clean/Combo Sorter"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Combo Sorter")

    if not os.path.exists("Keepin' It Clean/Combo Splitter"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Combo Splitter")

    if not os.path.exists("Keepin' It Clean/Domain Sorter"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Domain Sorter")

    if not os.path.exists("Keepin' It Clean/Duplicate Remover"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Duplicate Remover")

    if not os.path.exists("Keepin' It Clean/Email To Username"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Email To Username")

    if not os.path.exists("Keepin' It Clean/Empty Line Remover"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Empty Line Remover")

    if not os.path.exists("Keepin' It Clean/Line Counter"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Line Counter")

    if not os.path.exists("Keepin' It Clean/Randomize Lines"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Randomize Lines")

    if not os.path.exists("Keepin' It Clean/Random Utilities"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Random Utilities")

    if not os.path.exists("Keepin' It Clean/Password Filterer"):
        os.makedirs(os.getcwd() + "/Keepin' It Clean/Password Filterer")


def clear():
    if platform.system() == "Windows":
        return os.system("cls")
    else:
        return os.system("clear")


def currenttime():
    now = datetime.datetime.now()
    return now.isoformat().split(".")[0].replace("T", " ").replace(":", "-")


def pleasewait():
    i = 3
    while i != 0:
        print(Fore.YELLOW + "[*] Returning to menu in {} seconds".format(i).center(width), end="\r")
        time.sleep(1)
        i = i-1

MainMenu = (randomcolor() + """
 ██████╗ ██████╗ ███╗   ███╗██████╗  ██████╗     ██╗   ██╗████████╗██╗██╗     ██╗████████╗██╗███████╗███████╗
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔═══██╗    ██║   ██║╚══██╔══╝██║██║     ██║╚══██╔══╝██║██╔════╝██╔════╝
██║     ██║   ██║██╔████╔██║██████╔╝██║   ██║    ██║   ██║   ██║   ██║██║     ██║   ██║   ██║█████╗  ███████╗
██║     ██║   ██║██║╚██╔╝██║██╔══██╗██║   ██║    ██║   ██║   ██║   ██║██║     ██║   ██║   ██║██╔══╝  ╚════██║
╚██████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝╚██████╔╝    ╚██████╔╝   ██║   ██║███████╗██║   ██║   ██║███████╗███████║
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝  ╚═════╝      ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝    
                                                                                                  By Kid#0001""")


def menu():
    to_write.clear()
    colorama.init()
    clear()
    print(MainMenu)
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Combo Cleaner")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Combo Combiner")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Combo Parser")
    print(Fore.YELLOW + "[4]" + Fore.LIGHTWHITE_EX + " | Combo Sorter")
    print(Fore.YELLOW + "[5]" + Fore.LIGHTWHITE_EX + " | Combo Splitter")
    print(Fore.YELLOW + "[6]" + Fore.LIGHTWHITE_EX + " | Domain Sorter")
    print(Fore.YELLOW + "[7]" + Fore.LIGHTWHITE_EX + " | Duplicate Remover")
    print(Fore.YELLOW + "[8]" + Fore.LIGHTWHITE_EX + " | Email To Username")
    print(Fore.YELLOW + "[9]" + Fore.LIGHTWHITE_EX + " | Empty Line Remover")
    print(Fore.YELLOW + "[10]" + Fore.LIGHTWHITE_EX + " | Line Counter")
    print(Fore.YELLOW + "[11]" + Fore.LIGHTWHITE_EX + " | Randomize Line")
    print(Fore.YELLOW + "[12]" + Fore.LIGHTWHITE_EX + " | Hash Identifier")
    print(Fore.YELLOW + "[13]" + Fore.LIGHTWHITE_EX + " | Password Filterer")
    print(Fore.YELLOW + "[14]" + Fore.LIGHTWHITE_EX + " | Random Utilities" + Style.RESET_ALL)
    try:
        select = input('\n' + Fore.YELLOW + 'Select one: ' + Fore.LIGHTWHITE_EX)
        if select == "1":
            combo_cleaner()
        if select == "2":
            combo_combiner()
        if select == "3":
            combo_parser()
        if select == "4":
            combo_sorter()
        if select == "5":
            combo_splitter()
        if select == "6":
            domain_sorter()
        if select == "7":
            duplicate_remover()
        if select == "8":
            email_to_user()
        if select == "9":
            empty_lines_remover()
        if select == "10":
            lines_counter()
        if select == "11":
            randomize_lines()
        if select == "12":
            hash_identifier()
        if select == "13":
            password_filterer()
        if select == "14":
            randomutilities()
        if select is not int or select > str(int(14)):
            menu()
    except Exception as e:
        print(e)
        pleasewait()
        menu()


def combo_cleaner():
    to_write.clear()
    count = 0
    clear()
    RPC.update(state="Combo Cleaner", details="Version 0.1a", large_image="large", start=int(ct))
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Replace all ;'s with :'s")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Remove all lines containing { or }")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Remove all lines that don't contain : or ;")
    print(Fore.YELLOW + "[4]" + Fore.LIGHTWHITE_EX + " | Remove all lines that don't contain @")
    print(Fore.YELLOW + "[5]" + Fore.LIGHTWHITE_EX + " | Remove all lines that contain @")
    print(Fore.YELLOW + "[6]" + Fore.LIGHTWHITE_EX + " | Remove all of the above [Except option 5]" + Fore.LIGHTRED_EX + " [Most recommended!]" + Style.RESET_ALL)
    print(Fore.YELLOW + "[7]" + Fore.LIGHTWHITE_EX + " | Remove all lines containing a certain string")
    print(Fore.YELLOW + "[8]" + Fore.LIGHTWHITE_EX + " | Invalid combo remover [example@gmail.com: ] or [ :example]")
    print(Fore.YELLOW + "[9]" + Fore.LIGHTWHITE_EX + " | Remove all lines longer than or shorter than x amount of characters")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            with open(openfile(), 'r', errors="ignore") as file:
                RPC.update(state="Editing file: {}".format(os.path.split(file.name)[-1]), details="Combo Cleaner | Option 1", large_image="large", start=int(ct))
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in progressbar(file, total_lines):
                    if ';' in lines:
                        line = lines.replace(";", ":")
                        to_write.append(line)
                        count += 1
                    else:
                        to_write.append(lines)
            if count >= 1:
                with open(savelocation("Combo Cleaner") + "/" + files("ComboCleaner") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_cleaner()

        if select == "2":
            RPC.update(state="Combo Cleaner | Option 2", details="Version 0.1a", large_image="large", start=int(ct))
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in progressbar(file, total_lines):
                    if "{" in lines or "}" in lines:
                        count += 1
                        pass
                    else:
                        to_write.append(lines)
            if count >= 1:
                with open(savelocation("Combo Cleaner") + "/" + files("ComboCleaner") + currenttime() +  '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_cleaner()

        if select == "3":
            RPC.update(state="Combo Cleaner | Option 3", details="Version 0.1a", large_image="large", start=int(ct))
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in progressbar(file, total_lines):
                    if ":" not in lines or ";" not in lines:
                        count += 1
                        pass
                    else:
                        to_write.append(lines)
            if count >= 1:
                with open(savelocation("Combo Cleaner") + "/" + files("ComboCleaner") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_cleaner()

        if select == "4":
            RPC.update(state="Combo Cleaner | Option 4", details="Version 0.1a", large_image="large", start=int(ct))
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                for lines in progressbar(file, total_lines):
                    if "@" not in lines:
                        count += 1
                    else:
                        to_write.append(lines)
            if count >= 1:
                with open(savelocation("Combo Cleaner") + "/" + files("ComboCleaner") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_cleaner()

        if select == "5":
            RPC.update(state="Combo Cleaner | Option 5", details="Version 0.1a", large_image="large", start=int(ct))
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                for lines in progressbar(file, total_lines):
                    if "@" in lines:
                        count += 1
                        pass
                    else:
                        to_write.append(lines)
            if count >= 1:
                with open(savelocation("Combo Cleaner") + "/" + files("ComboCleaner") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_cleaner()

        if select == "6":
            RPC.update(state="Combo Cleaner | Option 6", details="Version 0.1a", large_image="large", start=int(ct))
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines+1).center(width) + Style.RESET_ALL)
                temp = []
                for lines in progressbar(file, total_lines):
                    if ";" in lines:
                        line = lines.replace(";", ":")
                        temp.append(line)
                    else:
                        temp.append(lines)
                for lines in temp:
                    if "{" in lines or "}" in lines or "@" not in lines or ":" not in lines:
                        count += 1
                        pass
                    else:
                        to_write.append(lines)
            if count >= 1:
                with open(savelocation("Combo Cleaner") + "/" + files("ComboCleaner") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_cleaner()

        if select == "7":
            RPC.update(state="Combo Cleaner | Option 7", details="Version 0.1a", large_image="large", start=int(ct))
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                word = input(Fore.YELLOW + "[?] Input the word you would like to search for: ".center(width).split(':')[0] + ': ' + Fore.LIGHTWHITE_EX)
                for lines in progressbar(file, total_lines):
                    if re.search(word, lines, re.IGNORECASE):
                        count += 1
                        pass
                    else:
                        to_write.append(lines)
            if count >= 1:
                with open(savelocation("Combo Cleaner") + "/" + files("ComboCleaner") + currenttime() + f'{[word]}.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_cleaner()

        if select == "8":
            RPC.update(state="Combo Cleaner | Option 8", details="Version 0.1a", large_image="large", start=int(ct))
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in progressbar(file, total_lines):
                    if not lines_checker(lines):
                        count += 1
                        pass
                    else:
                        to_write.append(lines)
            if count >= 1:
                with open(savelocation("Combo Cleaner") + "/" + files("ComboCleaner") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_cleaner()

        if select == "9":
            RPC.update(state="Combo Cleaner | Option 9", details="Version 0.1a", large_image="large", start=int(ct))
            with open(openfile(), 'r', errors="ignore") as file:
                pick = input(Fore.YELLOW + "[?] Would you like to remove lines longer or shorter than x? | [longer/shorter]: ".center(width).split(':')[0] + ': ' + Fore.LIGHTWHITE_EX).lower()
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                if pick == "longer":
                    longest = int(input(Fore.YELLOW + "[?] How long would you like the maximum to be? ".center(width).split('? ')[0] + '? ' + Fore.LIGHTWHITE_EX))
                    for lines in progressbar(file, total_lines):
                        if len(lines) >= longest:
                            count += 1
                            pass
                        elif len(lines) <= longest:
                            to_write.append(lines)

                elif pick == "shorter":
                    shortest = int(input(Fore.YELLOW + "[?] How long would you like the shortest to be? ".center(width).split('? ')[0] + '? ' + Fore.LIGHTWHITE_EX))
                    for lines in progressbar(file, total_lines):
                        if len(lines) <= shortest:
                            count += 1
                            pass
                        elif len(lines) >= shortest:
                            to_write.append(lines)
            if count >= 1:
                with open(savelocation("Combo Cleaner") + "/" + files("ComboCleaner") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_cleaner()

    except TypeError as e:
        print(e)
        pleasewait()
        MainMenu()


def combo_combiner():
    to_write.clear()
    clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Combine multilple files into 1 file.")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Combine usernames/emails.txt & passwords.txt into 1 text file.")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input(Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            print(Fore.YELLOW + "[+] You can select multiple combos!".center(width))
            root = Tk()
            root.withdraw()
            root.filename = filedialog.askopenfilenames(initialdir=os.path.expanduser("~/Desktop"), title="Select combo list(s)", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            start = time.time()
            lines = fileinput.input(root.filename, openhook=fileinput.hook_encoded("utf-8", errors="ignore"))
            to_write.append(lines)

            output = savelocation("Combo Combiner") + "/" + str(files("ComboCombiner"))
            with open(output + currenttime() + ".txt", "a", errors="ignore") as outfile:
                outfile.writelines(lines)

            root.destroy()
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_combiner()

        if select == "2":
            root = Tk()
            root.withdraw()
            root.filename = filedialog.askopenfilename(initialdir=os.path.expanduser("~/Desktop"), title="Select username list", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            with open(root.filename, "r") as user:
                print(Fore.YELLOW + "Loaded {:,} usernames".center(width).format(rawbigcount(root.filename)))

                root.filename1 = filedialog.askopenfilename(initialdir=os.path.expanduser("~/Desktop"), title="Select password list", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
                with open(root.filename1, "r") as passw:
                    print(Fore.YELLOW + "Loaded {:,} passwords".center(width).format(rawbigcount(root.filename1)))
                    start = time.time()
                    for x, y in zip(user, passw):
                        to_write.append(x.strip() + ":" + y.strip() + '\n')
            output = savelocation("Combo Combiner") + '/' + str(files("ComboCombiner"))
            with open(output + currenttime() + '.txt', "a", errors="ignore") as outfile:
                outfile.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_combiner()

    except TypeError as e:
        print(e)
        pleasewait()
        menu()


def combo_parser():
    to_write.clear()
    clear()
    count = 0
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Password:Email/Username -> Email/Username:Password [Works for reversing email:password too]")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Username/email:Password:Email/username -> 2 files [user:pass, email:pass]")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Combo Parser")
    print(Fore.YELLOW + "[4]" + Fore.LIGHTWHITE_EX + " | Email Extractor")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in progressbar(file, total_lines):
                    tmp = lines.split(":")
                    to_write.append(tmp[0].rstrip() + ':' + tmp[1].rstrip() + '\n')
                    count += 1
            if count >= 1:
                with open(savelocation("Combo Parser") + '/' + files("ComboParser") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_parser()

        if select == "2":
            dest = []
            dest2 = []
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in progressbar(file, total_lines):
                    eachlines = lines.split()
                    count += 1
                    dest.append(eachlines[2] + ":" + eachlines[1] + "\n")
                    dest2.append(eachlines[0] + ":" + eachlines[1] + "\n")
            if count >= 1:
                with open(savelocation("Combo Parser") + '/' + files("ComboParser1") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(dest)
                with open(savelocation("Combo Parser") + '/' + files("ComboParser2") + currenttime() + '.txt', 'w', errors="ignore") as outfile2:
                    outfile2.writelines(dest2)
                print(Fore.YELLOW + "[+] Lines cleaned: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_parser()

        if select == "3":
            print(Fore.YELLOW + "If you're having trouble with this module, contact me on discord and I'll try my best to help.")
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                output = savelocation("Combo Parser") + '/' + str(files("ComboParser"))
                dest = open(output + currenttime() + ".txt", "a", encoding="ANSI")
                sep = input(Fore.YELLOW + "Separator: ".split(':')[0] + ':'.center(width))
                try:
                    _posa = int(input("[?] How many columns do you want to extract: "))
                except ValueError:
                    sys.exit("[-] No number given")
                try:
                    _posq = input("[?] How do you want to extract it (Example: 2:3:1): ").split(":")
                except Exception:
                    sys.exit("[-] Can't split with given separator")
                print("[+] Splitting")
                _ret_list = []
                for _i in file:
                    _spl = ""
                    for _a in range(0, _posa):
                        try:
                            _spl += ":" + _i.rstrip().split(sep)[int(_posq[_a])]  # _sop
                            count += 1
                        except Exception as e:
                            print(e)
                            pleasewait()
                            pass
                    _ret_list.append(_spl[1:] + "\n")
                dest.writelines(_ret_list)
            dest.close()
            print(Fore.YELLOW + "[+] lines Sorted: %s".center(width) % count)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_parser()

        if select == "4":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in progressbar(file, total_lines):
                    match = re.search(r"""(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-zA-Z0-9-]*[a-zA-Z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", lines)
                    if match:
                        to_write.append(match.group(0) + "\n")
                        count += 1

            if count >= 1:
                with open(savelocation("Combo Parser") + '/' + files("ComboParser") + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
                print(Fore.YELLOW + "[+] Emails extracted: {:,}".center(width).format(count))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            pleasewait()
            combo_parser()

    except TypeError as e:
        print(e)
        pleasewait()
        menu()


def combo_sorter():
    to_write.clear()
    clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Sort by lines length")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Sort by lines length [Reversed, longest first]")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Sort alphabetically ")
    print(Fore.YELLOW + "[4]" + Fore.LIGHTWHITE_EX + " | Comma adder + remover")
    print(Fore.YELLOW + "[5]" + Fore.LIGHTWHITE_EX + " | Add prefix or suffix")
    print(Fore.YELLOW + "[6]" + Fore.LIGHTWHITE_EX + " | Add domains to user:pass combos")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                start = time.time()
                lines = file.readlines()
                lines.sort(key=len)
                to_write.append(lines)
            with open(savelocation("Combo Sorter") + '/' + str(files("ComboSorter")) + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(to_write)
            print(Fore.YELLOW + "[+] lines Sorted: %s".center(width) % total_lines)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_sorter()

        if select == "2":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                lines = file.readlines()
                lines.sort(key=len, reverse=True)
                to_write.append(lines)

            with open(savelocation("Combo Sorter") + "/" + str(files("ComboSorter")) + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(to_write)
            print("[+] lines Split: %s".center(width) % total_lines)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_sorter()

        if select == "3":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                lines = file.readlines()
                lines.sort()
                to_write.append(lines)
            with open(savelocation("Combo Sorter") + '/' + str(files("ComboSorter")) + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(to_write)
            print("[+] lines Split: %s".center(width) % total_lines)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_sorter()

        if select == "4":
            with open(openfile(), 'r', errors="ignore") as file:
                pick = input(Fore.YELLOW + "[?] Do you want to add or remove commas? - [add/remove]: ".center(width).split(':') + ': ')
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in progressbar(file, total_lines):
                    if pick == "remove":
                        lines = re.sub('(,)[^,]*$', "\r", lines.rstrip())
                        to_write.append(lines)
                    else:
                        lines = lines.rstrip()
                        result = "".join(lines) + ",\n"
                        to_write.append(result)

            with open(savelocation("Combo Sorter") + '/' + str(files("ComboSorter")) + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(to_write)
            print(Fore.YELLOW + "[+] lines Split: %s".center(width) % total_lines)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_sorter()

        if select == "5":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                pick = input("[?] Do you want to add a prefix or a suffix? - [prefix/suffix]: ".center(width).split(':')[0] + ': ')
                prefixorsuffix = input("[?] What would you like to add?: ".center(width).split(":")[0] + ': ')

                for lines in progressbar(file, total_lines):
                    if pick == "prefix":
                        to_write.append(prefixorsuffix + f"{lines}")
                    else:
                        to_write.append(["".join([x.strip(), prefixorsuffix, "\n"]) for x in file.readlines()])
            output = savelocation("Combo Sorter") + '/' + str(files("ComboSorter"))
            with open(output + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                for lines in to_write:
                    outfile.writelines(lines)
            print(Fore.YELLOW + "[+] lines Sorted: %s".center(width) % total_lines)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_sorter()

        if select == "6":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                email = input(Fore.YELLOW + "[?] What email would you like to add? [Domain [Example: gmail.com]/Random]".center(width).split("Random]")[0] + 'Random]: ').lower()
                req = requests.get("http://comboutils.000webhostapp.com/email-providers.txt").json()

                for lines in progressbar(file, total_lines):
                    if email == "Random":
                        slines = lines.split(":")
                        username = slines[0]
                        to_write.append(username + "@" + random.choice(req) + ":" + slines[1])
                    else:
                        slines = lines.split(":")
                        username = slines[0]
                        to_write.append(username + "@" + email + ":" + slines[1])

            output = savelocation("Combo Sorter") + '/' + str(files("ComboSorter"))
            with open(output + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(to_write)
            print(Fore.YELLOW + "[+] lines Split: %s".center(width) % total_lines)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_sorter()

    except TypeError as e:
        print(e)
        pleasewait()
        menu()


def combo_splitter():
    to_write.clear()
    clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Split combos into multiple smaller combos")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Split combo into 2 files, user/email + password")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Split Email:pass into 3 files, emails, passwords and usernames")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            splitlen = int(input(Fore.YELLOW + "Input the amount of lines you'd like per file: ".center(width).split(':')[0] + ": "))
            with open(openfile(), "r", errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print("File contains {} lines.".format(total_lines).center(width))
                print("Estimated amount of files: {}".format(total_lines / splitlen).split(".")[0].center(width) + Style.RESET_ALL)
                at = 0
                count = 0
                output = savelocation("Combo Splitter") + "/" + str(files("ComboSplitter"))
                for lines in file:
                    if count % splitlen == 0:
                        dest = open(output + " - " + str(at) + " - " + currenttime() + ".txt", "a", errors="ignore")
                        at += 1
                    dest.writelines(lines)
                    count += 1

            print(Fore.YELLOW + "[+] Lines split: %s".center(width) % total_lines)
            dest.close()
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_splitter()

        if select == "2":
            to_write0 = []
            to_write1 = []

            with open(openfile(), "r", errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                output = savelocation("Combo Splitter") + "/" + str(files("ComboSplitter2Email"))
                output2 = savelocation("Combo Splitter") + "/" + str(files("ComboSplitter2Password"))

                dest = open(output + currenttime() + ".txt", "a", errors="ignore")
                dest2 = open(output2 + currenttime() + ".txt", "a", errors="ignore")

                count = 0
                try:
                    for lines in file:
                        inputlines = lines.split(":")
                        to_write0.append(inputlines[0])
                        to_write1.append(inputlines[1])
                        count += 1
                except IndexError:
                    pass
            for l, ll in zip(to_write0, to_write1):
                dest.writelines("{}\n".format(l))
                dest2.writelines("{}".format(ll))
            dest.close()
            dest2.close()
            print("[+] lines Split: %s".center(width) % count)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_splitter()

        if select == "3":
            emails = []
            usernames = []
            passwords = []

            with open(openfile(), "r", errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                output = savelocation("Combo Splitter") + "/" + str(files("ComboSplitter3Email"))
                output2 = savelocation("Combo Splitter") + "/" + str(files("ComboSplitter3Username"))
                output3 = savelocation("Combo Splitter") + "/" + str(files("ComboSplitter3Password"))
                count = 0
                try:
                    for lines in file:
                        emails.append(lines.split(":")[0] + '\n')
                        usernames.append(lines.split(":")[0].split('@')[0] + '\n')
                        passwords.append(lines.split(":")[1] + '\n')
                        count += 1
                except IndexError:
                    pass
            with open(output + currenttime() + '.txt', 'a', errors="ignore") as outfile1:
                outfile1.writelines(emails)
            with open(output2 + currenttime() + ".txt", "a", errors="ignore") as outfile2:
                outfile2.writelines(usernames)
            with open(output3 + currenttime() + ".txt", "a", errors="ignore") as outfile3:
                outfile3.writelines(passwords)
            print(Fore.YELLOW + "[+] Lines Split: %s".rstrip().center(width) % count)
            print(Fore.YELLOW + "[+] Time took: {}".rstrip().center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            combo_splitter()

    except TypeError as e:
        print(e)
        pleasewait()
        menu()


def domain_sorter():
    to_write.clear()
    clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Sort by email extension [.com, .de, .ru, .jp, .co.uk, .gov, .net, .org, .edu, .fr, .ca, .pl, .es, .it]")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Sort by email domain [Gmail, Yahoo, Hotmail, Aol, Outlook, Icloud, Yandex, Live, Protonmail, Mail, Zoho, T-Online]")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Filter all email domain")
    print(Fore.YELLOW + "[4]" + Fore.LIGHTWHITE_EX + " | Filter all email extensions.")
    print(Fore.YELLOW + "[5]" + Fore.LIGHTWHITE_EX + " | Filter custom email domains.")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.\n")
    try:
        select = input(Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)
        if select == "1":
            d = defaultdict(list)

            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    if re.search(r"@.*\.com:", lines):
                        d["COM"].append(lines)
                    elif re.search(r"@.*\.de:", lines):
                        d["DE"].append(lines)
                    elif re.search(r"@.*\.ru:", lines):
                        d["RU"].append(lines)
                    elif re.search(r"@.*\.jp:", lines):
                        d["JP"].append(lines)
                    elif re.search(r"@.*\.co\.uk:", lines):
                        d["COUK"].append(lines)
                    elif re.search(r"@.*\.gov:", lines):
                        d["GOV"].append(lines)
                    elif re.search(r"@.*\.net:", lines):
                        d["NET"].append(lines)
                    elif re.search(r"@.*\.org:", lines):
                        d["ORG"].append(lines)
                    elif re.search(r"@.*\.edu:", lines):
                        d["EDU"].append(lines)
                    elif re.search(r"@.*\.fr:", lines):
                        d["FR"].append(lines)
                    elif re.search(r"@.*\.ca:", lines):
                        d["CA"].append(lines)
                    elif re.search(r"@.*\.pl:", lines):
                        d["PL"].append(lines)
                    elif re.search(r"@.*\.es:", lines):
                        d["ES"].append(lines)
                    elif re.search(r"@.*\.it:", lines):
                        d["IT"].append(lines)
                    else:
                        d["OTHERS"].append(lines)
            comout = savelocation("Domain Sorter") + "/" + str(files("DomainSorter"))
            try:
                for key in d.keys():
                    if len(d.get(key)) >= 1:
                        with open(comout + currenttime() + f'[{key.replace(":", "").lower()}].txt', 'a', errors="ignore") as outfile:
                            outfile.writelines(d.get(key))
            except Exception as e:
                print(e)
                pass
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            domain_sorter()

        if select == "2":
            d = defaultdict(list)
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                for lines in progressbar(file, total_lines):
                    if re.search(r"[@](gmail.*):", lines):
                        d["GMAIL"].append(lines)
                    elif re.search(r"[@](yahoo.*):", lines):
                        d["YAHOO"].append(lines)
                    elif re.search(r"[@](hotmail.*):", lines):
                        d["HOTMAIL"].append(lines)
                    elif re.search(r"[@](aol.*):", lines):
                        d["AOL"].append(lines)
                    elif re.search(r"[@](outlook.*):", lines):
                        d["OUTLOOK"].append(lines)
                    elif re.search(r"[@](icloud.*):", lines):
                        d["ICLOUD"].append(lines)
                    elif re.search(r"[@](yandex.*):", lines):
                        d["YANDEX"].append(lines)
                    elif re.search(r"[@](live.*):", lines):
                        d["LIVE"].append(lines)
                    elif re.search(r"[@](mail.*):", lines):
                        d["MAIL"].append(lines)
                    elif re.search(r"[@](t-online.*):", lines):
                        d["TONLINE"].append(lines)
                    else:
                        d["OTHERS"].append(lines)
            try:
                for key in d.keys():
                    if len(d.get(key)) >= 1:
                        comout = savelocation("Domain Sorter") + "/" + str(files("DomainSorter"))
                        with open(comout + currenttime() + f'[{key.replace(":", "").lower()}].txt', 'a', errors="ignore") as outfile:
                            outfile.writelines(d.get(key))
            except Exception as e:
                print(e)
                pass
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            domain_sorter()

        if select == "3":
            d = defaultdict(list)
            with open(openfile(), 'r') as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                for lines in progressbar(file, total_lines):
                    reg = re.search(r'@(.*):', lines)
                    d[reg.group(1)].append(lines)
            for key in d.keys():
                output = savelocation("Domain Sorter") + "/" + str(files("DomainSorter")) + currenttime() + "[{}].txt".format(key.replace(":", "").lower())
                with open(output, 'a+', errors="ignore") as outfile:
                    outfile.writelines(d.get(key))
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            domain_sorter()

        if select == "4":
            d = defaultdict(list)
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                try:
                    for lines in progressbar(file, total_lines):
                        reg = re.search(r"@[^.]*(\..*\..*|\..*):", lines)
                        d[reg.group(1)].append(lines)
                    for key in d.keys():
                        output = savelocation("Domain Sorter") + "/" + str(files("DomainSorter")) + currenttime() + "[{}].txt".format(key.replace(":", "").lower())
                        with open(output, 'a+', errors="replace") as outfile:
                            outfile.writelines(d.get(key))
                except Exception as e:
                    print(e)
                    pass
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            domain_sorter()
        
        if select == "5":
            # TODO | Think it works - need feedback
            d = defaultdict(list)
            domains = [x for x in input("Select domains [Seperated with a space]: ").split(" ")]
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                try:
                    for lines in progressbar(file, total_lines):
                        for line in domains:
                            reg = re.search(f"@({line}):", lines)
                            if reg:
                                d[reg.group(1)].append(lines)
                            else:
                                pass
                    for key in d.keys():
                        output = savelocation("Domain Sorter") + "/" + str(files("DomainSorter")) + currenttime() + "[{}].txt".format(key.replace(":", "").lower())
                        with open(output, 'a+', errors="replace") as outfile:
                            outfile.writelines(d.get(key))
                except Exception as e:
                    print(e)
                    pass
            print(Fore.YELLOW + "[+] lines Sorted: %s".center(width) % total_lines)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            domain_sorter()
        
    except Exception as e:
        print(e)
        pleasewait()
        menu()


def duplicate_remover():
    to_write.clear()
    clear()
    with open(openfile(), 'r', errors="ignore") as file:
        total_lines = rawbigcount(file.name)
        start = time.time()
        print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
        print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
        uniquelines = set(file.readlines())

    if not len(uniquelines) == total_lines:
        output = savelocation("Duplicate Remover") + "/" + str(files("DuplicateRemover"))
        with open(output + currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(uniquelines)
        print("[+] Duplicates Removed: %s".center(width) % str(int(total_lines) - len(uniquelines)))
    else:
        print("[-] No duplicates found".center(width))
    print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
    pleasewait()
    menu()


def email_to_user():
    clear()
    to_write.clear()
    with open(openfile(), 'r', errors="ignore") as file:
        total_lines = rawbigcount(file.name)
        start = time.time()
        print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
        print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

        output = savelocation("Email To Username") + "/" + str(files("EmailToUsername"))

        for line in file:
            lines = line.split(":")
            to_write.append(lines[0].split("@")[0] + ":" + lines[1])

    print(Fore.YELLOW + "[+] lines Converted: %s".rstrip().center(width) % total_lines)
    print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
    with open(output + currenttime() + '.txt', 'w', errors="ignore") as outfile:
        outfile.writelines(to_write)
    pleasewait()
    menu()


def empty_lines_remover():
    to_write.clear()
    clear()
    with open(openfile(), 'r', errors="ignore") as file:
        total_lines = rawbigcount(file.name)
        start = time.time()
        print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
        print(Fore.YELLOW + "File contains {:,} lines.".format(total_lines).rstrip().center(width) + Style.RESET_ALL)

        cleaned = list(filter(lambda x: not re.match(r'^\s*$', x), file.readlines()))
        print(Fore.YELLOW + "[+] Time took: {}".rstrip().center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
        if len(cleaned) >= 1 and len(cleaned) < total_lines:
            output = savelocation("Empty Line Remover") + "/" + str(files("EmptylinesRemover"))
            with open(output + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(cleaned)
            print(Fore.YELLOW + "[+] Empty Lines Removed: %s".rstrip().center(width) % str(int(total_lines) - int(len(cleaned))))
        else:
            print(Fore.YELLOW + "No invalid lines were found.".rstrip().center(width))
    pleasewait()
    menu()


def lines_counter():
    to_write.clear()
    clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Count all lines")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Count all lines containing a certain string")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            lines_counter()

        if select == "2":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                word = input(Fore.YELLOW + "Input the word you would like to search for: ".center(width).split(':')[0] + ': ' + Fore.LIGHTWHITE_EX)
                count = 0
                for lines in progressbar(file, total_lines):
                    reg = re.search(r"^((?!{}).)*$".format(word), lines)
                    if reg:
                        pass
                    else:
                        count += 1
                        to_write.append(lines)
            output = savelocation("Line Counter") + "/" + str(files("linesCounter")) + "[{}]".format(word)
            with open(output + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(to_write)
            print(Fore.YELLOW + "[+] lines Containing '{}': {}".center(width).format(word.capitalize(), count))
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            lines_counter()

    except TypeError as e:
        print(e)
        pleasewait()
        menu()


def randomize_lines():
    to_write.clear()
    clear()
    with open(openfile(), 'r', errors="ignore") as inputf:
        lines = inputf.readlines()
        total_lines = rawbigcount(inputf.name)
        start = time.time()
        print(Fore.YELLOW + "Loaded {} ".format(os.path.basename(inputf.name)).center(width))
        print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
        output = savelocation("Randomize Lines") + "/" + str(files("Randomizelines"))
        with open(output + currenttime() + ".txt", "a", errors="ignore") as output:
            i = 0
            amount = input(Fore.YELLOW + "[?] How many times would you like to randomize?: ".center(width).split(":")[0] + ": ")
            while i < int(amount):
                random.shuffle(lines)
                print(f"[+] Randomized {i} times.", end="\r")
                i += 1
            output.writelines(lines)
        print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
        pleasewait()
        menu()


def randomutilities():
    to_write.clear()
    clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Random string generator")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Random number generator")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Line break remover")
    print(Fore.YELLOW + "[4]" + Fore.LIGHTWHITE_EX + " | Line break adder")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            i = 0
            print("[?] Generating over 25 keys will automatically get saved instead of getting printed.")
            amount = int(input(Fore.YELLOW + "[?] How many would you like to generate?: "))
            length = int(input(Fore.YELLOW + "[?] How long should the string be?: "))
            if amount > 25:
                output = savelocation("Random Utilities") + "/" + str(files("RandomUtilities"))
                with open(output + currenttime() + '[String].txt', 'w') as outfile:
                    start = time.time()
                    while i < amount:
                        to_write.append(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length)) + '\n')
                        i += 1
                        print(f"[+] Generated: {i}", end="\r")
                    outfile.writelines(to_write)
            else:
                start = time.time()
                while i < amount:
                    print(Style.RESET_ALL + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length)))
                    i += 1
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            randomutilities()

        if select == "2":
            i = 0
            output = savelocation("Random Utilities") + "/" + str(files("RandomUtilities"))
            length = input(Fore.YELLOW + "[?] Input the range you'd like to generate [Example: 1-1000]: ")
            start = time.time()
            while i <= int(length.split("-")[1]):
                to_write.append(str(i))
                i += 1
            with open(output + currenttime() + '.txt', 'w', errors="ignore") as outfile:
                for lines in to_write:
                    outfile.writelines(lines + '\n')
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            randomutilities()

        if select == "3":
            with open(openfile(), 'r', errors="ignore") as inputf:
                start = time.time()
                for lines in inputf:
                    to_write.append(lines.replace("\n", " "))
                output = savelocation("Random Utilities") + "/" + str(files("RandomUtilities"))
                with open(output + currenttime() + '.txt', 'w') as outfile:
                    outfile.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            randomutilities()

        if select == "4":
            with open(openfile(), 'r', errors="ignore") as inputf:
                start = time.time()
                delimiter = input(Fore.YELLOW + "[?] What delimiter should I split at to add the lines break?: ")
                for lines in inputf:
                    try:
                        lines = lines.split(str(delimiter))
                        a = lines[0]
                        b = lines[1]
                        outputs = a + '\n' + delimiter + b
                        to_write.append(outputs)
                    except IndexError:
                        print(f"Unable to split at given delimiter: '{delimiter}'")
                output = savelocation("Random Utilities") + "/" + str(files("RandomUtilities"))
                with open(output + currenttime() + '.txt', 'w') as outfile:
                    outfile.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            randomutilities()

    except TypeError as e:
        print(e)
        pleasewait()
        menu()


def hash_identifier():
    print("\nCredit to psypanda: \nhttps://github.com/psypanda/hashID\n")
    hinput = input("Input your hash: ")
    result = subprocess.check_output("python HashID.py -m -j " + hinput)
    print(str(result).replace("\\r\\n", "\n").replace('b"', ''.rstrip()).replace('"', "".rstrip()))
    time.sleep(5)
    menu()


def password_filterer():
    to_write.clear()
    count = 0
    clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 uppercase letter.")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 number.")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 symbol.")
    print(Fore.YELLOW + "[4]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 uppercase and 1 symbol.")
    print(Fore.YELLOW + "[5]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 number and 1 uppercase.")
    print(Fore.YELLOW + "[6]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't contain at least 1 number, 1 uppercase and is shorter than x amount of characters.")
    print(Fore.YELLOW + "[7]" + Fore.LIGHTWHITE_EX + " | Remove all passwords shorter or longer than x amount of characters.")
    print(Fore.YELLOW + "\nPresets:")
    print(Fore.YELLOW + "[Fortnite]" + Fore.LIGHTWHITE_EX + " | Removes all passwords that don't meet Fortnite's requirements.")
    print(Fore.YELLOW + "[Minecraft]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't meet Minecraft's requirements.")
    print(Fore.YELLOW + "[Origin]" + Fore.LIGHTWHITE_EX + " | Remove all passwords that don't meet Origin's requirements.")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX).lower()

        if select == "1":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r".*[A-Z]+.*", line)
                        if reg:
                            to_write.append(lines)
                            count += 1
                            pass
                        else:
                            pass
                    except IndexError as e:
                        continue
            with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
            pleasewait()
            password_filterer()

        if select == "2":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        lines = lines.split(':')[1]
                        reg = re.search(r".*[0-9]+.*", lines)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
            pleasewait()
            password_filterer()

        if select == "3":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        lines = lines.split(':')[1]
                        reg = re.search(r".*[\\!$%^&*()_+|~\-=`{}[\]:\";'<>?,./@#]+.*", lines)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
            pleasewait()
            password_filterer()

        if select == "4":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        lines = lines.split(':')[1]
                        reg = re.search(r"((.*[A-Z]+).*([\\!$%^&*()_+|~\-=`{}[\]:\";'<>?,./@#]+.*))", lines)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
            pleasewait()
            password_filterer()

        if select == "5":
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        lines = lines.split(':')[1]
                        reg = re.search(r"((.*[A-Z]+).*([0-9]+.*))", lines)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
            pleasewait()
            password_filterer()

        if select == "6":
            with open(openfile(), 'r', errors="ignore") as file:
                amount = int(input("[?] How long should the password minimum be?: "))
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        lines = lines.split(':')[1]
                        if len(lines) >= amount:
                            reg = re.search(r"((.*[A-Z]+).*([0-9]+.*))", lines)
                            if reg:
                                to_write.append(lines)
                            else:
                                pass
                        else:
                            pass
                    except IndexError as e:
                        continue
            with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
            pleasewait()
            password_filterer()

        if select == "7":
            with open(openfile(), 'r', errors="ignore") as file:
                lonorsho = input(Fore.YELLOW + "[?] Would you like to remove passwords longer or shorter than x?: [Shorter/Longer] ".center(width).split("r] ")[0] + "r] ")
                amount = int(input(Fore.YELLOW + "[?] How long should the password minimum be?: ".center(width).split("?: ")[0] + "?: "+ Fore.LIGHTWHITE_EX))
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        if lonorsho == "Longer":
                            line = lines.split(':')[1]
                            if len(line) >= amount:
                                to_write.append(lines)
                            else:
                                pass
                        else:
                            line = lines.split(":")[1]
                            if len(line) <= amount:
                                to_write.append(lines)
                            else:
                                pass
                    except IndexError as e:
                        continue
            with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
            pleasewait()
            password_filterer()

        if select == "Fortnite".lower():
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        line = lines.rstrip().split(':')[1]
                        reg = re.search(r"((?=.*?[0-9]+)(?=.*?[A-Za-z]+)[^ \n\r]{7,})", line)
                        if not reg:
                            count += 1
                            pass
                        else:
                            to_write.append(lines)
                    except IndexError as e:
                        continue
            if count >= 1:
                with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '[Fortnite].txt', 'w') as output:
                    output.writelines(to_write)
                print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            password_filterer()

        if select == "Minecraft".lower():
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r"((?=.*?[0-9]+)|(?=.*?[A-Z]+)|(?=.*?[!#$%&'*+@/=?^_`{|}~-]+)[^ \n\r]{7,})", line)
                        if reg:
                            to_write.append(lines)
                            count += 1
                        else:
                            pass
                    except IndexError as e:
                        continue
            if count >= 1:
                with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '[Minecraft].txt', 'w') as output:
                    output.writelines(to_write)
                print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            password_filterer()

        if select == "Origin".lower():
            with open(openfile(), 'r', errors="ignore") as file:
                total_lines = rawbigcount(file.name)
                start = time.time()
                for lines in progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r"((?=.*?[0-9]+)(?=.*?[A-Z]+)(?=.*?[a-z]+).{8,16})", line)
                        if reg:
                            to_write.append(lines)
                            count += 1
                        else:
                            pass
                    except IndexError as e:
                        continue
            if count >= 1:
                with open(savelocation('Password Filterer') + '/' + str(files("PasswordFilterer")) + currenttime() + '[Origin].txt', 'w') as output:
                    output.writelines(to_write)
                print(Fore.YELLOW + "[+] Invalid passwords removed: {}".center(width).format(int(total_lines) - int(count) + 1))
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            pleasewait()
            password_filterer()

    except TypeError as e:
        print(e)
        pleasewait()
        menu()


if __name__ == '__main__':
    to_write.clear()
    try:
        shutil.rmtree("./__pycache__", ignore_errors=True)
        clear()
        settitle()
        try:
            with open("config.json") as f:
                data = json.load(f)
            if data["DiscordRichPresence"] == "True":
                RPC.connect()
                current_time = time.time()
                ct = str(current_time).split(".")[0]
                RPC.update(state="In the main menu", details="Version 0.1a", large_image="large", start=int(ct))
            else:
                pass
        except Exception as e:
            print(e)
        createfiles()
        menu()
    except Exception as e:
        print(e)
        pass