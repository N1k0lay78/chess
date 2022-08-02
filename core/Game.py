from Source.settings import params, set_random_nickname
from core.online.Client import Client
from core.windows.LoadingWindow import LoadingWindow
from core.windows.GameWidow import GameWindow
from core.windows.MainMenuWindow import MainMenuWindow
import pygame

from core.windows.PlayerChoiceWindow import PlayerChoiceWindow
from core.windows.TestWindow import TestWindow
from loguru import logger


class Game:
    def __init__(self):
        # init app
        logger.info("start game")
        self.screen = pygame.display.set_mode(params["screen_size"])
        pygame.display.set_caption(params["app_name"])
        pygame.display.set_icon(pygame.image.load(params["app_icon"]))

        # colors
        """
        yellow
        (245, 127, 23)
        (249, 168, 37)
        (251, 192, 45)
        red
        (191, 54, 12)
        (216, 67, 21)
        (230, 74, 25)
        green
        (13, 83, 2)
        (5, 111, 0)
        (10, 126, 7)
        """

        # font
        # cell   1  2   3   4   5   6  px
        # sizes (9, 17, 25, 33, 41, 50)
        # offline
        self.font = pygame.font.Font('Source/Fonts/Chava.ttf', 25 * 2)
        self.small_font = pygame.font.Font('Source/Fonts/Chava.ttf', 25)

        # game is running
        self.running = True

        # delta and fps
        self.clock = pygame.time.Clock()
        self.max_fps = params["max_fps"]
        self.last_time = pygame.time.get_ticks()
        self.delta = 0
        self.is_flip_screen = params["is_flip_screen"]

        # windows
        self.windows = {
            "Game": GameWindow,
            "Load": LoadingWindow,
            "Menu": MainMenuWindow,
            "Test": TestWindow,
            "Choice": PlayerChoiceWindow,
        }
        self.window = None
        self.text_version = self.render_text('0.1.5 Alpha', (249, 168, 37), True)
        # server
        # self.client = Client(set_random_nickname(), params["online_host_ip"], params["online_host_port"], self)
        # self.client.run()

        # open start window
        self.open_window(params["start_window"])

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
            self.window.fixed_update()
            self.screen.fill((20, 20, 50))
            self.window.draw()
            pygame.draw.rect(self.screen, (97,)*3, ((8, 600 - self.text_version.get_height() - 12),
                                                         (self.text_version.get_width() + 6,
                                                          self.text_version.get_height() + 4)))
            self.screen.blit(self.text_version, (10, 600 - self.text_version.get_height() - 10))
            # if flip screen mode
            if self.is_flip_screen:
                pygame.display.flip()
            else:
                pygame.display.update()
            # lock fps
            self.clock.tick(self.max_fps)
            # if False:
            #     print(self.clock.get_fps())

    def render_text(self, text, color=(0, 0, 0), is_small=True):
        if is_small:
            return self.small_font.render(text, False, color)
        return self.font.render(text, False, color)

    def open_window(self, name=""):
        if name:
            if self.window:
                self.window.on_close()
            self.window = self.windows[name](self)
            logger.info(f"open window \"{name}\"")

    def quit(self):
        self.open_window()
        self.running = False
        self.client.stop()
        logger.info(f"close game")
        quit(0)

    def __quit__(self):
        self.quit()
