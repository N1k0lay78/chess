from unittest import TestCase
from core.Board import Board
from core.windows.Game import Game

testing_boards = [
    "a7w1 a5b1",  # White Pawn at A7 and Black Pawn at A5

    "b6w0 b5b0 b7b0 a5b0 a6b0 c7b0 c5b0 c6b0 c7b0",  # White Pawn at B6 and 8 Black Pawns around
    "a7w1 a5b0 c7b0",  # Pawn and two pawn at 2 cells out

    "Kc2w0 a3b0 a2b0 a1b0 b3b0 b2b0 b1b0 c3b0 c1b0 d3b0 d2b0 d1b0 e3b0 e2b0 e1b0",  # King at C2 and 14 Black Pawn
    "Kc2w0 c4b0 f2b0",  # King at C2 and Black Pawn at C4 and F2

    "Qc2w0 a3b0 a2b0 a1b0 b3b0 b2b0 b1b0 c3b0 c1b0 d3b0 d2b0 d1b0 e3b0 e2b0 e1b0",  # Queen at C2 and 14 Black Pawn
    "Qc2w0 c4b0 f2b0",  # Queen at C2 and Black Pawn at C4 and F2

    "Nc2w0 a3b0 a2b0 a1b0 b3b0 b2b0 b1b0 c3b0 c1b0 d3b0 d2b0 d1b0 e3b0 e2b0 e1b0",  # Horse at C2 and 14 Black Pawn
    "Nc2w0 c4b0 f2b0",  # Horse at C2 and Black Pawn at C4 and F2

    "Rb6w0 b5b0 b7b0 a5b0 a6b0 c7b0 c5b0 c6b0 c7b0",  # White Rook at B6 and 8 Black Pawns around
    "Ra7w1 a5b0 c7b0",  # Rook and two pawn at 2 cells out

    "Bb6w0 b5b0 b7b0 a5b0 a6b0 c7b0 c5b0 c6b0 c7b0",  # Elephant Rook at B6 and 8 Black Pawns around
    "Ba7w1 a5b0 c7b0",  # Elephant and two pawn at 2 cells out

    "Ka1w0 Qb1w1 Nc1w1 Rd1w0 Be1w0 f1w0 Kg1b0",  # White and Black Kings and all type Pieces in line

    "Ka1w0 Kg1b0",  # White and Black Kings

    "Ka1w0 Qb1b1 Nc1b1 Rd1w0 Be1w0 f1w0 Kg1b0",  # 13 with hanged colors
]


class TestBoard(TestCase):
    def setUp(self) -> None:
        self.game = Game((600, 600), "", 0, False, "empty")
        self.board = self.game.board

    # board index 13
    def test_get_pos(self):
        self.board.load_board(testing_boards[13])
        self.assertEqual(self.board.get_pos((0, 7)), self.board.board[0], 'Wrong get Piece at (0, 7)')
        self.assertEqual(self.board.get_pos([1, 7]), self.board.board[1], 'Wrong get Piece at (1, 7)')
        self.assertEqual(self.board.get_pos((2, 7)), self.board.board[2], 'Wrong get Piece at (2, 7)')
        self.assertEqual(self.board.get_pos((3, 7)), self.board.board[3], 'Wrong get Piece at (3, 7)')
        self.assertEqual(self.board.get_pos((4, 7)), self.board.board[4], 'Wrong get Piece at (4, 7)')
        self.assertEqual(self.board.get_pos((5, 7)), self.board.board[5], 'Wrong get Piece at (5, 7)')
        self.assertEqual(self.board.get_pos((6, 7)), self.board.board[6], 'Wrong get Piece at (6, 7)')

    # board index 13
    def test_remove_piece(self):
        self.board.load_board(testing_boards[13])
        a = self.board.board[:]
        self.board.remove_piece(a[1])
        a.pop(1)
        self.assertEqual(self.board.board, a, 'Wrong getting Black')

    # board index 14
    def test_add_piece(self):
        self.board.load_board(testing_boards[14])
        self.board.add_piece("Qb1w1")
        self.board.add_piece("Nc1w1")
        self.board.add_piece("Rd1w0")
        self.board.add_piece("Be1w0")
        self.board.add_piece("f1w0")
        self.assertEqual(self.board.pieces_manager.get_line(self.board.board),
                         "Ka1w0 Kg1b0 Qb1w1 Nc1w1 Rd1w0 Be1w0 f1w0", 'Error in method add_piece or get_board_line')
