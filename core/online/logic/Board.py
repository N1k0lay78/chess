from Source.boards import boards
from core.online.logic.Elephant import LogicElephant
from core.online.logic.Horse import LogicHorse
from core.online.logic.King import LogicKing
from core.online.logic.Pawn import LogicPawn
from core.online.logic.Rook import LogicRook
from core.online.logic.Queen import LogicQueen


class LogicBoard:
    def __init__(self, line):
        self.pieces = []
        self.load_board(line)
        self.step = 0

    def move(self, from_cell, to_cell):
        print(from_cell, to_cell, type(from_cell[0]))
        piece = self.get_piece(from_cell)
        print(piece)
        if piece and piece.update(to_cell):
            self.step += 1
            return True
        else:
            return False

    def can_view(self, color):
        visible = []
        player_pieces = self.get_pieces(color)
        for piece in self.pieces:
            if piece.color == color:
                visible.append(piece)
            else:
                for player_piece in player_pieces:
                    if player_piece.can_view(piece.cell):
                        visible.append(piece)
                        break
        return self.get_board_line(visible)

    def get_piece(self, cell):
        for piece in self.pieces:
            if piece.cell[0] == cell[0] and piece.cell[1] == cell[1]:
                return piece

    def remove_piece(self, piece):
        self.pieces.remove(piece)

    def add_figure(self, choose, cell, color):
        if choose == 'r':
            self.pieces.append(LogicRook(cell, color))
        elif choose == 'q':
            self.pieces.append(LogicQueen(cell, color))
        elif choose == 'k':
            self.pieces.append(LogicKing(cell, color))
        elif choose == 'e':
            self.pieces.append(LogicElephant(cell, color))
        elif choose == 'h':
            self.pieces.append(LogicHorse(cell, color))
        self.pieces[-1].set_board(self)

    def get_pieces(self, color):
        return list(filter(lambda p: p.color == color, self.pieces))

    def get_board_line(self, pieces):
        res = ''
        for piece in pieces:
            res += str(piece) + ' '
        return res[:-1]

    def load_board(self, line):
        # loading pieces from line with pieces info
        self.pieces = []
        for piece in line.split():
            if len(piece) == 4:
                if piece[0] == "K" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                    self.pieces.append(LogicKing([104-ord(piece[1]), 8 - int(piece[2])], (0 if piece[3] == 'w' else 1)))
                    self.pieces[-1].set_board(self)
                elif piece[0] == "Q" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                    self.pieces.append(LogicQueen([104-ord(piece[1]), 8 - int(piece[2])], (0 if piece[3] == 'w' else 1)))
                    self.pieces[-1].set_board(self)
                elif piece[0] == "R" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                    self.pieces.append(LogicRook([104-ord(piece[1]), 8 - int(piece[2])], (0 if piece[3] == 'w' else 1)))
                    self.pieces[-1].set_board(self)
                elif piece[0] == "N" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                    self.pieces.append(LogicHorse([104-ord(piece[1]), 8 - int(piece[2])], (0 if piece[3] == 'w' else 1)))
                    self.pieces[-1].set_board(self)
                elif piece[0] == "B" and piece[1] in 'abcdefgh' and piece[2] in '12345678' and piece[3] in "bw":
                    self.pieces.append(LogicElephant([104-ord(piece[1]), 8 - int(piece[2])], (0 if piece[3] == 'w' else 1)))
                    self.pieces[-1].set_board(self)
                else:
                    print(f"File have ERROR {piece}")
            elif len(piece) == 3:
                if piece[0] in 'abcdefgh' and piece[1] in '12345678' and piece[2] in "bw":
                    self.pieces.append(LogicPawn([104-ord(piece[0]), 8 - int(piece[1])], (0 if piece[2] == 'w' else 1)))
                    self.pieces[-1].set_board(self)
                else:
                    print(f"File have ERROR {piece}")
            else:
                print(f"File have ERROR {piece}")


if __name__ == '__main__':
    board = LogicBoard("")
    board.load_board(boards["classic"])
    print(board.can_view(1))
