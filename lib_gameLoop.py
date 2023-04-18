from lib_dice import roll_d20
from getch import getch
import lib_strutil
from lib_termutil import cprint

def menuAndInput(menuoptions):
    print(menuoptions)
    option = getch().lower()
    print(option)
    return option


def endOfTurnOptions(option, character, menuoptions):
    print(menuoptions)
    while not (option == "y" or option == "n"): ## skip if we are repeating prompt or moving to next character
        option = getch().lower()
        print(option)
        if option == "r": ## we are rolling a d20
            cprint(f'\tA d20 is rolled. The result is: {roll_d20()}',"white")
            option = menuAndInput(menuoptions)
        elif option == "i": ## we are messing with inventory
            while not (option == "a" or option == "r"):
                option = menuAndInput("(a)dd or (r)emove inventory?)")
                if option == "a":
                    item = input("What to add to inventory: ")
                    character.inventory.append(item)
                    print(f"{character.name}'s inventory now has: {lib_strutil.oxfordize(character.inventory)}")
                elif option == "r":
                    print(f"{character.name}'s inventory now has: {lib_strutil.oxfordize(character.inventory)}")
                    remitem = input("What to remove?: ")
                    try:
                        character.inventory.remove(remitem)
                    except ValueError:
                        print("Element not found in the list")
            option = menuAndInput(menuoptions)
        elif option == "h":  ## we are adjusting hit points of current character
            while not (option == "a" or option == "r"):
                option = menuAndInput("(a)dd or (r)emove hit points?)")
                print(option)
                if option == "a":
                    heal = input("How many hp to add: ")
                    try:
                        character.hp += int(heal)
                    except ValueError:
                        print("Error occurred")
                    print(f"{character.name}'s hp is now: {character.hp}")
                elif option == "r":
                    print(f"{character.name}'s hp is now: {character.hp}")
                    damage = input("How much damage=?: ")
                    try:
                        character.hp -= int(damage)
                    except ValueError:
                        print("Error occurred")
                    print(f"{character.name}'s hp is now: {character.hp}")
            
            option = menuAndInput(menuoptions)
    return option