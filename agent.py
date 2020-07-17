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
        self.rect.y = 300
        self.vector = 0
        self.personality = Personality(positivity)
        self.target = self.rect.x
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
            if proximity and (self is not agent) and (self.vector == 0):                
                self.engaged = True
                interaction = (self.personality.positivity + (self.personality.mood / 10) + agent.personality.positivity + (agent.personality.mood / 10))/2 > random.randint(1,20)
                if (self.personality.update_mood(interaction, 5) is False) and (self.playable is False):
                    self.interrupt()
                agent.personality.update_mood(interaction, 5)

    def change_side(self, facing_right):
        self.facing_right = facing_right

    def change_vector(self, vector):
        self.vector = vector

    def move(self):
        self.rect.x += self.vector
        if self.leaving is False:
            if self.rect.x < 0:
                self.vector = 0
                self.rect.x = 0
            if self.rect.x > SCREEN_WIDTH - 100:
                self.vector = 0
                self.rect.x = SCREEN_WIDTH - 100

    def update_button_colors(self):
        self.personality.mood_button.update_color(self.personality.mood) 

class NonPlayableAgent(Agent):
    def __init__(self, name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable):
        super().__init__(name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable)

    def feels_extroverted(self):
        return random.randint(1, self.personality.extroversion) > random.randint(1, 500)

    def interrupt(self):
        self.engaged = False
        target_x_value = self.rect.x - 500 if self.facing_right else self.rect.x + 500
        self.acquire_target(target_x_value)

    def acquire_target(self, target_x_value):
        self.target = target_x_value
        if self.target > self.rect.x:
            self.change_vector(5)
            self.change_side(True)
        if self.target < self.rect.x:
            self.change_vector(-5)
            self.change_side(False)
    
    def stop(self):
        distance = self.rect.x - self.target
        if (distance in range(-90, -110)) or (distance in range(90, 110)):
            self.change_vector(0)
            self.target = self.rect.x

    def leave(self):
         if self.get_mood() == 0:
#        if self.personality.mood < ((self.personality.positivity * 10) / 2): 
            self.acquire_target(-100 if self.facing_right else SCREEN_WIDTH + 100)
            self.leaving = True

    def quit(self):
       if self.vector == 0:
           self.quitting = True

class PlayableAgent(Agent):
    def __init__(self, name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable):
        super().__init__(name, LSprites, Lstand,  RSprites, Rstand, position, positivity, playable)
