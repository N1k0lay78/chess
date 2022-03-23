from core.logic.pieces_view import small_view


class LogicPieces:
    def __init__(self, board, name, cell, color, is_can):
        # settings
        self.board = board
        self.name = name
        self.color = color  # 0 - downside (green), 1 - upside (red)
        self.is_can = is_can
        # init
        self.cell = [0, 0]
        self.set_cell(cell)

    def can_move(self, cell):  # can move to cell
        return cell != self.cell

    can_view = small_view

    def get_piece(self, cell):  # get figure from board
        return self.board.get_piece(cell)

    def remove_piece(self, piece):  # remove figure from board
        return self.board.remove_piece(piece)

    def check_clear_cell(self, cell):  # cell is clear
        return not self.get_piece(cell)

    def check_not_friendly_cell(self, cell):  # cell is clear or enemy on cell
        piece = self.get_piece(cell)
        if piece:
            if piece.s != self.s:
                self.remove_piece(piece)
                return True
            else:
                return False
        return True

    def check_eat(self, cell):  # enemy on cell
        piece = self.get_piece(cell)
        if piece and piece.s != self.s:
            self.remove_piece(piece)
            return True
        return False

    def update(self, cell):
        if 0 <= self.r <= 7 and 0 <= self.c <= 7 and self.can_move(cell):
            self.set_cell(cell)
            self.on_move()
            return True
        else:
            return False

    def set_cell(self, cell):
        self.cell = cell

    def on_move(self):
        pass

    def __repr__(self):
        return f"{self.name}{chr(97+self.cell[0])}{8-self.cell[1]}{'w' if self.color == 0 else 'b'}{int(self.is_can)}"

    def __getattr__(self, item):
        res = []
        for ch in item.lower():
            if ch == 'r':
                res.append(self.cell[1])
            elif ch == 'c':
                res.append(self.cell[0])
            elif ch == 't':
                res.append(self.name)
            elif ch == 's':  # s is side (c is column)
                res.append(self.color)
            elif ch == 'x':
                res.append(self.pos[0])
            elif ch == 'y':
                res.append(self.pos[1])
            elif ch == 'i':
                res.append(self.is_can)
        if len(res) != 1:
            return res
        else:
            return res[0]

    def test(self):
        return [self.cell, self.name, self.is_can, self.color]
