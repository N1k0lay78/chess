import pygame

from Source.settings import params
from core.UI.PressAnyKeyUI import PressAnyKey
from core.UI.TransformLogo import TransformLogo
from core.textures.load_image import load_image
from core.windows.Window import Window


class LoadingWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.timer = params["loading_window_time"]

    def set_ui(self):
        center_sc = params["screen_size"][0]//2, params["screen_size"][1]//2
        center = center_sc[0], center_sc[1]
        self.ui = {
            "Logo": [
                TransformLogo(self, center, load_image('TestLogo'), 114/6, 114*2, 1),
             ],
            "PressAnyKey": [
                PressAnyKey(self, (0, 0), "нажмите любую кнопку"),
            ],
        }
        self.set_active_object(self.ui["PressAnyKey"][0])
        self.active.pos = [
            (params["screen_size"][0] - self.active.image.get_size()[0]) // 2,
            params["screen_size"][1] - 100
        ]

    def set_active(self, event):
        pass

    def update(self):
        super().update()
        self.timer -= self.game.delta
        if self.timer < params["loading_window_time"] - 2:
            self.active.set_ready()
        if self.timer < 0:
            self.game.open_window(params["after_load"])

    def draw(self):
        self.game.screen.fill((245, 127, 23))
        super().draw()
