import socket
from threading import Thread
import time
from Source.settings import params

# Получаем свой локальный ip адрес
# self_ip = socket.gethostbyname(socket.gethostname())


class Room:
    def __init__(self, board, judge, client):
        # game objects
        self.client = client
        self.board = board
        self.judge = judge
        self.message_queue = []

        # game
        self.is_choice = False
        self.color = 0
        self.running = True

        self.run_thread = Thread(target=self.run)
        self.run_thread.start()

    def get_server_message(self, message):
        # print("????????????????????????", message)
        self.message_queue.append(message)

    def send_to_server(self, message):
        self.client.sending_to_the_server(message)

    def run(self):
        while self.running:
            if len(self.message_queue):
                data = self.message_queue[0]
                # print(data, "!!!!DATA!!!!")
                if data[:2] == "su":
                    self.board.load_board(data[7 + len(data.split()[2]) - 1:])
                    a = data.split()
                    print(f"color: {a[1]} step: {a[2]} pieces: {a[3:]}")

                    self.color = int(data.split()[1])
                    self.board.color = int(data.split()[1])
                    self.judge.color = int(data.split()[1])
                    self.board.step = int(data.split()[2])

                    # if self.color:
                    #     self.judge.flip()

                elif data[:2] == "sp":
                    self.board.load_board(data[7 + len(data.split()[2]) - 1:])
                    self.color = int(data.split()[1])
                    self.board.color = int(data.split()[1])
                    self.judge.color = int(data.split()[1])
                    self.board.step = int(data.split()[2])

                elif data[:2] in ["nm", "im"]:
                    self.board.step = int(data.split(":")[1])
                    print(data)
                    print(self.board.step)
                    self.board.load_board(data.split(":")[2])

                    # if self.color:
                    #     self.judge.flip()

                elif data[:2] in ["ch", "er"]:
                    wait_user_choice_thread = Thread(target=self.wait_user_choice)
                    wait_user_choice_thread.start()
                self.message_queue.pop(0)

    def wait_user_choice(self):
        self.board.set_pause(True)
        self.send_to_server(f"mc {input('????3@#R#QWFE')}")
        self.board.set_pause(False)

    def stop(self):
        self.running = False
        self.run_thread.join(0)


class Client:
    def __init__(self, nickname, server, port):
        # print(server, port)
        # settings
        self.nickname = nickname
        self.server = server
        self.port = port

        # server
        self.socket = None
        self.connection_monitoring_thread = None
        self.getting_from_the_server_thread = None
        self.running = True
        self.send_to = []
        self.room = None

    def is_connected(self):
        return True if self.socket else False

    def connect_to_game(self, code, board, judge):
        # print("!!!?!?!?!?!")
        if not self.room and self.socket:
            # print("????????????????????????????????????????????????????????????????????????")
            self.room = Room(board, judge, self)
            self.send_to.append(self.room.get_server_message)
            time.sleep(1)
            self.sending_to_the_server(f"cg {code}")
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
                if not self.sending_to_the_server("Check connection"):
                    # print("Something is wrong")
                    self.socket.close()
                    self.socket = None
                    self.room = None
                    self.send_to = []
                time.sleep(1)

    def sending_to_the_server(self, message):
        # print(f"{message} Почему то я не хочу это отправлять")
        if self.socket:
            try:
                self.socket.send(self.to_bytes(message))
            except Exception as e:
                # print(f"Bad connection with server - {e}")
                # print(f"Bad connection with server - {e}")
                return False
        return True

    def getting_from_the_server(self):
        while self.running:
            if self.socket:
                try:
                    data = self.to_text(self.socket.recv(1024))
                    if data and data != "Check connection" and len(data) >= 2:
                        # print(data)
                        if data[:2] == "ga":
                            print("?SA?Fas/f/saf/as/fas")
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

    def stop(self):
        self.running = False
        self.connection_monitoring_thread.join(0)
        self.getting_from_the_server_thread.join(0)
        if self.socket:
            self.socket.close()
        if self.room:
            self.room.stop()
        print("Что за хуйня???")


if __name__ == '__main__':
    self_ip = socket.gethostbyname(socket.gethostname())
    client = Client("Nickolausus", self_ip, 9090)
    client.run()
