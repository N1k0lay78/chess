from core.windows.Game import Game
from core.windows.LoadingGame import LoadingGame
from core.windows.test import Test
import pygame


screen = pygame.display.set_mode((700, 600))

# test = Test(screen)
# test.run()

# loading = LoadingGame(screen)
# loading.run()
color = 0
game = Game((600, 600), "Шахматы", color, icon=pygame.image.load('Source/Image/icon.png'))
game.run()
