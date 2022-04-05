import pygame
from loguru import logger


class Window:
    def __init__(self, game):
        self.ui = []
        self.game = game
        self.active = None

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.set_active(event)
            logger.info(f"active is {self.active}")
        if self.active:
            self.active.event(event)
        if event.type == pygame.MOUSEMOTION:
            self.check_hover(event)

    def check_hover(self, event):
        pass

    def fixed_update(self):
        pass

    def set_active_object(self, object):
        if object != self.active:
            if self.active:
                self.active.on_disactive()
            self.active = object

    def remove_active(self):
        self.set_active_object(None)

    def set_active(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def on_close(self):
        pass
