import sys
import os
import math
import pygame
import random
import time
from constants import *
from button import Button
from personality import Personality

"""
This class has one super class ('agent') and two subclasses ('playable' and 'nonplayable').
Each agent object has a personality object.
Agent objects are passed .png images that are loaded as pygame images into two arrays (left-facing and right-facing) upon creation.

Nonplayable agents have a 'state' which determines their behaviour.
There are five states an npc can be in:
	- idle: agent is standing still, not doing anything
        - engaged: agent is either approaching another agent or interacting with another agent.
        - disengaged: agent is moving away from another agent after a negative interaction.
        - leaving: agent is leaving the party.
        - quitting: agent object is being removed from the list owned by the main game object.
"""

class Agent:
    def __init__(self, name, personality, LWalk, LStand,  RWalk, RStand, position, playable):
        self.name = name
        self.LWalk = self.image_list(LWalk, 9)
        self.RWalk = self.image_list(RWalk, 9)
        self.LStand = self.add_image(LStand)
        self.RStand = self.add_image(RStand)
        self.rect = self.LStand.get_rect()
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
        self.extroversion_button = Button("Extroversion: " + str(self.personality.extroversion), (self.rect.x, self.rect.y - 30), BLACK, 12)
        self.positivity_button = Button("Positivity: " + str(self.personality.positivity), (self.rect.x, self.rect.y - 20), BLACK, 12)
        self.mood_button = Button("Mood: " + str(self.personality.mood), (self.rect.x, self.rect.y - 10), BLACK, 12)
        self.temperament_button = Button(self.personality.temperament, (self.rect.x, self.rect.y - 40), WHITE, 12)
        self.buttons.append(self.extroversion_button)
        self.buttons.append(self.positivity_button)
        self.buttons.append(self.mood_button)
        self.buttons.append(self.temperament_button)
        self.playable = playable
        self.item_prox = False
        self.inventory = []
        self.circle = []

    def add_image(self, image):
        path = CHARACTERS + self.name + '/'
        full_path = os.path.join(path + image + ASSET_FILE_TYPE)
        return pygame.image.load(os.path.join(full_path)).convert_alpha()

    def image_list(self, image, loop):
        return_list = []
        for x in range(1, loop):
            return_list.append(self.add_image(image + str(x)))
        return return_list

    def get_mood(self):
        return self.personality.mood

    def get_extroversion(self):
        return self.personality.extroversion

    def get_positivity(self):
        return self.personality.positivity

    def get_mood(self):
        return self.personality.mood

    def item_proximity(self, items):
        for item in items:
            if (self.rect.x in range(item.rect.x - 101, item.rect.x + 101)) and (self.rect.y in range(item.rect.y - 100, item.rect.y + 20)):
                self.item_prox = item
                return item
        return False

    """
    Calculates most proximal agent and updates the agent's 'circle'.
    """

    def calculate_distance(self, agent):
        return math.sqrt(pow(self.rect.x - agent.rect.x, 2) + pow(self.rect.y - agent.rect.y, 2)) 

    def agent_proximity(self, agents):
        self.circle.sort(key=lambda agent: agent.proximity, reverse=False)     

    def update_circle(self, agents):
        for agent in agents:
            proximity = self.calculate_distance(agent) < 100
            if (agent not in self.circle) and proximity and (self is not agent):
                self.circle.append(agent)
                agent.proximity = proximity
            elif agent in self.circle and not proximity:
                self.circle.remove(agent)

    """
    Calculates whether an interaction with another agent is 'positive' or 'negative' according to the agent's positivity trait with a slight influence of the agent's mood.
    """

    def calculate_interaction(self, agent):
        return (self.personality.positivity + (self.personality.mood / 20) + agent.personality.positivity + (agent.personality.mood / 20))/2 > random.randint(1,20)

    """
    An npc agent will interrupt its interaction if its interaction is negative and will disengage (walk away).
    """

    def interact(self):
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
        elif (not self.circle) and (self.xvector == 0) and (self.yvector == 0):
            self.state = "idle"

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

    """
    An agent's likelihood to approach another agent is determined by its extroversion trait.
    """

    def feels_extroverted(self, agent):
        if self == agent:
            return
        if random.randint(1, self.personality.extroversion) > random.randint(1, 500):
            self.state = "engaged"
            self.acquire_targetx(agent.rect.x)
            self.acquire_targety(agent.rect.y)

    def interrupt(self):
        self.state = "disengaged"
        xrand = random.randint(1, 300)
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
