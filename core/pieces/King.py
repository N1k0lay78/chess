from core.pieces.Pieces import Pieces


class King(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, cell, surface, color)

    def check_move(self, pos):
        if abs(self.cell[0] - pos[0]) < 2 and abs(self.cell[1] - pos[1]) < 2:
            return self.check_not_friendly_cell(pos)
        return False
