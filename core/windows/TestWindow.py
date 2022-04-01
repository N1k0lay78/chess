from core.UI.InputField import InputField
from core.windows.Window import Window


class TestWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.ui = []
        self.ui.append(InputField(self, (10, 10), "C O D E", [(0, 0, 0), (150, 150, 150)], "nickname"))
        self.active = self.ui[0]

    def update(self):
        self.active.update()

    def draw(self):
        self.game.screen.fill((255, 255, 255))
        self.active.draw()
