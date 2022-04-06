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
        p = lambda x: 160 + 80 * x
        self.ui = {
            "static": [BaseUI(self, (180, 110), image=self.game.render_text(f"код игры: {params['code']}", (230, 81, 0)))],
            "players": [PlayerChoiceUI(self, (150, p(0)), params['nickname'], 0),
                        PlayerChoiceUI(self, (150, p(1)), "Niki", 1),
                        PlayerChoiceUI(self, (150, p(2)), "Alexei", 2),
                        PlayerChoiceUI(self, (150, p(3)), "Slava", 2),
                        ],
            "ready": [ReadyButton(self, (250, p(4)))]
        }

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
