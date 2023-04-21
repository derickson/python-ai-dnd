
import platform

if platform.system() == 'Windows':

    from colorama import init, Fore, Back, Style

    init()

    def color2Code(color):
        c = color.lower()
        if(c == 'white'):
            return Fore.WHITE
        elif(c == 'red'):
            return Fore.RED
        elif(c == 'blue'):
            return Fore.BLUE
        elif(c == 'yellow'):
            return Fore.YELLOW
        elif(c == 'green'):
            return Fore.GREEN
        else:
            return Fore.WHITE

    def cprint(text, color):
        code = color2Code(color)
        print(code + text + Style.RESET_ALL)


else:

    from termcolor import colored

    ## color text printer
    def cprint(text, color):
        print(colored(text, color))


