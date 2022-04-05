from core.UI.DefaultButton import DefaultButton
from core.UI.InputField import InputField
from core.UI.InputFieldPopUp import InputFieldPopUp
from core.UI.PlayButton import PlayButton
from core.UI.ReadyButton import ReadyButton
from core.UI.SwapPopUp import SwapPopUp
from core.windows.Window import Window


class TestWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.ui.append(SwapPopUp(self, (250, 10), 1))
        self.ui.append(InputFieldPopUp(self, [0, 300], "code", "войти"))
        self.ui.append(InputFieldPopUp(self, [300, 300], "nickname", "создать"))
        self.ui.append(DefaultButton(self, (10, 40), "войти", 3))
        self.ui.append(InputField(self, (10, 10), "C O D E", [(0, 0, 0), (150, 150, 150)], "code"))
        # self.ui.append(ReadyButton(self, (10, 85)))
        self.ui.append(PlayButton(self, (10, 190), "онлайн", "Game", {"mode": "online"}))
        # self.ui.append(PlayButton(self, (10, 260), "офлайн", "Game", {"mode": "offline"}))
        # self.ui.append(PlayButton(self, (10, 330), "туман войны", "Game", {"mode": "fog of war"}))
        self.active = self.ui[-1]

    def update(self):
        if self.active:
            self.active.update()

    def set_active(self, event):
        for element in self.ui:
            if element.check_collide_point(event.pos):
                self.set_active_object(element)
                break

    def fixed_update(self):
        for element in self.ui:
            element.fixed_update()

    def check_hover(self, event):
        pos = event.pos
        for element in self.ui:
            if element.check_collide_point(pos):
                pos = [-1, -1]

    def draw(self):
        self.game.screen.fill((255, 255, 255))
        for element in self.ui[::-1]:
            element.draw()
