import pygame

from core.UI.TransformLogo import TransformLogo
from core.textures.load_image import load_image
from core.windows.Window import Window


class LoadingGame(Window):
    def __init__(self, screen):
        super().__init__(screen, max_fps=60)
        min_size = screen.get_size()[0]//30
        st_height = min_size
        end_height = min_size*10
        center_sc = screen.get_size()[0]//2, screen.get_size()[1]//2
        center = center_sc[0], center_sc[1]
        self.transformLogo = [TransformLogo(self, center, load_image('logo'), st_height, end_height, 1)]
        center = center_sc[0]//2, screen.get_height() - min_size*7/3
        self.transformLogo.append(TransformLogo(self, center, load_image('pygame'), st_height, end_height/3, 1, -1))
        center = center_sc[0] + center_sc[0]//2, screen.get_height() - min_size*7/3
        self.transformLogo.append(TransformLogo(self, center, load_image('pygame'), st_height, end_height/3, 1, -2))
        self.time_st = pygame.time.get_ticks()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    def update(self):
        [x.update(None) for x in self.transformLogo]
        if pygame.time.get_ticks() - self.time_st > 3100:
            print('end')
            self.running = False

    def draw(self):
        self.screen.fill((20, 20, 50))
        [x.draw() for x in self.transformLogo]
