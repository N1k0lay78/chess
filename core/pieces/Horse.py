from core.pieces.Pieces import Pieces
from core.logic.pieces_move import horse_move


class Horse(Pieces):
    def __init__(self, game, cell, color):
        super().__init__(game, "N", cell, color)

    def load_surface(self):
        return self.board.board.pieces_tile_set[5, self.color]

    can_move = horse_move
