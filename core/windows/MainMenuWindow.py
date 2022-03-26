from core.textures.load_image import load_image
from core.windows.Window import Window


class MainMenuWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.background = load_image('main_menu')
        self.buttons = [self.game.font.render(name, False, (0, 0, 0))
                        for name in ("Онлайн", "Офлайн", "Туман войны")]

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        for i in range(len(self.buttons)):
            self.game.screen.blit(self.buttons[i],
                                  (300 - self.buttons[i].get_width() // 2, 200 + 100 * i))
