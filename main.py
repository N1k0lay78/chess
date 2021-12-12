from core.windows.Game import Game
from core.windows.test import Test
import pygame


game = Game((600, 600), "Шахматы", icon=pygame.image.load('Source/Image/icon.png'))
game.run()

# screen = pygame.display.set_mode((600, 600))
# test = Test(screen)
# test.run()