from core.pieces.Pieces import Pieces
from core.logic.pieces_move import elephant_move


class Elephant(Pieces):
    def __init__(self, game, cell, color):
        super().__init__(game, "B", cell, color)

    def load_surface(self):
        return self.board.board.pieces_tile_set[4, self.color]

    can_move = elephant_move
