from unittest import TestCase
from core.BoardLEGACY import Board
from core.online.logic.Board import LogicBoard

testing_boards = [
    "Kb7w0",             # White King              at B7 can't castling
    "Qb7w1",             # White Queen             at B7
    "Nc6w1",             # White Horse (Knight)    at C6
    "Rb7w1",             # White Rook              at B7
    "Bb7w1",             # White Elephant (Bishop) at B7
    "b2w1",              # White Pawn              at B2 can make long step

    "Ra1w1 Ke1w1",       # White Rook at A1 not move and White King at E1 not move
    "Ra1b1 Ke1w1",       # Black Rook at A1 not move and White King at E1 not move
    "Rh1w1 Ke1w1",       # White Rook at H1 not move and White King at E1 not move
    "Rh1b1 Ke1w1",       # Black Rook at H1 not move and White King at E1 not move
    "Rh8w1 Ke1w1",       # White Rook at H8 not move and White King at E1 not move
    "Rh8b1 Ke1w1",       # Black Rook at H8 not move and White King at E1 not move
    "Ra8w1 Ke1w1",       # White Rook at A8 not move and White King at E1 not move
    "Ra8b1 Ke1w1",       # Black Rook at A8 not move and White King at E1 not move
    "Rb7w1 Ke1w1",       # White Rook at B7 not move and White King at E1 not move
    "Rb7b1 Ke1w1",       # Black Rook at B7 not move and White King at E1 not move

    "b2w1 Qa3w1 Qc3b1",  # Black Pawn at B2 not move and White Queen at A3 and Black Queen at C3

    "b3w0",              # White pawn make move

    "Kd1w0 Qd3w0 Rc3w0 Bd2w0 c2w1 Nc1w0 Kh8b0 a2w1 a1w0 b2w1 b3w0 a7b1 a8b0 b7b1 b6b0",  # test move in or over
    "Kd1w0 Qd3w0 Rc3w0 Bd2w0 c2w1 Nc1w0 Kh8b0 a4w0 a1w0 b2w1 b3w0 a7b1 a8b0 b7b1 b6b0",
    "Kd1w0 Qd3w0 Rc3w0 Bd2w0 c2w1 Nc1w0 Kh8b0 a4w0 a1w0 b2w1 b3w0 a5b0 a8b0 b7b1 b6b0",
]


class TestPiecesMove(TestCase):
    def setUp(self) -> None:
        self.logic_board = LogicBoard("Server")

    def test_king(self):
        self.logic_board.load_board(testing_boards[0])
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 0]), True, 'King Left Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 1]), True, 'King Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 2]), True, 'King Right Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 0]), True, 'King Left')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 2]), True, 'King Right')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 0]), True, 'King Left Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 1]), True, 'King Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 2]), True, 'King Right Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 3]), False, 'King 2Right')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 7]), False, 'King RU')
        self.assertEqual(self.logic_board.pieces[0].can_move([7, 7]), False, 'King RD')
        self.assertEqual(self.logic_board.pieces[0].can_move([7, 0]), False, 'King LD')

    def test_queen(self):
        self.logic_board.load_board(testing_boards[1])
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 0]), True, 'Queen Left Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 1]), True, 'Queen Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 2]), True, 'Queen Right Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 0]), True, 'Queen Left')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 2]), True, 'Queen Right')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 0]), True, 'Queen Left Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 1]), True, 'Queen Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 2]), True, 'Queen Right Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 3]), True, 'Queen 2Right')
        self.assertEqual(self.logic_board.pieces[0].can_move([3, 1]), True, 'Queen 2Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 7]), False, 'Queen RU')
        self.assertEqual(self.logic_board.pieces[0].can_move([7, 7]), True, 'Queen RD')
        self.assertEqual(self.logic_board.pieces[0].can_move([7, 0]), False, 'Queen LD')

    def test_horse(self):
        self.logic_board.load_board(testing_boards[2])
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 0]), False, 'Horse (-2,  2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 0]), True,  'Horse (-1,  2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 0]), False, 'Horse (0,   2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([3, 0]), True,  'Horse (1,   2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([4, 0]), False, 'Horse (2,   2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([4, 1]), True,  'Horse (2,   1)')
        self.assertEqual(self.logic_board.pieces[0].can_move([4, 2]), False, 'Horse (2,   0)')
        self.assertEqual(self.logic_board.pieces[0].can_move([4, 3]), True,  'Horse (2,  -1)')
        self.assertEqual(self.logic_board.pieces[0].can_move([4, 4]), False, 'Horse (2,  -2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([3, 4]), True,  'Horse (1,  -2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 4]), False, 'Horse (0,  -2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 4]), True,  'Horse (-1, -2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 4]), False, 'Horse (-2, -2)')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 3]), True,  'Horse (-2, -1)')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 2]), False, 'Horse (-2, -0)')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 1]), True,  'Horse (-2, 1)')

    def test_rook(self):
        self.logic_board.load_board(testing_boards[3])
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 0]), False, 'Rook Left Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 1]), True,  'Rook Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 2]), False, 'Rook Right Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 0]), True,  'Rook Left')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 2]), True,  'Rook Right')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 0]), False, 'Rook Left Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 1]), True,  'Rook Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 2]), False, 'Rook Right Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 3]), True,  'Rook 2Right')
        self.assertEqual(self.logic_board.pieces[0].can_move([3, 1]), True,  'Rook 2Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 7]), False, 'Rook RU')
        self.assertEqual(self.logic_board.pieces[0].can_move([7, 7]), False, 'Rook RD')
        self.assertEqual(self.logic_board.pieces[0].can_move([7, 0]), False, 'Rook LD')

    def test_elephant(self):
        self.logic_board.load_board(testing_boards[4])
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 0]), True,  'Elephant Left Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 1]), False, 'Elephant Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 2]), True,  'Elephant Right Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 0]), False, 'Elephant Left')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 2]), False, 'Elephant Right')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 0]), True,  'Elephant Left Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 1]), False, 'Elephant Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 2]), True,  'Elephant Right Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 3]), False, 'Elephant 2Right')
        self.assertEqual(self.logic_board.pieces[0].can_move([3, 1]), False, 'Elephant 2Down')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 7]), False, 'Elephant RU')
        self.assertEqual(self.logic_board.pieces[0].can_move([7, 7]), True,  'Elephant RD')
        self.assertEqual(self.logic_board.pieces[0].can_move([7, 0]), False, 'Elephant LD')

    def test_pawn(self):
        self.logic_board.load_board(testing_boards[5])
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 5]), True,  'Pawn Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 4]), True,  'Pawn 2Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 5]), False, 'Pawn left Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 4]), False, 'Pawn left 2Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 5]), False, 'Pawn right Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 4]), False, 'Pawn right 2Up')

    def test_castling(self):
        self.logic_board.load_board(testing_boards[6])
        self.assertEqual(self.logic_board.pieces[1].can_move([0, 7]), True,  'King Long Castling')
        self.logic_board.load_board(testing_boards[7])
        self.assertEqual(self.logic_board.pieces[1].can_move([0, 7]), False, 'Castling White King Black Rook')
        self.logic_board.load_board(testing_boards[8])
        self.assertEqual(self.logic_board.pieces[1].can_move([7, 7]), True,  'King Castling')
        self.logic_board.load_board(testing_boards[9])
        self.assertEqual(self.logic_board.pieces[1].can_move([7, 7]), False, 'Castling White King Black Rook')

        self.logic_board.load_board(testing_boards[10])
        self.assertEqual(self.logic_board.pieces[1].can_move([7, 0]), False, 'Castling White Rook False Position H8')
        self.logic_board.load_board(testing_boards[11])
        self.assertEqual(self.logic_board.pieces[1].can_move([7, 0]), False, 'Castling White King Black Rook')
        self.logic_board.load_board(testing_boards[12])
        self.assertEqual(self.logic_board.pieces[1].can_move([0, 0]), False, 'Castling White Rook False Position A8')
        self.logic_board.load_board(testing_boards[13])
        self.assertEqual(self.logic_board.pieces[1].can_move([0, 0]), False, 'Castling White King Black Rook')

        self.logic_board.load_board(testing_boards[14])
        self.assertEqual(self.logic_board.pieces[1].can_move([1, 1]), False, 'Castling White Rook False Position B7')
        self.logic_board.load_board(testing_boards[15])
        self.assertEqual(self.logic_board.pieces[1].can_move([1, 1]), False, 'Castling White King Black Rook')

    def test_pawn_eat(self):
        self.logic_board.load_board(testing_boards[16])
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 5]), False, 'Pawn Can\'t eat teammate')
        self.assertEqual(self.logic_board.pieces[0].can_move([0, 4]), False, 'Pawn Can\'t')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 5]), True,  'Pawn Can\'t eat enemy Queen')
        self.assertEqual(self.logic_board.pieces[0].can_move([2, 4]), False, 'Pawn don\'t')

    def test_moved_pawn(self):
        self.logic_board.load_board(testing_boards[17])
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 4]), True,  'Pawn Up')
        self.assertEqual(self.logic_board.pieces[0].can_move([1, 3]), False, 'Pawn 2Up')

    def test_move_in(self):
        self.logic_board.load_board(testing_boards[18])

        # King
        self.logic_board.move([3, 7], [3, 6])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'King move into friendly figure')

        # Queen
        self.logic_board.move([3, 5], [2, 5])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Queen move into friendly figure')

        # Horse (Knight)
        self.logic_board.move([2, 7], [3, 5])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Horse move into friendly figure')

        # Rook
        self.logic_board.move([2, 5], [2, 6])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Rook move into friendly figure')

        # Elephant (Bishop)
        self.logic_board.move([3, 6], [2, 7])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Elephant move into friendly figure')

        # Pawn
        self.logic_board.move([2, 6], [2, 5])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Pawn move into friendly figure')

    def test_move_over(self):
        self.logic_board.load_board(testing_boards[18])

        # Queen
        self.logic_board.move([3, 5], [1, 5])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Queen move over friendly figure')

        # Rook
        self.logic_board.move([2, 5], [4, 5])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Rook move over friendly figure')

        # Elephant (Bishop)
        self.logic_board.move([3, 6], [1, 4])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Elephant move over friendly figure')

        # Pawn
        self.logic_board.move([2, 6], [2, 4])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Pawn move over friendly figure')

        self.logic_board.move([1, 6], [1, 4])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Pawn move over friendly figure')

        self.logic_board.move([1, 1], [1, 3])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[18],
                         'Pawn move over friendly figure')

        self.logic_board.move([0, 6], [0, 4])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[19],
                         'Pawn pawn can make this move')

        self.logic_board.move([0, 1], [0, 3])
        self.assertEqual(self.logic_board.get_board_line(self.logic_board.pieces), testing_boards[20],
                         'Pawn pawn can make this move')
