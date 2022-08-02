import pygame

from Source.settings import params
from core.windows.Window import Window
from core.online.logic.Board import LogicBoard
from core.Judge import Judge
from core.OnlineJudge import OnlineJudge
from core.UI.StandardBoardUI import StandardBoardUI
from  loguru import logger


class GameWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        if params["mode"] == "online":
            self.logic_board = LogicBoard(False)
            self.judge = OnlineJudge(self.logic_board, self.game.client)
        elif params["mode"] == "fog of war":
            self.logic_board = LogicBoard(True)
            self.judge = OnlineJudge(self.logic_board, self.game.client)
            # self.judge = Judge(self, self.logic_board, params["board_name"])
        else:
            self.logic_board = LogicBoard(False)
            self.judge = Judge(self, self.logic_board, params["board_name"])
        self.game_board = StandardBoardUI(self, (100, 100), self.judge, self.logic_board)
        self.ui['pop-up'] = []
        self.ui['game'] = [self.game_board]
        self.set_active_object(self.game_board)
        logger.info(f"create game with mode {params['mode']}")
        self.connect_to_the_game()

    def connect_to_the_game(self):
        if params['mode'] != "offline":
            # self.game.client.sending_to_the_server(f"hg {params['code']}")
            print(f"!!!!!!!!!!!!!!! {self.game.client.is_connected()} {type(self.game.client.is_connected())}")
            if self.game.client.is_connected():
                # print("Я пидарас")
                self.game.client.connect_to_game(params['code'], self.logic_board, self.judge)
                self.game.client.sending_to_the_server("ac")
            logger.info(f"connect to game with code {params['code']}")

    def events(self, event):
        # self.active.event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.set_active(event)
        if self.active:
            self.active.event(event)
        if event.type == pygame.MOUSEMOTION:
            self.check_hover(event)
        self.game_board.event(event)
