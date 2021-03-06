from loguru import logger

from Source.settings import params


class OnlineJudge:
    def __init__(self, board, client):
        self.board = board
        self.nickname = params["nickname"]
        self.socket, self.port = params["online_host_ip"], params["online_host_port"]
        self.client = client
        self.make_castling = False
        self.color = 0

    def get_color(self):
        return self.color

    def on_move(self, fr: tuple, to: tuple) -> None:
        """pieces make move"""
        piece = self.board.get_piece(to)

        logger.info(f"move {piece.t}{'b' if piece.s else 'w'} {self.chr_cell(fr)} — {self.chr_cell(to)}")

        self.client.sending_to_the_server(f"mo {fr[0]},{fr[1]}:{to[0]},{to[1]}:{str(piece).lower()}")

    def on_remove(self, name: str) -> None:
        """on pieces eat"""

        # TODO: this

        # if the king died, then we restart the game
        # if name == "K":
        #     self.board.game.restart = True

    def on_swap(self, choice: str) -> None:
        """swap pawn"""
        self.client.room.figure = choice

    def on_castling(self, is_right: bool, color: int) -> None:
        """king make castling"""
        pass

    def update(self) -> None:
        pass

    def restart(self) -> None:
        pass

    def quit(self) -> None:
        pass

    def chr_cell(self, cell):
        return f"{chr(65 + cell[0])}{8 - cell[1]}"
