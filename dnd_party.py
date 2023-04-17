from  lib_voice import Voice
from lib_voice import GVoice
from lib_voice import SVoice

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

PRINTMONEYCOUNTER = True

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
    
    def bufferOtherPlayersTurn(self, playerName, dm_text, player_response, dm_result):
        what_happened = f"Human: it's {playerName}'s turn, {dm_text}.\n{playerName}: {player_response}\nHuman:{dm_result}"
        for character in self.characters:
            if playerName != character.name:
                character.otherPlayerTurnBuffer.append(what_happened)


class AICharacter():
    def __init__(self, name, knowledge, inventory, player_class, goal_text, voice_name="Fred", text_color="blue", hp=6, voice_speed=200):
        self.name = name
        self.knowledge = knowledge
        self.inventory = inventory
        self.player_class = player_class
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
                    self.player_class+\
                    f"{self.goal_text}\n"+\
                    f"Your inventory contains {lib_strutil.oxfordize(self.inventory)} and you have {str(self.hp)} hit points left. "+\
                    "Recent conversation:\n{history}\n Human:{input}\n"+\
                    f"Tell me what {self.name} tries to do next and wait to learn from me what happens. \n"+\
                    self.name+": "

    def initAI(self, verbose=False):
        llm = OpenAI(temperature=1)
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
        self.conversation.prompt.template = self.genTemplate()
        with get_openai_callback() as cb:
            result = self.conversation.run(new_human_info_since_last_move)
            if verbose or PRINTMONEYCOUNTER:
                textcolor = "white"
                cprint(f'\ttokens so far: {tokens_so_far}',textcolor)
                cprint(f'\tSpent a total of {cb.total_tokens} tokens',textcolor)
                new_token_count  = tokens_so_far + cb.total_tokens
                cprint(f'\tcumulative tokens: {new_token_count}',textcolor)
                money = new_token_count * 0.015 / 1000.0
                formatted_money = "${:,.2f}".format(money)
                cprint(f'\t{formatted_money}',textcolor)
        return result, cb.total_tokens

    def catchUpPromptWithOtherPlayerBuffer(self, user_input):
        if len(self.otherPlayerTurnBuffer ) != 0:
            commandforAI = "\n".join(self.otherPlayerTurnBuffer)+"\n"+"Human:" +user_input 
        else:
            commandforAI = user_input
        self.otherPlayerTurnBuffer.clear()
        return commandforAI