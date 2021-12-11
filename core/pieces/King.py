from core.pieces.Pieces import Pieces
from core.pieces.Rook import Rook


class King(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, cell, surface, color)
        self.can_castled = False

    def check_move(self, pos):
        if abs(self.cell[0] - pos[0]) < 2 and abs(self.cell[1] - pos[1]) < 2:
            if self.check_not_friendly_cell(pos):
                self.can_castled = True
                return True
        figure = self.game.board.get_pos(pos)
        if not self.can_castled and type(figure) is Rook and not figure.is_moved and figure.color == self.color:
            self.can_castled = True
            figure.set_cell(self.cell[:])
            return True
        return False
