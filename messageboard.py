import pygame
from constants import *
from button import *

"""
This class creates a message board object.
"""

class MessageBoard:
    def __init__(self):
        self.buttons = []
        self.base_y_position = SCREEN_HEIGHT - 25

    def scroll_buttons(self):
        for button in list(reversed(self.buttons)):
            button.change_position_xy(button.rect.x, button.rect.y - 20)

    def add_button(self, text):
        if text not in (b.text for b in self.buttons):
            button = Button(text, (20, self.base_y_position), WHITE, BUTTON_FONT_SIZE)
            if self.buttons:
                self.scroll_buttons()
            self.buttons.append(button)        

    def leaving(self, name):
        self.add_button(name + " is leaving!")
