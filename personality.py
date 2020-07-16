import pygame
import random

class Personality:
    def __init__(self, positivity):
        self.extroversion = random.randint(1,10)
        self.positivity = random.randint(1, 10 - positivity)
        self.temperament = self.calculate_temperament()
        self.base_mood = self.positivity * 10
        self.mood = self.base_mood
        self.circadian_rhythm_on = False
        self.dt = pygame.time.get_ticks() / 1000

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
            for x in range(0, score):
               if self.mood > 0:
                   self.mood -= 1
            return False
        for point in range(0, score):
            if self.mood < 100:
                self.mood += 1

    def classical(self):
        if (self.temperament is "Phlegmatic") or (self.temperament is "Melancholic"):
            self.update_mood(True, 10)
        if (self.temperament is "Sanguine") or (self.temperament is "Choleric"):
            self.update_mood(False, 10)

    def pop(self):
        if (self.temperament is "Sanguine") or (self.temperament is "Phlegmatic"):
            self.update_mood(True, 10)
        if (self.temperament is "Melancholic") or (self.temperament is "Choleric"):
            self.update_mood(False, 10)

    def hiphop(self):
        if (self.temperament is "Sanguine") or (self.temperament is "Choleric"):
            self.update_mood(True, 10)
        if (self.temperament is "Melancholic") or (self.temperament is "Phlegmatic"):
            self.update_mood(False, 10)

    def metal(self):
        if (self.temperament is "Melancholic") or (self.temperament is "Choleric"):
            self.update_mood(True, 10)
        if (self.temperament is "Sanguine") or (self.temperament is "Phlegmatic"):
            self.update_mood(False, 10)

    def no_music(self):
        pass
