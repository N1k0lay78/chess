import socket
from threading import Thread
import time
import pygame

# Получаем свой локальный ip адрес
self_ip = socket.gethostbyname(socket.gethostname())


class Client:
    def __init__(self, game, nickname, server, port):
        self.game = game
        self.nickname = nickname
        self.server = server
        self.port = port
        self.is_connected = False
        self.socket = None
        self.connection_monitoring_thread = None
        self.getting_from_the_server_thread = None
        self.running = True

    def connection_monitoring(self):
        while self.running:
            if not self.socket:
                try:
                    sock = socket.socket()
                    sock.connect((self_ip, 9090))
                    sock.send(self.to_bytes(self.nickname))
                    data = self.to_text(sock.recv(1024))
                except:
                    # print("pidor")
                    continue
                # print(data, "ne ponimat")
                print(data)
                if data[:2] == "su":
                    print("Connected")
                    self.game.board.set_color(int(data.split()[1]))
                    self.game.color = int(data.split()[1])
                    self.game.board.step = int(data.split()[2])
                    self.game.board.load_board(data[7 + len(data.split()[2]) - 1:])
                    self.socket = sock
            else:
                try:
                    # print("norm")
                    self.socket.send(self.to_bytes("Check connection"))
                except:
                    # print("a net, gay")
                    self.socket = None
                time.sleep(1)

    def to_bytes(self, message):
        return bytes(message, encoding="utf-8")

    def to_text(self, message):
        return str(message)[2:-1]

    def getting_from_the_server(self):
        while self.running:
            if self.socket:
                try:
                    data = self.to_text(self.socket.recv(1024))
                    if data != "Check connection":
                        print(data)
                        if data[:2] == "nm":
                            print("load new map")
                            self.game.board.load_board(data[3:])
                            self.game.board.go_to_next_step()
                except:
                    print("Lost connection")
                    self.socket = None

    def sending_to_the_server(self, message):
        while self.running:
            if self.socket:
                try:
                    self.socket.send(self.to_bytes(message))
                except:
                    print("Lost connection")
                    self.socket = None
                    continue
            break

    def run(self):
        self.connection_monitoring_thread = Thread(target=self.connection_monitoring)
        self.connection_monitoring_thread.start()
        self.getting_from_the_server_thread = Thread(target=self.getting_from_the_server)
        self.getting_from_the_server_thread.start()

    def stop(self):
        self.running = False
        self.connection_monitoring_thread.join(0.1)
        self.getting_from_the_server_thread.join()


if __name__ == '__main__':
    client = Client(None, "Nickolausus", self_ip, 9090)
    client.run()
