import sys

import pygame
from loguru import logger

from core.Game import Game

pygame.init()
logger.add("file.log", rotation="1 week", format="{time:HH:mm:ss} | {level} | {module}.{function}.{line} | {message}")
Game().run()
