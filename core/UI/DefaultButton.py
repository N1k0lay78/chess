import pygame

from core.UI.Button import Button
from core.textures.Tileset import TileSet


def generate_textures(render, data, width, colors=((230, 81, 0), (255, 143, 0))):
    size = (50, 50)
    tile_set = TileSet("Button", size)
    surface = pygame.Surface((size[0] * width, size[1] * 3))
    surface.fill((1, 1, 1))
    surface.set_colorkey((1, 1, 1))

    delta = [0, 2, 6]
    if type(data) == str:
        content = render(data, colors[0])
        content_pos = ((width * size[0] - content.get_width()) / 2 - 2, 6)
    else:
        content = data
        content_pos = (0, 0)

    # draw background
    for i in range(3):
        for j in range(width):
            pos = [j * size[0], i * size[1]]
            if j == width - 1 == 0:
                surface.blit(tile_set[3, i], pos)
            elif j == 0:
                surface.blit(tile_set[0, i], pos)
            elif j == width - 1:
                surface.blit(tile_set[2, i], pos)
            else:
                surface.blit(tile_set[1, i], pos)
            # surface.blit(bg_text, (text_pos[0], size[1] * i + delta[i] + delta_text))
            surface.blit(content, (content_pos[0], content_pos[1] + size[1] * i + delta[i]))
    return TileSet(surface, (size[0] * width, size[1]))


class DefaultButton(Button):
    def __init__(self, window, pos, data, width, function=None):
        super().__init__(window, pos, generate_textures(window.game.render_text, data, width), (0, 1, 2))
        self.function = function

    def on_click(self):
        if self.function:
            self.function(self)