# import pyttsx3
# from gtts import gTTS
import subprocess
import os


# class Voice():
#     def __init__(self):
#         self.v = pyttsx3.init()

#     def say(self,text):
#         self.v.say(text)
#         self.v.runAndWait()


# class GVoice():
#     def __init__(self, speed=1.0):
#         self.speed = speed
    
#     def say(self,text):
#         tts = gTTS(text, speed=self.speed)
#         tts.save('temp.mp3')
#         subprocess.call(["afplay","temp.mp3"])

## only works on a mac
class SVoice():
    def __init__(self,name="Fred",rate=200):
        self.name = name
        self.rate = str(rate)
    
    def say(self,text):
        subprocess.call(["say","-v",self.name,"-r",self.rate,".  "+text])
