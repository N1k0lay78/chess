import pygame

from Source.settings import params
from core.UI.PressAnyKeyUI import PressAnyKey
from core.UI.TransformLogo import TransformLogo
from core.textures.load_image import load_image
from core.windows.Window import Window


class LoadingWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        center_sc = params["screen_size"][0]//2, params["screen_size"][1]//2
        center = center_sc[0], center_sc[1]
        self.transformLogo = [TransformLogo(self, center, load_image('TestLogo'), 114/6, 114*2, 1)]
        self.active = PressAnyKey(self, (0, 0), "нажмите любую кнопку")
        self.active.pos = [
            (params["screen_size"][0] - self.active.image.get_size()[0]) // 2,
            params["screen_size"][1] - 75
        ]
        self.timer = params["loading_window_time"]

    def fixed_update(self):
        self.active.fixed_update()

    def update(self):
        [x.update() for x in self.transformLogo]
        self.timer -= self.game.delta
        if self.timer < params["loading_window_time"] - 2:
            self.active.set_ready()
        if self.timer < 0:
            self.game.open_window(params["start_window"])

    def draw(self):
        self.game.screen.fill((245, 127, 23))
        [x.draw() for x in self.transformLogo]
        self.active.draw()
