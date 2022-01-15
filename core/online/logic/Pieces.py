class LogicPieces:
    def __init__(self, name, cell, color):
        self.board = None
        self.name = name
        self.cell = cell
        self.color = color  # 0 - downside (green), 1 - upside (red)

    def can_move(self, cell):  # can move to cell
        return cell != self.cell

    def can_view(self, cell):  # can view figure
        return self.cell[0] - 1 <= cell[0] <= self.cell[0] + 1 and self.cell[1] - 1 <= cell[1] <= self.cell[1] + 1

    def check_clear_cell(self, cell):  # cell is clear
        return not self.board.get_pos(cell)

    def check_not_friendly_cell(self, cell):  # cell is clear or enemy on cell
        piece = self.board.get_piece(cell)
        if piece:
            if piece.color != self.color:
                self.board.remove_piece(piece)
                return True
            else:
                return False
        return True

    def check_eat(self, cell):  # enemy on cell
        piece = self.board.get_piece(cell)
        if piece and piece.color != self.color:
            self.board.remove_from_board(piece)
            return True
        return False

    def update(self, cell):
        print(cell, self.cell)
        if 0 <= cell[0] <= 7 and 0 <= cell[1] <= 7 and self.can_move(cell):
            self.set_cell(cell)
            self.on_move()
            return True
        else:
            return False

    def set_cell(self, cell):
        self.cell = cell

    def set_board(self, board):
        self.board = board

    def on_move(self):
        pass

    def __repr__(self):
        return f"{self.name}{chr(104-self.cell[0])}{8-self.cell[1]}{'w' if self.color == 0 else 'b'}"
