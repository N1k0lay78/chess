from core.pieces.Pieces import Pieces


class Horse(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, "N", cell, surface, color)

    def can_move(self, pos):
        # clockwise from 12 o'clock
        moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        # heck that the target is where we can move
        return any([True for move in moves if pos == (self.cell[0] + move[0], self.cell[1] + move[1]) and self.check_not_friendly_cell(pos)])