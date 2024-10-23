"""
  Main file for i2i, a combination of all the other files lying around.
"""

import os
import sys
import time
import bleClient2, speech_naming, take_photo

addingFace = False

def button1Pressed(button: bleClient2.Button):
    global addingFace
    if addingFace:
        return None
    addingFace = True
    print("Adding face")
    print("Say the name of the person")
    name = speech_naming.transcribe(3, 3)
    if name == None:
        print("No name detected")
        return None
    print("Name detected: " + name)
    take_photo.takePhoto(name)
    print("Face added")
    addingFace = False

    return None

def button2Pressed(button: bleClient2.Button):
    # TODO: Implement recalling names here @Charlie
    return None

bleClient2.buttons.addButton(bleClient2.Button(1, button1Pressed))
bleClient2.buttons.addButton(bleClient2.Button(2, button2Pressed))

bleClient2.startClient()