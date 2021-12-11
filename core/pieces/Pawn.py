from core.pieces.Pieces import Pieces


class Pawn(Pieces):
    def __init__(self, game, cell, surface, color):
        super().__init__(game, cell, surface, color)
        self.first_move = True

    def check_move(self, pos):
        if pos[0] == self.cell[0]:
            if self.first_move and pos[1] == self.cell[1] + (-2 if self.color == 0 else 2) and self.check_clear_cell(pos):
                self.first_move = False
                return True
            elif pos[1] == self.cell[1] + (-1 if self.color == 0 else 1) and self.check_clear_cell(pos):
                self.first_move = False
                return True
        elif (pos[0] + 1 == self.cell[0] or pos[0] - 1 == self.cell[0]) and pos[1] == self.cell[1] + (-1 if self.color == 0 else 1) and self.can_eat(pos):
            self.first_move = False
            return True
        return False

    def on_move(self):
        if (self.color == 0 and self.cell[1] == 0) or (self.color == 1 and self.cell[1] == 7):
            print('choose a figure (q - Queen/h - Horse/r - Rook/e - Elephant)')
            choose = input('Choice: ').lower()
            while choose not in ['q', 'h', 'r', 'e']:
                choose = input('Choice: ').lower()
            self.game.board.add_figure(choose, self.cell, self.color)
            self.game.board.remove_from_board(self)
