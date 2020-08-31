import sys
import os
import math
import pygame
import random
import time
from constants import *
from button import Button
from personality import Personality

class Agent:
    def __init__(self, name, personality, LSprites, Lstand,  RSprites, Rstand, position, playable):
        self.name = name
        self.Limages = []
        self.Rimages = []
        path = CHARACTERS + self.name + '/'
        for x in range(1, 9):
            Lpath = os.path.join(path + LSprites + str(x) + ASSET_FILE_TYPE)
            Rpath = os.path.join(path + RSprites + str(x) + ASSET_FILE_TYPE)
            self.Limages.append(pygame.image.load(Lpath).convert_alpha())
            self.Rimages.append(pygame.image.load(Rpath).convert_alpha())
        Rpath = os.path.join(path + Rstand) + ASSET_FILE_TYPE 
        self.Rstand = pygame.image.load(Rpath).convert_alpha()
        Lpath = os.path.join(path + Lstand) + ASSET_FILE_TYPE
        self.Lstand = pygame.image.load(Lpath).convert_alpha()
        self.rect = self.Lstand.get_rect()
        self.facing_right = True
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.xvector = 0
        self.yvector = 0
        self.personality = personality 
        self.targetx = self.rect.x
        self.targety = self.rect.y
        self.state = "idle"
        self.buttons = []
        self.extroversion_button = Button("Extroversion: " + str(self.personality.extroversion), (self.rect.x, self.rect.y - 30), (0, 0, 0), 12)
        self.positivity_button = Button("Positivity: " + str(self.personality.positivity), (self.rect.x, self.rect.y - 20), (0, 0, 0), 12)
        self.mood_button = Button("Mood: " + str(self.personality.mood), (self.rect.x, self.rect.y - 10), (0, 0, 0), 12)
        self.buttons.append(self.extroversion_button)
        self.buttons.append(self.positivity_button)
        self.buttons.append(self.mood_button)
        self.playable = playable
        self.item_prox = False
        self.inventory = []
        self.circle = []

    def get_mood(self):
        return self.personality.mood

    def get_extroversion(self):
        return self.personality.extroversion

    def get_positivity(self):
        return self.personality.positivity

    def item_proximity(self, items):
        for item in items:
            if (self.rect.x in range(item.rect.x - 101, item.rect.x + 101)) and (self.rect.y in range(item.rect.y - 20, item.rect.y + 20)):
                self.item_prox = item
                return item
        return False

    def calculate_distance(self, agent):
        return math.sqrt(pow(self.rect.x - agent.rect.x, 2) + pow(self.rect.y - agent.rect.y, 2)) 

    def agent_proximity(self, agents):
        self.circle.sort(key=lambda agent: agent.proximity, reverse=False)     

    def update_circle(self, agents):
        for agent in agents:
            proximity = self.calculate_distance(agent) < 100
#            proximity = self.rect.x in range(agent.rect.x - 101, agent.rect.x + 101)
            if (agent not in self.circle) and proximity and (self is not agent):
                self.circle.append(agent)
                agent.proximity = proximity
            elif agent in self.circle and not proximity:
                self.circle.remove(agent)

    def calculate_interaction(self, agent):
        return (self.personality.positivity + (self.personality.mood / 20) + agent.personality.positivity + (agent.personality.mood / 20))/2 > random.randint(1,20)

    def interact(self, agents):
        if self.circle:
            for agent in self.circle:
                if self.calculate_interaction(agent) is False:
                    self.personality.update_mood(False, 5)
                    self.circle[0].personality.update_mood(False, 5)
                    if self.playable == False:
                        self.interrupt()
                    return
                self.personality.update_mood(True, 5)
                self.circle[0].personality.update_mood(True, 5)

    def change_side(self, facing_right):
        self.facing_right = facing_right

    def change_vector(self, vector, xy):
        if xy == 0:
            self.xvector = vector
        if xy == 1:
            self.yvector = vector

    def yboundaries(self):
        if self.rect.y < FLOOR_HEIGHT:
            self.yvector = 0
            self.rect.y = 400
        if self.rect.y > SCREEN_HEIGHT - 200:
            self.yvector = 0
            self.rect.y = SCREEN_HEIGHT - 200

    def xboundaries(self):
        if self.rect.x < 0:
            self.xvector = 0 
            self.rect.x = 0 
        if self.rect.x > SCREEN_WIDTH - 100:
            self.xvector = 0 
            self.rect.x = SCREEN_WIDTH - 100 

    def xmove(self):
        self.rect.x += self.xvector
        self.xboundaries()

    def ymove(self):
        self.rect.y += self.yvector
        self.yboundaries()

    def update_button_colors(self):
        self.personality.mood_button.update_color(self.personality.mood) 

class NonPlayableAgent(Agent):
    def __init__(self, name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable):
        super().__init__(name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable)

    def set_state(self):
        if (self.personality.mood == 0) and (self.state != "leaving") and (self.state != "quitting"):
            self.leave()
        elif ((self.xvector == 0) and (self.yvector == 0) and (self.state != "engaged") and (self.state != "leaving") and (self.state != "quitting")):
            self.state = "idle"

    def feels_extroverted(self, agent):
        if random.randint(1, self.personality.extroversion) > random.randint(1, 500):
            self.state = "engaged"
            self.acquire_targetx(agent.rect.x)
            self.acquire_targety(agent.rect.y)

    def interrupt(self):
        self.state = "disengaged"
        self.interrupted = True
        xrand = random.randint(1, 500)
        yrand = random.randint(FLOOR_HEIGHT, SCREEN_HEIGHT)
        target_x = self.rect.x - xrand if self.facing_right else self.rect.x + xrand
        target_y = self.rect.y - yrand if self.rect.y > (FLOOR_HEIGHT + 50) else self.rect.y + yrand 
        self.acquire_targetx(target_x)
        self.acquire_targety(target_y)

    def acquire_targetx(self, target_x):
        self.targetx = target_x
        if self.targetx > self.rect.x:
            self.change_vector(5, 0)
            self.change_side(True)
        if self.targetx < self.rect.x:
            self.change_vector(-5, 0)
            self.change_side(False)

    def acquire_targety(self, target_y):
        self.targety = target_y
        if self.targety > self.rect.y:
            self.change_vector(5, 1)
        if self.targety < self.rect.y:
            self.change_vector(-5, 1)    

    def stop(self):
        xdistance = self.rect.x - self.targetx
        if (xdistance in range(-90, -110)) or (xdistance in range(90, 110)):
            self.change_vector(0, 0)
            self.targetx = self.rect.x
        ydistance = self.rect.y - self.targety
        if (ydistance in range(-90, -110)) or (ydistance in range(90, 110)):
            self.change_vector(0, 1)
            self.targety = self.rect.y

    def leave(self):
        self.state = "leaving"
        self.change_vector(0, 1)
        self.acquire_targetx(-100 if self.facing_right else SCREEN_WIDTH + 100)

    def quit(self):
       if self.xvector == 0:
           self.state = "quitting"

class PlayableAgent(Agent):
    def __init__(self, name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable):
        super().__init__(name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable)

    def take_item(self):
        if self.item_prox is not False:
            self.inventory.append(self.item_prox)
            return self.item_prox
            self.item_prox = False
        return False
