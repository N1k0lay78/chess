from core.online.logic.Board import LogicBoard
from core.textures.load_image import load_image
from core.textures.Tileset import TileSet
from Source.settings import name_board_to_play
from Source.boards import boards
import pygame
from math import sin, cos, acos, radians, pi


class StandardBoardUI:
    def __init__(self, window, pos, judge, board):
        # settings
        self.window = window
        self.game = window.game
        self.pos = pos
        self.judge = judge
        self.size = 50
        # sprites
        self.pieces_tile_set = TileSet('pieces', (50, 150))
        self.board_image = load_image('board')
        # create logic board
        self.logic_board = board
        # user interaction
        self.last_mouse_pos = (0, 0)
        self.delta_pos = (0, 0)
        self.focused = None
        self.dragging = False
        self.wait = False
        self.timer = 7

    def draw(self):
        img = pygame.transform.rotate(self.board_image, -90 * self.timer)
        self.game.screen.blit(img, (self.pos[0] - img.get_width() // 2 + 200, self.pos[1] - img.get_width() // 2 + 200))
        layers = {}
        for piece in self.logic_board.get_visible(self.judge.get_color()):
            pos = self.get_pos_from_cell(piece.cr)
            if piece == self.focused and self.dragging:
                layers[10000] = [(piece, pos)]
            if pos[1] in layers:
                layers[pos[1]].append((piece, pos))
            else:
                layers[pos[1]] = [(piece, pos)]

        for layer in sorted(layers):
            for piece, pos in layers[layer]:
                if not self.focused or piece.cr != self.focused.cr:
                    if self.logic_board.get_last_move_piece() and \
                            self.logic_board.get_last_move_piece().cr == piece.cr:
                        self.game.screen.blit(self.get_pieces_texture(piece.t, 2), pos)
                    self.game.screen.blit(self.get_pieces_texture(*piece.ts), pos)
                elif self.dragging:
                    self.game.screen.blit(self.get_pieces_texture(piece.t, 2),
                                          (self.last_mouse_pos[0] + self.delta_pos[0],
                                           self.last_mouse_pos[1] + self.delta_pos[1]))
                    self.game.screen.blit(self.get_pieces_texture(*piece.ts),
                                          (self.last_mouse_pos[0] + self.delta_pos[0],
                                           self.last_mouse_pos[1] + self.delta_pos[1]))
                else:
                    self.game.screen.blit(self.get_pieces_texture(piece.t, 2), pos)
                    self.game.screen.blit(self.get_pieces_texture(*piece.ts), pos)
                # pygame.draw.circle(self.game.screen, (255, 250, 250),
                #                    (self.get_pos_from_cell(piece.cr)[0] , self.get_pos_from_cell(piece.cr)[1] ), 5)

    def event(self, event):
        if self.wait or self.timer != 0:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.logic_board.get_step() % 2 == 0:
                piece = self.logic_board.get_piece(((event.pos[0] - self.pos[0]) // self.size,
                                                    (event.pos[1] - self.pos[1]) // self.size))
            else:
                piece = self.logic_board.get_piece((7 -(event.pos[0] - self.pos[0]) // self.size,
                                                    7 - (event.pos[1] - self.pos[1]) // self.size))
            if piece and piece.s == self.judge.get_color() == self.logic_board.get_step() % 2:
                self.focused = piece
                self.dragging = True
                piece_pos = self.get_pos_from_cell(piece.cr)
                self.delta_pos = (piece_pos[0] - event.pos[0], piece_pos[1] - event.pos[1])
            if piece is None:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and self.focused:
            if self.dragging:
                goal_movement = [int(event.pos[0] + self.delta_pos[0] + 25 - self.pos[0]) // self.size,
                                 int(event.pos[1] + self.delta_pos[1] + 135 - self.pos[1]) // self.size]
            else:
                goal_movement = [int(event.pos[0] + self.delta_pos[0] - self.pos[0]) // self.size,
                                 int(event.pos[1] + self.delta_pos[1] + 100 - self.pos[1]) // self.size]
            if self.logic_board.get_step() % 2 == 1:
                goal_movement = [7 - goal_movement[0], 7 - goal_movement[1]]
            print(goal_movement)
            if self.logic_board.move(self.focused.cr, goal_movement):
                self.focused = None
                self.timer = 2

            self.dragging = False

    def update(self):
        if self.timer > 0:
            self.timer -= self.game.delta*10
            if self.timer < 0:
                self.timer = 0

    def get_pos_from_cell(self, cell):
        center_x = cell[0] * self.size + 25 - 200
        center_y = cell[1] * self.size + 125 - 300
        if center_x == center_y == 0:
            return [300, 300]
        # return center_x + 300, center_y + 300
        dist = (center_x**2 + center_y**2)**0.5
        rot = acos(center_x/dist)
        if center_y < 0:
            rot = 2*pi - rot
        if self.logic_board.get_step() % 2 == 0:
            return [dist * cos(rot + radians(90 * self.timer)) + 300 - 25,
                    dist * sin(rot + radians(90 * self.timer)) + 300 - 125]
        else:
            return [dist * cos(rot + radians(90 * self.timer) + pi) + 300 - 25,
                    dist * sin(rot + radians(90 * self.timer) + pi) + 300 - 125]

    def get_pieces_texture(self, name, color):
        names = {'': 0, "R": 1, "K": 2, "Q": 3, "B": 4, "N": 5}
        return self.pieces_tile_set[names[name], color]