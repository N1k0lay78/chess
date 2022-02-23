from core.pieces.Pieces import Pieces
from core.logic.pieces_move import rook_move


class Rook(Pieces):
    def __init__(self, game, cell, color):
        super().__init__(game, "R", cell, color)
        self.is_moved = False

    def load_surface(self):
        return self.board.board.pieces_tile_set[1, self.color]

    can_move = rook_move

    def on_move(self):
        self.is_moved = True
