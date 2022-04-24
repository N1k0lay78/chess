import socket
from threading import Thread
import time
from Source.settings import params

# Получаем свой локальный ip адрес
# self_ip = socket.gethostbyname(socket.gethostname())
from core.UI.SwapPopUp import SwapPopUp


class Room:
    def __init__(self, client):
        # game objects
        self.client = client
        self.board = None
        self.judge = None
        self.message_queue = []

        # game
        self.is_choice = False
        self.color = 0
        self.running = True
        self.figure = None
        self.game_started = False

        self.run_thread = Thread(target=self.run)
        self.run_thread.start()

    def start_game(self, board, judge):
        self.board = board
        self.judge = judge
        self.game_started = True
        print("Ват?")

    def stop_game(self):
        self.board = None
        self.judge = None
        self.game_started = False

    def get_server_message(self, message):
        # print("????????????????????????", message)
        self.message_queue.append(message)

    def send_to_server(self, message):
        self.client.sending_to_the_server(message)

    def run(self):
        while self.running:
            if len(self.message_queue):
                data = self.message_queue[0]
                print(data, "!!!!DATA!!!!")
                if self.game_started:
                    print("Угу, очень интересно")
                    if data[:2] == "su":
                        self.board.load_board(data[7 + len(data.split()[2]) - 1:])
                        a = data.split()
                        print("Дать")
                        print(f"color: {a[1]} step: {a[2]} pieces: {a[3:]}")

                        self.color = int(data.split()[1])
                        self.board.color = int(data.split()[1])
                        self.judge.color = int(data.split()[1])
                        self.board.step = int(data.split()[2])

                        # if self.color:
                        #     self.judge.flip()
                    elif data[:2] == "om":
                        self.client.game.window.game_board.wait_server_1 = False
                    elif data[:2] == "ok":
                        self.client.game.window.game_board.wait_server_1 = False
                        self.client.game.window.game_board.wait_server_2 = False
                    elif data[:2] in ["nm", "im"]:
                        # self.board.step = int(data.split(":")[1])
                        print(data)
                        print(data.split(":")[1])
                        self.board.load_board(data.split(":")[2])
                        self.client.game.window.game_board.load_board(int(data.split(":")[1]), data.split(":")[2])

                        # if self.color:
                        #     self.judge.flip()

                    elif data[:2] in ["ch", "er"]:
                        self.client.game.window.ui.append(SwapPopUp(self.client.game.window, (250, 10), self.color))
                        wait_user_choice_thread = Thread(target=self.wait_user_choice)
                        wait_user_choice_thread.start()
                else:
                    if data[:2] == "ye":
                        print("Берём новый цвет", data.split()[1])
                        # self.color = int(data.split()[1])
                        self.client.game.window.ui["players"][0].set_choice(int(data.split()[1]))
                    elif data[:2] == "no":
                        print("Неть")
                        self.client.game.window.ui["players"][0].set_choice(int(data.split()[1]))
                    elif data[:2] == "sr":
                        if int(data.split()[1]):
                            self.client.game.window.ui["ready"][0].start_countdown()
                        else:
                            self.client.game.window.ui["ready"][0].stop_countdown()
                    elif data[:2] == "mv":
                        nickname, color = data.split()[1:]
                        self.client.game.window.change_user(nickname, int(color))
                        # ФУНКЦИЯ ДЛЯ ИЗМЕНЕНИЯ ЦВЕТА ПОЛЬЗОВАТЕЛЯ
                    elif data[:2] == "mr":
                        nickname, ready = data.split()[1:]
                        self.client.game.window.set_user_ready(nickname, ready)
                        # ФУНКЦИЯ ДЛЯ ИЗМЕНЕНИЯ ГОТОВНОСТИ ПОЛЬЗОВАТЕЛЯ
                    elif data[:2] == "ju":
                        nickname, color = data.split()[1:]
                        self.client.game.window.add_user(nickname, int(color))
                        # ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
                    elif data[:2] == "lu":
                        nickname = data.split()[1]
                        self.client.game.window.delete_user(nickname)
                        # УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
                    elif data[:2] == "cl":
                        print(data, "инфа сотка")
                        for el in data[2:].strip().split(":"):
                            if len(el.split()) == 2:
                                print(el)
                                nick, color = el.split()
                                self.client.game.window.add_user(nick, int(color))
                self.message_queue.pop(0)

    def wait_user_choice(self):
        while True:
            # print(self.figure)
            if self.figure and self.figure in ["Q", "N", "R", "B"]:
                self.send_to_server(f"mc {self.figure}")
                self.client.game.window.ui.pop(0)
                return True
        # self.board.set_pause(True)
        # self.send_to_server(f"mc {input('????3@#R#QWFE')}")
        # self.board.set_pause(False)

    def stop(self):
        self.running = False
        self.run_thread.join(0)


class Client:
    def __init__(self, nickname, server, port, game):
        # print(server, port)
        # settings
        self.nickname = nickname
        self.server = server
        self.port = port
        self.game = game

        # server
        self.socket = None
        self.connection_monitoring_thread = None
        self.getting_from_the_server_thread = None
        self.sending_to_the_server_queue_thread = None
        self.running = True
        self.room = Room(self)
        self.send_to = [self.room.get_server_message]
        self.sending_to_the_server_list = []

    def is_connected(self):
        return bool(self.socket)

    def connect_to_game(self, code, board, judge):
        # print("!!!?!?!?!?!")
        if self.socket:
            # self.sending_to_the_server("rg 1")
            print("????????????????????????????????????????????????????????????????????????")
            self.room.start_game(board, judge)
            # time.sleep(1)
            # self.sending_to_the_server(f"sg {code}")
        else:
            pass
            # print("У пользователя уже есть игра!")

    def connect_with_server(self):
        while self.running:
            if not self.socket:
                try:
                    sock = socket.socket()
                    sock.connect((self.server, self.port))
                    sock.send(self.to_bytes(self.nickname))
                    data = self.to_text(sock.recv(1024))
                    if data and len(data) >= 2 and data[:2] == "sc":
                        print("Connected to the server")
                    self.socket = sock
                except Exception as e:
                    print("Something is wrong. Try to connect again")
            else:
                if not self.check_connection("Check connection"):
                    # print("Something is wrong")
                    self.socket.close()
                    self.socket = None
                    self.room = None
                    self.send_to = []
                time.sleep(1)

    def sending_to_the_server(self, message):
        if self.socket:
            self.sending_to_the_server_list.append(message)

    def sending_to_the_server_queue(self):
        while self.running:
            if self.socket and len(self.sending_to_the_server_list):
                message = self.sending_to_the_server_list.pop(0)
                try:
                    self.socket.send(self.to_bytes(message))
                except Exception as e:
                    # print(f"Bad connection with server - {e}")
                    pass

    def check_connection(self, message):
        if self.socket:
            try:
                self.socket.send(self.to_bytes(message))
            except Exception as e:
                # print(f"Bad connection with server - {e}")
                return False
        return True

    def getting_from_the_server(self):
        while self.running:
            if self.socket:
                try:
                    data = self.to_text(self.socket.recv(1024)).replace("Check connection", "")
                    if data and len(data) >= 2:
                        print("NEW DATA IN CLIENT", data)
                        if data[:2] == "ga":
                            params["game_exist"] = bool(int(data.split()[1]))
                            params["have_answer"] = True
                        for pol in self.send_to:
                            pol(data)
                except Exception as e:
                    # print(f"Bad connection with server - {e}")
                    time.sleep(1)

    def to_bytes(self, message):
        return bytes(message, encoding="utf-8")

    def to_text(self, message):
        return str(message)[2:-1]

    def run(self):
        self.connection_monitoring_thread = Thread(target=self.connect_with_server)
        self.connection_monitoring_thread.start()
        self.getting_from_the_server_thread = Thread(target=self.getting_from_the_server)
        self.getting_from_the_server_thread.start()
        self.sending_to_the_server_queue_thread = Thread(target=self.sending_to_the_server_queue)
        self.sending_to_the_server_queue_thread.start()

    def stop(self):
        self.running = False
        self.connection_monitoring_thread.join(0)
        self.getting_from_the_server_thread.join(0)
        self.sending_to_the_server_queue_thread.join(0)
        if self.socket:
            self.socket.close()
        if self.room:
            self.room.stop()
        print("Что за хуйня???")


if __name__ == '__main__':
    self_ip = socket.gethostbyname(socket.gethostname())
    client = Client("Nickolausus", self_ip, 9090, None)
    client.run()
