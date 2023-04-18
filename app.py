
from lib_termutil import cprint
import lib_strutil
from dnd_party import Party, AICharacter, tokenToMoneyPrint
from lib_gameLoop import menuAndInput, endOfTurnOptions




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

# a tracker for LLM tokens spent
cumulative_tokens = 0

#############################
### Start the game         ##
#############################

cprint(art,"red")

for character in party.characters:
    character.speak(f"I have arrived at the A.I Dungeon.")
    cprint( f"\t Inventory: {lib_strutil.oxfordize(character.inventory)}","white")
    cprint( f"\t Hit Points: {character.hp}","white")

## First Character lays it out
firstChar =  party.characters[0]
if(len(party.characters) > 1):
    start = "We are the players and you are the Game Master, "+\
        lib_strutil.oxfordize(firstChar.othercharacters) + " and I are here to play Dungeons and Dragons taking turns. "+\
        "I go first, what do I see?"
else:
        start = "I am here to play Dungeons and Dragons."+\
        "What do I see?"
firstChar.speak(start)

menuoptions = "Move on to next character's turn? \n(y)es, (n)o, (r)oll a d20, (i)nventory (h)p mods"
alive_counter = len(party.characters)
turn_counter = 0;


while alive_counter > 0:  # exit if all the adventurers die
    turn_counter += 1
    for character in party.characters: 
        if character.alive : # loop through the living characters
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
                
                party.bufferOtherPlayersTurn(character.name, user_input,player_action)

                print(f"As the GM, tell the result of {character.name}'s action after adjusting game state. You can narrate the result when speaking to the next character.")
                option = endOfTurnOptions(option, character, menuoptions)
            
            ## potentially remove a character from the turn order if they have died
            if character.hp <= 0:
                character.alive = False
                alive_counter -= 1
                print(f"{character.name} has died")

cprint(f"All the characters have died and the adventure has ended.","red")
cprint(f"Thank you for playing.","red")
cprint(f"Turns survived {turn_counter}","red")
tokenToMoneyPrint(cumulative_tokens)
            