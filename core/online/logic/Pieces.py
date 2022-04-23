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

    def get_path(self, cell):
        if cell != self.cr:
            return [(cell[0], cell[1], 2)]

    def can_move(self, cell):  # can move to cell
        path = self.get_path(cell)
        if not path:
            return False
        # column, row and type check of path
        for c, r, t in path:
            if not self.board.can_view_cell([c, r], self.color):
                return False
            if not (0 <= c <= 7 and 0 <= r <= 7) or (
                    t == 0 and not self.check_clear_cell([c, r]) or
                    t == 1 and not self.check_not_friendly_cell([c, r]) or
                    t == 2 and not self.check_eat([c, r])):
                return False
        return True

    can_view = small_view

    def update(self, cell):
        if self.can_move(cell):
            piece = self.get_piece(cell)
            if piece:
                self.remove_piece(piece)
            self.set_cell(cell)
            self.on_move()
            return True
        else:
            return False

    # rarely edited methods

    def get_piece(self, cell):  # get figure from board
        return self.board.get_piece(cell)

    def remove_piece(self, piece):  # remove figure from board
        return self.board.remove_piece(piece)

    # for check is can make move
    def check_clear_cell(self, cell):  # cell is clear
        return not self.get_piece(cell)

    # for check is can make move
    def check_not_friendly_cell(self, cell):  # cell is clear or enemy on cell
        piece = self.get_piece(cell)
        if piece:
            if piece.s != self.s:
                # for offline
                # self.remove_piece(piece)
                return True
            else:
                return False
        return True

    # for check is can make move
    def check_eat(self, cell):  # enemy on cell
        piece = self.get_piece(cell)
        if piece and piece.s != self.s:
            # for offline
            # self.remove_piece(piece)
            return True
        return False

    def set_cell(self, cell):
        self.cell = cell

    def on_move(self):
        pass

    def __repr__(self):
        return f"{self.name}{chr(97 + self.cell[0])}{8 - self.cell[1]}{'w' if self.color == 0 else 'b'}{int(self.is_can)}"

    def __getattr__(self, item):
        res = []
        for ch in item.lower():
            if ch == 'r':  # row
                res.append(self.cell[1])
            elif ch == 'c':  # column
                res.append(self.cell[0])
            elif ch == 't':  # type (name)
                res.append(self.name)
            elif ch == 's':  # s is side like color (c is column)
                res.append(self.color)
            elif ch == 'x':  # x position
                res.append(self.pos[0])
            elif ch == 'y':  # y position
                res.append(self.pos[1])
            elif ch == 'i':  # is can
                res.append(self.is_can)
        if len(res) != 1:
            return res
        else:
            return res[0]

    def test(self):
        return [self.cell, self.name, self.is_can, self.color]
