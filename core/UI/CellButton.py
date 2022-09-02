import pygame
from core.textures.Tileset import TileSet
from Source.animations import bg_light_anim
from core.UI.BaseUI import BaseUI


class PlayButton(BaseUI):
    def __init__(self, window, pos, image, on_funk=None, pre_funk=None, size=None):
        if size is None:
            size = (100, 100)
        super().__init__(window, pos, image=image, size=size)
        self.tile_set = TileSet("BgLight", (100, 100))
        self.timer = 0
        self.animation_step = 0
        self.animation = ""
        self.pressed = False
        self.on_funk = on_funk
        self.pre_funk = pre_funk

    def fixed_update(self):
        if (self.pressed or self.hovered)and self.animation not in ["in", "hovered"]:
            self.animation = "in"
        elif not (self.pressed or self.hovered)and self.animation in ["in", "hovered"]:
            self.animation = "out"

        if self.y_pos > set_point:
            self.y_pos -= self.window.game.delta * 40
            if self.y_pos < set_point:
                self.y_pos = set_point
        elif self.y_pos < set_point:
            self.y_pos += self.window.game.delta * 60
            if self.y_pos > set_point:
                self.y_pos = set_point

    def event(self, event):
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pressed = True
            self.on_press()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
            if self.check_collide_point(event.pos):
                self.on_click()

    def draw(self, pos=(0, 0)):
        tmp = list(map(lambda x: (x[0] - x[1]) / 2, zip(self.get_size(), self.image.get_size())))
        pos = [tmp[0] + pos[0], tmp[1] + pos[1] - self.y_pos]
        super().draw(pos)

    def on_click(self):
        if self.on_funk:
            self.on_funk(self)

    def on_press(self):
        if self.pre_funk:
            self.pre_funk(self)


# 37
# zxyw
# 457380
# 21

# 8 12 16 26 27
# 19 20 21