from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import king_path
from core.logic.pieces_view import big_view


class LogicKing(LogicPieces):
    def __init__(self, board, cell, color, is_can):
        super().__init__(board, "K", cell, color, is_can)

    can_view = big_view
    get_path = king_path

    def on_move(self):
        self.is_can = False
