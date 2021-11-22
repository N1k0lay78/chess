class Pieces:
    def __init__(self, game, cell, surface, color):
        self.game = game
        self.pos = [0, 0]
        self.cell = [0, 0]
        self.set_cell(cell)
        self.surface = surface
        self.color = color

    def check_move(self, pos):
        return pos != self.pos

    def draw(self):
        self.game.screen.blit(self.surface, (self.pos[0],
                                             self.pos[1] - 100))

    def check_clear_cell(self, cell):
        piece = self.game.board.get_pos(cell)
        if piece:
            return False
        return True

    def check_not_friendly_cell(self, cell):
        piece = self.game.board.get_pos(cell)
        if piece:
            if piece.color != self.color:
                self.game.board.remove_from_board(piece)
                return True
            elif piece.color == self.color:
                return False
        return True

    def can_eat(self, cell):
        piece = self.game.board.get_pos(cell)
        if piece:
            if piece.color != self.color:
                self.game.board.remove_from_board(piece)
                return True
        return False

    def update(self, cell):
        print(cell)
        if self.check_move(cell):
            self.set_cell(cell)
            self.game.board.go_to_next_step()
            self.game.board.focused = None
        else:
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

    def __repr__(self):
        return f"{self.color}"
