from core.UI.BaseUI import BaseUI
from core.UI.DefaultButton import DefaultButton
from core.UI.PopUp import PopUp
from core.textures.Tileset import TileSet


def swap_to_queen(button):
    button.window.game.client.room.figure = "Q"
    print('Q')


def swap_to_knight(button):
    button.window.game.client.room.figure = "N"
    print('N')


def swap_to_rook(button):
    button.window.game.client.room.figure = "R"
    print('R')


def swap_to_bishop(button):
    button.window.game.client.room.figure = "B"
    print('B')


class SwapPopUp(PopUp):
    def __init__(self, window, pos, color):
        tile_set = TileSet('SwapIcons', (50, 50))
        description = BaseUI(window, (0, 0), image=window.game.render_text("выберите фигуру", (230, 81, 0)))
        description.pos = (300 - description.image.get_width()) // 2, 50
        super().__init__(window, pos, (3, 2), [
            description,
            DefaultButton(window, (35, 100), tile_set[1, color], 1, swap_to_queen),
            DefaultButton(window, (95, 100), tile_set[3, color], 1, swap_to_knight),
            DefaultButton(window, (155, 100), tile_set[0, color], 1, swap_to_rook),
            DefaultButton(window, (215, 100), tile_set[2, color], 1, swap_to_bishop),
        ])
