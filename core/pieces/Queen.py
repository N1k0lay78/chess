from core.pieces.Pieces import Pieces
from core.logic.pieces_move import queen_move


class Queen(Pieces):
    def __init__(self, game, cell, color, is_can):
        super().__init__(game, "Q", cell, color, is_can)

    def load_surface(self):
        return self.board.board.pieces_tile_set[3, self.color]

    can_move = queen_move
