from core.pieces.King import King
from core.pieces.Pawn import Pawn
from core.pieces.Horse import Horse
from core.pieces.Elephant import Elephant
from core.pieces.Queen import Queen
from core.pieces.Rook import Rook


class LogicBoard:
    def __init__(self):
        self.board = []
        self.step = 0

    def add_figure(self, type, pos, color):  # add a figure to the board
        if type == 'p':
            self.board.append(Pawn(self.game, pos, self.pieces_tile_set[0, not color], color))
        elif type == 'r':
            self.board.append(Rook(self.game, pos, self.pieces_tile_set[1, not color], color))
        elif type == 'q':
            self.board.append(Queen(self.game, pos, self.pieces_tile_set[3, not color], color))
        elif type == 'k':
            self.board.append(King(self.game, pos, self.pieces_tile_set[2, not color], color))
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