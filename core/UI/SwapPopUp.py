from core.UI.BaseUI import BaseUI
from core.UI.DefaultButton import DefaultButton
from core.UI.PopUp import PopUp
from core.textures.Tileset import TileSet
from loguru import logger


def swap_to_queen(button):
    button.window.judge.on_swap("Q")
    button.window.game_logs.save_swap("Q")
    logger.info("on swap user choice Queen (Q)")
    for pop_up in button.window.ui["pop-up"]:
        if type(pop_up) == SwapPopUp:
            button.window.ui['pop-up'].remove(pop_up)


def swap_to_knight(button):
    button.window.judge.on_swap("N")
    button.window.game_logs.save_swap("N")
    logger.info("on swap user choice Horse (N)")
    for pop_up in button.window.ui["pop-up"]:
        if type(pop_up) == SwapPopUp:
            button.window.ui['pop-up'].remove(pop_up)


def swap_to_rook(button):
    button.window.judge.on_swap("R")
    button.window.game_logs.save_swap("R")
    logger.info("on swap user choice Rook (R)")
    for pop_up in button.window.ui["pop-up"]:
        if type(pop_up) == SwapPopUp:
            button.window.ui['pop-up'].remove(pop_up)


def swap_to_bishop(button):
    button.window.judge.on_swap("B")
    button.window.game_logs.save_swap("B")
    logger.info("on swap user choice Elephant (B)")
    for pop_up in button.window.ui["pop-up"]:
        if type(pop_up) == SwapPopUp:
            button.window.ui['pop-up'].remove(pop_up)


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
