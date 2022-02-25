from core.pieces.Pieces import Pieces
from core.logic.pieces_move import king_move


class King(Pieces):
    def __init__(self, game, cell, color, is_can):
        super().__init__(game, "K", cell, color, is_can)

    def load_surface(self):
        return self.board.board.pieces_tile_set[2, self.color]

    can_move = king_move

    def check_castling(self, figure,  pos) -> bool:
        figure.set_cell(self.cell[:])
        self.board.judge.on_castling(pos[0] > self.cell[0], self.color)
        return True

    def on_move(self) -> None:
        self.is_can = False
