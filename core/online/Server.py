import socket
import time
from Source.boards import boards
from threading import Thread
from Source.settings import name_board_to_play, is_on_fog_of_war
from Source.special_functools import special_print
from core.online.logic.Board import LogicBoard


# class Socket(Thread):
#     def __init__(self, port, ip_address, max_users, check_time):
#         super().__init__()
#         # settings
#         self.port = port
#         self.ip_address = ip_address
#         self.max_users = max_users
#         self.check_time = check_time
#         # socket
#         self.sock = socket.socket()
#         self.sock.bind((self.ip_address, self.port))
#         self.sock.listen(self.max_users)
#         self.queue = []
#         # work with user
#         self.users = {}
#         self.players = []
#         self.active_players = []
#         self.wait_choice = False
#         # logic of game
#         self.pawn_coord = []
#         self.choice_color = 4
#         self.line = boards[name_board_to_play]
#         self.board = LogicBoard(self, is_on_fog_of_war)
#         self.board.load_board(self.line)
#
#     def ask_user_choice(self, color, coord):
#         while True:
#             try:
#                 for address, data in self.users.items():
#                     if data[2] == color:
#                         self.wait_choice = True
#                         self.pawn_coord = coord
#                         self.choice_color = color
#                         self.send_to_user(data[0], "ch make right choice")
#                         self.update_all_users_condition()
#                 break
#             except:
#                 continue
#
#     def send_to_user(self, conn, message):
#         if conn and message:
#             try:
#                 conn.send(self.to_bytes(message))
#             except:
#                 special_print("Error with send message", message, level=10)
#                 return False
#         return True
#
#     def user_master(self):
#         special_print("Success create user master", level=10)
#         Thread(target=self.user_queue).start()
#         while True:
#             conn, address = self.sock.accept()
#             nickname = self.to_text(conn.recv(1024))
#             special_print(f"{nickname} try to connect", level=10)
#             self.queue.append([nickname, conn, address])
#
#     def user_queue(self):
#         while True:
#             users = [[nickname, conn, address] for nickname, conn, address in self.queue]
#             for nickname, conn, address in users:
#                 if len(self.users) < self.max_users and (((nickname, 0) in self.players or (nickname, 1) in self.players) or len(self.players) < self.max_users) and nickname not in self.active_players:
#                     if (nickname, 0) in self.players or (nickname, 1) in self.players:
#                         color = list(filter(lambda x: x[0] == nickname, self.players))[0][1]
#                     else:
#                         color = len(self.active_players)
#                     self.players.append((nickname, color))
#                     self.active_players.append(nickname)
#                     self.users[address] = [conn, nickname, color]
#                     special_print(f"{nickname} joined the game", level=10)
#                     special_print(f"Users {len(self.users)}/{self.max_users}", level=10)
#                     self.queue.remove([nickname, conn, address])
#                     Thread(target=self.check_user_connect, args=(nickname, address, conn, color)).start()
#                     Thread(target=self.get_user_message, args=(nickname, address, conn, color)).start()
#             time.sleep(1)
#
#     def check_user_connect(self, nickname, address, conn, color):
#         f = False
#         while True:
#             if not f:
#                 res = self.send_to_user(conn, f"su {color} {self.board.step} {self.board.can_view(color)}")
#                 f = True
#             else:
#                 res = self.send_to_user(conn, "Check connection")
#             if not res:
#                 if address in self.users:
#                     self.active_players.remove(nickname)
#                     del self.users[address]
#                 special_print(f"{nickname} left the game", level=10)
#                 special_print(f"Connection timed out with {address[0]}:{address[1]}", level=10)
#                 special_print(f"Users {len(self.users)}/{self.max_users}", level=10)
#                 return
#             time.sleep(self.check_time)
#
#     def update_all_users_condition(self):
#         print("Обновляю кондиции")
#         while True:
#             try:
#                 for address, data in self.users.items():
#                     self.send_to_user(data[0], f"nm:{self.board.step}:{self.board.can_view(data[2])}")
#                 return
#             except:
#                 continue
#
#     def return_all_back(self):
#         print("Накладываю санкции на ход")
#         while True:
#             try:
#                 for address, data in self.users.items():
#                     self.send_to_user(data[0], f"im:{self.board.step}:{self.board.can_view(data[2])}")
#                 return
#             except:
#                 continue
#
#     def get_user_message(self, nickname, address, conn, color):
#         while True:
#             try:
#                 data = self.to_text(conn.recv(1024))
#                 if data and data != "Check connection":
#                     if data[:2] == "mo":
#                         data = data[3:].split(":")
#                         move = self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(","))))
#                         special_print(("can" if move else "can't") + " move", level=10)
#                         if not self.wait_choice and move:
#                             self.update_all_users_condition()
#                         elif not move:
#                             self.return_all_back()
#                         # special_print(self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(",")))), level=10)
#                     elif data[:2] == "mc" and self.wait_choice and color == self.choice_color:
#                         if self.board.get_piece(self.pawn_coord).replace(data[3]):
#                             self.update_all_users_condition()
#                             self.wait_choice = False
#                         else:
#                             self.ask_user_choice(self.choice_color, self.pawn_coord)
#                     else:
#                         pass
#                         # special_print(f"Message from {nickname} - {data}", level=10)
#             except Exception as e:
#                 special_print(e, level=10)
#                 special_print(f"Bad connection with {nickname} {address}", level=10)
#                 return
#
#     def run(self):
#         Thread(target=self.user_master).start()
#
#     def to_bytes(self, message):
#         return bytes(message, encoding="utf-8")
#
#     def to_text(self, message):
#         return str(message)[2:-1]
#
#     def restart(self):
#         self.wait_choice = False
#         self.pawn_coord = []
#         self.choice_color = 4

class Game(Thread):
    def __init__(self, port, ip_address, max_users, check_time, users):
        super().__init__()
        # settings
        self.port = port
        self.ip_address = ip_address
        self.max_users = max_users
        self.check_time = check_time

        # socket
        self.sock = socket.socket()
        self.sock.bind((self.ip_address, self.port))
        self.sock.listen(self.max_users)
        self.queue = []

        # work with user
        self.users = users
        self.players = []
        self.active_players = []
        self.wait_choice = False

        # logic of game
        self.pawn_coord = []
        self.choice_color = 4
        self.line = boards[name_board_to_play]
        self.board = LogicBoard(self, is_on_fog_of_war)
        self.board.load_board(self.line)

    def ask_user_choice(self, color, coord):
        while True:
            try:
                for address, data in self.users.items():
                    if data[2] == color:
                        self.wait_choice = True
                        self.pawn_coord = coord
                        self.choice_color = color
                        self.send_to_user(data[0], "ch make right choice")
                        self.update_all_users_condition()
                break
            except:
                continue

    def send_to_user(self, conn, message):
        if conn and message:
            try:
                conn.send(self.to_bytes(message))
            except:
                special_print("Error with send message", message, level=10)
                return False
        return True

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
                special_print(f"{nickname} left the game", level=10)
                special_print(f"Connection timed out with {address[0]}:{address[1]}", level=10)
                special_print(f"Users {len(self.users)}/{self.max_users}", level=10)
                return
            time.sleep(self.check_time)

    def update_all_users_condition(self):
        print("Обновляю кондиции")
        while True:
            try:
                for address, data in self.users.items():
                    self.send_to_user(data[0], f"nm:{self.board.step}:{self.board.can_view(data[2])}")
                return
            except:
                continue

    def return_all_back(self):
        print("Накладываю санкции на ход")
        while True:
            try:
                for address, data in self.users.items():
                    self.send_to_user(data[0], f"im:{self.board.step}:{self.board.can_view(data[2])}")
                return
            except:
                continue

    def get_user_message(self, nickname, address, conn, color):
        while True:
            try:
                data = self.to_text(conn.recv(1024))
                if data and data != "Check connection":
                    if data[:2] == "mo":
                        data = data[3:].split(":")
                        move = self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(","))))
                        special_print(("can" if move else "can't") + " move", level=10)
                        if not self.wait_choice and move:
                            self.update_all_users_condition()
                        elif not move:
                            self.return_all_back()
                        # special_print(self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(",")))), level=10)
                    elif data[:2] == "mc" and self.wait_choice and color == self.choice_color:
                        if self.board.get_piece(self.pawn_coord).replace(data[3]):
                            self.update_all_users_condition()
                            self.wait_choice = False
                        else:
                            self.ask_user_choice(self.choice_color, self.pawn_coord)
                    else:
                        pass
                        # special_print(f"Message from {nickname} - {data}", level=10)
            except Exception as e:
                special_print(e, level=10)
                special_print(f"Bad connection with {nickname} {address}", level=10)
                return

    def run(self):
        Thread(target=self.user_master).start()

    def to_bytes(self, message):
        return bytes(message, encoding="utf-8")

    def to_text(self, message):
        return str(message)[2:-1]

    def restart(self):
        self.wait_choice = False
        self.pawn_coord = []
        self.choice_color = 4


class Server:
    def __init__(self, ip_address, port=5050):
        self.max_user_count = 100
        self.check_time = 1
        self.ip_address = ip_address
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((self.ip_address, self.port))
        self.sock.listen(self.max_user_count)

        self.users = {}
        self.queue = []
        self.games = {}

        self.check_connect_thread = Thread(target=self.check_connect)
        self.check_connect_thread.start()
        self.user_queue_thread = Thread(target=self.user_queue)
        self.user_queue_thread.start()
        self.check_user_connections_thread = Thread(target=self.check_user_connections)
        self.check_user_connections_thread.start()

    def check_connect(self):
        special_print("Success create user master", level=10)
        while True:
            conn, address = self.sock.accept()
            nickname = self.to_text(conn.recv(1024))
            special_print(f"{nickname} try to connect", level=10)
            self.queue.append([nickname, conn, address])

    def user_queue(self):
        while True:
            users = [[nickname, conn, address] for nickname, conn, address in self.queue]
            for nickname, conn, address in users:
                if len(self.users) < self.max_user_count and nickname not in self.users:
                    listen_thread = Thread(target=self.listen_user, args=(nickname, address, conn))
                    listen_thread.start()
                    self.users[nickname] = [conn, address, listen_thread, False]
                    self.queue.remove([nickname, conn, address])

    def listen_user(self, nickname, address, conn):
        while True:
            try:
                data = self.to_text(conn.recv(1024))
                if data and data != "Check connection":
                    special_print(f"Get message from user {nickname} {data}")
            except Exception as e:
                # special_print(f"Bad connection with {nickname} {address}", level=10)
                time.sleep(self.check_time)

    def send_to_user(self, conn, message):
        if conn and message:
            try:
                conn.send(self.to_bytes(message))
            except Exception as e:
                special_print("Error with send message", message, level=10)
                return False
        return True

    def check_user_connections(self):
        while True:
            users = []
            for key, values in self.users.items():
                users.append([key, *values])
            for nickname, conn, address, listen_thread, send_m in users:
                # print(nickname, conn, address, listen_thread, send_m, sep="\n")
                if not send_m:
                    res = self.send_to_user(conn, f"su")
                    special_print(f"User {nickname} connected", level=10)
                    special_print(f"Users {len(self.users)}/{self.max_user_count}", level=10)

                    self.users[nickname][3] = True
                else:
                    res = self.send_to_user(conn, "Check connection")
                if not res:
                    if nickname in self.users:
                        listen_thread.join(0)
                        self.users.pop(nickname)
                    special_print(f"{nickname} left the game", level=10)
                    # special_print(f"Connection timed out with {address[0]}:{address[1]}", level=10)
                    special_print(f"Users {len(self.users)}/{self.max_user_count}", level=10)
            time.sleep(self.check_time)

    def create_game(self, port, ip_address, max_users=2):
        if port not in self.games:  # Проверяем, что игры с таким портом не существует
            game = Game(port, ip_address, max_users, 3)
            game_thread = Thread(target=game.run)
            game_thread.start()
            self.games[port] = [game, game_thread]
            return {"success": "Game success created"}
        else:
            return {"error": "This port for game is already in use"}  # Просим так больше не делать

    def to_bytes(self, message):
        return bytes(message, encoding="utf-8")

    def to_text(self, message):
        return str(message)[2:-1]

# class Server:
#     def __init__(self):
#         self.ports = []
#         self.sockets = []
#
#     def create_socket(self, port, ip_address, max_users=2):
#         if port not in self.ports:  # Проверяем, что сокета с таким портом не существует
#             sock = Socket(port, ip_address, max_users, 3)
#             self.sockets.append(sock)
#             self.ports.append(port)
#             Thread(target=sock.run).start()
#
#             return {"success": "Port success started"}
#         else:
#             return {"error": "This port is already in use"}  # Просим так больше не делать


if __name__ == '__main__':

    self_ip = socket.gethostbyname(socket.gethostname())

    print(self_ip)

    server = Server()
    print(server.create_socket(9090, self_ip))
    # print(server.create_socket(9091, self_ip))
