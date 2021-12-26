from core.online.logic.pieces import LogicPieces


class LogicElephant(LogicPieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, cell, surface, color)

    def check_move(self, pos):
        move_x, move_y = pos[0] - self.cell[0], pos[1] - self.cell[1]
        # check that we are moving diagonally
        if move_y != 0 and move_x / move_y in (-1, 1):
            # get direction
            move_x = 1 if move_x > 0 else -1
            move_y = 1 if move_y > 0 else -1
            # make ray cast to the target, if it did not intersect with anything, then we go to the cell
            # we check that there is either nothing with the destination or the enemy
            return all([self.check_clear_cell((self.cell[0] + move_x * i, self.cell[1] + move_y * i)) for i in range(1, abs(self.cell[0] - pos[0]))]) and self.check_not_friendly_cell(pos)
        return False

    def __repr__(self):
        return "E"
