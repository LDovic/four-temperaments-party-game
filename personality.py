import pygame
import random

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
            for x in range(0, score):
               if self.mood > 0:
                   self.mood -= 1
            return False
        for point in range(0, score):
            if self.mood < 100:
                self.mood += 1

    def classical(self):
        if (self.temperament == "Phlegmatic") or (self.temperament == "Melancholic"):
            self.update_mood(True, 10)
        if (self.temperament == "Sanguine") or (self.temperament == "Choleric"):
            self.update_mood(False, 10)

    def pop(self):
        if (self.temperament == "Sanguine") or (self.temperament == "Phlegmatic"):
            self.update_mood(True, 10)
        if (self.temperament == "Melancholic") or (self.temperament == "Choleric"):
            self.update_mood(False, 10)

    def hiphop(self):
        if (self.temperament == "Sanguine") or (self.temperament == "Choleric"):
            self.update_mood(True, 10)
        if (self.temperament == "Melancholic") or (self.temperament == "Phlegmatic"):
            self.update_mood(False, 10)

    def metal(self):
        if (self.temperament == "Melancholic") or (self.temperament == "Choleric"):
            self.update_mood(True, 10)
        if (self.temperament == "Sanguine") or (self.temperament == "Phlegmatic"):
            self.update_mood(False, 15)

    def no_music(self):
        pass

    def get_drunk(self, strength):
        for x in range(0, strength):
            if self.extroversion < 10:
                self.extroversion += 1

class Sanguine(Personality):
    def __init__(self, temperament, extroversion, positivity):
        super().__init__(temperament, extroversion, positivity)

class Choleric(Personality):
    def __init__(self, temperament, extroversion, positivity):
        super().__init__(temperament, extroversion, positivity)

class Phlegmatic(Personality):
    def __init__(self, temperament, extroversion, positivity):
        super().__init__(temperament, extroversion, positivity)

class Melancholic(Personality):
    def __init__(self, temperament, extroversion, positivity):
        super().__init__(temperament, extroversion, positivity)
