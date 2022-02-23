from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import king_move


class LogicKing(LogicPieces):
    def __init__(self, cell, color):
        super().__init__("K", cell, color)
        self.can_castled = True

    def can_view(self, cell):
        return self.cell[0] - 2 <= cell[0] <= self.cell[0] + 2 and self.cell[1] - 1 <= cell[1] <= self.cell[1] + 1

    can_move = king_move

    def on_move(self):
        self.can_castled = False
