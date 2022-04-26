from Source.settings import params
from core.UI.BaseUI import BaseUI
from core.UI.PlayerChoiceUI import PlayerChoiceUI
from core.UI.ReadyButton import ReadyButton
from core.textures.load_image import load_image
from core.windows.Window import Window


class PlayerChoiceWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.connect_to_the_game()

    def p(self, x):
        return 160 + 80 * x

    def add_user(self, name, color):
        self.ui["players"].append(PlayerChoiceUI(self, (150, self.p(len(self.ui["players"]))), name, color))

    def set_user_ready(self, name, ready):
        for i in range(len(self.ui["players"])):
            if self.ui["players"][i].get_name() == name:
                self.ui["players"][i].set_ready(ready == "True")

    def change_user(self, name, color):
        for i in range(len(self.ui["players"])):
            if self.ui["players"][i].get_name() == name:
                self.ui["players"][i].set_color(color)

    def remove_user(self, name):
        for i in range(len(self.ui["players"])):
            if self.ui["players"][i].get_name() == name:
                self.ui["players"].pop(i)
        for i in range(len(self.ui["players"])):
            self.ui["players"][i].pos = (150, self.p(i))

    def connect_to_the_game(self):
        self.game.client.sending_to_the_server(f"cg {params['code']}")

    def set_ui(self):
        self.ui = {
            "static": [
                BaseUI(self, (180, 110), image=self.game.render_text(f"код игры: {params['code']}", (230, 81, 0))),
            ],
            "players": [
                PlayerChoiceUI(self, (150, self.p(0)), params['nickname'], 2),
            ],
            "ready": [
                ReadyButton(self, (250, self.p(4))),
            ],
            "background": [
                # BaseUI(self, (0, 0), image=load_image('main_menu'), size=(0, 0))
            ],
        }
