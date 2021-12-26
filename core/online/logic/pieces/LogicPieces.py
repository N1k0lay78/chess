class LogicPieces():
    def __init__(self):
        pass

    def check_clear_cell(self, cell):  # cell is clear
        return not self.game.board.get_pos(cell)

    def check_not_friendly_cell(self, cell):  # cell is clear or enemy on cell
        piece = self.game.board.get_pos(cell)
        if piece:
            if piece.color != self.color:
                self.game.board.remove_from_board(piece)
                return True
            elif piece.color == self.color:
                return False
        return True

    def can_eat(self, cell):  # enemy on cell
        piece = self.game.board.get_pos(cell)
        if piece and piece.color != self.color:
            self.game.board.remove_from_board(piece)
            return True
        return False