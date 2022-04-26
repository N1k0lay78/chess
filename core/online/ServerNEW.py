import socket
import time
from Source.boards import boards
from threading import Thread
from Source.settings import params
from core.online.logic.Board import LogicBoard

commands = {
    "crgm"
}


def to_bytes(message):
    return bytes(message, encoding="utf-8")


def to_text(message):
    return str(message)[2:-1]


class Game:
    pass


class Server:
    def __init__(self, id_address, port=8080):
        # Main settings of server
        self.ip_address = id_address
        self.port = port
        self.max_count_of_user = 100
        self.check_connection_time = 5
        self.running = False

        # Auxiliary data
        self.users = {}
        self.games = {}
        self.queue_user = []
        self.queue_message = {"main": []}

        # Socket
        self.sock = None

    def user_master(self):
        print("Success create user master")
        while self.running:
            try:
                conn, address = self.sock.accept()
                nickname = to_text(conn.recv(1024))
                print(f"{nickname} try to connect")
                self.queue_user.append([nickname, conn, address])
            except Exception as e:
                # print(e)
                pass

    def user_manager(self):
        while self.running:
            if len(self.queue_user) == 0 or len(self.users) >= self.max_count_of_user:
                continue

            nickname, conn, address = self.queue_user.pop(0)
            send_to = []

            listen_thread = Thread(target=self.get_from_user, args=(nickname, conn, send_to))
            listen_thread.start()

            self.users[nickname] = [conn, address, False, send_to, listen_thread]

    def get_from_user(self, nickname, conn, send_to):
        while self.running:
            try:
                data = to_text(conn.recv(1024)).replace("Check connection", "")
                if len(data) >= 2:
                    for recipient in send_to:
                        recipient(nickname, data)
            except Exception as e:
                pass

    def run(self):

        self.sock = socket.socket()
        self.sock.bind((self.ip_address, self.port))
        self.sock.listen(self.max_count_of_user)
        self.running = True

    def stop(self):
        self.sock.close()
        self.running = False


if __name__ == '__main__':

    self_ip = socket.gethostbyname(socket.gethostname())

    print(self_ip)

    server = Server(self_ip)
    print(server.create_game())