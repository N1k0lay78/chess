from core.pieces.Pieces import Pieces
from core.logic.pieces_move import rook_move


class Rook(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, "R", cell, surface, color)
        self.is_moved = False

    can_move = rook_move

    def on_move(self):
        self.is_moved = True
