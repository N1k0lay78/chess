import pygame

from core.pieces.King import King
from core.pieces.Pawn import Pawn
from core.pieces.Horse import Horse
from core.pieces.Elephant import Elephant
from core.pieces.Queen import Queen
from core.pieces.Rook import Rook
from core.textures.Tileset import TileSet


class Board:
    def __init__(self, game, pos, size):
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
        self.pieces_tile_set = TileSet('pieces', (50, 150))
        self.surface = pygame.image.load('Source/Image/board.png')

    def draw(self):
        # draw the background
        self.game.screen.blit(self.surface, self.position)
        # draw the figures
        layers = {}
        for piece in self.board:
            if self.focused == piece and self.dragging:
                layers[100000] = [piece]
            if piece.pos[1] in layers:
                layers[piece.pos[1]].append(piece)
            else:
                layers[piece.pos[1]] = [piece]
        for key in sorted(list(layers.keys())):
            for figure in layers[key]:
                figure.draw()

    def update(self, event):
        # focused - the figure we are moving
        # dragging - whether to move the shape when moving the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.last_mouse_pos = event.pos
            figure = self.get_pos(((event.pos[0] - self.position[0]) // self.size[0], (event.pos[1] - self.position[1]) // self.size[1]))
            # is there a piece and check that its move
            if figure != None and figure.color == self.step % 2:
                self.focused = figure
                self.dragging = True
            elif figure is None:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            # move figure if dragging
            if self.dragging and self.focused:
                self.focused.move((self.last_mouse_pos[0] - event.pos[0], self.last_mouse_pos[1] - event.pos[1]))
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            # move figure to new cell
            if self.focused:
                self.focused.update(((event.pos[0] - self.position[0]) // self.size[0], (event.pos[1] - self.position[1]) // self.size[1]))

    def get_pos(self, pos):  # get a figure using position
        for i in range(len(self.board)):
            if self.board[i].cell == pos:
                return self.board[i]

    def remove_from_board(self, piece):
        # if the king died, then we recreate the game
        if type(piece) == King:
            print(f"win is {'red' if piece.color == 0 else 'green'}")
            self.generate_board()
        elif piece in self.board:
            self.board.remove(piece)

    def go_to_next_step(self):
        self.step += 1
        # flip the board
        for figure in self.board:
            figure.set_cell((7 - figure.cell[0], 7 - figure.cell[1]))
        self.game.fog.update()

    def add_figure(self, type, pos, color):  # add a figure to the board
        if type == 'p':
            self.board.append(Pawn(self.game, pos, self.pieces_tile_set[0, not color], color))
        elif type == 'r':
            self.board.append(Rook(self.game, pos, self.pieces_tile_set[1, not color], color))
        elif type == 'q':
            self.board.append(Queen(self.game, pos, self.pieces_tile_set[2, not color], color))
        elif type == 'k':
            self.board.append(King(self.game, pos, self.pieces_tile_set[3, not color], color))
        elif type == 'e':
            self.board.append(Elephant(self.game, pos, self.pieces_tile_set[4, not color], color))
        elif type == 'h':
            self.board.append(Horse(self.game, pos, self.pieces_tile_set[5, not color], color))

    def generate_board(self):
        # clear board
        self.board = []
        # add figures to the field
        for i in range(8):
            self.add_figure('p', (i, 6), 0)
            if i % 7 == 0:
                self.add_figure('r', (i, 0), 1)
                self.add_figure('r', (i, 7), 0)
            if i % 5 == 1:
                self.add_figure('h', (i, 0), 1)
                self.add_figure('h', (i, 7), 0)
            if i % 3 == 2:
                self.add_figure('e', (i, 0), 1)
                self.add_figure('e', (i, 7), 0)
            if i == 3:
                self.add_figure('q', (i, 0), 1)
                self.add_figure('q', (i, 7), 0)
            if i == 4:
                self.add_figure('k', (i, 0), 1)
                self.add_figure('k', (i, 7), 0)
            self.add_figure('p', (i, 1), 1)
