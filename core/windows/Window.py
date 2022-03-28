import pygame


class Window:
    def __init__(self, game):
        self.game = game
        self.active = None

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.set_active(event)
        if self.active:
            self.active.event(event)
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

    def on_close(self):
        pass
