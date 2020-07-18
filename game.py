import pygame
import os
from constants import *
from agent import *
from button import Button
from screen import * 
from musicplayer import *
import math
import random
import simpleaudio as audio

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("L Noble Project")

        self.musicplayer = MusicPlayer()

        self.tick = 0
        self.choose_character_tick = 0
        self.invitees = len(os.listdir(ASSETS)) - 1
        self.difficulty_level = 1

        self.create_screens()
        self.create_meta_buttons()
        self.create_options_buttons()
        self.create_character_profiles()
        self.attach_profile_audios()

        """Loading buttons"""
        self.loading_buttons = []
        self.loading = Button("Loading", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.loading_buttons.append(self.loading)
        self.loading_screen.position_buttons_vertical_center(self.loading_buttons)

        """Display buttons"""
        self.in_game_stats = []
        self.mean = Button("", ((SCREEN_WIDTH / 3), 0), BLACK, BUTTON_FONT_SIZE)
        self.sd = Button("", ((SCREEN_WIDTH / 3 ) * 2, 0), BLACK, BUTTON_FONT_SIZE)
        self.in_game_stats.append(self.mean)
        self.in_game_stats.append(self.sd)

        """Win buttons"""
        self.win_buttons = []
        self.win = Button("Success", ((SCREEN_WIDTH / 3), 0), BLACK, BUTTON_FONT_SIZE)
        self.win_buttons.append(self.win)
        self.win_screen.position_buttons_horizontal(self.win_buttons, (SCREEN_HEIGHT / 4) * 3, 50)

        """Lose buttons"""
        self.lose_buttons = []
        self.lose = Button("Game Over", ((SCREEN_WIDTH / 3), 0), BLACK, BUTTON_FONT_SIZE)
        self.lose_buttons.append(self.lose)
        self.lose_screen.position_buttons_horizontal(self.lose_buttons, (SCREEN_HEIGHT / 4) * 3, 50)

        """Choose character buttons"""
        self.choose_character_buttons = []
        self.next = Button("Next", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.play = Button("Play", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.choose_character_buttons.append(self.next)
        self.choose_character_buttons.append(self.play)
        self.choose_character_screen.position_buttons_horizontal(self.choose_character_buttons, (SCREEN_HEIGHT / 4) * 3, 50)

    """RUN - Always running"""

    def run(self):
        self.this_screen.fill()
        if self.this_screen.name == "Start":
            self.this_screen.blit_buttons(self.meta_buttons)
        elif self.this_screen.name == "Loading":
            self.this_screen.blit_buttons(self.loading_buttons)
            self.create_agents() 
        elif self.this_screen.name == "Game":           
            self.this_screen.blit_buttons(self.in_game_stats + self.musicplayer.musicplayer_primary_buttons + self.musicplayer.musicplayer_secondary_buttons)
            self.this_screen.position_buttons_horizontal(self.musicplayer.musicplayer_primary_buttons, (SCREEN_HEIGHT / 4) * 3, 100)
            self.this_screen.position_buttons_horizontal(self.musicplayer.musicplayer_secondary_buttons, (SCREEN_HEIGHT / 4) * 3.5, 100)
            self.this_screen.update_track(self.musicplayer)
            self.musicplayer.has_stopped()

            self.this_screen.update_mean(self.mean, self.calculate_mean())
            self.this_screen.update_sd(self.sd, self.calculate_sd()) 

            for agent in self.nonplayable_agents + self.playable_agents:
                self.this_screen.update_agents(agent)
                self.this_screen.update_agent_info(agent)
                if agent.display_info:
                    self.this_screen.blit_buttons(agent.buttons)
#                    self.this_screen.display.blit(agent.extroversion_button.surface, agent.extroversion_button.rect)
#                    self.this_screen.display.blit(agent.positivity_button.surface, agent.positivity_button.rect)
#                    self.this_screen.display.blit(agent.mood_button.surface, agent.mood_button.rect) 
            self.mingle()         
            self.calculate_win()
            self.calculate_lose()
        elif self.this_screen.name == "Options":
            self.this_screen.position_buttons_vertical_center(self.options_buttons)
            self.this_screen.blit_buttons(self.options_buttons)
        elif self.this_screen.name == "Win":
            self.this_screen.blit_buttons(self.win_buttons)
        elif self.this_screen.name == "Lose":
            self.this_screen.blit_buttons(self.lose_buttons)
        elif self.this_screen.name == "ChooseCharacter":
            self.this_screen.blit_buttons(self.choose_character_buttons)
            self.this_screen.show(self.character_profiles)

    """LOAD GAME DATA"""

    def create_screens(self):
        self.choose_character_screen = ChooseCharacterScreen("ChooseCharacter", False, self.display)
        self.loading_screen = LoadingScreen("Loading", False, self.display)
        self.win_screen = WinScreen("Win", False, self.display)
        self.lose_screen = LoseScreen("Lose", False, self.display)
        self.game_screen = GameScreen("Game", False, self.display)
        self.options_screen = OptionsScreen("Options", False, self.display)
        self.start_screen = StartScreen("Start", True, self.display) 
        self.back_screen = self.start_screen
        self.this_screen = self.start_screen

        self.screens = []
        self.screens.append(self.choose_character_screen)
        self.screens.append(self.loading_screen)
        self.screens.append(self.win_screen)
        self.screens.append(self.game_screen) 
        self.screens.append(self.options_screen) 
        self.screens.append(self.start_screen) 

    def create_meta_buttons(self):
        self.meta_buttons = []
        self.quit = Button("Quit", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.new_game = Button("New Game", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.options = Button("Options", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.meta_buttons.append(self.new_game)
        self.meta_buttons.append(self.options)
        self.meta_buttons.append(self.quit)
        self.start_screen.position_buttons_vertical_center(self.meta_buttons)

    def create_options_buttons(self):
        self.options_buttons = []
        self.guests = Button("Guests: " + str(self.invitees), (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.difficulty = Button("Difficulty: " + str(self.difficulty_level), (0, 0), BLACK, BUTTON_FONT_SIZE)         
        self.close = Button("Close", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.options_buttons.append(self.guests)
        self.options_buttons.append(self.difficulty)
        self.options_buttons.append(self.close)

    def attach_profile_audios(self):
        contents = os.listdir(CHARACTER_AUDIO)
        for item in contents:
            if os.path.isdir(CHARACTER_AUDIO + item):
                audio_directory = os.listdir(CHARACTER_AUDIO + item)
                for name, character in self.character_profiles.items():
                    if name == item:
                        self.character_profiles[name]['audio'] = []
                        for file in audio_directory: 
                            if AUDIO_FILE_TYPE in file:
                                self.character_profiles[name]['audio'].append(audio.WaveObject.from_wave_file(CHARACTER_AUDIO + name + "/" + file)) 

    def create_character_profiles(self):
        self.character_profiles = {}
        contents = os.listdir(ASSETS)
        for item in contents:
            if os.path.isdir(ASSETS + item):
                self.choose_character_tick += 1
                self.character_profiles[item] = {}
                self.character_profiles[item]['name'] = item
                self.character_profiles[item]['profile'] = pygame.image.load(os.path.join(ASSETS + item + "/" + item + 'RightStand') + ASSET_FILE_TYPE).convert_alpha()
                self.character_profiles[item]['display'] = False
                self.character_profiles[item]['selected'] = False 

    def create_agents(self):
        self.nonplayable_agents = []
        self.playable_agents = []
        x = 0

        contents = os.listdir(ASSETS)
        for item in contents:
            if x <= self.invitees:
                if os.path.isdir(ASSETS + item):
                    if self.player != item:
                        self.nonplayable_agents.append(
                            NonPlayableAgent(
                            item,
                            item + 'Left',
                            item + 'LeftStand',
                            item + 'Right',
                            item + 'RightStand',
                            (random.randint(0, SCREEN_WIDTH), 0),
                            self.difficulty_level,
                            False
                            )
                        )
                    else:
                        self.playable_agents.append(
                            PlayableAgent(
                            item,
                            item + 'Left',
                            item + 'LeftStand',
                            item + 'Right',
                            item + 'RightStand',
                            (random.randint(0, SCREEN_WIDTH), 0),
                            self.difficulty_level,
                            True
                            )
                        )
            x += 1 

        self.player1 = self.playable_agents[0]
        self.set_screens(self.game_screen)

    """CONTROLS"""

    def key_up(self, key):
        if key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.player1.change_vector(0)

    def key_down(self, key):
        if key == pygame.K_SPACE:
            self.player1.interact(self.nonplayable_agents)
        if key == pygame.K_LEFT:
            self.player1.change_vector(-5)
            self.player1.change_side(False)
        elif key == pygame.K_RIGHT:
            self.player1.change_vector(5)
            self.player1.change_side(True)

    def mouse_button_down(self, pos):
        if self.this_screen.name == "Options":
            if self.close.rect.collidepoint(pos):
                self.set_screens(self.back_screen)
            if self.guests.rect.collidepoint(pos):
                self.add_guests()
            if self.difficulty.rect.collidepoint(pos):
                self.increase_difficulty()
        elif self.this_screen.name == "Start":
            if self.options.rect.collidepoint(pos):
                self.set_screens(self.options_screen)

            if self.quit.rect.collidepoint(pos):
                return True
            if self.new_game.rect.collidepoint(pos):                
                self.set_screens(self.choose_character_screen)
                self.choose_character()

        elif self.this_screen.name == "ChooseCharacter":
            if self.next.rect.collidepoint(pos):
                self.choose_character()
            if self.play.rect.collidepoint(pos):
                self.play_game()

        elif self.this_screen.name == "Game":
            if self.musicplayer.next_track_button.rect.collidepoint(pos):
                self.musicplayer.change_track()
            if self.musicplayer.now_playing is False:
                if self.musicplayer.play_button.rect.collidepoint(pos):
                    self.musicplayer.play()
            else:
                if self.musicplayer.stop_button.rect.collidepoint(pos):
                    self.musicplayer.stop()

    def mouse_hover(self, pos):
        for agent in self.nonplayable_agents:
            if agent.rect.collidepoint(pos): 
                agent.display_info = True
            else:
                agent.display_info = False

    def event_listen(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_button_down(pos) is True:
                    return True
            if self.this_screen.name == "Game":
                if event.type == pygame.KEYDOWN:
                    self.key_down(event.key)
                if event.type == pygame.KEYUP:
                    self.key_up(event.key)
                self.mouse_hover(pos)

    """OTHER"""

    def set_screens(self, new_screen):
        self.back_screen = self.this_screen
        for screen in self.screens:
            if screen is not new_screen:
                screen.on = False
        new_screen.on = True
        self.this_screen = new_screen

    def mingle(self):
        for agent in self.nonplayable_agents:
            if agent.quitting is True:
                self.nonplayable_agents.remove(agent)
            if agent.leaving is True:
                agent.quit()
            else:
                agent.leave()
                if (agent.feels_extroverted() is True):
                    agent.acquire_target(random.choice(self.nonplayable_agents).rect.x) 
                agent.interact(self.nonplayable_agents)
            agent.stop()
        for agent in self.nonplayable_agents + self.playable_agents:
            agent.personality.circadian_rhythm()
            if agent.personality.circadian_rhythm_live():
                if self.musicplayer.get_genre() is False:
                    agent.personality.return_to_base_mood()
                    agent.personality.reset_rhythm()
                else:
                    agent.music(self.musicplayer.get_genre())
                    agent.personality.reset_rhythm()
            agent.move()

    def play_character_audio(self):
        try:
            self.active_character_audio.stop()
        except AttributeError:
            pass
        for character in self.character_profiles.values():
            if character['display']:
                self.active_character_audio = character['audio'][random.randint(0, len(character['audio']) - 1)].play()
 
    def choose_character(self):
        tick = 0
 
        end_of_loop = self.choose_character_tick == len(self.character_profiles)

        if end_of_loop:
            self.choose_character_tick = 0

        for name, character in self.character_profiles.items():
            if tick == (self.choose_character_tick - 1) or end_of_loop:                
                character['display'] = False
            if tick == self.choose_character_tick:
                self.player = character['name']
                character['display'] = True
            tick += 1

        self.play_character_audio()
        self.choose_character_tick += 1

    def play_game(self): 
        self.set_screens(self.loading_screen)

    def increase_difficulty(self):
        self.difficulty_level += 1
        if self.difficulty_level > 9:
            self.difficulty_level = 1 
        self.update_options(self.difficulty, "Difficulty: ", self.difficulty_level)

    def add_guests(self):
        self.invitees += 1
        if self.invitees >= len(os.listdir(ASSETS)):
            self.invitees = 1
        self.update_options(self.guests, "Guests: ", self.invitees)

    def update_options(self,option, string, count):
        option.change_text(string + str(count))

    def calculate_mean(self):
        total_agents = self.nonplayable_agents

        if len(total_agents) == 0:
            return 0

        mean = 0
        for agent in total_agents:
            mean += agent.get_mood()
        return mean / len(total_agents)

    def calculate_sd(self):
        total_agents = self.nonplayable_agents

        if len(total_agents) == 0:
            return 0

        mean = self.calculate_mean()
        squares = []
        for agent in total_agents:
            squares.append(pow(agent.get_mood() - mean, 2))
        sd1 = sum(squares) - 1 / len(total_agents)
        sd = math.sqrt(sd1) if sd1 > 0 else 0
        return sd

    def calculate_win(self):
        if (self.calculate_mean() > 95) and (self.calculate_sd() < 30):
            self.set_screens(self.win_screen)

    def calculate_lose(self):
        if not self.nonplayable_agents:
#        if (self.calculate_mean() < 30) or (not self.nonplayable_agents):
            self.set_screens(self.lose_screen)
