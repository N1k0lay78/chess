from core.pieces.Pieces import Pieces
from core.logic.pieces_move import horse_move


class Horse(Pieces):
    def __init__(self, game, cell, color, is_can):
        super().__init__(game, "N", cell, color, is_can)

    def load_surface(self):
        return self.board.board.pieces_tile_set[5, self.color]

    can_move = horse_move
