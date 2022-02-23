from core.pieces.Pieces import Pieces
from core.logic.pieces_move import queen_move


class Queen(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, "Q", cell, surface, color)

    can_move = queen_move
