from core.online.logic.Pieces import LogicPieces
from core.logic.pieces_move import logic_pawn_move


class LogicPawn(LogicPieces):
    def __init__(self, board, cell, color, is_can):
        super().__init__(board, "", cell, color, is_can)

    can_move = logic_pawn_move

    def on_move(self):
        # we cannot walk 2 cells
        self.is_can = False
        if self.cell[1] in [0, 7]:
            self.board.server.ask_user_choice(self.color, self.cell)
        # if we reach the other end of the map, then we change the figure

    def replace(self, choose):
        if self.cell[1] in [0, 7] and choose in ['Q', 'N', 'R', 'B']:
            self.board.remove_piece(self)
            # if a new game has started, then you do not need to add a piece
            if self.check_clear_cell(self.cell):
                self.board.add_piece(choose + str(self))
                return True
        return False
