import os
from itertools import takewhile, repeat
import re
import shutil
import json
import time
from tkinter import Tk, filedialog
import fileinput
import random
from collections import defaultdict
import string
import subprocess
import requests
from tqdm import tqdm
from colorama import Fore, Style, init
from Utilities import Utilities

to_write = []
width = shutil.get_terminal_size().columns
PYTHONDONTWRITEBYTECODE = 1
regex = re.compile(r':\s*\S')
regex2 = re.compile(r'\s*\S:')

if not os.path.isfile(os.getcwd() + "/config.json"):
    
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
    file_save_location = input("\nWould you like to save the output to a different location? [Full file path to save to/Default] ")
    progress_bar = input("\nWould you like to use a progress bar? [True/False] ")
    
    config["FileNameType"] = file_name_type
    config["RandomMenuColor"] = random_menu_color
    config["SaveLocation"] = file_save_location
    config["ProgressBar"] = progress_bar

    with open("config.json", "w") as file:
        json.dump(config, file, indent=2)


def lines_checker(text):
    if regex.search(text):
        if regex2.search(text):
            return True
        else:
            return False
    else:
        return False

MainMenu = (Utilities().randomcolor() + """
 ██████╗ ██████╗ ███╗   ███╗██████╗  ██████╗     ██╗   ██╗████████╗██╗██╗     ██╗████████╗██╗███████╗███████╗
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔═══██╗    ██║   ██║╚══██╔══╝██║██║     ██║╚══██╔══╝██║██╔════╝██╔════╝
██║     ██║   ██║██╔████╔██║██████╔╝██║   ██║    ██║   ██║   ██║   ██║██║     ██║   ██║   ██║█████╗  ███████╗
██║     ██║   ██║██║╚██╔╝██║██╔══██╗██║   ██║    ██║   ██║   ██║   ██║██║     ██║   ██║   ██║██╔══╝  ╚════██║
╚██████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝╚██████╔╝    ╚██████╔╝   ██║   ██║███████╗██║   ██║   ██║███████╗███████║
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝  ╚═════╝      ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝    
                                                                                                  By Kid#0001""")



def menu():
    to_write.clear()
    init()
    Utilities().clear()
    print(MainMenu)
    print(Fore.YELLOW + "[1] " + Fore.LIGHTWHITE_EX + " | Combo Cleaner")
    print(Fore.YELLOW + "[2] " + Fore.LIGHTWHITE_EX + " | Combo Combiner")
    print(Fore.YELLOW + "[3] " + Fore.LIGHTWHITE_EX + " | Combo Parser")
    print(Fore.YELLOW + "[4] " + Fore.LIGHTWHITE_EX + " | Combo Sorter")
    print(Fore.YELLOW + "[5] " + Fore.LIGHTWHITE_EX + " | Combo Splitter")
    print(Fore.YELLOW + "[6] " + Fore.LIGHTWHITE_EX + " | Domain Sorter")
    print(Fore.YELLOW + "[7] " + Fore.LIGHTWHITE_EX + " | Duplicate Remover")
    print(Fore.YELLOW + "[8] " + Fore.LIGHTWHITE_EX + " | Email To Username")
    print(Fore.YELLOW + "[9] " + Fore.LIGHTWHITE_EX + " | Empty Line Remover")
    print(Fore.YELLOW + "[10]" + Fore.LIGHTWHITE_EX + " | Line Counter")
    print(Fore.YELLOW + "[11]" + Fore.LIGHTWHITE_EX + " | Randomize Line")
    print(Fore.YELLOW + "[12]" + Fore.LIGHTWHITE_EX + " | Hash Identifier")
    print(Fore.YELLOW + "[13]" + Fore.LIGHTWHITE_EX + " | Password Filterer")
    print(Fore.YELLOW + "[14]" + Fore.LIGHTWHITE_EX + " | Random Utilities" + Style.RESET_ALL)
    try:
        selected = input('\n' + Fore.YELLOW + 'Select one: ' + Fore.LIGHTWHITE_EX)
        
        options = {
            "1": "combo_cleaner()",
            "2": "combo_combiner()",
            "3": "combo_parser()",
            "4": "combo_sorter()",
            "5": "combo_splitter()",
            "6": "domain_sorter()",
            "7": "duplicate_remover()",
            "8": "email_to_user()",
            "9": "empty_lines_remover()",
            "10": "lines_counter()",
            "11": "randomize_lines()",
            "12": "hash_identifier()",
            "13": "password_filterer()",
            "14": "randomutilities()"
        }

        if selected in options:
            eval(options[selected])
        if selected is not int:
            menu()
    
    except Exception as e:
        print(e)
        Utilities().pleasewait()
        menu()


def combo_cleaner():
    to_write.clear()
    Utilities().clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Replace all ;'s with :'s")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Remove all lines containing '{' or '}'")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Remove all lines not containing ':' or ';'")
    print(Fore.YELLOW + "[4]" + Fore.LIGHTWHITE_EX + " | Remove all lines not containing '@'")
    print(Fore.YELLOW + "[5]" + Fore.LIGHTWHITE_EX + " | Remove all lines containing '@'")
    print(Fore.YELLOW + "[6]" + Fore.LIGHTWHITE_EX + " | Remove all of the above [Except option 5]" + Fore.LIGHTRED_EX + " [Most recommended!]" + Style.RESET_ALL)
    print(Fore.YELLOW + "[7]" + Fore.LIGHTWHITE_EX + " | Remove all lines containing a certain string")
    print(Fore.YELLOW + "[8]" + Fore.LIGHTWHITE_EX + " | Invalid combo remover [example@example.com: ] or [ :example]")
    print(Fore.YELLOW + "[9]" + Fore.LIGHTWHITE_EX + " | Remove all lines longer than or shorter than x")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in Utilities().progressbar(file, total_lines):
                    if ';' in lines:
                        line = lines.replace(";", ":")
                        to_write.append(line)
                    else:
                        to_write.append(lines)
            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Cleaner") + "/" + Utilities().files("ComboCleaner") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_cleaner()

        if select == "2":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in Utilities().progressbar(file, total_lines):
                    if "{" in lines or "}" in lines:
                        pass
                    else:
                        to_write.append(lines)
            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Cleaner") + "/" + Utilities().files("ComboCleaner") + Utilities().currenttime() +  '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_cleaner()

        if select == "3":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in Utilities().progressbar(file, total_lines):
                    if ":" in lines or ";" in lines:
                        to_write.append(lines)
                    else:
                        print(lines)
            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Cleaner") + "/" + Utilities().files("ComboCleaner") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_cleaner()

        if select == "4":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                for lines in Utilities().progressbar(file, total_lines):
                    if "@" not in lines:
                        pass
                    else:
                        to_write.append(lines)
            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Cleaner") + "/" + Utilities().files("ComboCleaner") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_cleaner()

        if select == "5":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                for lines in Utilities().progressbar(file, total_lines):
                    if "@" not in lines:
                        to_write.append(lines)
                    else:
                        pass
            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Cleaner") + "/" + Utilities().files("ComboCleaner") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_cleaner()

        if select == "6":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines+1).center(width) + Style.RESET_ALL)
                for lines in Utilities().progressbar(file, total_lines):
                    if "{" in lines or "}" in lines or "@" not in lines:
                        pass
                    else:
                        if ";" in lines:
                            line = lines.replace(';', ':')
                            to_write.append(line)
                        else:
                            if ":" not in lines:
                                pass
                            else:
                                to_write.append(lines)

            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Cleaner") + "/" + Utilities().files("ComboCleaner") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_cleaner()

        if select == "7":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                word = input(Fore.YELLOW + "[?] Input the word to search for: ".center(width).split(':')[0] + ': ' + Fore.LIGHTWHITE_EX)
                for lines in Utilities().progressbar(file, total_lines):
                    if word in lines:
                        pass
                    else:
                        to_write.append(lines)
            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Cleaner") + "/" + Utilities().files("ComboCleaner") + Utilities().currenttime() + f'{[word]}.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_cleaner()

        if select == "8":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.split(":")
                        if line[0] in ("\n", ""):
                            pass
                        elif line[1] in ("\n", ""):
                            pass
                        else:
                            to_write.append(lines)
                    except Exception:
                        pass
            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Cleaner") + "/" + Utilities().files("ComboCleaner") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_cleaner()

        if select == "9":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                pick = input(Fore.YELLOW + "[?] Would you like to remove lines longer or shorter than x? | [longer/shorter]: ".center(width).split(':')[0] + ': ' + Fore.LIGHTWHITE_EX).lower()
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                if pick == "longer":
                    longest = int(input(Fore.YELLOW + "[?] How long should the maximum be? ".center(width).split('? ')[0] + '? ' + Fore.LIGHTWHITE_EX))
                    for lines in Utilities().progressbar(file, total_lines):
                        if len(lines) > longest:
                            pass
                        else:
                            to_write.append(lines)

                elif pick == "shorter":
                    shortest = int(input(Fore.YELLOW + "[?] How long should the shortest be? ".center(width).split('? ')[0] + '? ' + Fore.LIGHTWHITE_EX))
                    for lines in Utilities().progressbar(file, total_lines):
                        if len(lines) < shortest:
                            pass
                        else:
                            to_write.append(lines)
            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Cleaner") + "/" + Utilities().files("ComboCleaner") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_cleaner()

    except TypeError as e:
        print(e)
        Utilities().pleasewait()
        menu()


def combo_combiner():
    to_write.clear()
    Utilities().clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Combine multilple files into 1 file.")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Combine usernames/emails.txt & passwords.txt into 1 text file.")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input(Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            print(Fore.YELLOW + "[+] You can select multiple combos!".center(width))
            root = Tk()
            root.withdraw()
            root.filename = filedialog.askopenfilenames(title="Select combo list(s)", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            start = time.time()
            lines = fileinput.input(root.filename, openhook=fileinput.hook_encoded("ISO-8859-1", errors="ignore"))
            
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            output = Utilities().savelocation("Combo Combiner") + "/" + Utilities().files("ComboCombiner")
            with open(output + Utilities().currenttime() + ".txt", "a", errors="ignore") as outfile:
                outfile.writelines(lines)

            root.destroy()
            Utilities().pleasewait()
            combo_combiner()

        if select == "2":
            root = Tk()
            root.withdraw()
            root.filename = filedialog.askopenfilename(title="Select username list", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            with open(root.filename, "r", errors="ignore") as user:
                print(Fore.YELLOW + "Loaded {:,} usernames".center(width).format(Utilities().rawbigcount(root.filename)))

                root.filename1 = filedialog.askopenfilename(title="Select password list", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
                with open(root.filename1, "r", errors="ignore") as passw:
                    print(Fore.YELLOW + "Loaded {:,} passwords".center(width).format(Utilities().rawbigcount(root.filename1)))
                    start = time.time()
                    for x, y in zip(user, passw):
                        to_write.append(x.strip() + ":" + y.strip() + '\n')
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            output = Utilities().savelocation("Combo Combiner") + '/' + Utilities().files("ComboCombiner")
            with open(output + Utilities().currenttime() + '.txt', "a", errors="ignore") as outfile:
                outfile.writelines(to_write)
            Utilities().pleasewait()
            combo_combiner()

    except TypeError as e:
        print(e)
        Utilities().pleasewait()
        menu()


def combo_parser():
    to_write.clear()
    Utilities().clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Password:Email/Username -> Email/Username:Password [Works for reversing email:password too]")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Username/email:Password:Email/username -> 2 files [user:pass, email:pass]")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Email Extractor")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in Utilities().progressbar(file, total_lines):
                    tmp = lines.split(":")
                    to_write.append(tmp[0].rstrip() + ':' + tmp[1].rstrip() + '\n')
            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Parser") + '/' + Utilities().files("ComboParser") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_parser()

        if select == "2":
            dest = []
            dest2 = []
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in Utilities().progressbar(file, total_lines):
                    eachlines = lines.split()
                    dest.append(eachlines[2] + ":" + eachlines[1] + "\n")
                    dest2.append(eachlines[0] + ":" + eachlines[1] + "\n")
            if len(dest) >= 1 and len(dest2) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Parser") + '/' + Utilities().files("ComboParser1") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(dest)
                with open(Utilities().savelocation("Combo Parser") + '/' + Utilities().files("ComboParser2") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile2:
                    outfile2.writelines(dest2)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_parser()

        if select == "3":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in Utilities().progressbar(file, total_lines):
                    match = re.search(r"""(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-zA-Z0-9-]*[a-zA-Z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""", lines)
                    if match:
                        to_write.append(match.group(0) + "\n")

            if len(to_write) >= 1:
                print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                with open(Utilities().savelocation("Combo Parser") + '/' + Utilities().files("ComboParser") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                    outfile.writelines(to_write)
            else:
                print(Fore.YELLOW + "No invalid lines were found.".center(width))
            Utilities().pleasewait()
            combo_parser()

    except TypeError as e:
        print(e)
        Utilities().pleasewait()
        menu()


def combo_sorter():
    to_write.clear()
    Utilities().clear()
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
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                start = time.time()
                lines = sorted(file.readlines(), key=len)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(lines)
            Utilities().pleasewait()
            combo_sorter()

        if select == "2":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                lines = sorted(file.readlines(), key=len, reverse=True)
            
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation("Combo Sorter") + "/" + Utilities().files("ComboSorter") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(lines)
            Utilities().pleasewait()
            combo_sorter()

        if select == "3":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                lines = sorted(file.readlines())
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(lines)
            Utilities().pleasewait()
            combo_sorter()

        if select == "4":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                pick = input(Fore.YELLOW + "[?] Do you want to add or remove commas? - [add/remove]: ".center(width).split(':')[0] + ': ')
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                for lines in Utilities().progressbar(file, total_lines):
                    if pick == "remove":
                        lines = re.sub('(,)[^,]*$', "\r", lines.rstrip())
                        to_write.append(lines)
                    else:
                        lines = lines.rstrip()
                        result = "".join(lines) + ",\n"
                        to_write.append(result)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter") + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(to_write)
            Utilities().pleasewait()
            combo_sorter()

        if select == "5":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                pick = input("[?] Do you want to add a prefix or a suffix? - [prefix/suffix]: ".center(width).split(':')[0] + ': ')
                prefixorsuffix = input("[?] What would you like to add?: ".center(width).split(":")[0] + ': ')
                done = []
                for lines in Utilities().progressbar(file, total_lines):
                    if pick == "prefix":
                        done.append(prefixorsuffix + f"{lines}")
                    else:
                        done = (["".join([x.strip(), prefixorsuffix, "\n"]) for x in file.readlines()])
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            output = Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter")
            with open(output + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(done)
            Utilities().pleasewait()
            combo_sorter()

        if select == "6":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                email = input(Fore.YELLOW + "[?] What email would you like to add? [Domain [Example: gmail.com]/Random]".center(width).split("Random]")[0] + 'Random]: ').lower()
                with open("email-providers.json") as json_file:
                    emails = json.load(json_file)
                for lines in Utilities().progressbar(file, total_lines):
                    if email == "random":
                        slines = lines.split(":")
                        username = slines[0]
                        to_write.append(username + "@" + random.choice(emails) + ":" + slines[1])
                    else:
                        slines = lines.split(":")
                        username = slines[0]
                        to_write.append(username + "@" + email + ":" + slines[1])
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            output = Utilities().savelocation("Combo Sorter") + '/' + Utilities().files("ComboSorter")
            with open(output + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(to_write)
            Utilities().pleasewait()
            combo_sorter()

    except TypeError as e:
        print(e)
        Utilities().pleasewait()
        menu()


def combo_splitter():
    to_write.clear()
    Utilities().clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Split combos into multiple smaller combos")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Split combo into 2 files, user/email + password")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Split Email:pass into 3 files, emails, passwords and usernames")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            splitlen = int(input(Fore.YELLOW + "Input the amount of lines you'd like per file: ".center(width).split(':')[0] + ": "))
            with open(Utilities().openfile(), "r", errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print("File contains {} lines.".format(total_lines).center(width))
                print("Estimated amount of files: {}".format(total_lines / splitlen).split(".")[0].center(width) + Style.RESET_ALL)
                at = 0
                count = 0
                output = Utilities().savelocation("Combo Splitter") + "/" + Utilities().files("ComboSplitter")
                for lines in file:
                    if count % splitlen == 0:
                        dest = open(output + " - " + str(at) + " - " + Utilities().currenttime() + ".txt", "a", errors="ignore")
                        at += 1
                    dest.writelines(lines)
                    count += 1

            dest.close()
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            Utilities().pleasewait()
            combo_splitter()

        if select == "2":
            to_write0 = []
            to_write1 = []

            with open(Utilities().openfile(), "r", errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                output = Utilities().savelocation("Combo Splitter") + "/" + Utilities().files("ComboSplitter2Email")
                output2 = Utilities().savelocation("Combo Splitter") + "/" + Utilities().files("ComboSplitter2Password")

                for lines in file:
                    try:
                        inputlines = lines.split(":")
                        to_write0.append("{}".format(inputlines[0]))
                        to_write1.append("{}\n".format(inputlines[1]))
                    except Exception:
                        pass
            with open(output + Utilities().currenttime() + ".txt", "a", errors="ignore") as file1:
                file1.writelines(to_write0)
            with open(output2 + Utilities().currenttime() + ".txt", "a", errors="ignore") as file2:
                file2.writelines(to_write1) 
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            Utilities().pleasewait()
            combo_splitter()

        if select == "3":
            emails = []
            usernames = []
            passwords = []

            with open(Utilities().openfile(), "r", errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                output = Utilities().savelocation("Combo Splitter") + "/" + Utilities().files("ComboSplitter3Email")
                output2 = Utilities().savelocation("Combo Splitter") + "/" + Utilities().files("ComboSplitter3Username")
                output3 = Utilities().savelocation("Combo Splitter") + "/" + Utilities().files("ComboSplitter3Password")
                try:
                    for lines in file:
                        emails.append(lines.split(":")[0] + '\n')
                        usernames.append(lines.split(":")[0].split('@')[0] + '\n')
                        passwords.append(lines.split(":")[1])
                except IndexError:
                    pass
            with open(output + Utilities().currenttime() + '.txt', 'a', errors="ignore") as outfile1:
                outfile1.writelines(emails)
            with open(output2 + Utilities().currenttime() + ".txt", "a", errors="ignore") as outfile2:
                outfile2.writelines(usernames)
            with open(output3 + Utilities().currenttime() + ".txt", "a", errors="ignore") as outfile3:
                outfile3.writelines(passwords)
            print(Fore.YELLOW + "[+] Time took: {}".rstrip().center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            Utilities().pleasewait()
            combo_splitter()

    except TypeError as e:
        print(e)
        Utilities().pleasewait()
        menu()


def domain_sorter():
    to_write.clear()
    Utilities().clear()
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

            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
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
            comout = Utilities().savelocation("Domain Sorter") + "/" + Utilities().files("DomainSorter")
            try:
                for key in d.keys():
                    if len(d.get(key)) >= 1:
                        with open(comout + Utilities().currenttime() + f'[{key.replace(":", "").lower()}].txt', 'a', errors="ignore") as outfile:
                            outfile.writelines(d.get(key))
            except Exception as e:
                print(e)
                pass
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            Utilities().pleasewait()
            domain_sorter()

        if select == "2":
            d = defaultdict(list)
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                for lines in Utilities().progressbar(file, total_lines):
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
                        comout = Utilities().savelocation("Domain Sorter") + "/" + Utilities().files("DomainSorter")
                        with open(comout + Utilities().currenttime() + f'[{key.replace(":", "").lower()}].txt', 'a', errors="ignore") as outfile:
                            outfile.writelines(d.get(key))
            except Exception as e:
                print(e)
                pass
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            Utilities().pleasewait()
            domain_sorter()

        if select == "3":
            d = defaultdict(list)
            with open(Utilities().openfile(), 'r', encoding="iso-8859-1") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                for lines in Utilities().progressbar(file, total_lines):
                    reg = re.search(r'@(.*):', lines)
                    if ":" in reg.group(1):
                        reggy = reg.group(1).split(":")[0]
                    else:
                        reggy = reg.group(1)

                    d[reggy].append(lines)
            for key in d.keys():
                output = Utilities().savelocation("Domain Sorter") + "/" + Utilities().files("DomainSorter") + Utilities().currenttime() + "[{}].txt".format(key.replace(":", "").lower())
                with open(output, 'a+', errors="ignore") as outfile:
                    outfile.writelines(d.get(key))
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            Utilities().pleasewait()
            domain_sorter()

        if select == "4":
            d = defaultdict(list)
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                try:
                    for lines in Utilities().progressbar(file, total_lines):
                        reg = re.search(r"@[^.]*(\..*\..*|\..*):", lines)
                        if ':' in reg.group(1):
                            reggy = reg.group(1).split(":")[0]
                        else:
                            reggy = reg.group(1)
                        d[reggy].append(lines)
                    for key in d.keys():
                        output = Utilities().savelocation("Domain Sorter") + "/" + Utilities().files("DomainSorter") + Utilities().currenttime() + "[{}].txt".format(key.replace(":", "").lower())
                        with open(output, 'a+', errors="ignore") as outfile:
                            outfile.writelines(d.get(key))
                except Exception as e:
                    print(e)
                    pass
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            Utilities().pleasewait()
            domain_sorter()
        
        if select == "5":
            d = defaultdict(list)
            domains = [x for x in input("Select domains [Seperated with a space]: ").split(" ")]
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
                try:
                    for lines in Utilities().progressbar(file, total_lines):
                        for line in domains:
                            reg = re.search(f"@({line}):", lines)
                            if reg:
                                d[reg.group(1)].append(lines)
                            else:
                                pass
                    for key in d.keys():
                        output = Utilities().savelocation("Domain Sorter") + "/" + Utilities().files("DomainSorter") + Utilities().currenttime() + "[{}].txt".format(key.replace(":", "").lower())
                        with open(output, 'a+', errors="replace") as outfile:
                            outfile.writelines(d.get(key))
                except Exception as e:
                    print(e)
                    pass
            print(Fore.YELLOW + "[+] lines Sorted: %s".center(width) % total_lines)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            Utilities().pleasewait()
            domain_sorter()
        
    except Exception as e:
        print(e)
        Utilities().pleasewait()
        menu()


def duplicate_remover():
    to_write.clear()
    Utilities().clear()
    with open(Utilities().openfile(), 'r', errors="ignore") as file:
        total_lines = Utilities().rawbigcount(file.name)
        start = time.time()
        print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
        print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
        uniquelines = set(file.readlines())

    if not len(uniquelines) == total_lines:
        output = Utilities().savelocation("Duplicate Remover") + "/" + Utilities().files("DuplicateRemover")
        with open(output + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
            outfile.writelines(uniquelines)
        print("[+] Duplicates Removed: %s".center(width) % str(len(uniquelines) - total_lines))
    else:
        print("[-] No duplicates found".center(width))
    print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
    Utilities().pleasewait()
    menu()


def email_to_user():
    Utilities().clear()
    to_write.clear()
    with open(Utilities().openfile(), 'r', errors="ignore") as file:
        total_lines = Utilities().rawbigcount(file.name)
        start = time.time()
        print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
        print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

        output = Utilities().savelocation("Email To Username") + "/" + Utilities().files("EmailToUsername")

        for line in file:
            lines = line.split(":")
            to_write.append(lines[0].split("@")[0] + ":" + lines[1])

    print(Fore.YELLOW + "[+] lines Converted: %s".rstrip().center(width) % total_lines)
    print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
    with open(output + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
        outfile.writelines(to_write)
    Utilities().pleasewait()
    menu()


def empty_lines_remover():
    to_write.clear()
    Utilities().clear()
    with open(Utilities().openfile(), 'r', errors="ignore") as file:
        total_lines = Utilities().rawbigcount(file.name)
        start = time.time()
        print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
        print(Fore.YELLOW + "File contains {:,} lines.".format(total_lines).rstrip().center(width) + Style.RESET_ALL)

        cleaned = list(filter(lambda x: not re.match(r'^\s*$', x), file.readlines()))
        print(Fore.YELLOW + "[+] Time took: {}".rstrip().center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
        if len(cleaned) >= 1 and len(cleaned) < total_lines:
            output = Utilities().savelocation("Empty Line Remover") + "/" + Utilities().files("EmptylinesRemover")
            with open(output + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(cleaned)
            print(Fore.YELLOW + "[+] Empty Lines Removed: %s".rstrip().center(width) % str(int(total_lines) - int(len(cleaned))))
        else:
            print(Fore.YELLOW + "No invalid lines were found.".rstrip().center(width))
    Utilities().pleasewait()
    menu()


def lines_counter():
    to_write.clear()
    Utilities().clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Count all lines")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Count all lines containing a certain string")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            Utilities().pleasewait()
            lines_counter()

        if select == "2":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                print(Fore.YELLOW + f"Loaded {os.path.basename(file.name)}".rstrip().center(width))
                print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)

                word = input(Fore.YELLOW + "Input the word to search for: ".center(width).split(':')[0] + ': ' + Fore.LIGHTWHITE_EX)
                for lines in file:
                    if not word in lines:
                        pass
                    else:
                        to_write.append(lines)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")            
            output = Utilities().savelocation("Line Counter") + "/" + Utilities().files("linesCounter") + "[{}]".format(word)
            with open(output + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(to_write)
            Utilities().pleasewait()
            lines_counter()

    except TypeError as e:
        print(e)
        Utilities().pleasewait()
        menu()


def randomize_lines():
    to_write.clear()
    Utilities().clear()
    with open(Utilities().openfile(), 'r', errors="ignore") as file:
        lines = file.readlines()
        total_lines = Utilities().rawbigcount(file.name)
        start = time.time()
        print(Fore.YELLOW + "Loaded {} ".format(os.path.basename(file.name)).center(width))
        print(Fore.YELLOW + "File contains {:,} lines.".rstrip().format(total_lines).center(width) + Style.RESET_ALL)
        output = Utilities().savelocation("Randomize Lines") + "/" + Utilities().files("Randomizelines")
        amount = input(Fore.YELLOW + "[?] How many times would you like to randomize?: ".center(width).split(":")[0] + ": ")
        for _ in range(int(amount)):
            random.shuffle(lines)
            print(f"[+] Randomized {_} times.".center(width), end="\r")
        print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
        with open(output + Utilities().currenttime() + ".txt", "a", errors="ignore") as output:
            output.writelines(lines)
        Utilities().pleasewait()
        menu()


def randomutilities():
    to_write.clear()
    Utilities().clear()
    print(Fore.YELLOW + "[1]" + Fore.LIGHTWHITE_EX + " | Random string generator")
    print(Fore.YELLOW + "[2]" + Fore.LIGHTWHITE_EX + " | Number generator")
    print(Fore.YELLOW + "[3]" + Fore.LIGHTWHITE_EX + " | Line break remover")
    print(Fore.YELLOW + "[4]" + Fore.LIGHTWHITE_EX + " | Line break adder")
    print(Fore.YELLOW + "\nPress enter to go back to the main menu.")
    try:
        select = input("\n" + Fore.YELLOW + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

        if select == "1":
            print("[*] Generating over 25 keys will automatically get saved instead of getting printed.")
            amount = int(input(Fore.YELLOW + "[?] How many would you like to generate?: "))
            length = int(input(Fore.YELLOW + "[?] How long should the string be?: "))
            if amount >= 25:
                output = Utilities().savelocation("Random Utilities") + "/" + Utilities().files("RandomUtilities")
                with open(output + Utilities().currenttime() + '[String].txt', 'w') as outfile:
                    start = time.time()
                    for _ in range(amount)[::-1]:
                        to_write.append(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length)) + '\n')
                    print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
                    outfile.writelines(to_write)
            else:
                start = time.time()
                for _ in range(amount)[::-1]:
                    print(Style.RESET_ALL + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length)))
            Utilities().pleasewait()
            randomutilities()

        if select == "2":
            output = Utilities().savelocation("Random Utilities") + "/" + Utilities().files("RandomUtilities")
            amount = int(str(input(Fore.YELLOW + "[?] Input how many numbers to generate: ".center(width).split(":")[0] + ":")))
            start = time.time()
            for i in range(amount+1):
                to_write.append(i)
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(output + Utilities().currenttime() + '.txt', 'w', errors="ignore") as outfile:
                outfile.writelines(str((x))+'\n' for x in to_write)
            Utilities().pleasewait()
            randomutilities()

        if select == "3":
            with open(Utilities().openfile(), 'r', errors="ignore") as inputf:
                start = time.time()
                for lines in inputf:
                    to_write.append(lines.replace("\n", " "))
            output = Utilities().savelocation("Random Utilities") + "/" + Utilities().files("RandomUtilities")
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(output + Utilities().currenttime() + '.txt', 'w') as outfile:
                outfile.writelines(to_write)
            Utilities().pleasewait()
            randomutilities()

        if select == "4":
            with open(Utilities().openfile(), 'r', errors="ignore") as inputf:
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
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            output = Utilities().savelocation("Random Utilities") + "/" + Utilities().files("RandomUtilities")
            with open(output + Utilities().currenttime() + '.txt', 'w') as outfile:
                outfile.writelines(to_write)
            Utilities().pleasewait()
            randomutilities()

    except TypeError as e:
        print(e)
        Utilities().pleasewait()
        menu()


def hash_identifier():
    print("\nCredit to psypanda: \nhttps://github.com/psypanda/hashID\n")
    subprocess.call("python HashID.py -m -j " + input("Input your hash: "), shell=False)
    Utilities().pleasewait()
    menu()


def password_filterer():
    to_write.clear()
    Utilities().clear()
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
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r".*[A-Z]+.*", line)
                        if reg:
                            to_write.append(lines)
                            pass
                        else:
                            pass
                    except IndexError as e:
                        continue
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")            
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

        if select == "2":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r".*[0-9]+.*", line)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

        if select == "3":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r".*[\\!$%^&*()_+|~\-=`{}[\]:\";'<>?,./@#]+.*", line)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

        if select == "4":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r"((.*[A-Z]+).*([\\!$%^&*()_+|~\-=`{}[\]:\";'<>?,./@#]+.*))", line)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

        if select == "5":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r"((.*[A-Z]+).*([0-9]+.*))", line)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

        if select == "6":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                amount = int(input("[?] How long should the password minimum be?: "))
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        if len(line) >= amount:
                            reg = re.search(r"((.*[A-Z]+).*([0-9]+.*))", line)
                            if reg:
                                to_write.append(lines)
                            else:
                                pass
                        else:
                            pass
                    except IndexError as e:
                        continue
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

        if select == "7":
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                lonorsho = input(Fore.YELLOW + "[?] Would you like to remove passwords longer or shorter than x?: [Shorter/Longer] ".center(width).split("r] ")[0] + "r] ").lower()
                amount = int(input(Fore.YELLOW + "[?] How long should the password minimum be?: ".center(width).split("?: ")[0] + "?: "+ Fore.LIGHTWHITE_EX))
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        if lonorsho == "longer":
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
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '.txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

        if select == "Fortnite".lower():
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.rstrip().split(':')[1]
                        reg = re.search(r"((?=.*?[0-9]+)(?=.*?[A-Za-z]+)[^ \n\r]{7,})", line)
                        if not reg:
                            pass
                        else:
                            to_write.append(lines)
                    except IndexError as e:
                        continue
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '[Fortnite].txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

        if select == "Minecraft".lower():
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r"((?=.*?[0-9]+)|(?=.*?[A-Z]+)|(?=.*?[!#$%&'*+@/=?^_`{|}~-]+)[^ \n\r]{7,})", line)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '[Minecraft].txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

        if select == "Origin".lower():
            with open(Utilities().openfile(), 'r', errors="ignore") as file:
                total_lines = Utilities().rawbigcount(file.name)
                start = time.time()
                for lines in Utilities().progressbar(file, total_lines):
                    try:
                        line = lines.split(':')[1]
                        reg = re.search(r"((?=.*?[0-9]+)(?=.*?[A-Z]+)(?=.*?[a-z]+).{8,16})", line)
                        if reg:
                            to_write.append(lines)
                        else:
                            pass
                    except IndexError as e:
                        continue
            print(Fore.YELLOW + "[+] Time took: {}".center(width - 7).format(time.time() - start).split('.')[0] + " seconds")
            with open(Utilities().savelocation('Password Filterer') + '/' + Utilities().files("PasswordFilterer") + Utilities().currenttime() + '[Origin].txt', 'w') as output:
                output.writelines(to_write)
            Utilities().pleasewait()
            password_filterer()

    except TypeError as e:
        print(e)
        Utilities().pleasewait()
        menu()


if __name__ == '__main__':
    to_write.clear()
    try:
        shutil.rmtree("./__pycache__", ignore_errors=True)
        Utilities().clear()
        Utilities().settitle()
        Utilities().createfiles()
        menu()
    
    except Exception as e:
        print(e)
        pass