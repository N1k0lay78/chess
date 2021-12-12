import pygame

from core.UI.BaseUI import BaseUI


class PopUp(BaseUI):
    def __init__(self, window, pos, content, buttons=[]):
        super().__init__(window, pos, buttons, content)
        self.mouse_last_pos = (0, 0)

    def update(self, event):
        super().update(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_last_pos = event.pos
        elif event.type == pygame.MOUSEMOTION:
            self.move((event.pos[0] - self.mouse_last_pos[0], event.pos[1] - self.mouse_last_pos[1]))
            self.mouse_last_pos = event.pos