import pygame

from Source.settings import params
from core.UI.BaseUI import BaseUI
from core.textures.Tileset import TileSet
from loguru import logger


class PlayerTypeSelect(BaseUI):
    def __init__(self, window, pos, selected, editable):
        self.tile_set = TileSet("PlayerType", (75, 75))
        super().__init__(window, pos, childs=[PlayerTypeSelectChoice(window, self.tile_set)])
        self.selected = selected
        self.open_select = False
        self.editable = editable
        self.hovered = -1

    def draw(self, pos=(0, 0)):
        pos = [pos[0] + self.pos[0], pos[1] + self.pos[1]]
        if not self.editable:
            self.window.game.screen.blit(self.tile_set[1, 4], pos)
        else:
            self.window.game.screen.blit(self.tile_set[0, 3], pos)
            self.window.game.screen.blit(self.tile_set[1, 3], (pos[0] + 75, pos[1]))
        if self.open_select:
            self.child[0].draw(pos)
        self.window.game.screen.blit(self.tile_set[1, self.selected], pos)
        # print(self.hovered)
        if self.hovered == 0:
            self.window.game.screen.blit(self.tile_set[0, 4], pos)

    def check_collide_point(self, pos):
        pos = self.get_pos(pos)

        if 0 <= pos[0] <= 105 and 0 <= pos[1] <= 75:
            return True
        if self.open_select and 0 <= pos[0] <= 75 and 0 <= pos[1] <= 210:
            return True
        return False

    def event(self, event):
        if self.editable:
            if event.type == pygame.MOUSEBUTTONUP and self.check_collide_point(event.pos):
                if self.open_select:
                    pos = self.get_pos(event.pos)
                    self.set_choice(self.child[0].values[pos[1] // 75])
                self.open_select = not self.open_select

    def check_hover(self, event):
        pos = self.get_pos(event.pos)
        if 0 <= pos[0] <= 110 and 0 <= pos[1] < 75:
            self.hovered = 0
        elif 0 <= pos[0] <= 75 and 0 <= pos[1] <= 210:
            self.hovered = pos[1] // 75
        else:
            self.hovered = -1

    def get_pos(self, pos):
        if self.parent:
            pos = [pos[0] - self.pos[0] - self.parent.pos[0], pos[1] - self.pos[1] - self.parent.pos[1]]
        else:
            pos = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
        return pos

    def set_choice(self, value):
        logger.info(f"user {params['nickname']} choice {['White', 'Black', 'Viewer'][value]}")
        self.selected = value

    def on_disactive(self):
        self.open_select = False


class PlayerTypeSelectChoice(BaseUI):
    def __init__(self, window, tile_set):
        super().__init__(window, (0,0))
        self.tile_set = tile_set
        self.values = [0, 0]

    def draw(self, pos=(0, 0)):
        pos = [pos[0] + self.pos[0], pos[1] + self.pos[1]]
        self.window.game.screen.blit(self.tile_set[0, 0], pos)
        self.window.game.screen.blit(self.tile_set[0, 1], (pos[0], pos[1] + 75))
        self.window.game.screen.blit(self.tile_set[0, 2], (pos[0], pos[1] + 150))
        k = 1
        self.values = [self.parent.selected]
        for i in range(3):
            if i != self.parent.selected:
                self.window.game.screen.blit(self.tile_set[1, i], (pos[0], pos[1] + 70 * k))
                self.values.append(i)
                if self.parent.hovered == k:
                    self.window.game.screen.blit(self.tile_set[0, 4], (pos[0], pos[1] + 70 * k))
                k += 1

