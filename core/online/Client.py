import socket
from threading import Thread
import time
from Source.special_functools import special_print

# Получаем свой локальный ip адрес
self_ip = socket.gethostbyname(socket.gethostname())


class Client:
    def __init__(self, board, nickname, server, port, judge):
        # settings
        self.board = board
        self.nickname = nickname
        self.server = server
        self.port = port
        self.judge = judge

        # server
        self.is_connected = False
        self.socket = None
        self.connection_monitoring_thread = None
        self.getting_from_the_server_thread = None
        self.running = True

        # game
        self.is_choice = False
        self.color = 0

    def connect_with_server(self):
        while self.running:
            if not self.socket:
                try:
                    sock = socket.socket()
                    sock.connect((self.server, self.port))
                    sock.send(self.to_bytes(self.nickname))
                    data = self.to_text(sock.recv(1024))
                    if data[:2] == "sc":
                        special_print("Connected to the server", level=10)
                        # self.board.load_board(data[7 + len(data.split()[2]) - 1:])
                        # a = data.split()
                        # special_print(f"color: {a[1]} step: {a[2]} pieces: {a[3:]}", level=10)
                        # self.color = int(data.split()[1])
                        # self.board.step = int(data.split()[2])
                        # if self.color:
                        #     self.judge.flip()
                    self.socket = sock
                except Exception as e:
                    special_print("Something is wrong. Try to connect again")
                    continue
            else:
                if not self.sending_to_the_server("Check connection"):
                    print("Something is wrong")
                    self.socket.close()
                    self.socket = None
                time.sleep(1)

    def sending_to_the_server(self, message):
        # print(f"{message} Почему то я не хочу это отправлять")
        if self.socket:
            try:
                self.socket.send(self.to_bytes(message))
            except Exception as e:
                special_print(f"Bad connection with server - {e}", level=10)
                return False
        return True

    def getting_from_the_server(self):
        while self.running:
            if self.socket:
                try:
                    data = self.to_text(self.socket.recv(1024))
                    if data != "Check connection" and len(data) >= 2:
                        print(data)
                        if data[:2] == "su":
                            self.board.load_board(data[7 + len(data.split()[2]) - 1:])
                            a = data.split()
                            special_print(f"color: {a[1]} step: {a[2]} pieces: {a[3:]}", level=10)
                            self.color = int(data.split()[1])
                            self.board.step = int(data.split()[2])
                            if self.color:
                                self.judge.flip()
                        elif data[:2] in ["nm", "im"]:
                            self.board.step = int(data.split(":")[1])
                            special_print(data, level=10)
                            special_print(self.board.step, level=10)
                            self.board.load_board(data.split(":")[2])
                            if self.color:
                                self.judge.flip()
                        elif data[:2] == "ch":
                            wait_user_choice_thread = Thread(target=self.wait_user_choice)
                            wait_user_choice_thread.start()
                except Exception as e:
                    special_print(f"Bad connection with server - {e}", level=10)

    def wait_user_choice(self):
        self.board.set_pause(True)
        self.sending_to_the_server(f"mc {input()}")
        self.board.set_pause(False)

    def to_bytes(self, message):
        return bytes(message, encoding="utf-8")

    def to_text(self, message):
        return str(message)[2:-1]

    def run(self):
        self.connection_monitoring_thread = Thread(target=self.connect_with_server)
        self.connection_monitoring_thread.start()
        self.getting_from_the_server_thread = Thread(target=self.getting_from_the_server)
        self.getting_from_the_server_thread.start()

    def stop(self):
        self.running = False
        self.connection_monitoring_thread.join(0.1)
        self.getting_from_the_server_thread.join()


if __name__ == '__main__':
    client = Client(None, "Nickolausus", self_ip, 9090, None)
    client.run()
