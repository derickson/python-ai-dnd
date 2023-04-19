# from  lib_voice import Voice
# from lib_voice import GVoice
from lib_voice import SVoice
from lib_dice import roll_d20

import lib_strutil

from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks import get_openai_callback
from langchain import PromptTemplate

from lib_termutil import cprint

voice_male = SVoice(name="Fred")

conversation_memory_interaction_length = 2


PRINTMONEYCOUNTER = False

def generateAI():
    return OpenAI(temperature=1)

def tokenToMoneyPrint(new_token_count, textcolor="white"):
    cprint(f'\tCumulative tokens spent: {new_token_count}',textcolor)
    money = new_token_count * 0.015 / 1000.0
    formatted_money = "${:,.2f}".format(money)
    cprint(f'\tThis session so far: {formatted_money}',textcolor)

class Party():
    def __init__(self, characters=[]):
        self.characters = characters
    
    def addCharacter(self, character):
        self.characters.append(character)

    def initCharacters(self, verbose=False):
        for character in self.characters:
            for othercharacter in self.characters:
                if character.name != othercharacter.name:
                    character.othercharacters.append(othercharacter.name)
            character.initAI(verbose)
    
    def bufferOtherPlayersTurn(self, playerName, dm_text, player_response, dm_result=None):
        if dm_result:
            what_happened = f"Human: it's {playerName}'s turn, {dm_text}.\n{playerName}: {player_response}\nHuman:{dm_result}"
        else:
            what_happened = f"Human: it's {playerName}'s turn, {dm_text}.\n{playerName}: {player_response}"
        for character in self.characters:
            if playerName != character.name:
                character.otherPlayerTurnBuffer.append(what_happened)


class GameMaster():
    def __init__(self, party, verbose=False):
        self.party = party

    def intro_the_party(self):
        for character in self.party.characters:
            character.speak(f"I have arrived at the A.I Dungeon.")
            cprint( f"\t Inventory: {lib_strutil.oxfordize(character.inventory)}","white")
            cprint( f"\t Hit Points: {character.hp}","white")

        ## First Character lays it out
        firstChar =  self.party.characters[0]
        if(len(self.party.characters) > 1):
            start = "We are the players and you are the Game Master, "+\
                lib_strutil.oxfordize(firstChar.othercharacters) + " and I are here to play Dungeons and Dragons taking turns. "+\
                "I go first, what do I see?"
        else:
                start = "I am here to play Dungeons and Dragons."+\
                "What do I see?"
        self.gm_listens_to_player_action(firstChar, start)
        firstChar.speak(start)

    def gm_prompts_ai(self, character_to_prompt, verbose=False):
        pass

    def gm_listens_to_player_action(self, character, player_action):
        pass

class HumanGM(GameMaster):
    def gm_prompts_ai(self, character_to_prompt, tokens_so_far, verbose=False):
        print(f"Describe situation to - {character_to_prompt.name}")
        user_input = input("Enter your text: ")
        new_tokens = 0
        return user_input, new_tokens

class AIGM(GameMaster):
    def __init__(self, party, verbose=False):
        super().__init__(party, verbose)
        self.lastCharacterName = None
        self.lastCharacterPrompt = None
        self.voice = SVoice(name="Grandpa (English (UK))",rate=180)
        self.text_color = "green"
        self.name = "the G.M"
        self.initAI(verbose)
    
    def gm_listens_to_player_action(self, character, player_action):
        self.lastCharacterName = character.name
        self.lastCharacterPrompt = player_action
    
    def gm_prompts_ai(self, character_to_prompt, tokens_so_far, verbose=False):
        print("GM:")
        response, new_tokens = self.ai_move(tokens_so_far, verbose)
        cprint(f"\t{response}",self.text_color)
        self.speak(response)
        return response, new_tokens
    
    def speak(self, text):
        self.voice.say(f"This is {self.name}. {text}")

    def genTemplate(self, character_name, success=True):
        #" There is a treasure chest in this dungeon to be discovered. "+\
        #, and then give  a brief description the surroundings and threats to the next player.
        result = "is successful in their attempt" if success else "is unsuccessful and has negative consequences"
        return f"You are {self.name}. You are the Dungeon Master of a D&D game. "+\
                    "You are having a conversation with adventureres exploring a dungeon with many rooms, traps, monsters."+\
                    "Recent conversation:\n{history}\n "+character_name+":{input}\n"+\
                    f"{character_name} {result}. Give a very short narrative description of the results of what {character_name} is attmpting to do \n"+\
                    self.name+": "
        

    def initAI(self, verbose=False):
        llm = generateAI()
        templateGM="This is just temporary {history} {input}"
        self.prompt = PromptTemplate(
            input_variables=["history","input"],
            template=templateGM,
        )

        gmMemory = conversation_memory_interaction_length * len(self.party.characters)
        self.memory = ConversationBufferWindowMemory( k=gmMemory )
        self.conversation = ConversationChain(
            llm=llm, 
            verbose=verbose, 
            memory=self.memory,
            prompt=self.prompt
        )
        self.conversation.memory.ai_prefix=self.name

    def ai_move(self, tokens_so_far, verbose):
        # regenerate the prompt template as items and hp may have changed

        r20 = roll_d20()
        success = r20 > 10
        cprint(f'\tA d20 is rolled. The result is: {r20}',"white")
        self.conversation.prompt.template = self.genTemplate(self.lastCharacterName,success)
        with get_openai_callback() as cb:
            result = self.conversation.run(self.lastCharacterPrompt)
            if verbose or PRINTMONEYCOUNTER:
                textcolor = "white"
                cprint(f'\tThis interaction spent {cb.total_tokens} tokens',textcolor)
                new_token_count  = tokens_so_far + cb.total_tokens
                tokenToMoneyPrint(new_token_count, textcolor)
        return result, cb.total_tokens

class AICharacter():
    def __init__(self, name, knowledge, inventory, class_name,class_abilities, goal_text, voice_name="Fred", text_color="blue", hp=6, voice_speed=200):
        self.name = name
        self.knowledge = knowledge
        self.inventory = inventory
        self.class_name = class_name
        self.class_abilities = class_abilities
        self.goal_text = goal_text
        self.voice = SVoice(name=voice_name,rate=voice_speed)
        self.text_color = text_color
        self.prompt = None
        self.memory = None
        self.conversation = None
        self.othercharacters = []
        self.otherPlayerTurnBuffer = []
        self.hp = hp
        self.alive = True
        
    
    def speak(self, text):
        print(f"{self.name}: ")
        cprint(f"\t{text}", self.text_color)
        self.voice.say(f"This is {self.name}. {text}")

    def genTemplate(self):
        return f"You are {self.name}. You are a player of a D&D game and are in a dungeon. "+\
                    self.knowledge+\
                    f'You are a {self.class_name} and {self.class_abilities}'+\
                    f"{self.goal_text}\n"+\
                    f"Your inventory contains {lib_strutil.oxfordize(self.inventory)} and you have {str(self.hp)} hit points left. "+\
                    "Recent conversation:\n{history}\n Human:{input}\n"+\
                    f"Tell me what {self.name} tries to do next and wait to learn from me what happens. \n"+\
                    self.name+": "

    def initAI(self, verbose=False):
        llm = generateAI()
        templateCharacter=self.genTemplate()
        self.prompt = PromptTemplate(
            input_variables=["history","input"],
            template=templateCharacter,
        )

        # self.memory = ConversationBufferMemory(return_messages=True)
        # self.memory = ConversationBufferMemory()
        self.memory = ConversationBufferWindowMemory( k=conversation_memory_interaction_length )
        self.conversation = ConversationChain(
            llm=llm, 
            verbose=verbose, 
            memory=self.memory,
            prompt=self.prompt
        )
        self.conversation.memory.ai_prefix=self.name
    
    def ai_move(self, new_human_info_since_last_move, tokens_so_far, verbose=False):
        # regenerate the prompt template as items and hp may have changed
        self.conversation.prompt.template = self.genTemplate()
        with get_openai_callback() as cb:
            result = self.conversation.run(new_human_info_since_last_move)
            if verbose or PRINTMONEYCOUNTER:
                textcolor = "white"
                cprint(f'\tThis interaction spent {cb.total_tokens} tokens',textcolor)
                new_token_count  = tokens_so_far + cb.total_tokens
                tokenToMoneyPrint(new_token_count, textcolor)
        return result, cb.total_tokens

    def catchUpPromptWithOtherPlayerBuffer(self, user_input):
        if len(self.otherPlayerTurnBuffer ) != 0:
            commandforAI = "\n".join(self.otherPlayerTurnBuffer)+"\n"+"Human:" +user_input 
        else:
            commandforAI = user_input
        self.otherPlayerTurnBuffer.clear()
        return commandforAI