import pygame
import os
from constants import *
from agent import *
from button import Button
from screen import * 
from musicplayer import *
from background import *
from item import *
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
        self.invitees = len(os.listdir(CHARACTERS)) - 1
        self.difficulty_level = 1

        self.create_screens()
        self.create_meta_buttons()
        self.create_options_buttons()
        self.create_character_profiles()
        self.attach_profile_audios()
        self.create_background()
        self.create_items()

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

        """Instructions buttons"""
        self.instructions_buttons = []
        self.instructions_text1 = Button("Press E to interact", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_text2 = Button("Press WASD to move", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_text3 = Button("Press 1, 2 and 3 to control the music", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_text4 = Button("Press 0 to see how everyone is feeling", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_text5 = Button("If all of the guests leave, you lose!", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_text6 = Button("Music will affect different personalities", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_text7 = Button("For example, people who are introverted and negative will prefer metal", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_text8 = Button("whereas people who are extroverted and positive like pop", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_text9 = Button("See how long you can keep the party going", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_text10 = Button("Some guests don't mix well!", (0, 0), BLACK, BUTTON_FONT_SIZE)
        self.instructions_textplay = Button("Play", (0, 0), BLACK, BUTTON_FONT_SIZE) 
        self.instructions_buttons.append(self.instructions_text1)
        self.instructions_buttons.append(self.instructions_text2)
        self.instructions_buttons.append(self.instructions_text3)
        self.instructions_buttons.append(self.instructions_text4)
        self.instructions_buttons.append(self.instructions_text5)
        self.instructions_buttons.append(self.instructions_text6)
        self.instructions_buttons.append(self.instructions_text7)
        self.instructions_buttons.append(self.instructions_text8)
        self.instructions_buttons.append(self.instructions_text9)
        self.instructions_buttons.append(self.instructions_text10)
        self.instructions_buttons.append(self.instructions_textplay)

    """RUN - Always running"""

    def run(self):
        self.this_screen.fill()
        if self.this_screen.name == "Start":
            self.this_screen.blit_buttons(self.meta_buttons)
        elif self.this_screen.name == "Loading":
            self.this_screen.blit_buttons(self.loading_buttons)
            self.create_agents() 
        elif self.this_screen.name == "Game":
            for asset in self.background:
                self.this_screen.display.blit(asset.image, asset.rect)

            self.this_screen.blit_buttons(self.in_game_stats + self.musicplayer.musicplayer_secondary_buttons)

            for item in self.items:
                self.this_screen.update_items(item)

            self.this_screen.update_track(self.musicplayer)
            self.musicplayer.has_stopped()

            self.total_agents.sort(key=lambda x: x.rect.y, reverse=False)

            for agent in self.playable_agents:
                item = agent.item_proximity(self.items)
                if item is not False:
                    self.this_screen.display.blit(item.button.surface, item.button.rect)      

            for agent in self.total_agents:
                self.this_screen.update_agents(agent)
                self.this_screen.update_agent_info(agent)
                if agent.personality.display_info:
                    self.this_screen.blit_buttons(agent.buttons)
            self.mingle()
 
            self.is_game_over()
        elif self.this_screen.name == "Instructions":
            self.this_screen.position_buttons_vertical_center(self.instructions_buttons)
            self.this_screen.blit_buttons(self.instructions_buttons)
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
        self.instructions_screen = InstructionsScreen("Instructions", False, self.display)

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
        contents = os.listdir(CHARACTERS)
        for item in contents:
            if os.path.isdir(CHARACTERS + item):
                self.choose_character_tick += 1
                self.character_profiles[item] = {}
                self.character_profiles[item]['name'] = item
                self.character_profiles[item]['profile'] = pygame.image.load(os.path.join(CHARACTERS + item + "/" + item + 'RightStand') + ASSET_FILE_TYPE).convert_alpha()
                self.character_profiles[item]['display'] = False
                self.character_profiles[item]['selected'] = False 

    def create_agents(self):
        self.nonplayable_agents = []
        self.playable_agents = []
        x = 0

        contents = os.listdir(CHARACTERS)
        for item in contents:
            if x <= self.invitees:
                if os.path.isdir(CHARACTERS + item):
                    if self.player != item:
                        self.nonplayable_agents.append(
                            NonPlayableAgent(
                            item,
                            item + 'Left',
                            item + 'LeftStand',
                            item + 'Right',
                            item + 'RightStand',
                            (random.randint(0, SCREEN_WIDTH), random.randint(FLOOR_HEIGHT, SCREEN_HEIGHT)),
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
        self.total_agents = self.nonplayable_agents + self.playable_agents
        self.set_screens(self.game_screen)

    def create_background(self):
        self.background = []
        contents = os.listdir(BACKGROUND)
        for item in contents:
            if ASSET_FILE_TYPE in item:
                self.background.append(Background(item, (0, 0)))

    def create_items(self):
        self.items = []
        contents = os.listdir(ITEMS)
        for item in contents:
            if ASSET_FILE_TYPE in item:
                self.items.append(Item(item, (400, 390)))

    """CONTROLS"""

    def key_up(self, key):
        if key == pygame.K_0:
            for agent in self.total_agents:
                agent.personality.display_info = False
        if key == pygame.K_a or key == pygame.K_d:
            self.player1.change_vector(0, 0)
        if key == pygame.K_w or key == pygame.K_s:
            self.player1.change_vector(0, 1)

    def key_down(self, key):
        if key == pygame.K_2:
                self.musicplayer.change_track()
        if self.musicplayer.now_playing is False:
                if key == pygame.K_1:
                    self.musicplayer.play()
        else:
            if key == pygame.K_3:
                self.musicplayer.stop()
        if key == pygame.K_0:
            for agent in self.total_agents:
                agent.personality.display_info = True
        if key == pygame.K_e:
            self.player1.interact(self.nonplayable_agents)
        if key == pygame.K_w:
            self.player1.change_vector(-5, 1)
        if key == pygame.K_s:
            self.player1.change_vector(5, 1)
        if key == pygame.K_a:
            self.player1.change_vector(-5, 0)
            self.player1.change_side(False)
        elif key == pygame.K_d:
            self.player1.change_vector(5, 0)
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
                self.set_screens(self.instructions_screen)

        elif self.this_screen.name == "Instructions":
            if self.instructions_textplay.rect.collidepoint(pos):
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
                    target = random.choice(self.nonplayable_agents)
                    agent.acquire_target(target.rect.x, target.rect.y) 
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
        if self.invitees >= len(os.listdir(CHARACTERS)):
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

    def is_game_over(self):
        if not self.nonplayable_agents:
            self.set_screens(self.lose_screen)
