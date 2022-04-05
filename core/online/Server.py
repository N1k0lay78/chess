import socket
import time
from Source.boards import boards
from threading import Thread
from Source.settings import params
from core.online.logic.Board import LogicBoard


class Game:
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
        self.line = boards[params["board_name"]]
        self.board = LogicBoard(params["mode"] == "fog of war")
        self.board.load_board(self.line)
        self.server = server

    def send_to_user(self, user, message):
        return self.server.send_to_user(user[0], message)

    def update_all_users_condition(self):
        for key in self.players.keys():
            # print(f"Send data to {key} -", f"nm:{self.board.step}:{self.board.can_view(self.players[key]['data'][3])}")
            self.send_to_user(self.players[key]["data"], f"nm:{self.board.step}:{self.board.can_view(self.players[key]['data'][3])}")
        # self.send_to_user(self.players[key], f"nm:{self.board.step}:{self.board.can_view(self.players[3])}") #!!!!!!

    def get_user_message(self, nickname, message):
        self.message_queue.append([nickname, message])

    def connect_user(self, nickname, user):
        # print(f"Connect {nickname}")
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
                # print("?????")
                self.send_to_user(self.players[nickname]["data"], f"su {self.players[nickname]['color']} {self.board.step} "
                                                                  f"{self.board.can_view(self.players[nickname]['color'])}")
            else:
                self.send_to_user(self.players[nickname]["data"], f"sp {2} {self.board.step} {self.board.can_view(2)}")

    def leave_game(self, nickname):
        if nickname in self.players:
            self.players.pop(nickname)

    def run(self):
        while self.running:
            if len(self.message_queue):
                # print(self.message_queue[0])
                nickname, data = self.message_queue[0]
                if nickname in self.players and self.players[nickname]["color"] in [0, 1]:
                    print(f"New LM from {nickname} - {data}")
                    if data[:2] == "mo" and not self.wait_choice:
                        data = data[3:].split(":")
                        move = self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(","))))
                        print(("can" if move else "can't") + " move")
                        if not self.wait_choice:
                            self.wait_choice, self.pawn_coord = self.board.check_pawn()
                            if move and self.wait_choice:
                                self.send_to_user(self.players[nickname]["data"], "ch")
                            else:
                                self.update_all_users_condition()
                        # print(self.board.move(list(map(int, data[0].split(","))), list(map(int, data[1].split(",")))))
                    elif data[:2] == "mc" and self.wait_choice:
                        if len(data) == 4 and self.board.get_piece(self.pawn_coord).replace(data[3]):
                            self.update_all_users_condition()
                            self.wait_choice = False
                            self.pawn_coord = [-1, -1]
                            self.send_to_user(self.players[nickname]["data"], "ok")
                            self.update_all_users_condition()
                        else:
                            self.send_to_user(self.players[nickname]["data"], "er")
                    # elif data[:2] == "mc" and self.wait_choice and color == self.choice_color:
                    #     if self.board.get_piece(self.pawn_coord).replace(data[3]):
                    #         self.update_all_users_condition()
                    #         self.wait_choice = False
                    #     else:
                    #         self.ask_user_choice(self.choice_color, self.pawn_coord)
                    # else:
                    #     pass
                    #     # print(f"Message from {nickname} - {data}")
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
    def __init__(self, ip_address, port=8080):
        # print(ip_address, port)
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
        print("Success create user master")
        while True:
            conn, address = self.sock.accept()
            nickname = self.to_text(conn.recv(1024))
            print(f"{nickname} try to connect")
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
                    # print(f"Add user {nickname}")
            time.sleep(3)

    def get_from_user(self, nickname, conn, send_to):
        while True:
            try:
                data = self.to_text(conn.recv(1024))
                if data and len(data) >= 2 and data != "Check connection":
                    # print(data)
                    if data[:2] == "cg":
                        # print("Da blyat")
                        self.games[int(data.split()[1])][0].connect_user(nickname, self.users[nickname])
                    # print(f"Get message from user {nickname} {data}")
                    elif data[:2] == "hg":
                        if int(data.split()[1]) in list(self.games.keys()):
                            self.send_to_user(conn, "ga 1")
                        else:
                            self.send_to_user(conn, "ga 0")
                    for pol in send_to:
                        pol(nickname, data)
            except Exception as e:
                # print(f"Bad connection with {nickname} {address}")
                time.sleep(self.check_time)

    def send_to_user(self, conn, message):
        if conn and message:
            try:
                conn.send(self.to_bytes(message))
            except Exception as e:
                print("Error with send message -", message)
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
                    print(f"User {nickname} connected")
                    print(f"Users {len(self.users)}/{self.max_user_count}")

                    self.users[nickname][2] = True
                else:
                    res = self.send_to_user(conn, "Check connection")
                if not res:
                    if nickname in self.users:
                        listen_thread.join(0)
                        for bkey in self.games.keys():
                            self.games[bkey][0].leave_game(nickname)
                        self.users.pop(nickname)
                    # print(f"Delete user {nickname}")
                    # print(f"Connection timed out with {address[0]}:{address[1]}")
                    print(f"Users {len(self.users)}/{self.max_user_count}")
            time.sleep(self.check_time)

    def create_game(self, code=1234, max_users=4):
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
            print(f"Message from {nickname} - {message}")

    def to_bytes(self, message):
        return bytes(message, encoding="utf-8")

    def to_text(self, message):
        return str(message)[2:-1]


if __name__ == '__main__':

    self_ip = socket.gethostbyname(socket.gethostname())

    print(self_ip)

    server = Server(self_ip)
    print(server.create_game())
