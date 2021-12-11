from core.Game import Game
import pygame


game = Game((600, 600), "Шашки", icon=pygame.image.load('Source/Image/icon.png'))
game.run()
