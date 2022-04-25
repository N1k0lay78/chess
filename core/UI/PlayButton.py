import pygame
from Source.settings import params
from core.UI.Button import Button
from core.textures.Tileset import TileSet


def create_tile_set(game, text):
    rendered_text = game.render_text(text, (251, 192, 45), False)
    rendered_back_text = game.render_text(text, (249, 168, 37), False)
    surface = pygame.Surface((rendered_text.get_width(), 180))
    surface.set_colorkey((0, 0, 0))
    surface.blit(rendered_text,      (-3, 0))
    surface.blit(rendered_back_text, (-3, 4))
    surface.blit(rendered_text,      (-3, 62))
    surface.blit(rendered_back_text, (-3, 64))
    surface.blit(rendered_text,      (-3, 124))
    return TileSet(surface, (rendered_text.get_width(), 60))


class PlayButton(Button):
    def __init__(self, window, pos, text, open_window, settings):
        super().__init__(window, pos, create_tile_set(window.game, text), size=[400, 100])
        self.open_window = open_window
        self.settings = settings

    def draw(self, pos=(0, 0)):
        tmp = list(map(lambda x: (x[0] - x[1]) / 2, zip(self.get_size(), self.image.get_size())))
        pos = [tmp[0] + pos[0], tmp[1] + pos[1]]
        super().draw(pos)

    def on_click(self):
        for key, val in self.settings.items():
            params[key] = val
        self.window.game.open_window(self.open_window)
