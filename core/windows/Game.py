from Source.boards import boards
from Source.settings import is_on_fog_of_war
from core.online.Client import Client
from core.FogOfWar import FogOfWar
from core.Board import Board
from threading import Thread
import socket
import pygame


class Game:
    def __init__(self, nickanme, size, title, color, fps=30, icon=None, **flags):
        self.screen = pygame.display.set_mode(size, **flags)
        if title:
            pygame.display.set_caption(title)
        if icon:
            pygame.display.set_icon(icon)
        self.color = color
        self.running = True
        self.clock = pygame.time.Clock()
        self.max_fps = fps
        self.client = Client(self, nickanme, socket.gethostbyname(socket.gethostname()), 9090)
        self.client_thread = Thread(target=self.client.run)
        self.client_thread.start()
        self.board = Board(self, (100, 100), (50, 50), 0)
        self.board.load_board(boards["classic"])
        self.fog = FogOfWar(self, (-50, -50), 3, (50, 50), 'fog', color)

    def disconnect(self):
        self.client.stop()
        self.client_thread.join()

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
                self.update()
                self.draw()
                pygame.display.update()
                self.clock.tick(self.max_fps)
        except KeyboardInterrupt:
            pass
        self.disconnect()
        self.save()

    def save(self):
        pass
