from core.online.logic.Elephant import LogicElephant
from core.online.logic.Horse import LogicHorse
from core.online.logic.King import LogicKing
from core.online.logic.Pawn import LogicPawn
from core.online.logic.Pieces import LogicPieces
from core.online.logic.Rook import LogicRook
from core.pieces.Queen import LogicQueen


class LogicBoard:
    def __init__(self, pieces=[]):
        self.pieces = pieces
        for piece in self.pieces:
            piece.set_board(self)
        self.step = 0

    def move(self, from_cell, to_cell):
        piece = self.get_piece(from_cell)
        if piece and piece.update(to_cell):
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
        return visible

    def get_piece(self, cell):
        for piece in self.pieces:
            if piece.cell == cell:
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


if __name__ == '__main__':
    pieces_1 = [LogicPieces((0, 0), 0), LogicPieces((2, 0), 1), LogicHorse((2, 1), 1)]
    board = [LogicPawn([0, 6], 0), LogicRook([0, 0], 1), LogicRook([0, 7], 0), LogicPawn([0, 1], 1), LogicPawn([1, 6], 0), LogicHorse([1, 0], 1), LogicHorse([1, 7], 0), LogicPawn([1, 1], 1), LogicPawn([2, 6], 0), LogicElephant([2, 0], 1), LogicElephant([2, 7], 0), LogicPawn([2, 1], 1), LogicPawn([3, 6], 0), LogicQueen([3, 0], 1), LogicQueen([3, 7], 0), LogicPawn([3, 1], 1), LogicPawn([4, 6], 0), LogicKing([4, 0], 1), LogicKing([4, 7], 0), LogicPawn([4, 1], 1), LogicPawn([5, 6], 0), LogicElephant([5, 0], 1), LogicElephant([5, 7], 0), LogicPawn([5, 1], 1), LogicPawn([6, 6], 0), LogicHorse([6, 0], 1), LogicHorse([6, 7], 0), LogicPawn([6, 1], 1), LogicPawn([7, 6], 0), LogicRook([7, 0], 1), LogicRook([7, 7], 0), LogicPawn([7, 1], 1)]
    lb = LogicBoard(pieces_1)
    print(lb.get_pieces(1))
    print(lb.get_pieces(0))
    print(lb.can_view(1))
    print(lb.can_view(0))
    print(lb.move((2, 1), (0, 0)))
    print(lb.get_pieces(1))
    print(lb.get_pieces(0))