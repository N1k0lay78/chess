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
        self.game.client.sending_to_the_server(f"hg {params['code']}")
        print(params["code"], self.game.client.is_connected())
        if self.game.client.is_connected():
            # print("A podkluchitca?")
            self.game.client.connect_to_game(params['code'], self.logic_board, self.judge)

    def draw(self):
        self.game_board.draw()

    def update(self):
        self.game_board.update()

    def events(self, event):
        self.active.event(event)
