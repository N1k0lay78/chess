import pygame

from core.pieces.Pieces import Pieces


class Board:
    def __init__(self, game, pos, size, color_w, color_b):
        self.game = game
        self.position = pos
        self.size = size
        self.color_w = color_w
        self.color_b = color_b
        self.surface = pygame.Surface((8 * size[0], 8 * size[1]))
        self.generate_surface()
        self.focused = None
        self.dragging = False
        self.set_on_next = False
        self.last_mouse_pos = (0, 0)
        self.pieces_texture = pygame.image.load('Source/Image/pieces.png')
        # Pieces(self.game, (0, 0), self.pieces_texture.subsurface((0, 0, 50, 150)))
        self.board = []

    def draw(self):
        self.game.screen.blit(self.surface, self.position)
        for piece in self.board:
                piece.draw()

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.last_mouse_pos = event.pos
            pos = ((event.pos[0] - self.position[0]) // self.size[0], (event.pos[1] - self.position[1]) // self.size[1])
            if not self.set_on_next or (self.focused and pos == self.focused.cell):
                self.dragging = True
                self.set_on_next = False
                self.last_mouse_pos = event.pos
                if not self.focused:
                    self.focused = self.get_pos(pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.focused and not self.set_on_next:
                self.focused.move((self.last_mouse_pos[0] - event.pos[0], self.last_mouse_pos[1] - event.pos[1]))
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            print(self.focused, self.set_on_next)
            if self.focused and not self.set_on_next:
                self.dragging = False
                pos = ((event.pos[0] - self.position[0]) // self.size[0], (event.pos[1] - self.position[1]) // self.size[1])
                print(self.focused.cell, pos)
                if self.focused.cell != pos:
                    self.focused.update(pos)
                else:
                    self.set_on_next = True
            elif self.set_on_next:
                last_pos = ((self.last_mouse_pos[0] - self.position[0]) // self.size[0], (self.last_mouse_pos[1] - self.position[1]) // self.size[1])
                pos = ((event.pos[0] - self.position[0]) // self.size[0], (event.pos[1] - self.position[1]) // self.size[1])
                if last_pos == pos:
                    self.focused.update(pos)
                    self.set_on_next = False

    def get_pos(self, pos):
        for i in range(len(self.board) - 1, -1, -1):
            if self.board[i].cell == pos:
                return self.board[i]

    def generate_surface(self):
        for i in range(8):
            for j in range(8):
                if i % 2 != j % 2:
                    pygame.draw.rect(self.surface, self.color_b,
                                     [self.size[0] * i, self.size[1] * j, *self.size])
                else:
                    pygame.draw.rect(self.surface, self.color_w,
                                     [self.size[0] * i, self.size[1] * j, *self.size])
        pygame.image.save(self.surface, "tmp.png")

    def generate_board(self):
        self.board = []
        for i in range(8):
            self.board.append(Pieces(self.game, (i, 1), self.pieces_texture.subsurface((0, 0, 50, 150)), 'b'))
            self.board.append(Pieces(self.game, (i, 6), self.pieces_texture.subsurface((0, 150, 50, 150)), 'w'))
            if i % 7 == 0:
                self.board.append(Pieces(self.game, (i, 0), self.pieces_texture.subsurface((50, 0, 50, 150)), 'b'))
                self.board.append(Pieces(self.game, (i, 7), self.pieces_texture.subsurface((50, 150, 50, 150)), 'w'))
            if i % 5 == 1:
                self.board.append(Pieces(self.game, (i, 0), self.pieces_texture.subsurface((250, 0, 50, 150)), 'b'))
                self.board.append(Pieces(self.game, (i, 7), self.pieces_texture.subsurface((250, 150, 50, 150)), 'w'))
            if i % 3 == 2:
                self.board.append(Pieces(self.game, (i, 0), self.pieces_texture.subsurface((200, 0, 50, 150)), 'b'))
                self.board.append(Pieces(self.game, (i, 7), self.pieces_texture.subsurface((200, 150, 50, 150)), 'w'))
            if i == 3:
                self.board.append(Pieces(self.game, (i, 0), self.pieces_texture.subsurface((100, 0, 50, 150)), 'b'))
                self.board.append(Pieces(self.game, (i, 7), self.pieces_texture.subsurface((100, 150, 50, 150)), 'w'))
            if i == 4:
                self.board.append(Pieces(self.game, (i, 0), self.pieces_texture.subsurface((150, 0, 50, 150)), 'b'))
                self.board.append(Pieces(self.game, (i, 7), self.pieces_texture.subsurface((150, 150, 50, 150)), 'w'))
