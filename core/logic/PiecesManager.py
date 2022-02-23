from core.pieces.King import King
from core.pieces.Queen import Queen
from core.pieces.Horse import Horse
from core.pieces.Rook import Rook
from core.pieces.Elephant import Elephant
from core.pieces.Pawn import Pawn

from core.online.logic.King import LogicKing
from core.online.logic.Queen import LogicQueen
from core.online.logic.Horse import LogicHorse
from core.online.logic.Rook import LogicRook
from core.online.logic.Elephant import LogicElephant
from core.online.logic.Pawn import LogicPawn

import re

game_pieces_dict = {"K": King, "Q": Queen, "N": Horse, "R": Rook, "B": Elephant, "P": Pawn, }
logic_pieces_dict = {"K": LogicKing, "Q": LogicQueen, "N": LogicHorse, "R": LogicRook,
                     "B": LogicElephant, "P": LogicPawn, }


class LoadingBoardError(Exception):
    pass


class PiecesManager:
    def __init__(self, board, pieces_dict=None):
        if pieces_dict is None:
            pieces_dict = {}

        self.pieces_dict = pieces_dict

        self.classes_dict = {}
        for key, val in self.pieces_dict.items():
            self.classes_dict[val] = key

        self.board = board
        self.check_line_rule = f"[{''.join(self.pieces_dict.keys()).lower()}][a-h][1-8][wb]"

    def add_piece(self, code: str):
        if len(code) == 3:
            code = "p" + code

        code = code.lower()

        if code[0].upper() in self.pieces_dict and re.match(self.check_line_rule, code):
            piece = self.pieces_dict[code[0].upper()](self.board, [104 - ord(code[1]), 8 - int(code[2])],
                                                      int(code[3] != 'w'))
            return piece
        else:
            raise LoadingBoardError(f"can't decode {code}")

    def read_line(self, line: str) -> list:
        loaded_pieces = []

        for code in line.split():
            loaded_pieces.append(self.add_piece(code))

        return loaded_pieces

    def get_line(self, pieces_to_line):
        return " ".join(map(str, pieces_to_line))


if __name__ == '__main__':
    from Source.boards import boards

    class Nothing1:
        type = "P"

        def __init__(self, board, pos, color):
            self.board = board
            self.pos = pos
            self.color = color

        def __repr__(self):
            return f"{self.type}:{self.pos[0]}x{self.pos[1]}:{self.color}"

    class Nothing2(Nothing1):
        type = "K"

    pieces = {"P": Nothing1, "K": Nothing2}
    pieces_manager = PiecesManager(None, pieces)
    assert list(map(str, board_line.read_line(boards["test2"]))) == ["K:7x0:1", "K:0x7:0", "P:5x1:0", "P:5x6:1"]
    try:
        board_line.read_line("0235")
        print("Wrong")
    except LoadingBoardError:
        pass
