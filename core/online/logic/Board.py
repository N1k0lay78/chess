from Source.boards import boards
from Source.settings import name_board_to_play
from core.logic.PiecesManager import PiecesManager, logic_pieces_dict, LoadingBoardError
from Source.special_functools import special_print


class LogicBoard:
    def __init__(self, server, is_on_fog_of_war=False):
        # settings
        self.server = server
        self.with_fog_of_war = is_on_fog_of_war
        # game logic
        self.pieces = []
        self.step = 0
        # init
        self.pieces_manager = PiecesManager(self, logic_pieces_dict)

    def move(self, from_cell, to_cell):
        piece = self.get_piece(from_cell)

        line_board = self.get_board_line(self.pieces)

        if piece and piece.color == self.step % 2 and piece.update(to_cell):
            if not self.check_shah(self.step % 2):
                special_print("NEXT MOVE", level=10)
                self.step += 1
                return True
            else:
                self.load_board(line_board)
                return False
        else:
            return False

    def can_view(self, color):

        if self.with_fog_of_war:
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
        else:
            return self.get_board_line(self.pieces)

    def get_piece(self, cell):
        for piece in self.pieces:
            if piece.cell[0] == cell[0] and piece.cell[1] == cell[1]:
                return piece

    def remove_piece(self, piece):
        if type(piece) == logic_pieces_dict["K"]:
            self.restart_game(piece.color)
        else:
            self.pieces.remove(piece)

    def restart_game(self, color):
        special_print('won', ("white" if color == 1 else "black"), level=10)
        self.step = -1
        self.load_board(boards[name_board_to_play])

    def get_pieces(self, color):
        return list(filter(lambda p: p.color == color, self.pieces))

    def get_board_line(self, pieces):
        return self.pieces_manager.get_line(pieces)

    def add_piece(self, code):
        try:
            self.pieces.append(self.pieces_manager.add_piece(code))
        except LoadingBoardError as e:
            special_print(e, level=10)

    def load_board(self, line):  # loading pieces from line with pieces info
        try:
            self.pieces = self.pieces_manager.read_line(line)
        except LoadingBoardError as e:
            self.pieces = []
            special_print(e, level=10)

    def check_shah(self, color):
        king = None
        for piece in self.pieces:
            if piece.st == [color, "K"]:
                king = piece

        if not king:
            return True

        for piece in self.get_pieces((color + 1) % 2):
            if piece.can_move(king.cr):
                # after check cannot castling
                king.is_can = False
                return True

        return False

    def check_mat(self, color):
        king = None
        for piece in self.pieces:
            if piece.st == [color, "K"]:
                king = piece

        if not king:
            return True

        attacking_pieces = []
        for piece in self.get_pieces((color + 1) % 2):
            if piece.can_move(king.cr):
                attacking_pieces.append(piece)

        if len(attacking_pieces) == 0:
            return False
        elif self.check_move_out(king, attacking_pieces):
            return False
        elif len(attacking_pieces) > 1:
            return True

        elif len(attacking_pieces) == 1 and attacking_pieces[0].t != "N":
            pass

    def under_attack(self, cell, pieces):
        return any(piece.can_move(cell) for piece in pieces)

    def check_king_move_out(self, king, pieces):
        # if the king is under the check, he cannot castling
        moves = ([0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1])
        # check that the king can make this move, and nothing threatens him there
        # (they won’t eat it on the next move)
        return any(
            king.can_move([king.c + move[0], king.r + move[1]]) and
            not self.under_attack([king.c + move[0], king.r + move[1]], pieces)
            for move in moves
        )
