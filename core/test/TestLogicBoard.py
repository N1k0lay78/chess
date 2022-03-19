from unittest import TestCase
from core.Board import Board
from core.online.logic.Board import LogicBoard

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


class TestLogicBoard(TestCase):
    def setUp(self) -> None:
        self.logic_board = LogicBoard("Server", True)

    # board index 0
    def test_get_pieces(self):
        self.logic_board.load_board(testing_boards[0])
        self.assertEqual(self.logic_board.get_pieces(1), [self.logic_board.pieces[1]], 'Wrong getting Black')
        self.assertEqual(self.logic_board.get_pieces(0), [self.logic_board.pieces[0]], 'Wrong getting White')

    # board index 1-12
    def test_can_view(self):
        # Pawn
        self.logic_board.load_board(testing_boards[1])
        self.assertEqual(self.logic_board.can_view(0), testing_boards[1], 'Pawn don\'t collide all 8 pieces')
        self.logic_board.load_board(testing_boards[2])
        self.assertEqual(self.logic_board.can_view(0), "a7w1", 'Pawn collide Wrong pieces')

        # King
        self.logic_board.load_board(testing_boards[3])
        self.assertEqual(self.logic_board.can_view(0), testing_boards[3], 'King don\'t collide all 14 pieces')
        self.logic_board.load_board(testing_boards[4])
        self.assertEqual(self.logic_board.can_view(0), "Kc2w0", 'King collide Wrong pieces')

        # Queen
        self.logic_board.load_board(testing_boards[5])
        self.assertEqual(self.logic_board.can_view(0), testing_boards[5], 'Queen don\'t collide all 14 pieces')
        self.logic_board.load_board(testing_boards[6])
        self.assertEqual(self.logic_board.can_view(0), "Qc2w0", 'Queen collide Wrong pieces')

        # Horse (Knight)
        self.logic_board.load_board(testing_boards[7])
        self.assertEqual(self.logic_board.can_view(0), testing_boards[7], 'Horse don\'t collide all 14 pieces')
        self.logic_board.load_board(testing_boards[8])
        self.assertEqual(self.logic_board.can_view(0), "Nc2w0", 'Horse collide Wrong pieces')

        # Rook
        self.logic_board.load_board(testing_boards[9])
        self.assertEqual(self.logic_board.can_view(0), testing_boards[9], 'Rook don\'t collide all 8 pieces')
        self.logic_board.load_board(testing_boards[10])
        self.assertEqual(self.logic_board.can_view(0), "Ra7w1", 'Rook collide Wrong pieces')

        # Elephant (Bishop)
        self.logic_board.load_board(testing_boards[11])
        self.assertEqual(self.logic_board.can_view(0), testing_boards[11], 'Elephant don\'t collide all 8 pieces')
        self.logic_board.load_board(testing_boards[12])
        self.assertEqual(self.logic_board.can_view(0), "Ba7w1", 'Elephant collide Wrong pieces')

    # board index 13
    def test_get_piece(self):
        self.logic_board.load_board(testing_boards[13])
        self.assertEqual(self.logic_board.get_piece((0, 7)), self.logic_board.pieces[0], 'Wrong get Piece at (0, 7)')
        self.assertEqual(self.logic_board.get_piece([1, 7]), self.logic_board.pieces[1], 'Wrong get Piece at (1, 7)')
        self.assertEqual(self.logic_board.get_piece((2, 7)), self.logic_board.pieces[2], 'Wrong get Piece at (2, 7)')
        self.assertEqual(self.logic_board.get_piece((3, 7)), self.logic_board.pieces[3], 'Wrong get Piece at (3, 7)')
        self.assertEqual(self.logic_board.get_piece((4, 7)), self.logic_board.pieces[4], 'Wrong get Piece at (4, 7)')
        self.assertEqual(self.logic_board.get_piece((5, 7)), self.logic_board.pieces[5], 'Wrong get Piece at (5, 7)')
        self.assertEqual(self.logic_board.get_piece((6, 7)), self.logic_board.pieces[6], 'Wrong get Piece at (6, 7)')

    # board index 13
    def test_remove_piece(self):
        self.logic_board.load_board(testing_boards[13])
        a = self.logic_board.pieces[:]
        self.logic_board.remove_piece(a[1])
        a.pop(1)
        self.assertEqual(self.logic_board.pieces, a, 'Wrong getting Black')

    # all boards
    def test_get_board_line(self):
        for test_board in testing_boards:
            self.logic_board.load_board(test_board)
            self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                             test_board, 'Wrong export to Line')

    # board index 14
    def test_add_piece(self):
        self.logic_board.load_board(testing_boards[14])
        self.logic_board.add_piece("Qb1w1")
        self.logic_board.add_piece("Nc1w1")
        self.logic_board.add_piece("Rd1w0")
        self.logic_board.add_piece("Be1w0")
        self.logic_board.add_piece("f1w0")
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                         "Ka1w0 Kg1b0 Qb1w1 Nc1w1 Rd1w0 Be1w0 f1w0", 'Error in method add_piece or get_board_line')

    # board index 15
    # !not tested move in fog if need
    def test_move(self):
        self.logic_board.load_board(testing_boards[15])
        self.logic_board.move((0, 7), (0, 6))  # White King Up
        self.logic_board.move((1, 7), (1, 5))  # Black Queen 2Up
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                         "Ka2w0 Qb3b1 Nc1b1 Rd1w0 Be1w0 f1w0 Kg1b0", "Error on move figure")
        self.logic_board.move((0, 6), (1, 5))  # White King eat Black Queen
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                         "Kb3w0 Nc1b1 Rd1w0 Be1w0 f1w0 Kg1b0", "Error on eat figure")
        self.logic_board.move((2, 7), (4, 5))  # Black Horse can't make this move
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                         "Kb3w0 Nc1b1 Rd1w0 Be1w0 f1w0 Kg1b0", "Figure can\'t make this move")
        self.logic_board.move((2, 7), (3, 5))  # Black Horse move 1Right 2Up
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                         "Kb3w0 Nd3b1 Rd1w0 Be1w0 f1w0 Kg1b0", "Figure can make this move")
        self.logic_board.move((3, 7), (3, 4))  # Rook can't make move Over enemy Piece
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                         "Kb3w0 Nd3b1 Rd1w0 Be1w0 f1w0 Kg1b0", "Figure can\'t make Over Figure")
        self.logic_board.move((3, 7), (3, 6))  # Rook move 1Up
        self.logic_board.move((6, 7), (6, 6))  # Black King move 1Up
        self.logic_board.move((4, 7), (3, 6))  # White Bishop can't eat White Rook
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                         "Kb3w0 Nd3b1 Rd2w0 Be1w0 f1w0 Kg2b0", "Figure can\'t eat Friendly Figure")
        self.logic_board.move((4, 7), (1, 4))  # White Bishop can't move Over friendly Figur
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                         "Kb3w0 Nd3b1 Rd2w0 Be1w0 f1w0 Kg2b0", "Figure can't move Over friendly Figur")
        self.logic_board.move((3, 6), (3, 5))  # Rook eat enemy Horse
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces),
                         "Kb3w0 Rd3w0 Be1w0 f1w0 Kg2b0", "Figure can't move Over friendly Figur")
