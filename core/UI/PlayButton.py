from Source.settings import params
from core.UI.TextButton import TextButton


class PlayButton(TextButton):
    def __init__(self, window, pos, text, open_window, settings):
        super().__init__(window, pos, text)
        self.open_window = open_window
        self.settings = settings

    def on_click(self):
        for key, val in self.settings.items():
            params[key] = val
        self.window.game.open_window(self.open_window)
