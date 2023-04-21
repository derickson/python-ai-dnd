import platform

if platform.system() == 'Windows':

    import pyttsx3

    class SVoice():
        def __init__(self, name="Fred", rate=200):
            self.v = pyttsx3.init()
            self.name = name
            self.rate = rate

        def say(self,text):
            self.v.say(text)
            self.v.runAndWait()

else: 
    import subprocess
    import os

    ## only works on a mac
    class SVoice():
        def __init__(self,name="Fred",rate=200):
            self.name = name
            self.rate = str(rate)
        
        def say(self,text):
            subprocess.call(["say","-v",self.name,"-r",self.rate,".  "+text])
