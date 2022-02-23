from core.pieces.Pieces import Pieces
from core.logic.pieces_move import elephant_move


class Elephant(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, "B", cell, surface, color)

    can_move = elephant_move
