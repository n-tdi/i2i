"""
  Main file for i2i, a combination of all the other files lying around.
"""

import os
import sys
import time
import bleClient2, speech_naming, take_photo
from speaker_notif import speaker_notif, Lines, added_name
import FaceStuff as fs

addingFace = False
fs.init()

def button1Pressed(button: bleClient2.Button):
    global addingFace
    if addingFace:
        return None
    addingFace = True
    speaker_notif("Please say the name of the person.")
    name = speech_naming.transcribe(3, 2)
    if name == None:
        speaker_notif("No name detected, please try again.")
        return None
    take_photo.takePhoto(name)
    added_name(name)
    addingFace = False

    return None

def say_name(names):
    # will be a function for saying the person's name
    print(names)
    pass
    exit

def button2Pressed(button: bleClient2.Button):
    # TODO: Implement recalling names here @Charlie
    print("Analyzing for faces...")
    while True:
        result, video_frame = fs.video_capture.read()
        print("Took photo")
        if result == False:
            print(result)
            break
        if fs.threading.active_count()<2:
            fs.detect_bounding_box(video_frame)
        if len(fs.foundfaces)>0:
            fs.threading.Thread(None, say_name, "Talk Thread", (fs.foundfaces, )).start()
            fs.foundfaces = []
            break
    return None

bleClient2.buttons.addButton(bleClient2.Button(1, button1Pressed))
bleClient2.buttons.addButton(bleClient2.Button(2, button2Pressed))

bleClient2.startClient()