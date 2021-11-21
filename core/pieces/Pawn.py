from core.pieces.Pieces import Pieces


class Pawn(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, cell, surface, color)
        self.first_move = True

    def check_move(self, pos):
        if pos[0] == self.cell[0]:
            if self.first_move and pos[1] == self.cell[1] + (-2 if self.color == "w" else 2) and self.check_clear_cell(pos):
                self.first_move = False
                return True
            elif pos[1] == self.cell[1] + (-1 if self.color == "w" else 1) and self.check_clear_cell(pos):
                self.first_move = False
                return True
        elif (pos[0] + 1 == self.cell[0] or pos[0] - 1 == self.cell[0]) and pos[1] == self.cell[1] + (-1 if self.color == "w" else 1) and self.can_eat(pos):
            self.first_move = False
            return True
        return False
