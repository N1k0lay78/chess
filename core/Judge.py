from Source.boards import boards
from loguru import logger


class Judge:
    def __init__(self, window, board, board_line: str):
        self.window = window
        self.board = board
        self.board_line = board_line
        self.board.load_board(boards[board_line])

    def get_color(self):
        return self.board.step % 2

    def on_move(self, fr: tuple, to: tuple) -> None:
        """pieces make move"""
        piece = self.board.get_piece(to)
        logger.info(f"move {piece.t}{'b' if piece.s else 'w'} {self.chr_cell(fr)} — {self.chr_cell(to)}")

    def on_remove(self, name: str) -> None:
        """on pieces eat"""
        pass

    def on_swap(self, choice: str) -> None:
        """swap pawn"""
        self.board.get_piece(self.board.check_pawn()[1]).replace(choice)

    def on_castling(self, is_right: bool, color: int) -> None:
        """king make castling"""
        pass

    def update(self) -> None:
        pass

    def restart(self) -> None:
        self.board.restart(self.board_line)

    def quit(self) -> None:
        pass

    def chr_cell(self, cell):
        return f"{chr(65 + cell[0])}{8 - cell[1]}"
