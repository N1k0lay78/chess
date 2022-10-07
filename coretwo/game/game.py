import pygame
from loguru import logger

from coretwo.config.initializer import config_initializer
from coretwo.config.validator import config_validator


def validation():
    result_validation = [config_validator()]

    for res in result_validation:
        if res != "":
            logger.error(res)

    return all(res == "" for res in result_validation)


class Game:
    def __init__(self):
        logger.info("start game")

        # validate files
        if not validation():
            quit(1)

        # game params
        self.config = {}
        self.running = True
        self.window = None

        # initialize config
        config_initializer(self.config)

        # initialize screen
        self.screen = pygame.display.set_mode(self.config["screen_size"])
        pygame.display.set_caption(self.config["app_name"])
        pygame.display.set_icon(pygame.image.load(self.config["app_icon"]))
        input()
