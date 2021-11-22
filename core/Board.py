import pygame

from core.pieces.King import King
from core.pieces.Pieces import Pieces
from core.pieces.Pawn import Pawn
from core.pieces.Horse import Horse
from core.pieces.Elephant import Elephant
from core.pieces.Queen import Queen
from core.pieces.Rook import Rook


class Board:
    def __init__(self, game, pos, size, color_w, color_b):
        # logic
        self.game = game
        self.position = pos
        self.size = size
        self.board = []
        self.step = 0
        # control
        self.focused = None
        self.dragging = False
        self.set_on_next = False
        self.last_mouse_pos = (0, 0)
        # surfaces
        self.pieces_texture = pygame.image.load('Source/Image/pieces.png')
        self.color_w = color_w
        self.color_b = color_b
        self.surface = pygame.Surface((8 * size[0], 8 * size[1]))
        self.generate_surface()

    def draw(self):
        self.game.screen.blit(self.surface, self.position)
        for piece in self.board:
                piece.draw()

    def update(self, event):
        """
        use:
        focused - action figure
        dragging - is moving figure
        set_on_next - ???
        last_mouse_pos - move from last action
        step - black move if step % 2 else white move
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.last_mouse_pos = event.pos
            figure = self.get_pos(((event.pos[0] - self.position[0]) // self.size[0], (event.pos[1] - self.position[1]) // self.size[1]))
            if figure != None and figure.color == self.step % 2:
                self.focused = figure
                print(type(self.focused))
                self.dragging = True
            elif figure is None:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.focused:
                self.focused.move((self.last_mouse_pos[0] - event.pos[0], self.last_mouse_pos[1] - event.pos[1]))
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            if self.focused:
                self.focused.update(((event.pos[0] - self.position[0]) // self.size[0], (event.pos[1] - self.position[1]) // self.size[1]))

    def get_pos(self, pos):
        for i in range(len(self.board) - 1, -1, -1):
            if self.board[i].cell == pos:
                return self.board[i]

    def remove_from_board(self, piece):
        if piece:
            if type(piece) == King:
                print(f"win is {'white' if piece.color == 'b' else 'black'}")
                self.generate_board()
            else:
                self.board.remove(piece)

    def go_to_next_step(self):
        self.step += 1

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
            self.board.append(Pawn(self.game, (i, 1), self.pieces_texture.subsurface((0, 0, 50, 150)), 1))
            self.board.append(Pawn(self.game, (i, 6), self.pieces_texture.subsurface((0, 150, 50, 150)), 0))
            if i % 7 == 0:
                self.board.append(Rook(self.game, (i, 0), self.pieces_texture.subsurface((50, 0, 50, 150)), 1))
                self.board.append(Rook(self.game, (i, 7), self.pieces_texture.subsurface((50, 150, 50, 150)), 0))
            if i % 5 == 1:
                self.board.append(Horse(self.game, (i, 0), self.pieces_texture.subsurface((250, 0, 50, 150)), 1))
                self.board.append(Horse(self.game, (i, 7), self.pieces_texture.subsurface((250, 150, 50, 150)), 0))
            if i % 3 == 2:
                self.board.append(Elephant(self.game, (i, 0), self.pieces_texture.subsurface((200, 0, 50, 150)), 1))
                self.board.append(Elephant(self.game, (i, 7), self.pieces_texture.subsurface((200, 150, 50, 150)), 0))
            if i == 3:
                self.board.append(Queen(self.game, (i, 0), self.pieces_texture.subsurface((100, 0, 50, 150)), 1))
                self.board.append(Queen(self.game, (i, 7), self.pieces_texture.subsurface((100, 150, 50, 150)), 0))
            if i == 4:
                self.board.append(King(self.game, (i, 0), self.pieces_texture.subsurface((150, 0, 50, 150)), 1))
                self.board.append(King(self.game, (i, 7), self.pieces_texture.subsurface((150, 150, 50, 150)), 0))
