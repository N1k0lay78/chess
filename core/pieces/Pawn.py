from core.pieces.Pieces import Pieces
from core.logic.pieces_move import game_pawn_move


class Pawn(Pieces):
    def __init__(self, game, cell, color, is_can):
        super().__init__(game, "", cell, color, is_can)

    def load_surface(self):
        return self.board.board.pieces_tile_set[0, self.color]

    can_move = game_pawn_move

    def on_move(self):
        # we can't walk 2 cells
        self.is_can = False
