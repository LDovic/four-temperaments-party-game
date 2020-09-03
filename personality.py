import pygame
import random

"""
The PersonalityFactory class uses the factory design pattern. It is created by the game object and returns a subclass personality object of the superclass personality object.

Personality objects allow each personality type (of the four temperaments) to react differently to different stimuli (for example, music or consumables).

Every agent object has a personality object.

The personality object has three important attributes: extroversion, positivity and mood. Extroversion and positivity are the two axes on which Hippocratic personality types are modelled. The agent's mood is first determined by their positivity value * 100 and then changes according to in game interactions.
Mood is arguably the most relevant attribute, as when it reaches 0 the agent leaves the game. This is an important dynamic in determining whether the player wins or loses.

Another important aspect to the regulation of mood is the 'circadian rhythm' functions. If there is no music playing, then the agent's mood will return to its base value, which is the agent's positivity value * 100. This is arguably a superfluous feature since the player is likely to always have music playing but is adds an extra level of variation to the game, preventing agents getting 'stuck' on one mood level.
"""

class PersonalityFactory():
    def calculate_temperament(self):
        extroversion = random.randint(1,10)
        positivity = random.randint(1,10)
        if extroversion >= 5:
            temperament = "Sanguine"
            if positivity <= 5:
                temperament = "Choleric"
        else:
            temperament = "Phlegmatic"
            if positivity <= 5:
                temperament = "Melancholic"
        return temperament, extroversion, positivity

    def factory(self):
        temperament, extroversion, positivity = self.calculate_temperament()
        if temperament == 'Sanguine':
            return Sanguine(temperament, extroversion, positivity)
        elif temperament == 'Choleric':
            return Choleric(temperament, extroversion, positivity)
        elif temperament == 'Phlegmatic':
            return Phlegmatic(temperament, extroversion, positivity)
        elif temperament == 'Melancholic':
            return Melancholic(temperament, extroversion, positivity)
        else:
            raise ValueError(temperament)

class Personality:
    def __init__(self, temperament, extroversion, positivity):
        self.temperament = temperament
        self.extroversion = extroversion
        self.positivity = positivity
        self.base_mood = self.positivity * 10
        self.mood = self.base_mood
        self.circadian_rhythm_on = False
        self.dt = pygame.time.get_ticks() / 1000
        self.display_info = False

    def calculate_temperament(self):
        if self.extroversion >= 5:
            temperament = "Sanguine"
            if self.positivity <= 5:
                temperament = "Choleric"
        else:
            temperament = "Phlegmatic"
            if self.positivity <= 5:
                temperament = "Melancholic"
        return temperament

    def reset_rhythm(self):
        self.circadian_rhythm_on = False

    def circadian_rhythm_live(self):
        if (round(self.dt % 10) < 1) and (self.circadian_rhythm_on is True):
            return True

    def circadian_rhythm(self):
        self.dt = pygame.time.get_ticks() / 1000 
        if (self.dt % 10) > 5:
            self.circadian_rhythm_on = True

    def return_to_base_mood(self):
        for x in range(0, 5):
            if self.mood > self.base_mood:
                self.mood -= 1           
            elif self.mood < self.base_mood:
                self.mood += 1

    def update_mood(self, positive, score):
        if not positive:
            for point in range(0, score):
               if self.mood > 0:
                   self.mood -= 1
            return False
        for point in range(0, score):
            if self.mood < 100:
                self.mood += 1

    def music(self, genre):
        switcher = { 
            "Metal": self.metal,
            "Hip Hop": self.hiphop, 
            "Pop": self.pop,
            "Classical": self.classical
        }   
        mood = switcher.get(genre, False)[0]
        value = switcher.get(genre, False)[1]
        self.update_mood(mood, value)

    def no_music(self):
        pass

    def get_drunk(self, strength):
        for x in range(0, strength):
            if self.extroversion < 10:
                self.extroversion += 1

    def get_magical(self):
        for x in range(0, 10):
            if self.positivity < 10:
                self.positivity += 1

    def eat(self, score):
        for x in range(0, score):
            if self.mood < 100:
                self.mood += 1

class Sanguine(Personality):
    def __init__(self, temperament, extroversion, positivity):
        super().__init__(temperament, extroversion, positivity)
        self.metal = (False, 10)
        self.hiphop = (True, 5)
        self.pop = (True, 10)
        self.classical = (False, 5)

class Choleric(Personality):
    def __init__(self, temperament, extroversion, positivity):
        super().__init__(temperament, extroversion, positivity)
        self.metal = (True, 5)
        self.hiphop = (True, 10)
        self.pop = (False, 5)
        self.classical = (False, 10)

class Phlegmatic(Personality):
    def __init__(self, temperament, extroversion, positivity):
        super().__init__(temperament, extroversion, positivity)
        self.metal = (False, 5)
        self.hiphop = (False, 10)
        self.pop = (True, 5)
        self.classical = (True, 10)

class Melancholic(Personality):
    def __init__(self, temperament, extroversion, positivity):
       super().__init__(temperament, extroversion, positivity)
       self.metal = (True, 10)
       self.hiphop = (False, 5)
       self.pop = (False, 10)
       self.classical = (True, 5)
