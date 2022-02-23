import pygame

from Source.settings import debug
from core.pieces.King import King
from core.pieces.Pawn import Pawn
from core.pieces.Horse import Horse
from core.pieces.Elephant import Elephant
from core.pieces.Queen import Queen
from core.pieces.Rook import Rook
from core.textures.Tileset import TileSet
from core.textures.load_image import load_image


class Board:
    def __init__(self, game, pos, size, color):
        # logic
        self.color = color
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
        if self.focused and debug:
            pygame.draw.circle(self.game.screen, (255, 255, 255), (self.focused.pos[0] + 25,
                                                                   self.focused.pos[1]+35), 5)

    def update(self, event):
        # focused - the figure we are moving
        # dragging - whether to move the shape when moving the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.last_mouse_pos = event.pos
            figure = self.get_pos(((event.pos[0] - self.position[0]) // self.size[0],
                                   (event.pos[1] - self.position[1]) // self.size[1]))
            # is there a piece and check that its move
            if figure != None and figure.color == self.color == self.step % 2:
                self.focused = figure
                self.dragging = True
            elif figure is None:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            # move figure if dragging
            if self.dragging and self.focused:
                self.focused.move((self.last_mouse_pos[0] - event.pos[0],
                                   self.last_mouse_pos[1] - event.pos[1]))
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            # move figure to new cell
            if self.focused:
                self.focused.update(((self.focused.pos[0] + 25 - self.position[0]) // self.size[0],
                                     (self.focused.pos[1] + 35 - self.position[1]) // self.size[1]))

    def get_pos(self, pos):  # get a figure using position
        for i in range(len(self.board)):
            if self.board[i].cell[0] == pos[0] and self.board[i].cell[1] == pos[1]:
                return self.board[i]

    def remove_from_board(self, piece):
        # if the king died, then we recreate the game
        # if type(piece) == King:
        #     print(f"win is {'red' if piece.color == 0 else 'green'}")
        #     self.generate_board()
        # elif piece in self.board:
        self.board.remove(piece)

    def go_to_next_step(self):
        # self.step += 1
        # flip the board
        self.game.fog.update()

    def set_color(self, color):
        self.color = color

    def add_figure(self, piece):  # add a figure to the board
        if len(piece) == 4:
            if piece[0] == "K" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                self.board.append(King(self.game, [104-ord(piece[1]), 8 - int(piece[2])], self.pieces_tile_set[2, piece[3] == 'b'], (0 if piece[3] == 'w' else 1)))
            elif piece[0] == "Q" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                self.board.append(Queen(self.game, [104-ord(piece[1]), 8 - int(piece[2])], self.pieces_tile_set[3, piece[3] == 'b'], (0 if piece[3] == 'w' else 1)))
            elif piece[0] == "R" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                self.board.append(Rook(self.game, [104-ord(piece[1]), 8 - int(piece[2])], self.pieces_tile_set[1, piece[3] == 'b'], (0 if piece[3] == 'w' else 1)))
            elif piece[0] == "N" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                self.board.append(Horse(self.game, [104-ord(piece[1]), 8 - int(piece[2])], self.pieces_tile_set[5, piece[3] == 'b'], (0 if piece[3] == 'w' else 1)))
            elif piece[0] == "B" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                self.board.append(Elephant(self.game, [104-ord(piece[1]), 8 - int(piece[2])], self.pieces_tile_set[4, piece[3] == 'b'], (0 if piece[3] == 'w' else 1)))
            else:
                print(f"LoadingBoardError have ERROR {piece}")
        elif len(piece) == 3:
            if piece[0] in 'abcdefgh' and piece[1] in '12345678' and piece[2] in "bw":
                self.board.append(Pawn(self.game, [104-ord(piece[0]), 8 - int(piece[1])], self.pieces_tile_set[0, piece[2] == 'b'], (0 if piece[2] == 'w' else 1)))
            else:
                print(f"LoadingBoardError have ERROR {piece}")
        else:
            print(f"LoadingBoardError have ERROR {piece}")

    def load_board(self, line):
        # loading pieces from line with pieces info
        self.board = []
        for piece in line.split():
            self.add_figure(piece)
        if self.color == 1:
            for figure in self.board:
                figure.set_cell((7 - figure.cell[0], 7 - figure.cell[1]))
