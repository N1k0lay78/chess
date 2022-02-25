from core.online.Client import Client
from core.windows.Game import Game
from core.windows.LoadingGame import LoadingGame
from core.windows.test import Test
import pygame


# print("su 0 a2w b2w c2w d2w e2w f2w g2w h2w Bc1w Bf1w Nb1w Ng1w Ra1w Rh1w Qd1w Ke1w"[5:])
screen = pygame.display.set_mode((700, 600))
# test = Test(screen)
# test.run()

# loading = LoadingGame(screen)
# loading.run()
# nickname = "Nickolausus"
# nickname = "Rjkz"
color = 0
game = Game((600, 600), "Шахматы", color, icon=pygame.image.load('Source/Image/icon.png'))
game.run()
