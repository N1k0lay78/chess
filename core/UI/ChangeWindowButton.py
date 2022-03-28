from core.UI.Button import Button


class ChangeWindowButton(Button):
    def __init__(self, window, pos, tile_set, name_window):
        super().__init__(window, pos, tile_set, ((0, 0), (1, 0), (2, 0)))
        self.name_window = name_window

    def on_click(self):
        self.window.game.open_window(self.name_window)
