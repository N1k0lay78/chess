from core.UI.ChangeWindowButton import ChangeWindowButton
from core.textures.Tileset import TileSet
from core.textures.load_image import load_image
from core.windows.Window import Window


class MainMenuWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.background = load_image('main_menu')
        self.button = ChangeWindowButton(self, (500, 0), TileSet('settings', (100, 100)), "Game")
        self.buttons = [self.game.font.render(name, False, (0, 0, 0))
                        for name in ("Онлайн", "Офлайн", "Туман войны")]

    def check_hover(self, event):
        if self.button.check_collide_point(event.pos):
            self.button.check_collide_update()

    def set_active(self, event):
        if self.button.check_collide_point(event.pos):
            self.set_active_object(self.button)

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))

        self.button.draw()
        for i in range(len(self.buttons)):
            self.game.screen.blit(self.buttons[i],
                                  (300 - self.buttons[i].get_width() // 2, 200 + 100 * i))
