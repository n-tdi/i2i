# from playaudio import playaudio
from enum import Enum
import pyttsx3

class Lines(Enum):
    SAY_NAME_OF_PERSON = "audio/say_name_of_person.wav"
    NO_NAME_DETECTED = "audio/no_name_detected.wav"
    ADDED_FACE = "audio/face_added.wav"

# Initialize the converter
engine = pyttsx3.init()

def speaker_notif(text: str):
    engine.say(text)
    engine.runAndWait()

speaker_notif("Hello, world!")


