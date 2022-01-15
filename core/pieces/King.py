from core.pieces.Pieces import Pieces
from core.pieces.Rook import Rook


class King(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, "K", cell, surface, color)
        self.can_castled = True

    def check_move(self, pos):
        # check that we are moving one cell
        if abs(self.cell[0] - pos[0]) < 2 and abs(self.cell[1] - pos[1]) < 2:
            return self.check_not_friendly_cell(pos)
        # castling check
        figure = self.game.board.get_pos(pos)
        if self.can_castled and type(figure) is Rook and not figure.is_moved and figure.color == self.color:
            figure.set_cell(self.cell[:])
            return True
        return False

    def on_move(self):
        self.can_castled = False

    def __repr__(self):
        return "K"
