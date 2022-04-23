from Source.settings import params
from core.UI.BaseUI import BaseUI
from core.UI.SwapPopUp import SwapPopUp
from core.textures.Tileset import TileSet
import pygame
from math import sin, cos, acos, radians, pi


class StandardBoardUI(BaseUI):
    def __init__(self, window, pos, judge, board):
        super().__init__(window, pos, size=(600, 600))
        # settings
        self.window = window
        self.game = window.game
        self.pos = pos
        self.judge = judge
        self.logic_board = board
        self.size = 50

        # sprites
        self.pieces_tile_set = TileSet('pieces', (50, 150))
        self.board_image = TileSet('board', (440, 440))

        # user interaction
        self.last_mouse_pos = (0, 0)
        self.delta_pos = (0, 0)
        self.focused = None
        self.dragging = False

        # animation
        self.animation_step = 0
        # step 1 wait
        self.wait_server_1 = False
        # step 2 move
        self.move_percent = 0
        self.to_end = 1
        self.move_positions = ((0, 0), (0, 0))
        # step 3 ask user
        # step 4 wait server
        self.wait_server_2 = False
        # step 5 rotation
        self.rotation = 0
        # something
        self.wait = False

    def draw(self, pos=(0, 0)):
        if self.logic_board.get_step() % 2 == 0 and not self.rotation or \
                self.logic_board.get_step() % 2 != 0 and self.rotation:
            if self.rotation:
                img = pygame.transform.rotate(self.board_image[0], 360 + 180 * (1 - self.rotation))
            else:
                img = self.board_image[0]
        else:
            if self.rotation:
                img = pygame.transform.rotate(self.board_image[1], -360 - 180 * (1 - self.rotation))
            else:
                img = self.board_image[1]

        self.game.screen.blit(img, (self.pos[0] - img.get_width() // 2 + 200, self.pos[1] - img.get_width() // 2 + 200))
        layers = {}
        for piece in self.logic_board.get_visible(self.judge.get_color()):
            pos = self.get_pos_from_cell(piece.cr)
            if self.logic_board.get_last_move_piece() and self.move_percent and \
                    piece.cr == self.logic_board.get_last_move_piece().cr:
                pos = [
                    self.move_positions[0][0] + (self.move_positions[1][0] - self.move_positions[0][0]) *
                    (1 - self.move_percent),
                    self.move_positions[0][1] + (self.move_positions[1][1] - self.move_positions[0][1]) *
                    (1 - self.move_percent)
                ]

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

    def event(self, event):
        if self.animation_step or self.wait:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.logic_board.get_step() % 2 == 0:
                piece = self.logic_board.get_piece(((event.pos[0] - self.pos[0]) // self.size,
                                                    (event.pos[1] - self.pos[1]) // self.size))
            else:
                piece = self.logic_board.get_piece((7 - (event.pos[0] - self.pos[0]) // self.size,
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
                goal_movement = [int(event.pos[0] - self.pos[0]) // self.size,
                                 int(event.pos[1] - self.pos[1]) // self.size]

            if self.logic_board.get_step() % 2 == 1:
                goal_movement = [7 - goal_movement[0], 7 - goal_movement[1]]

            move_positions = (self.get_pos_from_cell(self.focused.cr), self.get_pos_from_cell(goal_movement))
            l_pose = self.focused.cr[:]
            if self.logic_board.move(self.focused.cr, goal_movement, False):
                self.judge.on_move(l_pose, goal_movement)
                self.focused = None

                self.animation_step = 1

                self.wait_server_1 = params['mode'] != 'offline'
                self.wait_server_2 = params['mode'] != 'offline' and self.logic_board.check_pawn()[0]

                if not self.dragging:
                    self.move_percent = 1
                    self.move_positions = move_positions

            self.dragging = False

    def animation_update(self):
        if self.animation_step == 1 and not self.wait_server_1:
            self.animation_step += 1
        if self.animation_step == 2 and not self.move_percent:
            self.animation_step += 1
        if self.animation_step == 3 and not self.logic_board.check_pawn()[0]:
            self.animation_step += 1
            for elem in self.window.ui:
                if type(elem) == SwapPopUp:
                    self.window.ui.remove(elem)
                    break
        if self.animation_step == 4 and not self.wait_server_2:
            self.animation_step += 1

            # change step
            self.logic_board.step += 1
            if params['is_on_rotation']:
                self.rotation = 1
        if self.animation_step == 5 and not self.rotation:
            self.animation_step += 1
        if self.animation_step == 6:
            # some to go to next step
            self.animation_step = 0

        if self.animation_step == 2:
            self.move_percent -= 8 * self.game.delta / self.get_dist(*self.move_positions)
            if self.move_percent < 0:
                self.move_percent = 0

        if self.animation_step == 3:
            for elem in self.window.ui:
                if type(elem) == SwapPopUp:
                    break
            else:
                self.window.ui.append(SwapPopUp(self.window, (250, 10), self.judge.get_color() % 2))

        if self.animation_step == 5:
            self.rotation -= (1 + 0.25 * cos(2*pi * self.rotation - pi)) * self.game.delta
            if self.rotation < 0:
                self.rotation = 0

    def fixed_update(self):
        if self.animation_step > 0:
            self.animation_update()

        if not self.logic_board.is_playing:
            self.to_end -= self.window.game.delta
            if self.to_end < 0:
                self.window.game.open_window("Menu")

    def get_dist(self, cell1, cell2):
        return ((cell1[0] - cell2[0])**2 + (cell1[1] - cell2[1])**2)**0.5/50

    def get_pos_from_cell(self, cell):
        center_x = cell[0] * self.size + 25 - 200
        center_y = cell[1] * self.size + 125 - 300
        if center_x == center_y == 0:
            return [300, 300]
        dist = (center_x**2 + center_y**2)**0.5
        rot = acos(center_x/dist)
        if center_y < 0:
            rot = 2*pi - rot
        if self.logic_board.get_step() % 2 == 0:
            return [dist * cos(rot - radians(180 * self.rotation)) + 300 - 25,
                    dist * sin(rot - radians(180 * self.rotation)) + 300 - 135]
        else:
            return [dist * cos(rot + radians(180 * self.rotation) + pi) + 300 - 25,
                    dist * sin(rot + radians(180 * self.rotation) + pi) + 300 - 135]

    def get_pieces_texture(self, name, color):
        names = {'': 0, "R": 1, "K": 2, "Q": 3, "B": 4, "N": 5}
        return self.pieces_tile_set[names[name], color]
