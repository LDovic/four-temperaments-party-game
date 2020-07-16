import pygame
from game import Game

game = Game()

def main():
    quit = False

    while not quit:
        quit = game.event_listen() 

        game.run()

        pygame.display.flip()
        game.clock.tick(40)

main()
pygame.quit()
