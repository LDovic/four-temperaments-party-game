import pygame
import os
from constants import *
from agent import *
from personality import *
from button import Button
from screen import * 
from musicplayer import *
from background import *
from item import *
import math
import random
import simpleaudio as audio
import datetime

"""

This class creates a game object that contains the entire game, from start screen to win screen.
The class' methods are divided into five sections:
- The 'always running' group which contains one method, 'run'. This method is called by main during the main 'while' loop and determines which methods will be called according to which screen is set.
- The 'always running during game' group that contain the methods that are constantly called when the set screen is the game screen.
- The methods that create the game objects (items, characters etc) that are called when game object is created and when set screen is the loading screen.
- The controls group which contain the game controls.
- The game logic group which contain the methods the control the flow of the game and win and lose conditions. 
Game flow is controlled by which screen is set. If, for example, the game screen is the set screen then the 'run' method will display the content for the game screen.
The flow of the game is controlled by game events (such as a win or a loss) but also by user control events, in the controls methods. When this happens, the set screen changes and the 'run' method will display the appropriate content.

"""

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.pause = False

        self.timer_on = False
        self.time_elapsed = 0

        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("L Noble Project")

        self.musicplayer = MusicPlayer()

        self.choose_character_tick = 0
        self.invitees = len(os.listdir(CHARACTERS)) - 1
        self.difficulty_level = 1

        self.choose_difficulty_tick = 0
        self.difficulty_level = 1

        self.create_screens()
        self.create_character_profiles()
        self.create_difficulty_profiles()
        self.attach_profile_audios()
        self.create_background()

    """Always running"""
    """
    This is always called by main.py
    It deals mainly with displaying (blitting) images to the screen
    """

    def run(self):
        self.this_screen.fill()
        if self.this_screen.name == "Start":
            self.timer_on = False
            self.time_elapsed = 0
            self.musicplayer.stop()
            self.this_screen.blit_buttons(self.this_screen.start_buttons)

        elif self.this_screen.name == "Loading":
            self.this_screen.blit_buttons(self.this_screen.loading_buttons)
            self.create_agents() 
            self.create_items()
            self.set_screens(self.instructions_screen)

        elif self.this_screen.name == "Game":
            if self.timer_on == False:
                self.start_timer()
                self.start_time = self.timer.get_rawtime()

            for asset in self.background:
                self.this_screen.display.blit(asset.image, asset.rect)

            self.this_screen.blit_buttons(self.musicplayer.musicplayer_secondary_buttons)

            for item in self.items:
                self.this_screen.update_items(item)

            self.this_screen.update_track(self.musicplayer)
            self.musicplayer.has_stopped()

            total_agents = self.playable_agents + self.nonplayable_agents

            total_agents.sort(key=lambda x: x.rect.y, reverse=False)

            for agent in self.playable_agents:
                item = agent.item_proximity(self.items)
                if item is not False:
                    self.this_screen.display.blit(item.take.surface, item.take.rect)
                else:
                    agent.item_prox = False

            for agent in total_agents:
                self.this_screen.update_agents(agent)
                self.this_screen.update_agent_info(agent)
                if agent.personality.display_info:
                    self.this_screen.blit_buttons(agent.buttons)

            if self.player1.inventory:
                if self.player1.circle:
                    self.this_screen.update_item_info(self.player1.inventory[0], self.player1)
                    self.this_screen.display.blit(self.player1.inventory[0].give.surface, self.player1.inventory[0].give.rect)
            
            self.this_screen.display.blit(self.this_screen.timer.surface, self.this_screen.timer.rect)
 
            if self.pause == False:
                self.playable_mingle() 
                self.npc_mingle()
                self.music()
                self.update_timer()
                self.this_screen.update_timer_info(self.convert(self.time_elapsed))
                self.calculate_win()
                self.is_game_over()
            else:
                self.set_screens(self.instructions_screen)

        elif self.this_screen.name == "Instructions":
            self.pause = True
            self.this_screen.position_buttons_vertical_center(self.this_screen.instructions_buttons)
            self.this_screen.blit_buttons(self.this_screen.instructions_buttons)

        elif self.this_screen.name == "Win":
            self.this_screen.blit_buttons(self.this_screen.win_buttons)

        elif self.this_screen.name == "Lose":
            self.this_screen.blit_buttons(self.this_screen.lose_buttons)

        elif self.this_screen.name == "ChooseCharacter":
            self.this_screen.blit_buttons(self.this_screen.choose_character_buttons)
            self.this_screen.show(self.character_profiles)

        elif self.this_screen.name == "ChooseDifficulty":
            self.this_screen.blit_buttons(self.this_screen.choose_difficulty_buttons)
            self.this_screen.show(self.difficulty_profiles)

        elif self.this_screen.name == "Introduction":
            self.this_screen.display.blit(self.this_screen.images[self.this_screen.get_index()], self.this_screen.images[self.this_screen.get_index()].get_rect())

    """Always running in game"""
    """
    These 'mingle' methods determine agent behaviour in-game and are always called, while the set screen is the game screen.
    """


    def playable_mingle(self):
        for agent in self.playable_agents:
            agent.agent_proximity(agent.circle)
            agent.update_circle(self.nonplayable_agents)
            agent.xmove()
            agent.ymove()

    """
    This method determines how an npc agent should behave according to its state.
    """
    def npc_mingle(self):
        for agent in self.nonplayable_agents:
            agent.set_state()
            agent.agent_proximity(agent.circle)
            agent.update_circle(self.nonplayable_agents)
            if agent.state == "quitting":
                self.nonplayable_agents.remove(agent)
            elif agent.state == "leaving":
                agent.xmove()
                agent.ymove()
                agent.stop()
                agent.quit()
            elif agent.state == "engaged":
                agent.xmove()
                agent.ymove()
                agent.stop()
                agent.interact()
            elif agent.state == "idle":
                agent.feels_extroverted(random.choice(self.nonplayable_agents))
            elif agent.state == "disengaged":
                agent.xmove()
                agent.ymove()
                agent.stop()

    """
    This method determines how the agent will respond to music. If there is no music playing, then the agent's mood will return to its baseline (the 'circadian rhythm' methods).
    """
    def music(self):
        for agent in self.nonplayable_agents:
            agent.personality.circadian_rhythm()
            if agent.personality.circadian_rhythm_live():
                if self.musicplayer.get_genre() is False:
                    agent.personality.return_to_base_mood()
                    agent.personality.reset_rhythm()
                else:
                    agent.personality.music(self.musicplayer.get_genre())
                    agent.personality.reset_rhythm()

    """LOAD GAME DATA"""

    def create_screens(self):
        self.choose_character_screen = ChooseCharacterScreen("ChooseCharacter", False, self.display)
        self.loading_screen = LoadingScreen("Loading", False, self.display)
        self.win_screen = WinScreen("Win", False, self.display)
        self.lose_screen = LoseScreen("Lose", False, self.display)
        self.game_screen = GameScreen("Game", False, self.display)
        self.start_screen = StartScreen("Start", True, self.display) 
        self.choose_difficulty_screen = ChooseDifficultyScreen("ChooseDifficulty", False, self.display)
        self.instructions_screen = InstructionsScreen("Instructions", False, self.display)
        self.introduction_screen = IntroductionScreen("Introduction", False, self.display)

        self.back_screen = self.introduction_screen
        self.this_screen = self.introduction_screen

        self.screens = []

        self.screens.append(self.choose_character_screen)
        self.screens.append(self.loading_screen)
        self.screens.append(self.win_screen)
        self.screens.append(self.lose_screen)
        self.screens.append(self.game_screen) 
        self.screens.append(self.start_screen) 
        self.screens.append(self.choose_difficulty_screen)
        self.screens.append(self.instructions_screen)
        self.screens.append(self.introduction_screen)

    def create_difficulty_profiles(self):
        self.difficulty_profiles = {}
        contents = os.listdir(DIFFICULTY)
        for item in contents:
            if os.path.isdir(DIFFICULTY + item):
                self.choose_difficulty_tick += 1
                self.difficulty_profiles[item] = {}
                self.difficulty_profiles[item]['name'] = item
                self.difficulty_profiles[item]['profile'] = pygame.image.load(os.path.join(DIFFICULTY + item + "/" + item) + ASSET_FILE_TYPE).convert_alpha()
                self.difficulty_profiles[item]['display'] = False
                self.difficulty_profiles[item]['selected'] = False

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
        personality = PersonalityFactory()        

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
                            personality.factory(),
                            item + 'Left',
                            item + 'LeftStand',
                            item + 'Right',
                            item + 'RightStand',
                            (random.randint(0, SCREEN_WIDTH), random.randint(FLOOR_HEIGHT, SCREEN_HEIGHT - 200)),
                            False
                            )
                        )
                    else:
                        self.playable_agents.append(
                            PlayableAgent(
                            item,
                            personality.factory(),
                            item + 'Left',
                            item + 'LeftStand',
                            item + 'Right',
                            item + 'RightStand',
                            (random.randint(0, SCREEN_WIDTH), random.randint(FLOOR_HEIGHT, SCREEN_HEIGHT - 200)),
                            True
                            )
                        )
            x += 1 
        self.nonplayable_agents_starting_total = len(self.nonplayable_agents)
        self.player1 = self.playable_agents[0]

    def create_background(self):
        self.background = []
        contents = os.listdir(BACKGROUND)
        for item in contents:
            if ASSET_FILE_TYPE in item:
                self.background.append(Background(item, (0, 0)))

    def create_items(self):
        self.items = []
        contents = os.listdir(ITEMS)
        factory = ItemFactory()
        for item in contents:
            if os.path.isdir(ITEMS + item): 
                self.items.append(ItemFactory.factory(item))

    """CONTROLS"""

    def key_up(self, key):
        if key == pygame.K_0:
            for agent in self.nonplayable_agents:
                agent.personality.display_info = False
        if key == pygame.K_a or key == pygame.K_d:
            self.player1.change_vector(0, 0)
        if key == pygame.K_w or key == pygame.K_s:
            self.player1.change_vector(0, 1)

    def key_down(self, key):
        if self.this_screen.name == "Game":
            if self.musicplayer.now_playing is False:
                    if key == pygame.K_1:
                        self.musicplayer.play()
            else:
                if key == pygame.K_3:
                    self.musicplayer.stop()
            if key == pygame.K_2:
                    self.musicplayer.change_track()
            elif key == pygame.K_0:
                for agent in self.nonplayable_agents:
                    agent.personality.display_info = True
            elif key == pygame.K_e:
                self.player1.interact()
            elif key == pygame.K_w:
                self.player1.change_vector(-5, 1)
            elif key == pygame.K_s:
                self.player1.change_vector(5, 1)
            elif key == pygame.K_a:
                self.player1.change_vector(-5, 0)
                self.player1.change_side(False)
            elif key == pygame.K_f:
                if not self.player1.inventory:
                    taken = self.player1.take_item()
                    if taken is not False:
                        self.items.remove(taken)
                else:
                    if self.player1.circle:
                        self.player1.inventory[0].apply_item(self.player1.circle[0])
                        self.player1.inventory.clear()                          
            elif key == pygame.K_d:
                self.player1.change_vector(5, 0)
                self.player1.change_side(True)
            elif key == pygame.K_SPACE:
                self.set_screens(self.instructions_screen)
        elif self.this_screen.name == "Instructions":
            if key == pygame.K_SPACE:
                self.pause = False
                self.set_screens(self.game_screen) 
        elif self.this_screen.name == "Lose":
            if key == pygame.K_SPACE or key == pygame.K_RETURN:
                self.set_screens(self.start_screen)
        elif self.this_screen.name == "Win":
            if key == pygame.K_SPACE or key == pygame.K_RETURN:
                self.set_screens(self.start_screen)

    def mouse_button_down(self, pos):
        if self.this_screen.name == "Start":
            if self.this_screen.quit.rect.collidepoint(pos):
                return True
            if self.this_screen.new_game.rect.collidepoint(pos):                
                self.set_screens(self.choose_character_screen)
                self.choose_character()

        elif self.this_screen.name == "ChooseCharacter":
            if self.this_screen.choose_character_next.rect.collidepoint(pos):
                self.choose_character()
            if self.this_screen.choose_character_play.rect.collidepoint(pos):
                self.set_screens(self.choose_difficulty_screen)
                self.choose_difficulty()

        elif self.this_screen.name == "ChooseDifficulty":
            if self.this_screen.choose_difficulty_next.rect.collidepoint(pos):
                self.choose_difficulty()
            if self.this_screen.choose_difficulty_play.rect.collidepoint(pos):
                for name, difficulty in self.difficulty_profiles.items():
                    if difficulty['selected'] is True:
                        self.difficulty_level = name
                self.set_screens(self.loading_screen)
      
        elif self.this_screen.name == "Introduction":
            if self.this_screen.index >= len(self.this_screen.images) - 1:
                self.set_screens(self.start_screen)
            else:
                self.this_screen.index += 1

    def event_listen(self):
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouse_button_down(pos) is True:
                    return True                
            if event.type == pygame.KEYDOWN:
                self.key_down(event.key)
            if event.type == pygame.KEYUP:
                self.key_up(event.key)

    """GAME LOGIC"""

    """
    This method is called whenever a screen changes.
    There is functionality for a back button to be used with it but it is not as of yet used.
    """
    def set_screens(self, new_screen):
        self.back_screen = self.this_screen
        for screen in self.screens:
            if screen is not new_screen:
                screen.on = False
        new_screen.on = True
        self.this_screen = new_screen

    def choose_difficulty(self):
        tick = 0
 
        end_of_loop = self.choose_difficulty_tick == len(self.difficulty_profiles)

        if end_of_loop:
            self.choose_difficulty_tick = 0

        for name, difficulty in self.difficulty_profiles.items():
            if tick == (self.choose_difficulty_tick - 1) or end_of_loop:
                difficulty['display'] = False
                difficulty['selected'] = False
            if tick == self.choose_difficulty_tick:
                difficulty['display'] = True
                difficulty['selected'] = True
            tick += 1

        self.choose_difficulty_tick += 1 

    def play_character_audio(self):
        try:
            self.active_character_audio.stop()
        except AttributeError:
            pass
        for character in self.character_profiles.values():
            if character['display']:
                try:
                    self.active_character_audio = character['audio'][random.randint(0, len(character['audio']) - 1)].play()
                except KeyError:
                    pass 

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

        self.choose_character_tick += 1

    #for displaying the timer on screen during the game
    def convert(self, milliseconds): 
        seconds = milliseconds/1000
        seconds = seconds % (24 * 3600) 
        seconds %= 3600
        minutes = 9 - seconds // 60
        seconds = 60 - seconds%60
      
        return "%02d:%02d" % (minutes, seconds) 

    def start_timer(self):
        self.timer_on = True
        self.timer = pygame.time.Clock()

    def update_timer(self):
        self.timer.tick(FRAMERATE)

    def calculate_win(self):
        self.time_elapsed += self.timer.get_rawtime()
        if self.time_elapsed > 600000:
            self.set_screens(self.win_screen)

    def is_game_over(self): 
        condition = 2
        if self.difficulty_level == 'Hard':
            condition = self.nonplayable_agents_starting_total
        if len(self.nonplayable_agents) < condition:
            self.set_screens(self.lose_screen)
