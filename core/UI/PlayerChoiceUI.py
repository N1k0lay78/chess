from loguru import logger

import pygame

from Source.settings import params
from core.UI.BaseUI import BaseUI
from core.UI.PlayerTypeSelect import PlayerTypeSelect


class PlayerChoiceUI(BaseUI):
    def __init__(self, window, pos, nickname, choice):
        super().__init__(window, pos, childs=[
            BaseUI(window, (125, 22), image=window.game.render_text(nickname, (230, 81, 0))),
            PlayerTypeSelect(window, (0, 0), choice, nickname == params['nickname']),
        ], size=[300, 75], un_active_on_mouse_up=False)
        self.active = None
        self.nickname = nickname

    def get_name(self):
        return self.nickname

    def set_color(self, color):
        self.child[1].selected = color

    def set_choice(self, value):
        logger.info(f"Back user {params['nickname']} choice from {['White', 'Black', 'Viewer'][self.child[1].selected]} to {['White', 'Black', 'Viewer'][value]}")
        self.child[1].selected = value

    def check_collide_point(self, pos):
        some_collided = False
        for element in self.child:
            if element.check_collide_point(pos):
                some_collided = True

        if not some_collided:
            if self.parent:
                pos = [pos[0] - self.pos[0] - self.parent.pos[0], pos[1] - self.pos[1] - self.parent.pos[1]]
            else:
                pos = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
            if self.image:
                self.hovered = 0 <= pos[0] <= self.image.get_width() and 0 <= pos[1] <= self.image.get_height()
            else:
                self.hovered = 0 <= pos[0] <= self.get_size()[0] and 0 <= pos[1] <= self.get_size()[1]
        else:
            self.hovered = True
        self.check_collide_update()
        return self.hovered

    def event(self, event):
        super().event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for elem in self.child:
                if type(elem) != BaseUI and elem.check_collide_point(event.pos):
                    if self.active and self.active != elem:
                        self.active.on_disactive()
                    self.active = elem
                    break
            else:
                if self.active:
                    self.active.on_disactive()
                    self.active = None
        if self.active:
            self.active.event(event)

    def on_disactive(self):
        if self.active:
            self.active.on_disactive()
            self.active = None