from Source.settings import params
from core.UI.TextButton import TextButton


class PlayButton(TextButton):
    def __init__(self, window, pos, text, open_window, settings, func=None):
        super().__init__(window, pos, text)
        self.open_window = open_window
        self.settings = settings
        self.func = func

    def on_click(self):
        for key, val in self.settings.items():
            params[key] = val
        if not self.func:
            self.window.game.open_window(self.open_window)
        else:
            self.func(int("".join(self.window.ui[0].text.split())))
