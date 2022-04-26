import pygame
from itertools import chain
from loguru import logger


class Window:
    def __init__(self, game):
        self.game = game
        self.active = None
        self.ui = {}
        self.set_ui()

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.set_active(event)
        if self.active:
            self.active.event(event)
        if event.type == pygame.MOUSEMOTION:
            self.check_hover(event)

    def check_hover(self, event):
        pos = event.pos
        for element in chain(*self.ui.values()):
            if element.check_collide_point(pos):
                pos = [-1, -1]

    def fixed_update(self):
        for element in chain(*self.ui.values()):
            element.fixed_update()

    def set_active_object(self, object):
        if object != self.active:
            if self.active:
                self.active.on_disactive()
            self.active = object
            logger.info(f"active is {self.active}")

    def remove_active(self):
        self.set_active_object(None)

    def set_active(self, event):
        for element in chain(*self.ui.values()):
            if element.check_collide_point(event.pos):
                self.set_active_object(element)
                return
        else:
            self.set_active_object(None)

    def update(self):
        if self.active:
            self.active.update()

    def draw(self):
        for element in chain(*self.ui.values().__reversed__()):
            element.draw()

    def set_ui(self):
        pass

    def on_close(self):
        pass
