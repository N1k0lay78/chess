import pygame
from core.UI.BaseUI import BaseUI


def create_tile_set(game, text):
    rendered_text = game.render_text(text, (251, 192, 45), False)
    rendered_back_text = game.render_text(text, (249, 168, 37), False)
    surface = pygame.Surface((rendered_text.get_width(), rendered_text.get_height() + 4))
    surface.set_colorkey((0, 0, 0))
    surface.blit(rendered_text,      (-3, 0))
    surface.blit(rendered_back_text, (-3, 4))
    return surface


class PlayButton(BaseUI):
    def __init__(self, window, pos, text: str, on_funk=None, pre_funk=None, size=None):
        if size is None:
            size = [400, 100]
        if type(text) == str:
            content = create_tile_set(window.game, text)
        else:
            content = text
        super().__init__(window, pos, image=content, size=size)
        self.y_pos = 0
        self.pressed = False
        self.on_funk = on_funk
        self.pre_funk = pre_funk

    def fixed_update(self):
        set_point = 0
        if self.pressed:
            set_point = 2
        elif self.hovered:
            set_point = 4
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
