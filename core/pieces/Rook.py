from core.pieces.Pieces import Pieces


class Rook(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, cell, surface, color)
        self.is_moved = False

    def check_move(self, pos):
        move_x, move_y = pos[0] - self.cell[0], pos[1] - self.cell[1]
        if move_x != move_y and (move_x == 0 or move_y == 0):
            move_x = 1 if move_x > 0 else (-1 if move_x < 0 else 0)
            move_y = 1 if move_y > 0 else (-1 if move_y < 0 else 0)
            # print([self.check_clear_cell((self.cell[0] + move_x * i, self.cell[1] + move_y * i)) for i in range(1, abs(self.cell[0] - pos[0] + self.cell[1] - pos[1]))])
            return all([self.check_clear_cell((self.cell[0] + move_x * i, self.cell[1] + move_y * i)) for i in range(1, abs(self.cell[0] - pos[0] + self.cell[1] - pos[1]))]) and self.check_not_friendly_cell(pos)
        return False

    def on_move(self):
        self.is_moved = True
