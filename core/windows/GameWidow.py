import pygame

from Source.settings import params
from core.windows.Window import Window
from core.online.logic.Board import LogicBoard
from core.Judge import Judge
from core.OnlineJudge import OnlineJudge
from core.UI.StandardBoardUI import StandardBoardUI


class GameWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        if params["mode"] == "online":
            self.logic_board = LogicBoard(False)
            self.judge = OnlineJudge(self.logic_board, self.game.client)
        elif params["mode"] == "fog of war":
            self.logic_board = LogicBoard(True)
            self.judge = OnlineJudge(self.logic_board, self.game.client)
        else:
            self.logic_board = LogicBoard(False)
            self.judge = Judge(self.logic_board, params["board_name"])
        self.game_board = StandardBoardUI(self, (100, 100), self.judge, self.logic_board)
        self.set_active_object(self.game_board)
        self.connect_to_the_game()

    def connect_to_the_game(self):
        if params['mode'] != "offline":
            self.game.client.sending_to_the_server(f"hg {params['code']}")
            # print(params["code"], self.game.client.is_connected())
            if self.game.client.is_connected():
                # print("A podkluchitca?")
                self.game.client.connect_to_game(params['code'], self.logic_board, self.judge)

    def draw(self):
        self.game_board.draw()
        for element in self.ui[::-1]:
            element.draw()

    def update(self):
        self.game_board.update()
        if self.active:
            self.active.update()

    def events(self, event):
        # self.active.event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.set_active(event)
        if self.active:
            self.active.event(event)
        if event.type == pygame.MOUSEMOTION:
            self.check_hover(event)
        self.game_board.event(event)

    def set_active(self, event):
        for element in self.ui:
            if element.check_collide_point(event.pos):
                self.set_active_object(element)
                break

    def fixed_update(self):
        for element in self.ui:
            element.fixed_update()

    def check_hover(self, event):
        pos = event.pos
        for element in self.ui:
            if element.check_collide_point(pos):
                pos = [-1, -1]
