from Modules.Utilities import Utilities
from tkinter import Tk, filedialog
from colorama import Fore, Style
import fileinput
import shutil
import time

class ComboCombiner():

    def __init__(self):
        self.to_write = []
        self.utilities = Utilities()
        self.width = shutil.get_terminal_size().columns
        self.total_lines = None

    def startup(self):
        self.utilities.clear()
        self.to_write.clear()
        print(self.utilities.custom_color() + "[1]" + Fore.LIGHTWHITE_EX + " | Combine multiple files into 1 file.")
        print(self.utilities.custom_color() + "[2]" + Fore.LIGHTWHITE_EX + " | Combine usernames/emails.txt & passwords.txt into 1 text file.")
        print(self.utilities.custom_color() + "\nPress enter to go back to the main menu.")
        try:
            select = input(self.utilities.custom_color() + "[?] Select the module you'd like to use: " + Fore.LIGHTWHITE_EX)

            self.modules = {
                "1": "self.module_1()",
                "2": "self.module_2()"
            }
            if select in self.modules:
                eval(self.modules[select])
        except Exception:
            self.utilities.pleasewait()
            self.startup()

    def module_1(self):
        print(self.utilities.custom_color() + "[*] You can select multiple combos!".center(self.width))
        root = Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilenames(title="Select combo list(s)", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        start = time.time()
        lines = fileinput.input(root.filename, openhook=fileinput.hook_encoded("ISO-8859-1", errors="ignore"))

        output = self.utilities.savelocation("Combo Combiner") + "/" + self.utilities.files("ComboCombiner")
        with open(output + self.utilities.currenttime() + ".txt", "a", errors="ignore") as outfile:
            outfile.writelines(lines)
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")

        root.destroy()
        self.utilities.pleasewait()
        self.startup()

    def module_2(self):
        root = Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(title="Select username list", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        with open(root.filename, "r", errors="ignore") as user:
            print(self.utilities.custom_color() + "Loaded {:,} usernames".center(self.width).format(self.utilities.rawbigcount(root.filename)))

            root.filename1 = filedialog.askopenfilename(title="Select password list", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            with open(root.filename1, "r", errors="ignore") as passw:
                print(self.utilities.custom_color() + "Loaded {:,} passwords".center(self.width).format(self.utilities.rawbigcount(root.filename1)))
                start = time.time()
                for x, y in zip(user, passw):
                    self.to_write.append(x.strip() + ":" + y.strip() + '\n')
        output = self.utilities.savelocation("Combo Combiner") + '/' + self.utilities.files("ComboCombiner")
        with open(output + self.utilities.currenttime() + '.txt', "a", errors="ignore") as outfile:
            outfile.writelines(self.to_write)
        print(self.utilities.custom_color() + "[+] Time took: {}".center(self.width - 7).format(time.time() - start).split('.')[0] + " seconds")
        self.utilities.pleasewait()
        self.startup()


