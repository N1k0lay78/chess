from Source.settings import get_param
from core.windows.LoadingGame import LoadingGame
from core.windows.GameWidow import GameWindow
import pygame


class Game:
    def __init__(self):
        # init app
        self.screen = pygame.display.set_mode(get_param("screen_size"))
        pygame.display.set_caption(get_param("app_name"))
        pygame.display.set_icon(pygame.image.load(get_param("app_icon")))
        # windows
        self.windows = {"Game": GameWindow, "Load": LoadingGame}
        self.window = self.windows[get_param("start_window")](self)
        # game is running
        self.running = True
        # delta and fps
        self.clock = pygame.time.Clock()
        self.max_fps = get_param("max_fps")
        self.last_time = pygame.time.get_ticks()
        self.delta = 0
        self.is_flip_screen = get_param("is_flip_screen")

    def run(self):
        while self.running:
            # eval delta time
            self.delta = (pygame.time.get_ticks() - self.last_time) / 1000.0
            # update last time
            self.last_time = pygame.time.get_ticks()
            # update events
            for event in pygame.event.get():
                # if quit event, then close the game
                if event.type != pygame.QUIT:
                    self.window.events(event)
                else:
                    self.quit()
            self.window.update()
            self.screen.fill((20, 20, 50))
            self.window.draw()
            # if flip screen mode
            if self.is_flip_screen:
                pygame.display.flip()
            else:
                pygame.display.update()
            # lock fps
            self.clock.tick(self.max_fps)
            if False:
                print(self.clock.get_fps())

    def open_window(self, name=""):
        self.window.on_close()
        if name:
            self.window = self.windows[name](self)

    def quit(self):
        self.open_window()
        self.running = False
