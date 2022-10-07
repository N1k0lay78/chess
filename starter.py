import pygame
from loguru import logger

from coretwo.game.game import Game


pygame.init()
logger.add("file2.log", rotation="1 week", format="{time:HH:mm:ss} | {level} | {module}.{function}.{line} | {message}")

Game()
