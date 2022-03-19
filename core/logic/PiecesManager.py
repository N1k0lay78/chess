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
        self.check_line_rule = f"[{''.join(self.pieces_dict.keys()).lower()}][a-h][1-8][wb][0-1]"

    def add_piece(self, code: str):
        if re.match("[a-h][1-8][wb][0-1]", code):
            code = "p" + code

        code = code.lower()

        if code[0].upper() in self.pieces_dict and re.match(self.check_line_rule, code):
            piece = self.pieces_dict[code[0].upper()](self.board, [ord(code[1]) - 97, 8 - int(code[2])],
                                                      int(code[3] != 'w'), code[4] == "1")
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
