import os
import pygame
from constants import *
from button import *

class ItemFactory():
    def factory(name):
        if name == 'WhiskeyBottle':
            return WhiskeyBottle(name)
        elif name == 'RedStripe':
            return RedStripe(name)
        else:
            raise ValueError(name)

class Item():
    def __init__(self, name):
        self.name = name
        path = os.path.join(ITEMS + name + '/' + name + ASSET_FILE_TYPE)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()

class WhiskeyBottle(Item):
    def __init__(self, name):
        super().__init__(name)
        self.rect.x = 400
        self.rect.y = 390
        self.take = Button("Take whiskey (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
        self.give = Button("Give whiskey (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)

    def apply_item(self, agent):
        agent.personality.get_drunk(3)

class RedStripe(Item):
    def __init__(self, name):
        super().__init__(name)
        self.rect.x = 600
        self.rect.y = 390
        self.take = Button("Take red stripe (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
        self.give = Button("Give red stripe (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)

    def apply_item(self, agent):
        agent.personality.get_drunk(2)
