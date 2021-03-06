from Source.boards import boards
from Source.settings import is_on_fog_of_war
from core.online.Client import Client
from core.Judge import Judge
from core.OnlineJudge import OnlineJudge
from core.FogOfWarLEGACY import FogOfWar
from core.BoardLEGACY import Board
from threading import Thread
import socket
import pygame


class Game:
    def __init__(self, size: tuple, title: str, color: int, is_online: bool, board_to_play: str,
                 fps=30, icon=None, **flags):
        self.screen = pygame.display.set_mode(size, **flags)
        if title:
            pygame.display.set_caption(title)
        if icon:
            pygame.display.set_icon(icon)
        self.running = True
        self.clock = pygame.time.Clock()
        self.max_fps = fps
        self.board = Board(self, (100, 100), (50, 50), 0)
        self.restart = False
        if is_online:
            self.judge = OnlineJudge(self.board)
        else:
            self.judge = Judge(self.board, boards[board_to_play])
        self.judge.restart()
        self.fog = FogOfWar(self, (-50, -50), 3, (50, 50), 'fog', color)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
                self.board.update(event)

    def draw(self):
        self.screen.fill((20, 20, 50))
        self.board.draw()
        if is_on_fog_of_war:
            self.fog.draw()

    def run(self):
        try:
            while self.running:
                if self.restart:
                    self.judge.restart()
                    self.restart = False
                self.update()
                self.draw()
                pygame.display.update()
                self.clock.tick(self.max_fps)
        except KeyboardInterrupt:
            pass
        self.quit()

    def quit(self):
        self.judge.quit()
        self.save()

    def save(self):
        pass
