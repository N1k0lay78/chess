from core.UI.BaseUI import BaseUI
from core.UI.PlayButton import PlayButton
from core.UI.AnimatedTorch import AnimatedTorch
from core.textures.load_image import load_image
from core.windows.Window import Window


class MainMenuWindow(Window):
    def __init__(self, game):
        super().__init__(game)

    def set_ui(self):
        self.ui = {
            "Lobby": [],
            "Settings": [
                # ChangeWindowButton(self, (500, 0), TileSet('settings4', (100, 100)), "Game")
            ],
            "Play": [
                PlayButton(self, (100, 200), "онлайн", "Game", {"mode": "online"}),
                PlayButton(self, (100, 300), "офлайн", "Game", {"mode": "offline"}),
                PlayButton(self, (100, 400), "туман войны", "Game", {"mode": "fog of war"}),
            ],
            "Decorations": [
                AnimatedTorch(self, (-10, 300)),
                AnimatedTorch(self, (510, 300)),
            ],
            "background": [
                BaseUI(self, (0, 0), image=load_image('main_menu'), size=(0, 0))
            ]
        }
