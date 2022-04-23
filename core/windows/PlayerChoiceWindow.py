from Source.settings import params
from core.UI.BaseUI import BaseUI
from core.UI.PlayerChoiceUI import PlayerChoiceUI
from core.UI.ReadyButton import ReadyButton
from core.textures.load_image import load_image
from core.windows.Window import Window


class PlayerChoiceWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.background = load_image('main_menu')
        self.ui = {
            "static": [BaseUI(self, (180, 110), image=self.game.render_text(f"код игры: {params['code']}", (230, 81, 0)))],
            "players": [PlayerChoiceUI(self, (150, self.p(0)), params['nickname'], 2),
                        ],
            "ready": [ReadyButton(self, (250, self.p(4)))]
        }
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

    def update(self):
        if self.active:
            self.active.update()

    def set_active(self, event):
        for key in self.ui:
            for element in self.ui[key]:
                if element.check_collide_point(event.pos):
                    self.set_active_object(element)
                    return
        else:
            self.set_active_object(None)

    def fixed_update(self):
        for key in self.ui:
            for element in self.ui[key]:
                element.fixed_update()

    def check_hover(self, event):
        pos = event.pos
        for key in self.ui:
            for element in self.ui[key]:
                if element.check_collide_point(pos):
                    pos = [-1, -1]

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        for key in reversed(self.ui.keys()):
            for elem in self.ui[key][::-1]:
                elem.draw()
