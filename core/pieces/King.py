from core.pieces.Pieces import Pieces
from core.logic.pieces_move import king_move


class King(Pieces):
    def __init__(self, game, cell, color, is_can):
        super().__init__(game, "K", cell, color, is_can)

    def load_surface(self):
        return self.board.board.pieces_tile_set[2, self.color]

    can_move = king_move

    def check_castling(self, figure,  pos) -> bool:
        # check position
        if tuple(figure.cell) in ((7, 7), (0, 7)) and (tuple(self.cell) == (4, 7) and self.color == 0 or
                                                       tuple(self.cell) == (3, 7) and self.color == 1):
            is_right = pos[0] > self.cell[0]
            make_castling = False
            if is_right and self.color == 0 and \
                    all([self.check_clear_cell((x, 7)) for x in range(5, 7)]):
                figure.set_cell((5, 7))
                pos[0] = 6
                make_castling = True
            elif not is_right and self.color == 0 and \
                    all([self.check_clear_cell((x, 7)) for x in range(1, 4)]):
                figure.set_cell((3, 7))
                pos[0] = 2
                make_castling = True
            elif is_right and self.color == 1 and \
                    all([self.check_clear_cell((x, 7)) for x in range(4, 7)]):
                figure.set_cell((4, 7))
                pos[0] = 5
                make_castling = True
            elif not is_right and self.color == 1 and \
                    all([self.check_clear_cell((x, 7)) for x in range(1, 3)]):
                figure.set_cell((2, 7))
                pos[0] = 1
                make_castling = True

            if make_castling:
                self.board.judge.on_castling(pos[0] > self.cell[0], self.color)
                return True
        return False

    def on_move(self) -> None:
        self.is_can = False
