from unittest import TestCase
from core.logic.PiecesManager import PiecesManager, game_pieces_dict, logic_pieces_dict
from core.Board import Board
from core.online.logic.Board import LogicBoard

testing_boards = [
    "a1b1",  # Left Bottom Black Active              1
    "a1b0",  # Left Bottom Black Dis-active          2
    "a1w1",  # Left Bottom White Active              3
    "a1w0",  # Left Bottom White Dis-active          4
    "h8b1",  # Right Top Black Active                5
    "h8w1",  # Right Top White Active                6

    "Ka1b1",  # Left Bottom Black King               7
    "Qa1b1",  # Left Bottom Black Queen              8
    "Na1b1",  # Left Bottom Black Horse (Knight)     9
    "Ra1b1",  # Left Bottom Black Rook               10
    "Ba1b1",  # Left Bottom Black Elephant (Bishop)  11

    "h1w1",  # Right Bottom White Active             12
    "a8w1",  # Left Top White Active                 13
]


class Game:
    def __init__(self, board):
        self.board = board


class TestPiecesManager(TestCase):
    def setUp(self) -> None:
        self.board_white = Game(Board(None, (0, 0), (8, 8), 0))
        self.logic_board = LogicBoard(None)
        self.pieces_manager_game = PiecesManager(self.board_white, game_pieces_dict)
        self.pieces_manager_logic = PiecesManager(self.logic_board, logic_pieces_dict)

    # Game Board White GBW

    def test_lbba(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[0])[0].test(),
                         game_pieces_dict["P"](self.board_white, [0, 7], 1, True).test(),
                         'Left Bottom Black Active')

    def test_lbbd(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[1])[0].test(),
                         game_pieces_dict["P"](self.board_white, [0, 7], 1, False).test(),
                         'Left Bottom Black Dis-active')

    def test_lbwa(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[2])[0].test(),
                         game_pieces_dict["P"](self.board_white, [0, 7], 0, True).test(),
                         'Left Bottom White Active')

    def test_lbwd(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[3])[0].test(),
                         game_pieces_dict["P"](self.board_white, [0, 7], 0, False).test(),
                         'Left Bottom White Dis-active')

    def test_rtba(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[4])[0].test(),
                         game_pieces_dict["P"](self.board_white, [7, 0], 1, True).test(),
                         'Right Top Black Active')

    def test_rtwa(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[5])[0].test(),
                         game_pieces_dict["P"](self.board_white, [7, 0], 0, True).test(),
                         'Right Top White Active')

    def test_klbba(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[6])[0].test(),
                         game_pieces_dict["K"](self.board_white, [0, 7], 1, True).test(),
                         'Left Bottom Black King')

    def test_qlbba(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[7])[0].test(),
                         game_pieces_dict["Q"](self.board_white, [0, 7], 1, True).test(),
                         'Left Bottom Black Queen')

    def test_nlbba(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[8])[0].test(),
                         game_pieces_dict["N"](self.board_white, [0, 7], 1, True).test(),
                         'Left Bottom Black Horse (Knight)')

    def test_rlbba(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[9])[0].test(),
                         game_pieces_dict["R"](self.board_white, [0, 7], 1, True).test(),
                         'Left Bottom Black Rook')

    def test_blbba(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[10])[0].test(),
                         game_pieces_dict["B"](self.board_white, [0, 7], 1, True).test(),
                         'Left Bottom Black Elephant (Bishop)')

    def test_rbwa(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[11])[0].test(),
                         game_pieces_dict["P"](self.board_white, [7, 7], 0, True).test(),
                         'Right Bottom White Active')

    def test_ltwa(self):
        self.assertEqual(self.pieces_manager_game.read_line(testing_boards[12])[0].test(),
                         game_pieces_dict["P"](self.board_white, [0, 0], 0, True).test(),
                         'Left Top White Active')

    # Logic Board LB

    def test_llbba(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[0])[0].test(),
                         logic_pieces_dict["P"](self.logic_board, [0, 7], 1, True).test(),
                         'Logic Left Bottom Black Active')

    def test_llbbd(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[1])[0].test(),
                         logic_pieces_dict["P"](self.logic_board, [0, 7], 1, False).test(),
                         'Logic Left Bottom Black Dis-active')

    def test_llbwa(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[2])[0].test(),
                         logic_pieces_dict["P"](self.logic_board, [0, 7], 0, True).test(),
                         'Logic Left Bottom White Active')

    def test_llbwd(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[3])[0].test(),
                         logic_pieces_dict["P"](self.logic_board, [0, 7], 0, False).test(),
                         'Logic Left Bottom White Dis-active')

    def test_lrtba(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[4])[0].test(),
                         logic_pieces_dict["P"](self.logic_board, [7, 0], 1, True).test(),
                         'Logic Right Top Black Active')

    def test_lrtwa(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[5])[0].test(),
                         logic_pieces_dict["P"](self.logic_board, [7, 0], 0, True).test(),
                         'Logic Right Top White Active')

    def test_lklbba(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[6])[0].test(),
                         logic_pieces_dict["K"](self.logic_board, [0, 7], 1, True).test(),
                         'Logic Left Bottom Black King')

    def test_lqlbba(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[7])[0].test(),
                         logic_pieces_dict["Q"](self.logic_board, [0, 7], 1, True).test(),
                         'Logic Left Bottom Black Queen')

    def test_lnlbba(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[8])[0].test(),
                         logic_pieces_dict["N"](self.logic_board, [0, 7], 1, True).test(),
                         'Logic Left Bottom Black Horse (Knight)')

    def test_lrlbba(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[9])[0].test(),
                         logic_pieces_dict["R"](self.logic_board, [0, 7], 1, True).test(),
                         'Logic Left Bottom Black Rook')

    def test_lblbba(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[10])[0].test(),
                         logic_pieces_dict["B"](self.logic_board, [0, 7], 1, True).test(),
                         'Logic Left Bottom Black Elephant (Bishop)')

    def test_lrbwa(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[11])[0].test(),
                         logic_pieces_dict["P"](self.logic_board, [7, 7], 0, True).test(),
                         'Logic Right Bottom White Active')

    def test_lltwa(self):
        self.assertEqual(self.pieces_manager_logic.read_line(testing_boards[12])[0].test(),
                         logic_pieces_dict["P"](self.logic_board, [0, 0], 0, True).test(),
                         'Logic Left Top White Active')
