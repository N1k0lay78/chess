from core.UI.ChangeWindowButton import ChangeWindowButton
from core.UI.ChechBox import CheckBox
from core.UI.PlayerTypeSelect import PlayerTypeSelect
from core.textures.Tileset import TileSet
from core.textures.load_image import load_image
from core.windows.Window import Window


class MainMenuWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.background = load_image('main_menu')
        self.button = ChangeWindowButton(self, (500, 0), TileSet('settings4', (100, 100)), "Game")
        self.check_box = CheckBox(self, (100, 100), "Some Text")
        self.player_type_select = PlayerTypeSelect(self, (100, 130), 2, True)
        self.buttons = [self.game.font.render(name, False, (0, 0, 0))
                        for name in ("Онлайн", "Офлайн", "Туман войны")]

    def check_hover(self, event):
        if self.button.check_collide_point(event.pos):
            self.button.check_collide_update()
        self.check_box.check_hover(event)
        self.player_type_select.check_hover(event)

    def set_active(self, event):
        if self.button.check_collide_point(event.pos):
            self.set_active_object(self.button)
        elif self.check_box.check_collide_point(event.pos):
            self.set_active_object(self.check_box)
        elif self.player_type_select.check_collide_point(event.pos):
            self.set_active_object(self.player_type_select)
        else:
            self.remove_active()

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))

        self.button.draw()
        self.check_box.draw()
        self.player_type_select.draw()
        for i in range(len(self.buttons)):
            self.game.screen.blit(self.buttons[i],
                                  (300 - self.buttons[i].get_width() // 2, 200 + 100 * i))
