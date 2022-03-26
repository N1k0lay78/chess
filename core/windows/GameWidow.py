from Source.settings import get_param
from core.windows.Window import Window
from core.online.logic.Board import LogicBoard
from core.Judge import Judge
from core.OnlineJudge import OnlineJudge
from core.UI.StandardBoardUI import StandardBoardUI


class GameWindow(Window):
    def __init__(self, game):
        super().__init__(game)
        if get_param("mode") == "online":
            self.logic_board = LogicBoard(False)
            self.judge = OnlineJudge(self.logic_board)
        elif get_param("mode") == "fog of war":
            self.logic_board = LogicBoard(True)
            self.judge = OnlineJudge(self.logic_board)
        else:
            self.logic_board = LogicBoard(False)
            self.judge = Judge(self.logic_board, get_param("board_name"))
        self.game_board = StandardBoardUI(self, (100, 100), self.judge, self.logic_board)
        self.set_active_object(self.game_board)

    def draw(self):
        self.game_board.draw()

    def update(self):
        self.game_board.update()

    def events(self, event):
        self.active.event(event)
