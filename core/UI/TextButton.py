import pygame

from core.UI.Button import Button
from core.textures.Tileset import TileSet


def create_tile_set(game, text):
    rendered_text = game.render_text(text, (191, 54, 12), False)
    rendered_back_text = game.render_text(text, (230, 74, 25), False)
    surface = pygame.Surface((rendered_text.get_width(), 180))
    surface.set_colorkey((0, 0, 0))
    surface.blit(rendered_back_text, (-3, 4))
    surface.blit(rendered_text,      (-3, 0))
    surface.blit(rendered_back_text, (-3, 64))
    surface.blit(rendered_text,      (-3, 62))
    surface.blit(rendered_text,      (-3, 124))
    return surface, (rendered_text.get_width(), 60)


class TextButton(Button):
    def __init__(self, window, pos, text):
        super().__init__(window, pos, TileSet(*create_tile_set(window.game, text)), (0, 1, 2))
