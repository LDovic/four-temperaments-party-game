import pygame
import random
from constants import *
from button import *

"""
This class creates a message board object.
"""

class MessageBoard:
    def __init__(self):
        self.buttons = []
        self.button_y_limit = SCREEN_HEIGHT - 25 - (20 * 1)
        self.base_y_position = SCREEN_HEIGHT - 25
        self.good_party_list = ["This party is rockin'!", "Everyone's having a good time!", "This party is going well!", "The neighbours are complaining about the noise!", "God has blessed this party!", "There are some seriously weird vibes going around!", "People are letting loose and being themselves!", "People have forgotten that they have to go to work on Monday!"]

    def scroll_buttons(self):
        for button in list(reversed(self.buttons)):
            if button.rect.y == self.button_y_limit:
                self.buttons.pop(0)
            button.change_position_xy(button.rect.x, button.rect.y - 20)

    def add_button(self, text, color, name):
        if name not in (b.name for b in self.buttons):
            button = Button(text, (20, self.base_y_position), color, BUTTON_FONT_SIZE, name)
            if self.buttons:
                if len(self.buttons) > 1:
                    self.buttons.pop(0)
                self.scroll_buttons()
            self.buttons.append(button)        

    def good_party(self):
        self.add_button(random.choice(self.good_party_list), GREEN, "Good Party")

    def low_mood(self, name):
        self.add_button(name + " is in a bad mood!", YELLOW, name + " Low Mood")

    def leaving(self, name):
        self.add_button(name + " is leaving!", RED, name + " Leaving")

    def quitting(self, name):
        self.add_button(name + " has left!", RED, name + "Quitting")
