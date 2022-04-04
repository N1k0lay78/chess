import pygame


class BaseUI:
    def __init__(self, window, pos, childs=[], image=None, un_active_on_mouse_up=True, size=(10, 10)):
        self.window = window
        self.pos = pos
        self.child = []
        self.image = image
        self.parent = None
        self.un_active_on_mouse_up = un_active_on_mouse_up
        self.hovered = False
        self.__size = size
        for child in childs:
            self.add_child(child)

    def set_size(self, size):
        self.__size = size

    def set_patent(self, parent):
        self.parent = parent

    def remove_parent(self):
        self.parent = None

    def add_child(self, child):
        child.set_patent(self)
        self.child.append(child)

    def remove_child(self, child):
        if child in self.child:
            self.child.remove(child)
            child.remove_parent()

    def draw_child(self):
        for child in self.child:
            child.draw(self.pos)

    def draw(self, pos=(0, 0)):
        if self.image:
            self.window.game.screen.blit(self.image, (self.pos[0] + pos[0], self.pos[1] + pos[1]))
        if self.child:
            self.draw_child()

    def check_collide_point(self, pos):
        if self.parent:
            pos = [pos[0] - self.pos[0] - self.parent.pos[0], pos[1] - self.pos[1] - self.parent.pos[1]]
        else:
            pos = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
        if self.image:
            self.hovered = 0 <= pos[0] <= self.image.get_width() and 0 <= pos[1] <= self.image.get_height()
        else:
            self.hovered = 0 <= pos[0] <= self.__size[0] and 0 <= pos[1] <= self.__size[1]
        self.check_collide_update()
        return self.hovered

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.un_active_on_mouse_up:
            self.window.remove_active()

    def check_collide_update(self):
        pass

    def get_size(self):
        return self.__size[:]

    def move(self, move):
        self.pos[0] += move[0]
        self.pos[1] += move[1]

    def check_hover(self, event):
        pass

    def on_disactive(self):
        pass

    def update(self):
        pass

    def fixed_update(self):
        pass
