from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import horse_move


class LogicHorse(LogicPieces):
    def __init__(self, board, cell, color, is_can):
        super().__init__(board, "N", cell, color, is_can)

    def can_view(self, cell):
        return self.cell[0] - 2 <= cell[0] <= self.cell[0] + 2 and self.cell[1] - 1 <= cell[1] <= self.cell[1] + 1

    can_move = horse_move
