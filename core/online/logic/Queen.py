from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import queen_path
from core.logic.pieces_view import big_view


class LogicQueen(LogicPieces):
    def __init__(self, board, cell, color, is_can):
        super().__init__(board, "Q", cell, color, is_can)

    can_view = big_view
    get_path = queen_path
