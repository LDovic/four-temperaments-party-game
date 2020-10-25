import pygame
import pygame.freetype
from constants import *

"""
Pygame 'buttons' are objects used for displaying text on screen. All in-game text are button objects that some class (for example, an agent or a screen) has.
"""

class Button:
    def __init__(self, text, position, color, size, name = None):
      self.name = name
      self.text = text
      self.font = self.get_font(size)
      self.surface, self.rect = self.font.render(text, color)
      self.rect.x = position[0]
      self.rect.y = position[1]
      self.x = position[0]
      self.y = position[1]
      self.color = color

    def get_font(self, size):
        try:
            f = pygame.font.get_default_font()
            font = pygame.freetype.SysFont(f, size)
        except:
            font = pygame.freetype.Font(FONTS + "Arial Unicode.ttf", size)   
        return font

    def change_text(self, text):  
        self.surface, self.rect = self.font.render(text, self.color)
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = text

    def change_position_xy(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def change_position_centerxy(self, x, y):
        self.rect.centerx = x
        self.rect.cetnery = y        

    def change_color(self, color):
        self.surface, self.rect = self.font.render(self.text, color)

    def update_color(self, name,  attribute):        
        x = round((255/100) * attribute)
        self.surface, self.rect = self.font.render(self.text, (255 - x, x, 0))
