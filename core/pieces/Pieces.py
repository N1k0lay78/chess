class Pieces:
    def __init__(self, game, pos, surface, color):
        self.game = game
        self.pos = pos
        self.surface = surface
        self.color = color

    def check_move(self, pos):
        return pos != self.pos

    def draw(self):
        self.game.screen.blit(self.surface, (self.game.board.position[0] + self.game.board.size[0] * self.pos[0],
                                             self.game.board.position[1] + self.game.board.size[1] * self.pos[1] - 100))

    def update(self, pos):
        res = self.check_move(pos)
        if res:
            if self.game.board.get_pos(pos):
                self.game.board.board.remove(self.game.board.get_pos(pos))
            self.pos = pos
            self.game.board.focused = None

    def __repr__(self):
        return f"{self.color}"
