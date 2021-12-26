import pygame

from core.windows.Window import Window


class Test(Window):
    def __init__(self, screen):
        super().__init__(screen, max_fps=30)


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
