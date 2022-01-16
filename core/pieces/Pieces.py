from core.online.logic.Pieces import LogicPieces


class Pieces(LogicPieces):
    def __init__(self, game, name, cell, surface, color):
        self.pos = [0, 0]
        self.game = game
        super().__init__(name, cell, color)
        self.surface = surface

    def draw(self):
        if self.game.board.step % 2 == 0:
            self.game.screen.blit(self.surface, (self.pos[0],
                                                 self.pos[1] - 100))
        else:
            self.game.screen.blit(self.surface, (self.pos[0],
                                                 self.pos[1] - 100))

    def update(self, cell):
        if 0 <= cell[0] <= 7 and 0 <= cell[1] <= 7 and self.can_move(cell):
            # move
            if self.game.board.color == 1:
                self.game.client.sending_to_the_server(f"mo {7-self.cell[0]},{7-self.cell[1]}:{7-cell[0]},{7-cell[1]}:{str(self).lower()}")
            else:
                self.game.client.sending_to_the_server(f"mo {self.cell[0]},{self.cell[1]}:{cell[0]},{cell[1]}:{str(self).lower()}")
            self.set_cell(cell)
            self.on_move()
            self.game.board.go_to_next_step()
            self.game.board.focused = None
        else:
            # move the figure to its original position
            self.set_cell(self.cell)

    def eval_pos(self):
        self.pos = [self.game.board.position[0] + self.game.board.size[0] * self.cell[0],
                    self.game.board.position[1] + self.game.board.size[1] * self.cell[1]]

    def move(self, move):
        self.pos[0] -= move[0]
        self.pos[1] -= move[1]

    def set_cell(self, cell):
        self.cell = cell
        self.eval_pos()

    def get_piece(self, cell):
        return self.game.board.get_pos(cell)

    def remove_piece(self, piece):
        return self.game.board.remove_from_board(piece)

    def __repr__(self):
        # everyone is watching from their side
        if self.game.color:
            return f"{self.name}{chr(97+self.cell[0])}{self.cell[1]+1}{'w' if self.color == 0 else 'b'}"
        else:
            return f"{self.name}{chr(104-self.cell[0])}{8-self.cell[1]}{'w' if self.color == 0 else 'b'}"
