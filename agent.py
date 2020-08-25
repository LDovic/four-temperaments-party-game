import sys
import os
import pygame
import random
import time
from constants import *
from button import Button
from personality import Personality

class Agent:
    def __init__(self, name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable):
        self.name = name
        self.Limages = []
        self.Rimages = []
        path = 'assets/' + self.name + '/'
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
        self.personality = Personality(positivity)
        self.targetx = self.rect.x
        self.targety = self.rect.y
        self.engaged = False
        self.leaving = False
        self.quitting = False
        self.buttons = []
        self.extroversion_button = Button("Extroversion: " + str(self.personality.extroversion), (self.rect.x, self.rect.y - 30), (0, 0, 0), 12)
        self.positivity_button = Button("Positivity: " + str(self.personality.positivity), (self.rect.x, self.rect.y - 20), (0, 0, 0), 12)
        self.mood_button = Button("Mood: " + str(self.personality.mood), (self.rect.x, self.rect.y - 10), (0, 0, 0), 12)
        self.buttons.append(self.extroversion_button)
        self.buttons.append(self.positivity_button)
        self.buttons.append(self.mood_button)
        self.playable = playable

    def get_mood(self):
        return self.personality.mood

    def get_extroversion(self):
        return self.personality.extroversion

    def get_positivity(self):
        return self.personality.positivity

    def music(self, genre):
        switcher = {
            "Metal": self.personality.metal,
            "Hip Hop": self.personality.hiphop,
            "Pop": self.personality.pop,
            "Classical": self.personality.classical
        }
        switch_genre = switcher.get(genre, False) 
        switch_genre() if switch_genre else self.no_music()

    def interact(self, agents):
        for agent in agents:
            proximity = self.rect.x in range(agent.rect.x - 101, agent.rect.x + 101)
            if proximity and (self is not agent) and (self.xvector == 0):                 
                self.engaged = True
                interaction = (self.personality.positivity + (self.personality.mood / 10) + agent.personality.positivity + (agent.personality.mood / 10))/2 > random.randint(1,20)
                if (self.personality.update_mood(interaction, 5) is False) and (self.playable is False):
                    self.interrupt()
                agent.personality.update_mood(interaction, 5)

    def change_side(self, facing_right):
        self.facing_right = facing_right

    def change_vector(self, vector, xy):
        if xy == 0:
            self.xvector = vector
        if xy == 1:
            self.yvector = vector

    def move(self):
        self.rect.x += self.xvector
        self.rect.y += self.yvector
        if self.leaving is False:
            if self.rect.x < 0:
                self.xvector = 0
                self.rect.x = 0
            if self.rect.x > SCREEN_WIDTH - 100:
                self.xvector = 0
                self.rect.x = SCREEN_WIDTH - 100
            if self.rect.y < FLOOR_HEIGHT:
                self.yvector = 0
                self.rect.y = 400
            if self.rect.y > SCREEN_HEIGHT - 200:
                self.yvector = 0
                self.rect.y = SCREEN_HEIGHT - 200

    def update_button_colors(self):
        self.personality.mood_button.update_color(self.personality.mood) 

class NonPlayableAgent(Agent):
    def __init__(self, name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable):
        super().__init__(name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable)

    def feels_extroverted(self):
        return random.randint(1, self.personality.extroversion) > random.randint(1, 500)

    def interrupt(self):
        self.engaged = False
        xrand = random.randint(1, 500)
        yrand = random.randint(FLOOR_HEIGHT, SCREEN_HEIGHT)
        target_x = self.rect.x - xrand if self.facing_right else self.rect.x + xrand
        target_y = self.rect.y - yrand if self.rect.y > (FLOOR_HEIGHT + 50) else self.rect.y + yrand 
        self.acquire_target(target_x, target_y)

    def acquire_target(self, target_x, target_y):
        self.targetx = target_x
        self.targety = target_y
        if self.targetx > self.rect.x:
            self.change_vector(5, 0)
            self.change_side(True)
        if self.targetx < self.rect.x:
            self.change_vector(-5, 0)
            self.change_side(False)
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
         if self.get_mood() == 0:
#        if self.personality.mood < ((self.personality.positivity * 10) / 2): 
            self.acquire_target(-100 if self.facing_right else SCREEN_WIDTH + 100, self.rect.y)
            self.leaving = True

    def quit(self):
       if self.xvector == 0:
           self.quitting = True

class PlayableAgent(Agent):
    def __init__(self, name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable):
        super().__init__(name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable)
