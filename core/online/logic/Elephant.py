from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import elephant_move


class LogicElephant(LogicPieces):
    def __init__(self, board, cell, color):
        super().__init__(board, "B", cell, color)

    can_move = elephant_move
