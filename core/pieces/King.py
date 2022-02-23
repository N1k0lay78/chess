from core.pieces.Pieces import Pieces
from core.logic.pieces_move import king_move


class King(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, "K", cell, surface, color)
        self.can_castled = True

    can_move = king_move

    def on_move(self):
        self.can_castled = False
