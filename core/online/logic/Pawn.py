from core.online.logic.Pieces import LogicPieces
from core.pieces.Pieces import Pieces


class LogicPawn(LogicPieces):
    def __init__(self, cell, color):
        super().__init__("", cell, color)
        self.first_move = True

    def can_move(self, pos):
        if pos[0] == self.cell[0]:
            # check that the point is 1 cell forward
            if pos[1] == self.cell[1] - 1 and self.check_clear_cell(pos):
                return True
            # if this is the first move, then we can move 2 cells
            elif self.first_move and pos[1] == self.cell[1] - 2 and self.check_clear_cell(pos):
                return True
        # if they want to go sideways, then we check that we can go and that there is an enemy
        elif (pos[0] + 1 == self.cell[0] or pos[0] - 1 == self.cell[0]) and pos[1] == self.cell[1] - 1 and self.check_eat(pos):
            return True
        return False

    def on_move(self):
        # we cannot walk 2 cells
        self.first_move = False
        # if we reach the other end of the map, then we change the figure
        if self.cell[1] == 0:
            print('choose a figure (q - Queen/h - Horse/r - Rook/e - Elephant)')
            input('MAKE')
            choose = "make"
            choose in ['q', 'h', 'r', 'e']
            # choose = input('Choice: ').lower()
            # while choose not in ['q', 'h', 'r', 'e']:
            #     choose = input('Choice: ').lower()
            self.board.remove_figure(self)
            # if a new game has started, then you do not need to add a piece
            if self.check_clear_cell(self.cell):
                self.board.add_figure(choose, self.cell, self.color)