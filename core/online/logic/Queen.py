from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import queen_move


class LogicQueen(LogicPieces):
    def __init__(self, board, cell, color):
        super().__init__(board, "Q", cell, color)

    can_move = queen_move
