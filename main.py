"""
  Main file for i2i, a combination of all the other files lying around.
"""

import os
import sys
import time
import bleClient2

def button1Pressed(button: bleClient2.Button):
    print("Button 1 pressed " + str(button.id))
    return None

def button2Pressed(button: bleClient2.Button):
    print("Button 2 pressed " + str(button.id))
    return None

bleClient2.buttons.addButton(bleClient2.Button(1, button1Pressed))
bleClient2.buttons.addButton(bleClient2.Button(2, button2Pressed))

bleClient2.startClient()