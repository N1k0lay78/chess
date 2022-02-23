from core.pieces.Pieces import Pieces
from core.logic.pieces_move import game_pawn_move


class Pawn(Pieces):
    def __init__(self, game, cell, color):
        super().__init__(game, "", cell, color)
        self.first_move = True

    def load_surface(self):
        return self.board.board.pieces_tile_set[0, self.color]

    can_move = game_pawn_move

    def on_move(self):
        # we cannot walk 2 cells
        self.first_move = False
        # if we reach the other end of the map, then we change the figure
        # if self.cell[1] == 0:
        #     print('choose a figure (q - Queen/h - Horse/r - Rook/e - Elephant)')
        #     choose = input('Choice: ').lower()
        #     while choose.lower() not in ['q', 'h', 'r', 'e']:
        #         choose = input('Choice: ').lower()
        #     self.game.board.remove_from_board(self)
        #     # if a new game has started, then you do not need to add a piece
        #     if self.check_clear_cell(self.cell):
        #         if self.color == 0:
        #             self.game.board.add_figure(f"{choose.upper()}{chr(104-self.cell[0])}{8-self.cell[1]}{'b' if self.color else 'w'}")
        #         else:
        #             self.game.board.add_figure(f"{choose.upper()}{chr(97+self.cell[0])}{self.cell[1]+1}{'b' if self.color else 'w'}")
