import os
import sys
from os import path

def bundle_check():
    try:
        getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS')
        print('running in a PyInstaller bundle')
        bundle = True
    except:
        print('running in a normal Python process')
        bundle = False

    return bundle

bundle = bundle_check()

"""
DIRECTORIES
"""

if not bundle:
    CWD = os.getcwd()
else:
    CWD = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))

CHARACTERS = CWD + "/characters/"
BACKGROUND = CWD + "/background/"
ITEMS = CWD + "/items/"
CHARACTER_AUDIO = CWD + "/audio/CharacterAudio/"
SOUNDTRACK = CWD + "/audio/MusicPlayer/"
FONTS = CWD + "/fonts/"

"""
AUDIO
"""

ASSET_FILE_TYPE = '.png'
AUDIO_FILE_TYPE = '.wav'

"""
VISUAL
"""

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (190, 190, 190)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800

FLOOR_HEIGHT = 400

BUTTON_FONT_SIZE = 12

Y_BOTTOM_Q = (SCREEN_HEIGHT / 4) * 3
