from Source.animations import fog
from core.pieces.Horse import Horse
from core.pieces.King import King
from core.pieces.Pawn import Pawn
from core.pieces.Queen import Queen
from core.textures.Tileset import TileSet
import pygame


class FogOfWar:
    def __init__(self, game, pos, padding_count, size, filename, color):
        self.color = color
        self.game = game
        self.pos = pos
        self.padding = padding_count
        self.size = size
        self.tile_set = TileSet(filename, (50, 50))
        self.map = []
        self.update()
        self.tic = 0
        self.time = pygame.time.Clock()
        self.update()

    def update(self):
        self.map = [[1] * (8 + self.padding * 2) for _ in range(8 + self.padding * 2)]
        for figure in self.game.board.board:
            if figure.color == self.game.color:
                if type(figure) == Pawn:
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding - 1] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding - 1] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding + 1] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding + 1] = 0
                if type(figure) in [Horse, King, Queen]:
                    self.map[figure.cell[1] + self.padding + 1][figure.cell[0] + self.padding - 2] = 0
                    self.map[figure.cell[1] + self.padding + 1][figure.cell[0] + self.padding - 1] = 0
                    self.map[figure.cell[1] + self.padding + 1][figure.cell[0] + self.padding] = 0
                    self.map[figure.cell[1] + self.padding + 1][figure.cell[0] + self.padding + 1] = 0
                    self.map[figure.cell[1] + self.padding + 1][figure.cell[0] + self.padding + 2] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding - 2] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding - 1] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding + 1] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding + 2] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding - 2] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding - 1] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding + 1] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding + 2] = 0
                else:
                    self.map[figure.cell[1] + self.padding + 1][figure.cell[0] + self.padding] = 0
                    self.map[figure.cell[1] + self.padding + 1][figure.cell[0] + self.padding - 1] = 0
                    self.map[figure.cell[1] + self.padding + 1][figure.cell[0] + self.padding + 1] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding - 1] = 0
                    self.map[figure.cell[1] + self.padding][figure.cell[0] + self.padding + 1] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding - 1] = 0
                    self.map[figure.cell[1] + self.padding - 1][figure.cell[0] + self.padding + 1] = 0

    def draw(self):
        for x in range(8 + self.padding * 2):
            for y in range(8 + self.padding * 2):
                # print(*self.map, sep='\n')
                if self.map[y][x]:
                    self.game.screen.blit(self.tile_set[fog['full'][0]], (x * self.size[0] + self.pos[0], y * self.size[1] + self.pos[1]))
                elif 1 <= x < self.padding * 2 + 7 and 1 <= y < self.padding * 2 + 7:
                    if self.map[y + 1][x] and not self.map[y - 1][x] and self.map[y][x + 1] and not self.map[y][x - 1]:
                        self.game.screen.blit(self.tile_set[fog['bottom-right'][0]], (x * self.size[0] + self.pos[0], y * self.size[1] + self.pos[1]))
                    elif self.map[y + 1][x] and not self.map[y - 1][x] and not self.map[y][x + 1] and self.map[y][x - 1]:
                        self.game.screen.blit(self.tile_set[fog['bottom-left'][0]], (x * self.size[0] + self.pos[0], y * self.size[1] + self.pos[1]))
                    elif not self.map[y + 1][x] and self.map[y - 1][x] and self.map[y][x + 1] and not self.map[y][x - 1]:
                        self.game.screen.blit(self.tile_set[fog['top-right'][0]], (x * self.size[0] + self.pos[0], y * self.size[1] + self.pos[1]))
                    elif not self.map[y + 1][x] and self.map[y - 1][x] and not self.map[y][x + 1] and self.map[y][x - 1]:
                        self.game.screen.blit(self.tile_set[fog['top-left'][0]], (x * self.size[0] + self.pos[0], y * self.size[1] + self.pos[1]))
                    elif not self.map[y + 1][x] and self.map[y - 1][x] and not self.map[y][x + 1] and not self.map[y][x - 1]:
                        self.game.screen.blit(self.tile_set[fog['top'][0]], (x * self.size[0] + self.pos[0], y * self.size[1] + self.pos[1]))
                    elif self.map[y + 1][x] and not self.map[y - 1][x] and not self.map[y][x + 1] and not self.map[y][x - 1]:
                        self.game.screen.blit(self.tile_set[fog['bottom'][0]], (x * self.size[0] + self.pos[0], y * self.size[1] + self.pos[1]))
                    elif not self.map[y + 1][x] and not self.map[y - 1][x] and self.map[y][x + 1] and not self.map[y][x - 1]:
                        self.game.screen.blit(self.tile_set[fog['right'][0]], (x * self.size[0] + self.pos[0], y * self.size[1] + self.pos[1]))
                    elif not self.map[y + 1][x] and not self.map[y - 1][x] and not self.map[y][x + 1] and self.map[y][x - 1]:
                        self.game.screen.blit(self.tile_set[fog['left'][0]], (x * self.size[0] + self.pos[0], y * self.size[1] + self.pos[1]))
