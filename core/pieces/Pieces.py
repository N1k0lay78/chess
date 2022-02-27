import pygame

from core.online.logic.Pieces import LogicPieces


class Pieces(LogicPieces):
    def __init__(self, game, name, cell, color, is_can):
        self.pos = [0, 0]
        super().__init__(game, name, cell, color, is_can)
        self.surface = self.load_surface()

    def load_surface(self):
        return pygame.Surface((100, 100))

    def draw(self):
        self.board.screen.blit(self.surface, (self.pos[0], self.pos[1] - 100))

    def update(self, cell: tuple):
        if 0 <= cell[0] <= 7 and 0 <= cell[1] <= 7 and self.can_move(cell):
            # move
            fr = self.cell[:]
            self.set_cell(cell)
            self.on_move()
            self.board.board.focused = None
            self.board.judge.on_move(fr, cell)
        else:
            # move the piece to its original position
            self.set_cell(self.cell)

    def eval_pos(self):
        self.pos = [self.board.board.position[0] + self.board.board.size[0] * self.cell[0],
                    self.board.board.position[1] + self.board.board.size[1] * self.cell[1]]

    def move(self, move):
        self.pos[0] -= move[0]
        self.pos[1] -= move[1]

    def set_cell(self, cell):
        self.cell = cell
        self.eval_pos()

    def get_piece(self, cell):
        return self.board.board.get_pos(cell)

    def remove_piece(self, piece):
        return self.board.board.remove_piece(piece)

    def __repr__(self):
        # everyone is watching from their side
        if self.board.board.color:
            return f"{self.name}{chr(97+self.cell[0])}{self.cell[1]+1}{'w' if self.color == 0 else 'b'}{int(self.is_can)}"
        else:
            return f"{self.name}{chr(104-self.cell[0])}{8-self.cell[1]}{'w' if self.color == 0 else 'b'}{int(self.is_can)}"
