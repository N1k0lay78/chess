from core.online.logic.Pieces import LogicPieces


class LogicHorse(LogicPieces):
    def __init__(self, cell, color):
        super().__init__("N", cell, color)

    def can_view(self, cell):
        return self.cell[0] - 2 <= cell[0] <= self.cell[0] + 2 and self.cell[1] - 1 <= cell[1] <= self.cell[1] + 1

    def can_move(self, pos):
        # clockwise from 12 o'clock
        moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        # heck that the target is where we can move
        print(self.cell, pos, "asfasfasf")
        print([[self.cell[0] + move[0], self.cell[1] + move[1]] for move in moves], self.check_not_friendly_cell(pos))
        return any([True for move in moves if pos == [self.cell[0] + move[0], self.cell[1] + move[1]] and self.check_not_friendly_cell(pos)])
