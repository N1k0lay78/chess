from core.UI.InputField import InputField
from core.UI.ReadyButton import ReadyButton
from core.windows.Window import Window


class TestWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.ui = []
        # self.ui.append(InputField(self, (10, 10), "C O D E", [(0, 0, 0), (150, 150, 150)], "nickname"))
        self.ui.append(ReadyButton(self, (10, 85)))
        self.active = self.ui[-1]

    def update(self):
        if self.active:
            self.active.update()

    def set_active(self, event):
        for element in self.ui:
            if element.check_collide_point(event.pos):
                self.set_active_object(element)
                break

    def check_hover(self, event):
        for element in self.ui:
            element.check_collide_point(event.pos)

    def draw(self):
        self.game.screen.fill((255, 255, 255))
        for element in self.ui:
            element.draw()
