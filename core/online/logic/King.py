from core.online.logic.Pieces import LogicPieces
from core.online.logic.Rook import LogicRook


class LogicKing(LogicPieces):
    def __init__(self, cell, color):
        super().__init__(cell, color)
        self.can_castled = True

    def can_view(self, cell):
        return self.cell[0] - 2 <= cell[0] <= self.cell[0] + 2 and self.cell[1] - 1 <= cell[1] <= self.cell[1] + 1

    def can_move(self, pos):
        # check that we are moving one cell
        if abs(self.cell[0] - pos[0]) < 2 and abs(self.cell[1] - pos[1]) < 2:
            return self.check_not_friendly_cell(pos)
        # castling check
        figure = self.board.get_piece(pos)
        if self.can_castled and type(figure) is LogicRook and not figure.is_moved and figure.color == self.color:
            figure.set_cell(self.cell[:])
            return True
        return False

    def on_move(self):
        self.can_castled = False
