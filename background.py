import pygame
from constants import *
import os

"""
This class creates a background object based the files in the background folder.
"""

class Background:
    def __init__(self, name, position):
        self.name = name
        path = os.path.join(BACKGROUND + self.name)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = position[1]
