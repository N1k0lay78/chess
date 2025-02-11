from core.online.Client import Client
# from core.windows.GameLEGACY import Game
from core.windows.test import Test
from core.Game import Game
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
game = Game()
game.run()
