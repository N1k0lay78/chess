from Source.boards import boards
from Source.settings import name_board_to_play
from core.logic.PiecesManager import PiecesManager, logic_pieces_dict, LoadingBoardError
from Source.settings import debug


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

        if piece and piece.color == self.step % 2 and piece.update(to_cell):
            if debug:
                print("NEXT MOVE")

            self.step += 1
            return True
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
            print('won', ("white" if piece.color == 1 else "black"))
            self.load_board(boards[name_board_to_play])
        else:
            self.pieces.remove(piece)

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
