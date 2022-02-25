from threading import Thread
from core.online.Client import Client


class OnlineJudge:
    def __init__(self, board, board_line: str):
        self.board = board
        self.board_line = board_line
        self.nickname = input()
        self.socket, self.port = "172.16.148.190", 8080
        self.client = Client(board, self.nickname, self.socket, self.port, self)
        self.client_thread = Thread(target=self.client.run)
        self.client_thread.start()

    def on_move(self, fr: tuple, to: tuple) -> None:
        """pieces make move"""
        piece = self.board.get_pos(to)
        if piece.name == "" and to[1] in [0, 7] and not self.board.game.restart:
            self.on_swap(to)

        if self.board.color == 1:
            self.client.sending_to_the_server(f"mo {7-fr[0]},{7-fr[1]}:{7-piece.cell[0]},{7-piece.cell[1]}:{str(piece).lower()}")
        else:
            self.client.sending_to_the_server(f"mo {fr[0]},{fr[1]}:{piece.cell[0]},{piece.cell[1]}:{str(piece).lower()}")

    def on_remove(self, name: str) -> None:
        """on pieces eat"""
        # if the king died, then we restart the game
        if name == "K":
            self.board.game.restart = True

    def on_swap(self, cell: tuple) -> None:
        """swap pawn"""
        pawn = self.board.get_pos(cell)
        self.board.remove_piece(pawn)
        self.board.add_piece(input("CHOICE: ").upper() + str(pawn))

    def on_castling(self, is_right: bool, color: int) -> None:
        """king make castling"""
        pass

    def update(self) -> None:
        pass

    def restart(self) -> None:
        pass
        # self.board.load_board(self.board_line)

    def flip(self):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        self.board.color = 1
        for piece in self.board.board:
            piece.set_cell((7 - piece.cell[0], 7 - piece.cell[1]))

    def quit(self) -> None:
        self.client.stop()
        self.client_thread.join()
