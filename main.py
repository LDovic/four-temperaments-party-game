import pygame
from game import Game
from constants import *

game = Game()

def main():
    quit = False

    while not quit:
        quit = game.event_listen() 

        game.run()

        pygame.display.flip()
        game.clock.tick(FRAMERATE)

main()
pygame.quit()
