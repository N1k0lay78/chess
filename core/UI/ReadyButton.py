from core.UI.Button import Button
from core.textures.Tileset import TileSet


class ReadyButton(Button):
    def __init__(self, window, pos):
        super().__init__(window, pos, TileSet("ReadyButton", (100, 100)), ((0, 0)) * 3)
        self.is_countdown = False
        self.countdown = 0
        # player is ready
        self.ready = False
        # error (not full team for example)
        self.game_error = False

    def on_click(self):
        # *send we are ready*
        self.ready = not self.ready
        if self.ready:
            self.start_countdown()
            # self.window.game.client.say(i'm ready)
        else:
            self.stop_countdown()
            # self.window.game.client.say(please wait)

    def start_countdown(self, delay=3):
        self.countdown = delay
        self.is_countdown = True

    def stop_countdown(self):
        self.is_countdown = False

    def check_collide_point(self, pos):
        pos = [pos[0] - self.pos[0], pos[1] - self.pos[1]]
        self.hovered = 9 <= pos[0] <= 94 and 9 <= pos[1] <= 94
        return self.hovered

    def draw(self, pos=(0, 0)):
        if self.is_countdown:
            self.countdown -= self.window.game.delta
            if self.countdown <= 0:
                # may be server do this \_('_')_/
                self.stop_countdown()
                self.window.game.open_window('Game')

        pos = [pos[0] + self.pos[0], pos[1] + self.pos[1]]
        if not self.ready:
            self.window.game.screen.blit(self.tile_set[0, 1], pos)
        else:
            if self.game_error:
                self.window.game.screen.blit(self.tile_set[1, 3], pos)
            elif self.is_countdown:
                self.window.game.screen.blit(self.tile_set[1, self.countdown // 1], pos)
            else:
                self.window.game.screen.blit(self.tile_set[0, 2], pos)
        if self.hovered:
            self.window.game.screen.blit(self.tile_set[0, 3], pos)
