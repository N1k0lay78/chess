import pygame

from Source.settings import params
from core.UI.BaseUI import BaseUI
from core.textures.Tileset import TileSet


def generate_pop_up(size):
    if size[0] < 2 or size[1] < 2:
        raise Exception("you can't make such a small pop-up")
    cell_size = (100, 100)
    surface = pygame.Surface((cell_size[0] * size[0], cell_size[1] * size[1]))
    surface.set_colorkey((0, 0, 0))
    tile_set = TileSet('PopUp', cell_size)
    for i in range(size[1]):
        for j in range(size[0]):
            pos = cell_size[0] * j, cell_size[1] * i
            if i == 0 and j == 0:
                surface.blit(tile_set[0, 0], pos)
            elif i == 0 and j == size[0] - 1:
                surface.blit(tile_set[2, 0], pos)
            elif i == size[1] - 1 and j == size[0] - 1:
                surface.blit(tile_set[2, 2], pos)
            elif i == size[1] - 1 and j == 0:
                surface.blit(tile_set[0, 2], pos)
            elif i == 0:
                surface.blit(tile_set[1, 0], pos)
            elif i == size[1] - 1:
                surface.blit(tile_set[1, 2], pos)
            elif j == 0:
                surface.blit(tile_set[0, 1], pos)
            elif j == size[0] - 1:
                surface.blit(tile_set[2, 1], pos)
            else:
                surface.blit(tile_set[1, 1], pos)
    return surface


class PopUp(BaseUI):
    def __init__(self, window, pos, size=[2, 2], buttons=[]):
        pos = list(pos)
        super().__init__(window, pos, buttons, generate_pop_up(size), un_active_on_mouse_up=False)
        self.mouse_last_pos = (0, 0)
        self.dragging = False
        self.active = None
        self.size = (100 * size[0], 100 * size[1])

    def check_collide_point(self, pos):
        for element in self.child:
            element.check_collide_point(pos)

        pos = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
        self.hovered = 0 <= pos[0] <= self.size[0] and 0 <= pos[1] <= self.size[1]
        return self.hovered

    def move(self, move):
        super().move(move)
        self.check_pos()

    def update(self):
        if self.active:
            self.active.update()

    def event(self, event):
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for elem in self.child:
                if elem.check_collide_point(event.pos) and type(elem) != BaseUI:
                    if self.active:
                        self.active.on_disactive()
                    self.active = elem
                    self.dragging = False
                    break
            else:
                if self.check_collide_point(event.pos):
                    self.dragging = True
                self.active = None
            self.mouse_last_pos = event.pos
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.move((event.pos[0] - self.mouse_last_pos[0], event.pos[1] - self.mouse_last_pos[1]))
            self.mouse_last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        if self.active:
            self.active.event(event)

    def check_pos(self):
        if 0 > self.pos[0]:
            self.pos[0] = 0
        elif self.pos[0] > params['screen_size'][0] - self.size[0]:
            self.pos[0] = params['screen_size'][0] - self.size[0]

        if 0 > self.pos[1]:
            self.pos[1] = 0
        elif self.pos[1] > params['screen_size'][1] - self.size[1]:
            self.pos[1] = params['screen_size'][1] - self.size[1]
