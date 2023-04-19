
from lib_termutil import cprint
import lib_strutil
from dnd_party import Party, AICharacter, HumanGM, AIGM, tokenToMoneyPrint
from lib_gameLoop import menuAndInput, endOfTurnOptions

import signal
import sys


art = """
######################################################
  /$$$$$$  /$$$$$$       /$$   /$$ /$$$$$$$   /$$$$$$ 
 /$$__  $$|_  $$_/      | $$$ | $$| $$__  $$ /$$__  $$
| $$  \ $$  | $$        | $$$$| $$| $$  \ $$| $$  \__/
| $$$$$$$$  | $$        | $$ $$ $$| $$$$$$$/| $$      
| $$__  $$  | $$        | $$  $$$$| $$____/ | $$      
| $$  | $$  | $$        | $$\  $$$| $$      | $$    $$
| $$  | $$ /$$$$$$      | $$ \  $$| $$      |  $$$$$$/
|__/  |__/|______/      |__/  \__/|__/       \______/ 
######################################################
"""

VERBOSE = False ## control flag for lots of text debug


turn_counter = 0;
# a tracker for LLM tokens spent
cumulative_tokens = 0

def printEnd(round, tokens):
    cprint(f"Thank you for playing.","red")
    cprint(f"Turns survived {turn_counter}","red")
    tokenToMoneyPrint(cumulative_tokens)

def signal_handler(sig, frame):
    """
    Signal handler function to catch CTRL-C and print a message before exiting
    """
    cprint(f"You have decided to exit the dungeon","white")
    printEnd(turn_counter, cumulative_tokens)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

helga = AICharacter(
    name="Helga",
    knowledge="you know negotiation is pointless and monsters must be slain. ",
    inventory=["a sword", "leather armor", "a crossbow"],
    class_name="warrior",
    class_abilities="can use items in your inventory but cannot cast spells. ",
    goal_text="Your goal is to explore the dungeon and find the treasure. ",
    text_color="red",
    hp=12,
    voice_name="Tessa",
    voice_speed=200
    )

fizban = AICharacter(
    name="Fizban",
    knowledge="you know clever play is the best way to win this game. ",
    inventory=["a staff","a floppy hat"],
    class_name="wizard",
    class_abilities="and can use items in your invetory and cast many spells but not healing or resurrection spells",
    goal_text="Your goal is to explore the dungeon and find the treasure. ",
    hp=4,
    voice_name="Reed (English (UK))",
    voice_speed=190
    )

rocko = AICharacter(
    name="Rocko",
    knowledge="you throw caution to the wind and attack any enemy who dares cross your path. ",
    inventory=["a dagger", "a long rope"],
    class_name="swashbucker",
    class_abilities="and can use items in your inventory but cannot cast spells. ",
    goal_text="Your goal is to explore the dungeon and find the treasure. ",
    text_color="yellow",
    hp=8,
    voice_name="Rocko (English (US))",
    voice_speed=190
    )

party = Party([helga,rocko, fizban])
party.initCharacters(VERBOSE)

gm = AIGM(party,VERBOSE)

#############################
### Start the game         ##
#############################

cprint(art,"red")

gm.intro_the_party()


menuoptions = "Move on to next character's turn? \n(y)es, (n)o, (r)oll a d20, (i)nventory (h)p mods"
alive_counter = len(party.characters)


while alive_counter > 0:  # exit if all the adventurers die
    turn_counter += 1
    for character in party.characters: 
        if character.alive : # loop through the living characters
            option = ""
            while option == "n" or option == "":
                option = ""
                
                # print(f"Describe situation to - {character.name}")
                # user_input = input("Enter your text: ")
                user_input, new_tokens = gm.gm_prompts_ai(character, VERBOSE)
                cumulative_tokens + new_tokens

                commandforAI = character.catchUpPromptWithOtherPlayerBuffer(user_input)
                if VERBOSE:
                    print(f"You are telling the AI named {character.name}: ")
                    cprint("\t"+commandforAI,"green")
                player_action, new_tokens = character.ai_move(commandforAI, cumulative_tokens, VERBOSE)
                cumulative_tokens += new_tokens
                
                gm.gm_listens_to_player_action(character, player_action)
                character.speak(player_action)
                
                party.bufferOtherPlayersTurn(character.name, user_input,player_action)

                print(f"As the GM, tell the result of {character.name}'s action after adjusting game state. You can narrate the result when speaking to the next character.")
                option = "y"# endOfTurnOptions(option, character, menuoptions)
            
            ## potentially remove a character from the turn order if they have died
            if character.hp <= 0:
                character.alive = False
                alive_counter -= 1
                print(f"{character.name} has died")

cprint(f"All the characters have died and the adventure has ended.","red")
printEnd(turn_counter, cumulative_tokens)