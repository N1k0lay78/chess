from core.pieces.Pieces import Pieces
from core.logic.pieces_move import horse_move


class Horse(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, "N", cell, surface, color)

    can_move = horse_move
