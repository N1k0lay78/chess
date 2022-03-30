import pygame

from core.UI.BaseUI import BaseUI
from core.textures.Tileset import TileSet


class CheckBox(BaseUI):
    def __init__(self, window, pos, text, is_active=False):
        super().__init__(window, pos)
        self.check_box_tile_set = TileSet("CheckBox", (25, 25))
        self.active = is_active
        self.text = text
        a = self.window.game.render_text(self.text, (0, 0, 0))
        self.size = [30 + a.get_width(), a.get_height()]

    def get_active(self):
        return self.active

    def set_active(self, val):
        self.active = val

    def check_hover(self, event):
        self.hovered = self.check_collide_point(event.pos)

    def check_collide_point(self, pos):
        size = self.size
        if self.pos[0] <= pos[0] <= self.pos[0] + size[0] and self.pos[1] <= pos[1] <= self.pos[1] + size[1]:
            return True

    def draw(self, pos=(0, 0)):
        pos = (self.pos[0] + pos[0], self.pos[1] + pos[1])
        if self.hovered:
            self.window.game.screen.blit(self.check_box_tile_set[1], pos)
        if not self.active:
            self.window.game.screen.blit(self.check_box_tile_set[0], pos)
            self.window.game.screen.blit(self.window.game.render_text(
                self.text, (0, 255 if self.hovered else 0, 0)),
                (pos[0] + 30, pos[1] - 2)
            )
        else:
            self.window.game.screen.blit(self.check_box_tile_set[2], pos)
            self.window.game.screen.blit(self.window.game.render_text(
                self.text, (255, 255 if self.hovered else 0, 0)),
                (pos[0] + 30, pos[1] - 2)
            )

    def event(self, event):
        super().event(event)
        if event.type == pygame.MOUSEBUTTONUP and self.check_collide_point(event.pos):
            self.active = not self.active
