from constants import *
import math

class Screen():
    def __init__(self, name, on, display):
        self.name = name
        self.on = on
        self.display = display

    def fill(self):
        self.display.fill(WHITE)

    def blit_buttons(self, buttons):
        for button in buttons:
            self.display.blit(button.surface, button.rect)

    def position_buttons_vertical_center(self, buttons):
        length = len(buttons)
        middle_button = length / 2 
        y = (SCREEN_HEIGHT / 2) - (middle_button * 50) 
        for button in buttons:
            button.rect.centerx = SCREEN_WIDTH / 2 
            button.rect.centery = y 
            y += 50

    def position_buttons_horizontal(self, buttons, y, xinterval):
        length = len(buttons)
        middle_button = length / 2
        x = (SCREEN_WIDTH / 2) - (middle_button * 50)
        for button in buttons:
            button.rect.centerx = x 
            button.rect.y = y
            x += xinterval

class StartScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)

    def play(self, buttons):
        self.fill()
        for button in buttons:
            self.display.blit(button.surface, button.rect)

class GameScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)
        self.tick = 0

    def update_agents(self, agent):
        if agent.vector == 0:
            self.display.blit(agent.Rstand, agent.rect) if agent.facing_right else self.display.blit(agent.Lstand, agent.rect) 
            return
        self.tick += 1
        rounded_tick = math.ceil(self.tick / 4) - 1 
        if self.tick >= len(agent.Rimages) * 4:
            self.tick = 0 
        self.display.blit(agent.Rimages[rounded_tick], agent.rect) if agent.facing_right else self.display.blit(agent.Limages[rounded_tick], agent.rect)

    def update_agent_info(self, agent):
        agent.mood_button.change_text("Mood: " + str(agent.get_mood()))

        agent.extroversion_button.update_color(agent.name, agent.get_extroversion() * 10)
        agent.positivity_button.update_color(agent.name, agent.get_positivity() * 10)
        agent.mood_button.update_color(agent.name, agent.get_mood())

        agent.mood_button.change_position(agent.rect.x, agent.rect.y - 30) 
        agent.positivity_button.change_position(agent.rect.x, agent.rect.y - 20) 
        agent.extroversion_button.change_position(agent.rect.x, agent.rect.y - 10) 

        self.display.blit(agent.extroversion_button.surface, agent.extroversion_button.rect)
        self.display.blit(agent.positivity_button.surface, agent.positivity_button.rect)
        self.display.blit(agent.mood_button.surface, agent.mood_button.rect)

    def update_track(self, musicplayer):
        loaded_track = musicplayer.tracks[musicplayer.track_index]
        musicplayer.track_info.change_text(loaded_track['title'] + " - " + loaded_track['artist'] + " - " + loaded_track['genre'])

    def update_mean(self, mean, calculated_mean):
        mean.change_text("Mean: " + str(round(calculated_mean)))

    def update_sd(self, sd, calculated_sd):
        sd.change_text("SD: " + str(round(calculated_sd)))

class OptionsScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)

    def play(self, options_buttons):
        for button in options_buttons:
            self.display.blit(button.surface, button.rect)

class WinScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)

class LoseScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)

class LoadingScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)

    def play(self, loading_buttons):
        for button in loading_buttons:
            self.display.blit(button.surface, button.rect)

class ChooseCharacterScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)

    def show(self, character_profiles):
        for name, character in character_profiles.items():
            if character['display'] is True:
                self.display.blit(character['profile'], character['profile'].get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 4))
