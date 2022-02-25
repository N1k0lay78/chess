class Judge:
    def __init__(self, board, board_line: str):
        self.board = board
        self.board_line = board_line

    def on_move(self, fr: tuple, to: tuple) -> None:
        """pieces make move"""
        if self.board.get_pos(to).name == "" and to[1] in [0, 7] and not self.board.game.restart:
            self.on_swap(to)
        self.board.go_to_next_step()
        self.board.color = int(not self.board.color)
        # flip the board
        self.flip()

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
        self.board.load_board(self.board_line)

    def flip(self):
        for piece in self.board.board:
            piece.set_cell((7 - piece.cell[0], 7 - piece.cell[1]))

    def quit(self) -> None:
        pass
