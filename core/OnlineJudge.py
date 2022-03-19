from threading import Thread
from Source.settings import online_host_ip, online_host_port, nickname
from core.online.Client import Client


class OnlineJudge:
    def __init__(self, board):
        self.board = board
        self.nickname = nickname if nickname else input()
        self.socket, self.port = online_host_ip, online_host_port
        self.client = Client(board, self.nickname, self.socket, self.port, self)
        self.client_thread = Thread(target=self.client.run)
        self.client_thread.start()
        self.make_castling = False

    def on_move(self, fr: tuple, to: tuple) -> None:
        """pieces make move"""
        piece = self.board.get_pos(to)

        if piece.name == "" and to[1] in [0, 7] and not self.board.game.restart:
            self.on_swap(to)

        if self.make_castling:
            to[0] = 0 if to[0] in [1, 2] else 7
            self.make_castling = False

        if self.board.color == 1:
            self.client.sending_to_the_server(f"mo {7-fr[0]},{7-fr[1]}:{7-to[0]},{7-to[1]}:{str(piece).lower()}")
        else:
            self.client.sending_to_the_server(f"mo {fr[0]},{fr[1]}:{to[0]},{to[1]}:{str(piece).lower()}")

    def on_remove(self, name: str) -> None:
        """on pieces eat"""

        # TODO: this

        # if the king died, then we restart the game
        # if name == "K":
        #     self.board.game.restart = True

    def on_swap(self, cell: tuple) -> None:
        """swap pawn"""

        # TODO: this

        # pawn = self.board.get_pos(cell)
        # self.board.remove_piece(pawn)
        # self.board.add_piece(input("CHOICE: ").upper() + str(pawn))

    def on_castling(self, is_right: bool, color: int) -> None:
        """king make castling"""
        self.make_castling = True

    def update(self) -> None:
        pass

    def restart(self) -> None:
        pass

    def flip(self):
        self.board.color = 1
        for piece in self.board.board:
            piece.set_cell((7 - piece.cell[0], 7 - piece.cell[1]))

    def quit(self) -> None:
        self.client.stop()
        self.client_thread.join()
