from core.Board import Board
import pygame

from core.FogOfWar import FogOfWar


class Game:
    def __init__(self, size, title, fps=30, icon=None, **flags):
        self.screen = pygame.display.set_mode(size, **flags)
        if title:
            pygame.display.set_caption(title)
        if icon:
            pygame.display.set_icon(icon)
        self.running = True
        self.clock = pygame.time.Clock()
        self.max_fps = fps
        self.board = Board(self, (100, 100), (50, 50))
        self.board.generate_board()
        self.fog = FogOfWar(self, (-50, -50), 3, (50, 50), 'fog')

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
                self.board.update(event)

    def draw(self):
        self.screen.fill((20, 20, 50))
        self.board.draw()
        self.fog.draw()

    def run(self):
        while self.running:
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.max_fps)
        self.save()

    def save(self):
        pass
