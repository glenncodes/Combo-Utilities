from colorama import Fore, Style
from Modules import *
import json
import re

regex = re.compile(r':\s*\S')
regex2 = re.compile(r'\s*\S:')


def lines_checker(text):
    if regex.search(text):
        if regex2.search(text):
            return True


MainMenu = (Utilities().randomcolor() + """
 ██████╗ ██████╗ ███╗   ███╗██████╗  ██████╗     ██╗   ██╗████████╗██╗██╗     ██╗████████╗██╗███████╗███████╗
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔═══██╗    ██║   ██║╚══██╔══╝██║██║     ██║╚══██╔══╝██║██╔════╝██╔════╝
██║     ██║   ██║██╔████╔██║██████╔╝██║   ██║    ██║   ██║   ██║   ██║██║     ██║   ██║   ██║█████╗  ███████╗
██║     ██║   ██║██║╚██╔╝██║██╔══██╗██║   ██║    ██║   ██║   ██║   ██║██║     ██║   ██║   ██║██╔══╝  ╚════██║
╚██████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝╚██████╔╝    ╚██████╔╝   ██║   ██║███████╗██║   ██║   ██║███████╗███████║
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝  ╚═════╝      ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝
                                                                                                  By Kid#0001""")


def color_print(msg, number):
    colors = {
        "{BLACK}", "{RED}", "{GREEN}", "{YELLOW}", "{BLUE}", "{MAGENTA}", "{CYAN}", "{WHITE}",
        "{LIGHTBLACK}", "{LIGHTRED}", "{LIGHTGREEN}", "{LIGHTYELLOW}", "{LIGHTBLUE}", "{LIGHTMAGENTA}", "{LIGHTCYAN}", "{LIGHTWHITE}"
    }

    other_options = {
        "{NUMBER}": number
    }

    for color in colors:
        if color.lower() in msg.lower():
            color = color.replace("{", "").replace("}", "")
            if color.startswith("LIGHT"):
                msg = msg.replace(color.lower(), getattr(Fore, color+"_EX"))
            else:
                msg = msg.replace(color.lower(), getattr(Fore, color))

    for option in other_options:
        if option.lower() in msg.lower():
            msg = msg.replace(option.lower(), other_options[option])
    msg = msg.replace("{", "").replace("}", "")
    return print(msg)


def menu():
    Utilities().clear()
    print(MainMenu)
    options = {}
    with open("settings/Configuration.json", "r") as file:
        file = json.load(file)
    for module in file['Modules']:
        if file['Modules'][module]['Enabled'] == 'True':
            module_num = file['Modules'][module]['Number']
            module_message = file['Modules'][module]['Message']
            module_startup = file['Modules'][module]['Startup']
            options.update({f"{module_num}": f"{module_startup}"})
            color_print(module_message, module_num)
    print(Style.RESET_ALL)
    try:
        selected = input('\n' + "" + 'Select one: ' + Fore.LIGHTWHITE_EX)

        if selected in options:
            eval(options[selected])
        if selected is not int:
            menu()

    except Exception as e:
        print(e)
        Utilities().pleasewait()
        menu()


if __name__ == '__main__':
    try:
        Utilities().startup_setup()
        menu()
    except Exception as e:
        exit(e)
