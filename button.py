import pygame
import pygame.freetype
from constants import *

class Button:
    def __init__(self, text, position, color, size):
      self.text = text
      self.font = self.get_font(size)
      self.surface, self.rect = self.font.render(text, color)
      self.rect.x = position[0]
      self.rect.y = position[1]
      self.x = position[0]
      self.y = position[1]

    def get_font(self, size):
        try:
            f = pygame.font.get_default_font()
            font = pygame.freetype.SysFont(f, size)
        except:
            font = pygame.freetype.Font(FONTS + "Arial Unicode.ttf", size)   
        return font

    def change_text(self, text):  
        self.surface, self.rect = self.font.render(text)
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = text

    def change_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update_color(self, name,  attribute):        
        x = round((255/100) * attribute)
        if attribute < 50:
            self.surface, self.rect = self.font.render(self.text, (255 - x, 0, 0))
        elif attribute > 50:
            self.surface, self.rect = self.font.render(self.text, (0, x, 0))
