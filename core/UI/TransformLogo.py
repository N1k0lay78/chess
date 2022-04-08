import pygame

from core.UI.BaseUI import BaseUI


class TransformLogo(BaseUI):
    def __init__(self, window, center, img, start_height, end_height, time, st_time=0):
        super().__init__(window, center, image=img)
        self.center = center
        self.otnosh = self.image.get_width() / self.image.get_height()
        self.start_height = start_height
        self.delta_height = end_height - start_height
        self.time = st_time
        self.end_time = time
        self.percent = 0

    def update(self):
        if self.percent != 1:
            self.time += self.window.game.delta
        self.percent = min(1, self.time / self.end_time)

    def draw(self, pos=(0, 0)):
        if 0 <= self.percent <= 1:
            size = int((self.start_height + self.delta_height * self.percent ** 2)*self.otnosh), int(self.start_height + self.delta_height * self.percent ** 2)
            self.window.game.screen.blit(pygame.transform.scale(self.image, size),
                                    (self.center[0] - size[0] // 2, self.center[1] - size[1] // 2))
