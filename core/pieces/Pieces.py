class Pieces:
    def __init__(self, game, cell, surface, color):
        self.game = game
        self.pos = [0, 0]
        self.set_cell(cell)
        self.surface = surface
        self.color = color

    def check_move(self, pos):
        return pos != self.pos

    def draw(self):
        self.game.screen.blit(self.surface, (self.pos[0],
                                             self.pos[1] - 100))

    def update(self, cell):
        if self.check_move(cell):
            if self.game.board.get_pos(cell):
                self.game.board.board.remove(self.game.board.get_pos(cell))
            self.set_cell(cell)
            self.game.board.focused = None

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
