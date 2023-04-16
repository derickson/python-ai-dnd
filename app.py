import pyttsx3
import speech_recognition as sr
import getch

from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from langchain import PromptTemplate

from termcolor import colored

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
PRINTMONEYCOUNTER = False
AUTOVOICE = False  ## take voice input
AUTOTEXT = True  ## take text input

## color text printer
def cprint(text, color):
    print(colored(text, color))

# Voice Recognition
r = sr.Recognizer()
def listen():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "UNKNOWN"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "UNKNOWN"


# Text to Voice Engine
engine = pyttsx3.init()


llm = OpenAI(temperature=1)

inventory = "a sword and a rope"
templateAggressive="You are an aggressive player of a D&D game. "+\
             "You are a warrior and can use items in your inventory but cannot cast spells. "+\
             f"Your inventory starts with {inventory}. "+\
             "Your goal is to explore the dungeon and find the treasure. \n"+\
             "Current conversation:\n{history}\n Human:{input}\n"+\
             "Tell me what your character tries to do next and wait to learn from me what happens. \n"+\
             "AI: "
prompt = PromptTemplate(
    input_variables=["history","input"],
    template=templateAggressive,
)

memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(
    llm=llm, 
    verbose=VERBOSE, 
    memory=ConversationBufferMemory(),
    prompt=prompt
)

cumulative_tokens = 1
def count_tokens(chain, query, tokens_so_far):
    with get_openai_callback() as cb:
        result = chain.run(query)
        if VERBOSE or PRINTMONEYCOUNTER:
            cprint(f'\ttokens so far: {tokens_so_far}',"white")
            cprint(f'\tSpent a total of {cb.total_tokens} tokens',"white")
            new_token_count  = tokens_so_far + cb.total_tokens
            cprint(f'\tcumulative tokens: {new_token_count}',"white")
            money = new_token_count * 0.015 / 1000.0
            formatted_money = "${:,.2f}".format(money)
            cprint(f'\t{formatted_money}',"white")
    return result, cb.total_tokens



# Define a function to speak text
def speak(text):
    print("The Response: ")
    cprint(text, "blue")
    engine.say(text)
    engine.runAndWait()



#############################
### Start the game         ##
#############################

cprint(art,"red")
speak("Hello and welcome to the AI Dungeon")
speak("I am an AI warrior and you are the Game Master, Let's Play Dungeons and Dragons. What do I see?")

instructions = "Enter an option (\n\t1 for text prompt, \n\t2 voice prompt): "
while True:
    if AUTOVOICE:
        option = "2"
    elif AUTOTEXT:
        option = "1"
    else:
        print(instructions)
        option = getch.getch()


    if option == "1":  ## take text input and send to AI
        print("What to tell the AI?")
        
        user_input = input("Enter your text: ")
            
        commandforAI = user_input
        if VERBOSE:
            print("You are telling the AI: ")
            cprint("\t"+commandforAI,"green")
        result, new_tokens = count_tokens(conversation, commandforAI, cumulative_tokens)
        cumulative_tokens += new_tokens
        # print(result)
        speak(result)

    elif option == "2":  ## voice input
        takingInput = True
        while takingInput:
            print("What to tell the AI?")
            user_input  = listen()
            print("You typed: ", user_input)
            send = getch.getch("send to AI? Y/N: ")
            if send.lower() == "y":
                takingInput = False
        commandforAI = user_input
        if VERBOSE:
            print("You are telling the AI: ")
            cprint("\t"+commandforAI,"green")
        result, new_tokens = count_tokens(conversation, commandforAI, cumulative_tokens)
        cumulative_tokens += new_tokens
        # print(result)
        speak(result)
    else:
        print("Invalid option. Please try again.")
        continue