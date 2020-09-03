import pygame
from game import Game
from constants import *

game = Game()

def main():
    quit = False

    while not quit:
        #gets user controller events, such as key down or mouse click
        quit = game.event_listen() 

        #controls the display for the screen
        game.run()

        pygame.display.flip()
        game.clock.tick(FRAMERATE)

main()
pygame.quit()
