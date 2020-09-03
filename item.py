import os
import pygame
from constants import *
from button import *

"""
ItemFactory is in the factory design pattern. It is created by the game object and used to return an item object, which is the super class of which all particular items are subclasses.
Division of items into particular subclasses allows the effects of items to be fine tuned.
"""

class ItemFactory():
    def factory(name):
        if name == 'WhiskeyBottle':
            return WhiskeyBottle(name)
        elif name == 'RedStripe':
            return RedStripe2(name)
        elif name == 'RedStripe2':
            return RedStripe3(name)
        elif name == 'RedStripe3':
            return RedStripe(name)
        elif name == 'MysteriousWhitePowder':
            return MysteriousWhitePowder(name)
        elif name == 'Apple':
            return Apple(name)
        elif name == 'StickOfRock':
            return StickOfRock(name)
        elif name == 'CrabSticks':
            return CrabSticks(name)
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
        agent.personality.get_drunk(4)

class RedStripe(Item):
    def __init__(self, name):
        super().__init__(name)
        self.rect.x = 600
        self.rect.y = 430
        self.take = Button("Take red stripe (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
        self.give = Button("Give red stripe (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)

    def apply_item(self, agent):
        agent.personality.get_drunk(2)

class RedStripe2(Item):
    def __init__(self, name):
        super().__init__(name)
        self.rect.x = 550
        self.rect.y = 430
        self.take = Button("Take red stripe (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
        self.give = Button("Give red stripe (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)

    def apply_item(self, agent):
        agent.personality.get_drunk(2)

class RedStripe3(Item):
    def __init__(self, name):
        super().__init__(name)
        self.rect.x = 500
        self.rect.y = 430
        self.take = Button("Take red stripe (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
        self.give = Button("Give red stripe (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)

    def apply_item(self, agent):
        agent.personality.get_drunk(2)

class MysteriousWhitePowder(Item):
    def __init__(self, name):
        super().__init__(name)
        self.rect.x = 1200
        self.rect.y = 390
        self.take = Button("Take mysterious white powder (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
        self.give = Button("Give mysterious white powder (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)

    def apply_item(self, agent):
        agent.personality.get_magical()

class Apple(Item):
    def __init__(self, name):
        super().__init__(name)
        self.rect.x = 1150
        self.rect.y = 430
        self.take = Button("Take apple (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
        self.give = Button("Give apple (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)

    def apply_item(self, agent):
        agent.personality.eat(10)

class StickOfRock(Item):
    def __init__(self, name):
        super().__init__(name)
        self.rect.x = 240
        self.rect.y = 530
        self.take = Button("Take stick of rock (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
        self.give = Button("Give stick of rock (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)

    def apply_item(self, agent):
        agent.personality.eat(20)

class CrabSticks(Item):
    def __init__(self, name):
        super().__init__(name)
        self.rect.x = 1250
        self.rect.y = 550
        self.take = Button("Take crabsticks (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)
        self.give = Button("Give crabsticks (F)", (self.rect.x, self.rect.y), RED, BUTTON_FONT_SIZE)

    def apply_item(self, agent):
        agent.personality.eat(50)
