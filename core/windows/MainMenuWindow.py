from Source.settings import params
from core.UI.BaseUI import BaseUI
from core.UI.PlayButton import PlayButton
from core.UI.AnimatedTorch import AnimatedTorch
from core.textures.load_image import load_image
from core.textures.Tileset import TileSet
from core.windows.Window import Window
# from core.UI.ChangeWindowButton import ChangeWindowButton


def start_offline(self):
    params["mode"] = "offline"
    self.window.game.open_window('Game')


def start_online(self):
    params["mode"] = "online"
    self.window.game.open_window('Choice')



class MainMenuWindow(Window):
    def __init__(self, game):
        super().__init__(game)

    def set_ui(self):
        self.ui = {
            "Lobby": [],
            "Settings": [
                # ChangeWindowButton(self, (500, 100), TileSet('settings', (100, 100)), "Game")
                PlayButton(self, (000, 100), TileSet('UserImages', (100, 100))[0, 0], size=(100, 100)),
                PlayButton(self, (100, 100), TileSet('UserImages', (100, 100))[0, 1], size=(100, 100)),
                PlayButton(self, (200, 100), TileSet('UserImages', (100, 100))[0, 2], size=(100, 100)),
                PlayButton(self, (300, 100), TileSet('UserImages', (100, 100))[0, 2], size=(100, 100)),
                PlayButton(self, (400, 100), TileSet('UserImages', (100, 100))[0, 2], size=(100, 100)),
                # PlayButton(self, (400, 100), TileSet('settings', (100, 100))[1], size=(100, 100)),
                PlayButton(self, (500, 100), TileSet('settings', (100, 100))[0], size=(100, 100)),
            ],
            "Play": [
                # PlayButton(self, (100, 200), "офлайн"),
                # PlayButton(self, (100, 300), "войти"),
                PlayButton(self, (100, 200), "онлайн", on_funk=start_online),
                PlayButton(self, (100, 300), "туман войны"),
                PlayButton(self, (100, 400), "офлайн", on_funk=start_offline),
            ],
            "Decorations": [
                AnimatedTorch(self, (-10, 300)),
                AnimatedTorch(self, (510, 300)),
            ],
            "background": [
                BaseUI(self, (0, 0), image=load_image('main_menu'), size=(0, 0))
            ]
        }
