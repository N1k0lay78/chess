import pygame

from core.UI.BaseUI import BaseUI


class Button(BaseUI):
    def __init__(self, window, pos, tile_set, frames):
        super().__init__(window, pos, image=tile_set[frames[0]])
        self.tile_set = tile_set
        self.frames = frames  # 0 - default, 1 - hovered, 2 - clicked
        self.pressed = False

    def check_collide_update(self):
        self.image = self.tile_set[self.frames[self.hovered]]

    def on_press(self):
        pass

    def while_pressed(self):
        pass

    def on_un_press(self):
        pass

    def on_click(self):
        pass

    def update(self, event):
        super().update(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.image = self.tile_set[self.frames[2]]
            self.on_press()
            self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.image = self.tile_set[self.frames[self.hovered]]
            self.on_un_press()
            if self.check_collide_point(event.pos):
                self.on_click()
            self.pressed = False
        elif self.pressed:
            self.while_pressed()