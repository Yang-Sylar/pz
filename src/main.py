import pygame
import sys
from pygame.locals import *
from const import *
from game import *

pygame.init()

DS = pygame.display.set_mode(GAME_SIZE)
game = Game(DS)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.mouseClickHandler(event.button)

    DS.fill((255, 255, 255))
    game.update()
    game.draw()

    pygame.display.update()
        