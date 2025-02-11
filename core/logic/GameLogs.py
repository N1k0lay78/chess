import time, os
from Source.settings import params


class GameLogs:
    def __init__(self, dir_path):
        self.dir = dir_path
        self.file = None
        self.start_time = 0

    def save_moves(self, moves):
        # сохраняем ходы, может быть 2 перемещения за ход (при рокировке)
        self.log(f"move:{':'.join(f'{fr}:{to}' for fr, to in moves)}")

    def save_swap(self, choice):
        self.log(f"swap:{choice}")

    def save_disconnect(self, user):
        # отключился игрок
        self.log(f"disc:{user}")

    def save_connect(self, user):
        # подключился игрок
        self.log(f"conc:{user}")

    def save_start_pause(self):
        # началась пауза
        self.log(f"rtpa")

    def save_stop_pause(self):
        # закончилась пауза
        self.log(f"oppa")

    def start_save(self, board: str, user1="user1", user2=None, filename=None):
        if filename is None:
            # создаём дефолтное название файла с логом
            filename = "default"
        if user1 is None:
            user1 = "user1"
        if user2 is None:
            user2 = "user2"
        self.create_filename(filename)
        self.start_time = time.time()
        self.create_log_file()
        self.log(f"sgb:{board}")  # start game board
        self.log(f"pn:{user1}:{user2}")  # players nicknames

    def check_files(self, filename) -> int:
        file = f"{os.getcwd()}{self.dir}\\{filename}.log"
        print(file)
        # with open(file, 'r') as f:
        try:
            open(file, 'r').close()
            n = 1
            while True:
                file = f"{os.getcwd()}{self.dir}\\{filename}_{n}.log"
                try:
                    open(file, 'r').close()
                except Exception as e:
                    return n
                n += 1
        except Exception as e:
            return 0

    def create_filename(self, filename):
        if params['game_logs_new_file']:
            n = self.check_files(filename)
            self.file = f"{os.getcwd()}{self.dir}\\{filename}_{n}.log"
        else:
            self.file = f"{os.getcwd()}{self.dir}\\{filename}.log"

    def create_log_file(self):
        # with open(self.file, 'w') as f:
        #     f.write('')
        pass

    def log(self, msg):
        # if self.file:
        #     with open(self.file, 'a') as f:
        #         f.write(f"{round(time.time() - self.start_time)}:{msg}\n")
        pass
