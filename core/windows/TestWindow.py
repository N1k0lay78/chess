from core.UI.AnimatedTorch import AnimatedTorch
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

    def set_ui(self):
        self.ui = {
            "PopUp": [
                SwapPopUp(self, (250, 10), 1),
                InputFieldPopUp(self, [0, 300], "code", "войти"),
                InputFieldPopUp(self, [300, 300], "nickname", "создать"),
            ],
            "Other": [
                AnimatedTorch(self, (0, 100)),
                DefaultButton(self, (10, 40), "войти", 3),
                InputField(self, (10, 10), "C O D E", [(0, 0, 0), (150, 150, 150)], ""),
                # ReadyButton(self, (10, 85)),
                # PlayButton(self, (10, 190), "онлайн", "Game", {"mode": "online"}),

            ],
        }

    def draw(self):
        self.game.screen.fill((255, 255, 255))
        super().draw()
