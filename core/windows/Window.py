import pygame


class Window:
    def __init__(self, screen, max_fps=120):
        self.screen = screen
        self.running = True
        self.active = None
        self.clock = pygame.time.Clock()
        self.max_fps = max_fps
        self.last_time = pygame.time.get_ticks()
        self.delta = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.set_active(event)
            if self.active:
                self.active.update(event)
            elif event.type == pygame.MOUSEMOTION:
                self.check_hover(event)

    def check_hover(self, event):
        pass

    def set_active_object(self, object):
        self.active = object

    def remove_active(self):
        self.active = None

    def set_active(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def run(self):
        while self.running:
            self.delta = (pygame.time.get_ticks() - self.last_time) / 1000.0
            self.last_time = pygame.time.get_ticks()
            self.events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.max_fps)