from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import horse_move


class LogicHorse(LogicPieces):
    def __init__(self, cell, color):
        super().__init__("N", cell, color)

    def can_view(self, cell):
        return self.cell[0] - 2 <= cell[0] <= self.cell[0] + 2 and self.cell[1] - 1 <= cell[1] <= self.cell[1] + 1

    can_move = horse_move
