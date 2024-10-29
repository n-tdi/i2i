# from playaudio import playaudio
from enum import Enum
import pyttsx3

class Lines(Enum):
    SAY_NAME_OF_PERSON = "Please say the name of the person."
    NO_NAME_DETECTED = "No name detected, please try again."
    ADDED_FACE = "Successfully added face "

# Initialize the converter
engine = pyttsx3.init()

def speaker_notif(line: Lines):
    engine.say(line.value)
    engine.runAndWait()

def say_name(name):
    engine.say("Added face " + name)
    engine.runAndWait()

def speaker_notif(text: str):
    engine.say(text)
    engine.runAndWait()

