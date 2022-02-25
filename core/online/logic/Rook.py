from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import rook_move


class LogicRook(LogicPieces):
    def __init__(self, board, cell, color, is_can):
        super().__init__(board, "R", cell, color, is_can)

    can_move = rook_move

    def on_move(self):
        self.is_can = False
