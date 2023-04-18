
from lib_termutil import cprint
import lib_strutil
from dnd_party import Party, AICharacter
from lib_gameLoop import menuAndInput, endOfTurnOptions




art = """
#############################################
   _____  .___   _______ ___________________  
  /  _  \ |   |  \      \\______   \_   ___ \ 
 /  /_\  \|   |  /   |   \|     ___/    \  \// 
/    |    \   | /    |    \    |   \     \____
\____|__  /___| \____|__  /____|    \______  /
        \/              \/                 \/ 
##############################################
"""

VERBOSE = False
AUTOVOICE = False  ## take voice input
AUTOTEXT = True  ## take text input


helga = AICharacter(
    name="Helga",
    knowledge="you know negotiation is pointless and monsters must be slain. ",
    inventory=["a sword"],
    player_class="You are a warrior and can use items in your inventory but cannot cast spells. ",
    goal_text="Your goal is to explore the dungeon and find the treasure. ",
    text_color="red",
    hp=12,
    voice_name="Tessa",
    voice_speed=200
    )

fizban = AICharacter(
    name="Fizban",
    knowledge="you know clever play is the best way to win this game. ",
    inventory=["a staff"],
    player_class="You are a wizard and and can use items in your invetory and cast spells.",
    goal_text="Your goal is to explore the dungeon and find the treasure. ",
    hp=4,
    voice_name="Reed (English (UK))",
    voice_speed=190
    )

rocko = AICharacter(
    name="Rocko",
    knowledge="you throw caution to the wind and attack any enemy who dares cross your path. ",
    inventory=["a dagger", "lockpicks"],
    player_class="You are a swashbucker and can use items in your inventory but cannot cast spells. ",
    goal_text="Your goal is to explore the dungeon and find the treasure. ",
    text_color="yellow",
    hp=12,
    voice_name="Rocko (English (US))",
    voice_speed=190
    )

party = Party([helga,rocko, fizban])
party.initCharacters(VERBOSE)

# a tracker for LLM tokens spent
cumulative_tokens = 0

#############################
### Start the game         ##
#############################

cprint(art,"red")

for character in party.characters:
    character.speak(f"I have arrived at the A.I Dungeon.") 

## First Character lays it out
firstChar =  party.characters[0]
start = "I am the player and you are the Game Master, "+\
    lib_strutil.oxfordize(firstChar.othercharacters) + " and I are here to play Dungeons and Dragons taking turns. "+\
    "What do I see?"
firstChar.speak(start)

menuoptions = "Move on to next character's turn? \n(y)es, (n)o, (r)oll a d20, (i)nventory (h)p mods"
alive_counter = len(party.characters)
turn_counter = 0;


while alive_counter > 0:
    turn_counter += 1
    for character in party.characters:
        if character.alive :
            option = ""
            while option == "n" or option == "":
                option = ""
                print(f"Describe situation to - {character.name}")
                user_input = input("Enter your text: ")
                commandforAI = character.catchUpPromptWithOtherPlayerBuffer(user_input)
                if VERBOSE:
                    print(f"You are telling the AI named {character.name}: ")
                    cprint("\t"+commandforAI,"green")
                player_action, new_tokens = character.ai_move(commandforAI, cumulative_tokens, VERBOSE)
                cumulative_tokens += new_tokens
                
                character.speak(player_action)
                
                
                # dm_result = input("Enter your text: ")
                party.bufferOtherPlayersTurn(character.name, user_input,player_action)#, dm_result)

                print(f"As the GM, tell the result of {character.name}'s action after adjusting game state. You can narrate the result when speaking to the next character.")
                option = endOfTurnOptions(option, character, menuoptions)
            
            ## potentially remove a character from the turn order if they have died
            if character.hp <= 0:
                character.alive = False
                alive_counter -= 1
                print(f"{character.name} has died")

cprint(f"All the characters have died and the adventure has ended. \nThank you for playing.\nTurns survived {turn_counter}","red")
            
            