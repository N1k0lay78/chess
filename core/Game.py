from core.Board import Board
import pygame


class Game:
    def __init__(self, size, title, fps=15, icon=None, flags={}):
        self.screen = pygame.display.set_mode(size, **flags)
        if title:
            pygame.display.set_caption(title)
        if icon:
            pygame.display.set_icon(icon)
        self.running = True
        self.clock = pygame.time.Clock()
        self.max_fps = fps
        self.board = Board(self, (0, 0), (50, 50), (220, 220, 220), (50, 50, 50))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("GAY")
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.board.update(event)

    def draw(self):
        self.board.draw()

    def run(self):
        while self.running:
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.max_fps)
        self.save()

    def save(self):
        pass
