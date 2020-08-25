import os
import pygame
from constants import *
from button import *

class Item:
    def __init__(self, name, position):
        self.name = name
        path = os.path.join(ITEMS + name)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.button = Button("F", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
