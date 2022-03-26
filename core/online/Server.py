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

class Game():
    def __init__(self, game_code, max_users, server):
        # settings
        self.game_code = game_code
        self.max_users = max_users
        self.running = True

        # work with user
        self.players = {}
        self.wait_choice = False
        self.message_queue = []

        # logic of game
        self.pawn_coord = []
        self.choice_color = 4
        self.line = boards[name_board_to_play]
        self.board = LogicBoard(self, is_on_fog_of_war)
        self.board.load_board(self.line)
        self.server = server

    def send_to_user(self, user, message):
        return self.server.send_to_user(user[0], message)

    def update_all_users_condition(self):
        for key in self.players.keys():
            self.send_to_user(self.players[key]["data"], f"nm:{self.board.step}:{self.board.can_view(self.players[key]['data'][3])}")
        # self.send_to_user(self.players[key], f"nm:{self.board.step}:{self.board.can_view(self.players[3])}") #!!!!!!

    def get_user_message(self, nickname, message):
        self.message_queue.append([nickname, message])

    def connect_user(self, nickname, user):
        if len(self.players) < self.max_users and nickname not in self.players:
            color = [0, 1]
            for key in self.players.keys():
                if self.players[key]["color"] in color:
                    color.remove(self.players[key]["color"])
            self.players[nickname] = {}
            self.players[nickname]["data"] = user
            self.players[nickname]["data"][3].append(self.get_user_message)
            self.players[nickname]["color"] = color[0] if len(color) > 0 else 2
            if self.players[nickname]["color"] in [0, 1]:
                self.send_to_user(self.players[nickname]["data"], f"su {self.players[nickname]['color']} "
                                                                  f"{self.board.step} {self.board.can_view(color)}")

    def leave_game(self, nickname):
        if nickname in self.players:
            self.players.pop(nickname)

    def run(self):
        while self.running:
            while len(self.message_queue):
                nickname, data = self.message_queue[0]
                if nickname in self.players and self.players[nickname]["color"] in [0, 1]:
                    special_print(f"New LM from {nickname} - {data}", level=10)
                    if data[:2] == "mo":
                        data = data[3:].split(":")
                        move = self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(","))))
                        special_print(("can" if move else "can't") + " move", level=10)
                        if not self.wait_choice:
                            self.update_all_users_condition()
                        # print(self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(",")))))
                    # elif data[:2] == "mc" and self.wait_choice and color == self.choice_color:
                    #     if self.board.get_piece(self.pawn_coord).replace(data[3]):
                    #         self.update_all_users_condition()
                    #         self.wait_choice = False
                    #     else:
                    #         self.ask_user_choice(self.choice_color, self.pawn_coord)
                    # else:
                    #     pass
                    #     # special_print(f"Message from {nickname} - {data}", level=10)
                self.message_queue.pop(0)

    def stop(self):
        self.running = False

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

                    send_to = [self.logic_with_user]

                    listen_thread = Thread(target=self.get_from_user, args=(nickname, conn, send_to))
                    listen_thread.start()

                    self.users[nickname] = [conn, address, False, send_to, listen_thread]
                    self.queue.remove([nickname, conn, address])
                    print(f"Add user {nickname}")

    def get_from_user(self, nickname, conn, send_to):
        while True:
            try:
                data = self.to_text(conn.recv(1024))
                if data and len(data) >= 2 and data != "Check connection":
                    # special_print(f"Get message from user {nickname} {data}")
                    for pol in send_to:
                        pol(nickname, data)
            except Exception as e:
                # special_print(f"Bad connection with {nickname} {address}", level=10)
                time.sleep(self.check_time)

    def send_to_user(self, conn, message):
        if conn and message:
            try:
                conn.send(self.to_bytes(message))
            except Exception as e:
                special_print("Error with send message -", message, level=10)
                return False
        return True

    def check_user_connections(self):
        while True:
            users = []
            for key, values in self.users.items():
                users.append([key, *values])
            for nickname, conn, address, send_m, st, listen_thread in users:
                # print(nickname, conn, address, listen_thread, send_m, sep="\n")
                if not send_m:
                    res = self.send_to_user(conn, f"sc")
                    special_print(f"User {nickname} connected", level=10)
                    special_print(f"Users {len(self.users)}/{self.max_user_count}", level=10)

                    self.users[nickname][2] = True
                    self.games[1234][0].connect_user(nickname, self.users[nickname])
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

    def create_game(self, code=1234, max_users=2):
        if code not in self.games:
            game = Game(code, max_users, self)
            game_thread = Thread(target=game.run)
            game_thread.start()
            self.games[code] = [game, game_thread]
            return {"success": "Game success created"}
        else:
            return {"error": "This port for game is already in use"}  # Просим так больше не делать

    def logic_with_user(self, nickname, message):
        if nickname in self.users:
            special_print(f"Message from {nickname} - {message}", level=10)

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

    server = Server(self_ip)
    print(server.create_game())
    # print(server.create_socket(9091, self_ip))
