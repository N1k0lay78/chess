from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import king_move


class LogicKing(LogicPieces):
    def __init__(self, board, cell, color, is_can):
        super().__init__(board, "K", cell, color, is_can)

    def can_view(self, cell):
        return self.cell[0] - 2 <= cell[0] <= self.cell[0] + 2 and self.cell[1] - 1 <= cell[1] <= self.cell[1] + 1

    can_move = king_move

    def check_castling(self, figure,  pos) -> bool:
        if ((self.color and figure.cell in ([7, 0], [0, 0]) and self.cell == [4, 0] or
             not self.color and figure.cell in ([7, 7], [0, 7]) and self.cell == [4, 7])):
            is_right = pos[0] > self.cell[0]
            if is_right and self.color == 0 and \
                    all([self.check_clear_cell((x, 7)) for x in range(5, 7)]):
                figure.set_cell((5, 7))
                pos[0] = 6
                return True
            elif not is_right and self.color == 0 and \
                    all([self.check_clear_cell((x, 7)) for x in range(1, 4)]):
                figure.set_cell((3, 7))
                pos[0] = 2
                return True
            elif is_right and self.color == 1 and \
                    all([self.check_clear_cell((x, 0)) for x in range(5, 7)]):
                figure.set_cell((5, 0))
                pos[0] = 6
                return True
            elif not is_right and self.color == 1 and \
                    all([self.check_clear_cell((x, 0)) for x in range(1, 4)]):
                figure.set_cell((3, 0))
                pos[0] = 2
                return True
        return False

    def on_move(self):
        self.is_can = False
