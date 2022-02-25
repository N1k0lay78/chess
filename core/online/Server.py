import socket
import time
from Source.boards import boards
from threading import Thread

from Source.settings import name_board_to_play
from core.online.logic.Board import LogicBoard


class Socket(Thread):
    def __init__(self, port, ip_address, max_users, check_time):
        super().__init__()
        self.line = boards[name_board_to_play]
        self.board = LogicBoard(self, self.line)
        self.port = port
        self.ip_address = ip_address
        self.max_users = max_users
        self.sock = socket.socket()
        self.sock.bind((self.ip_address, self.port))
        self.sock.listen(self.max_users)
        self.check_time = check_time
        self.users = {}
        self.queue = []
        self.players = []
        self.active_players = []
        self.wait_choice = False
        self.pawn_coord = []
        self.choice_color = 4

    def ask_user_choice(self, color, coord):
        while True:
            try:
                for address, data in self.users.items():
                    if data[2] == color:
                        self.wait_choice = True
                        self.pawn_coord = coord
                        self.choice_color = color
                        self.send_to_user(data[0], "ch make right choice")
                break
            except:
                continue

    def send_to_user(self, conn, message):
        if conn and message:
            try:
                conn.send(self.to_bytes(message))
            except:
                print("Error with send message", message)
                return False
        return True

    def user_master(self):
        print("Success create user master")
        Thread(target=self.user_queue).start()
        while True:
            conn, address = self.sock.accept()
            nickname = str(conn.recv(1024))[2:-1]
            print(f"{nickname} try to connect")
            self.queue.append([nickname, conn, address])

    def user_queue(self):
        while True:
            users = [[nickname, conn, address] for nickname, conn, address in self.queue]
            for nickname, conn, address in users:
                if len(self.users) < self.max_users and (((nickname, 0) in self.players or (nickname, 1) in self.players) or len(self.players) < self.max_users) and nickname not in self.active_players:
                    if (nickname, 0) in self.players or (nickname, 1) in self.players:
                        color = list(filter(lambda x: x[0] == nickname, self.players))[0][1]
                    else:
                        color = len(self.active_players)
                    self.players.append((nickname, color))
                    self.active_players.append(nickname)
                    self.users[address] = [conn, nickname, color]
                    print(f"{nickname} joined the game")
                    print(f"Users {len(self.users)}/{self.max_users}")
                    self.queue.remove([nickname, conn, address])
                    Thread(target=self.check_user_connect, args=(nickname, address, conn, color)).start()
                    Thread(target=self.get_user_message, args=(nickname, address, conn, color)).start()
            time.sleep(1)

    def check_user_connect(self, nickname, address, conn, color):
        f = False
        while True:
            if not f:
                res = self.send_to_user(conn, f"su {color} {self.board.step} {self.board.can_view(color)}")
                f = True
            else:
                res = self.send_to_user(conn, "Check connection")
            if not res:
                if address in self.users:
                    self.active_players.remove(nickname)
                    del self.users[address]
                print(f"{nickname} left the game")
                print(f"Connection timed out with {address[0]}:{address[1]}")
                print(f"Users {len(self.users)}/{self.max_users}")
                return
            time.sleep(self.check_time)

    def update_all_users_condition(self):
        while True:
            try:
                for address, data in self.users.items():
                    self.send_to_user(data[0], f"nm:{self.board.step}:{self.board.can_view(data[2])}")
                return
            except:
                continue

    def get_user_message(self, nickname, address, conn, color):
        while True:
            try:
                data = str(conn.recv(1024))[2:-1]
                if data and data != "Check connection":
                    print(data)
                    if data[:2] == "mo":
                        data = data[3:].split(":")
                        move = self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(","))))
                        print(move)
                        if not self.wait_choice and move:
                            self.update_all_users_condition()
                        # print(self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(",")))))
                    elif data[:2] == "mc" and self.wait_choice and color == self.choice_color:
                        if self.board.get_piece(self.pawn_coord).replace(data[3]):
                            self.update_all_users_condition()
                            self.wait_choice = False
                        else:
                            self.ask_user_choice(self.choice_color, self.pawn_coord)
                    else:
                        pass
                        # print(f"Message from {nickname} - {data}")
                    # Какие то данные какие то сравнения
            except Exception as e:
                print(e)
                print(f"Bad connection with {nickname} {address}")
                return

    def run(self):
        Thread(target=self.user_master).start()

    def to_bytes(self, message):
        return bytes(message, encoding="utf-8")

    def to_text(self, message):
        return str(message)[2:-1]


class Server:
    def __init__(self):
        self.ports = []
        self.sockets = []

    def create_socket(self, port, ip_address, max_users=2):
        if port not in self.ports:  # Проверяем, что сокета с таким портом не существует
            sock = Socket(port, ip_address, max_users, 3)
            self.sockets.append(sock)
            self.ports.append(port)
            Thread(target=sock.run).start()

            return {"success": "Port success started"}
        else:
            return {"error": "This port is already in use"}  # Просим так больше не делать


if __name__ == '__main__':

    self_ip = socket.gethostbyname(socket.gethostname())

    print(self_ip)

    server = Server()
    print(server.create_socket(9090, self_ip))
    # print(server.create_socket(9091, self_ip))