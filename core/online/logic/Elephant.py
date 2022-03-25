from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import elephant_path


class LogicElephant(LogicPieces):
    def __init__(self, board, cell, color, is_can):
        super().__init__(board, "B", cell, color, is_can)

    get_path = elephant_path
