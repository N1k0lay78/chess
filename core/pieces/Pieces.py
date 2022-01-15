from threading import Thread


class Pieces:
    def __init__(self, game, name, cell, surface, color):
        self.game = game
        self.pos = [0, 0]
        self.cell = [0, 0]
        self.name = name
        self.set_cell(cell)
        self.surface = surface
        self.color = color  # 0 - downside (green), 1 - upside (red)

    def check_move(self, pos):
        return pos != self.pos

    def draw(self):
        if self.game.board.step % 2 == 0:
            self.game.screen.blit(self.surface, (self.pos[0],
                                                 self.pos[1] - 100))
        else:
            self.game.screen.blit(self.surface, (self.pos[0],
                                                 self.pos[1] - 100))

    def check_clear_cell(self, cell):  # cell is clear
        return not self.game.board.get_pos(cell)

    def check_not_friendly_cell(self, cell):  # cell is clear or enemy on cell
        piece = self.game.board.get_pos(cell)
        if piece:
            if piece.color != self.color:
                self.game.board.remove_from_board(piece)
                return True
            elif piece.color == self.color:
                return False
        return True

    def can_eat(self, cell):  # enemy on cell
        piece = self.game.board.get_pos(cell)
        if piece and piece.color != self.color:
            self.game.board.remove_from_board(piece)
            return True
        return False

    def update(self, cell):
        if 0 <= cell[0] <= 7 and 0 <= cell[1] <= 7 and self.check_move(cell):
            # move
            self.game.client.sending_to_the_server(f"Mo{self.cell[0]},{self.cell[1]}:{cell[0]},{cell[1]}:{self.color}:{self}")
            self.set_cell(cell)
            self.on_move()
            self.game.board.go_to_next_step()
            self.game.board.focused = None
        else:
            # move the figure to its original position
            self.set_cell(self.cell)

    def set_cell(self, cell):
        self.cell = cell
        self.eval_pos()

    def eval_pos(self):
        self.pos = [self.game.board.position[0] + self.game.board.size[0] * self.cell[0],
                    self.game.board.position[1] + self.game.board.size[1] * self.cell[1]]

    def move(self, move):
        self.pos[0] -= move[0]
        self.pos[1] -= move[1]

    def on_move(self):
        pass

    def __repr__(self):
        return f"{self.name}{chr(104-self.cell[0])}{self.cell[1]+1}{'w' if self.color == 0 else 'b'}"
