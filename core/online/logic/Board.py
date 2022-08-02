from Source.boards import boards
from Source.settings import params
from core.logic.PiecesManager import PiecesManager, logic_pieces_dict, LoadingBoardError


class LogicBoard:
    def __init__(self, is_on_fog_of_war=False):
        # settings
        self.with_fog_of_war = is_on_fog_of_war
        # game logic
        self.last_moved = None
        self.pieces = []
        self.step = 0
        self.is_playing = True
        # init
        self.pieces_manager = PiecesManager(self, logic_pieces_dict)

    def check_pawn(self):
        for piece in self.pieces:
            if piece.t == "" and piece.r in [0, 7]:
                return True, piece.cr
        return False, [-1, -1]

    def move(self, from_cell, to_cell, increment=False):
        if not self.is_playing:
            return False
        piece = self.get_piece(from_cell)
        line_board = self.get_board_line(self.pieces)

        if piece and piece.color == self.step % 2 and piece.update(to_cell):

            # castling
            if piece.t == "K" and from_cell in [[4, 0], [4, 7]] and to_cell in [[2, 0], [2, 7], [6, 0], [6, 7]]:
                rook_pos = {"Kg8b0": [7, 0], "Kc8b0": [0, 0], "Kg1w0": [7, 7], "Kc1w0": [0, 7]}
                rook_to = {"Kg8b0": [5, 0], "Kc8b0": [3, 0], "Kg1w0": [5, 7], "Kc1w0": [3, 7]}
                rook = self.get_piece(rook_pos[str(piece)])
                if rook and rook.i:
                    rook.set_cell(rook_to[str(piece)])
                    if increment:
                        self.step += 1
                    self.last_moved = piece
                    return True
                self.load_board(line_board)
                return False

            if not self.check_shah(self.step % 2):
                # print("PAT IS", self.check_pat((self.step + 1) % 2))
                # print("MAT IS", self.check_mat((self.step + 1) % 2))
                if self.check_mat((self.step + 1) % 2):
                    print("SOME ONE LOSE")
                    self.is_playing = False
                    # self.restart_game(self.step % 2)
                elif self.check_pat((self.step + 1) % 2):
                    print("DRAW")
                    self.is_playing = False
                    # self.restart_game()
                else:
                    print("NEXT MOVE")
                    if increment:
                        self.step += 1
                self.last_moved = piece
                return True
        self.load_board(line_board)
        return False

    def get_visible(self, color):
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
            return visible
        else:
            return self.pieces

    def can_view_cell(self, pos, color):
        if params['mode'] == "fog of war":
            return any(piece.s == color and piece.can_view(pos) for piece in self.pieces)
        return True

    def can_view(self, color):
        return self.get_board_line(self.get_visible(color))

    def get_piece(self, cell):
        for piece in self.pieces:
            if piece.cell[0] == cell[0] and piece.cell[1] == cell[1]:
                return piece

    def remove_piece(self, piece):
        if type(piece) == logic_pieces_dict["K"]:
            self.restart_game(piece.color)
        else:
            self.pieces.remove(piece)

    def restart_game(self, color=None):
        self.is_playing = True
        if color:
            print('won', ("white" if color == 1 else "black"))
        self.step = 0
        self.load_board(boards[params["board_name"]])

    def get_step(self):
        return self.step

    def get_last_move_piece(self):
        return self.last_moved

    def get_pieces(self, color):
        return list(filter(lambda p: p.color == color, self.pieces))

    def get_board_line(self, pieces):
        return self.pieces_manager.get_line(pieces)

    def add_piece(self, code):
        try:
            self.pieces.append(self.pieces_manager.add_piece(code))
        except LoadingBoardError as e:
            print(e)

    def load_board(self, line):  # loading pieces from line with pieces info
        try:
            self.pieces = self.pieces_manager.read_line(line)
        except LoadingBoardError as e:
            self.pieces = []
            print(e)

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
        enemy_pieces = self.get_pieces((color + 1) % 2)
        for piece in enemy_pieces:
            if piece.can_move(king.cr):
                attacking_pieces.append(piece)

        if len(attacking_pieces) == 0:  # no attacking pieces
            return False
        elif self.check_king_move_out(king, enemy_pieces):  # can move out
            return False
        elif len(attacking_pieces) > 1:  # count attacking pieces > 1 and king can't move out
            return True

        friendly_pieces = self.get_pieces(king.s)

        # try to eat enemy pieces
        for piece in friendly_pieces:
            if piece.can_move(attacking_pieces[0].cr):
                if piece.t != "K":
                    return False
                elif not self.under_attack(attacking_pieces[0].cr, enemy_pieces):
                    return False

        # try blocking way
        # if Not (Horse or Pawn) and count attacking pieces == 1
        if attacking_pieces[0].t not in "NP":
            path = attacking_pieces[0].get_path(king.cr)[:-1]
            for piece in friendly_pieces:
                for c, r, _ in path:
                    if piece.t != "K" and piece.can_move([c, r]):
                        return False

        # can't eat or block way
        return True

    def check_pat(self, color):
        king = None
        for piece in self.pieces:
            if piece.st == [color, "K"]:
                king = piece

        if not king:
            return True

        enemy_pieces = self.get_pieces((color + 1) % 2)
        friendly_pieces = self.get_pieces(color)

        for piece in friendly_pieces:
            if piece.t != "K":
                for c in range(8):
                    for r in range(8):
                        if piece.can_move([c, r]):
                            return False
            elif self.check_king_move_out(king, enemy_pieces):
                return False

        # we can't make any step
        return True

    def under_attack(self, cell, pieces):
        return any(piece.get_path(cell) for piece in pieces)

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
