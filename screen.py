from constants import *
from button import *
import math

class Screen():
    def __init__(self, name, on, display):
        self.name = name
        self.on = on
        self.display = display

    def fill(self):
        self.display.fill(BLACK)

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
        self.start_buttons = []
        self.quit = Button("Quit", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.new_game = Button("New Game", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.options = Button("Options", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.start_buttons.append(self.new_game)
        self.start_buttons.append(self.quit)
        self.position_buttons_vertical_center(self.start_buttons)

    def play(self, buttons):
        self.fill()
        for button in buttons:
            self.display.blit(button.surface, button.rect)

class GameScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)
        self.tick = 0

    def update_items(self, item):
        self.display.blit(item.image, item.rect)

    def update_item_info(self, item, agent):
        item.give.change_position_xy(agent.rect.x, agent.rect.y - 30)

    def update_agents(self, agent):
        if agent.xvector == 0 and agent.yvector == 0:
            self.display.blit(agent.Rstand, agent.rect) if agent.facing_right else self.display.blit(agent.Lstand, agent.rect) 
            return
        self.tick += 1
        rounded_tick = math.ceil(self.tick / 4) - 1 
        if self.tick >= len(agent.Rimages) * 4:
            self.tick = 0 
        self.display.blit(agent.Rimages[rounded_tick], agent.rect) if agent.facing_right else self.display.blit(agent.Limages[rounded_tick], agent.rect)

    def update_agent_info(self, agent):
        agent.mood_button.change_text("Mood: " + str(agent.get_mood()))
        agent.extroversion_button.change_text("Extroversion: " + str(agent.get_extroversion()))

        agent.extroversion_button.update_color(agent.name, agent.get_extroversion() * 10)
        agent.positivity_button.update_color(agent.name, agent.get_positivity() * 10)
        agent.mood_button.update_color(agent.name, agent.get_mood())

        agent.mood_button.change_position_xy(agent.rect.x, agent.rect.y - 30) 
        agent.positivity_button.change_position_xy(agent.rect.x, agent.rect.y - 20) 
        agent.extroversion_button.change_position_xy(agent.rect.x, agent.rect.y - 10)

    def update_track(self, musicplayer):
        loaded_track = musicplayer.tracks[musicplayer.track_index]
        musicplayer.track_info.change_text(loaded_track['title'] + " - " + loaded_track['artist'] + " - " + loaded_track['genre'])

    def update_mean(self, mean, calculated_mean):
        mean.change_text("Mean: " + str(round(calculated_mean)))

    def update_sd(self, sd, calculated_sd):
        sd.change_text("SD: " + str(round(calculated_sd)))

class WinScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)
        """Win buttons"""
        self.win_buttons = []
        self.win = Button("Success", ((SCREEN_WIDTH / 3), 0), WHITE, BUTTON_FONT_SIZE)
        self.win_buttons.append(self.win)
        self.position_buttons_horizontal(self.win_buttons, (SCREEN_HEIGHT / 4) * 3, 50)

class LoseScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)
        """Lose buttons"""
        self.lose_buttons = []
        self.lose = Button("Game Over", ((SCREEN_WIDTH / 3), 0), WHITE, BUTTON_FONT_SIZE)
        self.lose_buttons.append(self.lose)
        self.position_buttons_horizontal(self.lose_buttons, (SCREEN_HEIGHT / 4) * 3, 50)

class LoadingScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)
        """Loading buttons"""
        self.loading_buttons = []
        self.loading = Button("Loading", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.loading_buttons.append(self.loading)
        self.position_buttons_vertical_center(self.loading_buttons)

class ChooseCharacterScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)
        """Choose character buttons"""
        self.choose_character_buttons = []
        self.choose_character_next = Button("Next", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.choose_character_play = Button("Play", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.choose_character_buttons.append(self.choose_character_next)
        self.choose_character_buttons.append(self.choose_character_play)
        self.position_buttons_horizontal(self.choose_character_buttons, (SCREEN_HEIGHT / 4) * 3, 50)

    def show(self, character_profiles):
        for name, character in character_profiles.items():
            if character['display'] is True:
                self.display.blit(character['profile'], character['profile'].get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 4))

class InstructionsScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)
        """Instructions buttons"""
        self.instructions_buttons = []
        self.instructions_text1 = Button("Press E to interact", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_text2 = Button("Press WASD to move", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_text3 = Button("Press 1, 2 and 3 to control the music", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_text4 = Button("Press 0 to see how everyone is feeling", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_text5 = Button("If all of the guests leave, you lose!", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_text6 = Button("Music will affect different personalities", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_text7 = Button("For example, people who are introverted and negative will prefer metal", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_text8 = Button("whereas people who are extroverted and positive like pop", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_text9 = Button("See how long you can keep the party going", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_text10 = Button("Some guests don't mix well!", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.instructions_textplay = Button("Play", (0, 0), WHITE, BUTTON_FONT_SIZE)
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


class ChooseDifficultyScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)
        """Choose difficulty buttons"""
        self.choose_difficulty_buttons = []
        self.choose_difficulty_next = Button("Next", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.choose_difficulty_play = Button("Play", (0, 0), WHITE, BUTTON_FONT_SIZE)
        self.choose_difficulty_buttons.append(self.choose_difficulty_next)
        self.choose_difficulty_buttons.append(self.choose_difficulty_play)
        self.position_buttons_horizontal(self.choose_difficulty_buttons, (SCREEN_HEIGHT / 4) * 3, 50)

    def show(self, difficulty_profiles):
        for name, difficulty in difficulty_profiles.items():
            if difficulty['display'] is True:
                self.display.blit(difficulty['profile'], difficulty['profile'].get_rect())

class IntroductionScreen(Screen):
    def __init__(self, name, on, display):
        super().__init__(name, on, display)
        self.images = self.get_images()
        self.index = 0

    def get_images(self):
        items = []
        contents = os.listdir(INTRODUCTION)
        for item in contents:
            if ASSET_FILE_TYPE in item:
                path = os.path.join(INTRODUCTION + item)
                image = pygame.image.load(path).convert_alpha()
                items.append(image)
        return items

    

    def get_index(self):
        return self.index
