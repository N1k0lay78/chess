from core.UI.ChangeWindowButton import ChangeWindowButton
from core.UI.ChechBox import CheckBox
from core.UI.PlayButton import PlayButton
from core.UI.PlayerTypeSelect import PlayerTypeSelect
from core.textures.Tileset import TileSet
from core.textures.load_image import load_image
from core.windows.Window import Window


class MainMenuWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        self.background = load_image('main_menu')
        self.button = ChangeWindowButton(self, (500, 0), TileSet('settings4', (100, 100)), "Game")

        self.buttons = [
            PlayButton(self, (10, 190), "онлайн", "Game", {"mode": "online"}),
            PlayButton(self, (10, 260), "офлайн", "Game", {"mode": "offline"}),
            PlayButton(self, (10, 330), "туман войны", "Game", {"mode": "fog of war"}),
        ]

    def check_hover(self, event):
        for button in self.buttons:
            button.check_collide_point(event.pos)
        if self.button.check_collide_point(event.pos):
            self.button.check_collide_update()

    def set_active(self, event):
        if self.button.check_collide_point(event.pos):
            self.set_active_object(self.button)
        else:
            for button in self.buttons:
                if button.check_collide_point(event.pos):
                    self.set_active_object(button)
                    break
            else:
                self.remove_active()

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        self.button.draw()

        for button in self.buttons:
            button.draw()
