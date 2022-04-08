import pygame

from core.UI.BaseUI import BaseUI


class PressAnyKey(BaseUI):
    def __init__(self, window, pos, text):
        super().__init__(window, pos, image=window.game.render_text(text, (230, 81, 0)))
        self.ready = False
        self.timer = 0

    def event(self, event):
        if self.ready and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            self.window.timer = 0

    def set_ready(self):
        self.ready = True

    def fixed_update(self):
        if self.ready:
            self.timer += self.window.game.delta * 1.5
            if self.timer >= 2:
                self.timer = 0

    def draw(self, pos=(0, 0)):
        if self.timer < 1 and self.ready:
            super().draw(pos)