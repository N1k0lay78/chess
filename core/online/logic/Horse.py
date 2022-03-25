from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import horse_path
from core.logic.pieces_view import big_view


class LogicHorse(LogicPieces):
    def __init__(self, board, cell, color, is_can):
        super().__init__(board, "N", cell, color, is_can)

    can_view = big_view
    get_path = horse_path
