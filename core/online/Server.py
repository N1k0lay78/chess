import socket
import time
from threading import Thread


class Socket(Thread):
    def __init__(self, port, ip_address, max_users, check_time):
        super().__init__()
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
                if len(self.users) < self.max_users and (nickname in self.players or len(self.players) < self.max_users) and nickname not in self.active_players:
                    self.active_players.append(nickname)
                    self.players.append(nickname)
                    self.users[address] = [conn, nickname]
                    print(f"{nickname} joined the game")
                    print(f"Users {len(self.users)}/{self.max_users}")
                    self.queue.remove([nickname, conn, address])
                    Thread(target=self.check_user_connect, args=(nickname, address, conn)).start()
            time.sleep(1)

    def check_user_connect(self, nickname, address, conn):
        f = False
        while True:
            try:
                if not f:
                    conn.send(b"Success connection")
                    f = True
                else:
                    conn.send(b"Check connection")
            except:
                if address in self.users:
                    self.active_players.remove(nickname)
                    del self.users[address]
                print(f"{nickname} left the game")
                print(f"Connection timed out with {address[0]}:{address[1]}")
                print(f"Users {len(self.users)}/{self.max_users}")
                break
            time.sleep(self.check_time)

    def run(self):
        Thread(target=self.user_master).start()
        while True:
            try:
                users = [[address, data[0], data[1]] for address, data in self.users.items()]
            except:
                continue
            for address, conn, nickname in users:
                data = None
                try:
                    data = str(conn.recv(1024))[2:-1]
                except:
                    print(f"Bad connection with {nickname} {address}")
                    time.sleep(1)
                if data:
                    print(f"Message from {nickname} - {data}")
                    # Какие то данные какие то сравнения


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


self_ip = socket.gethostbyname(socket.gethostname())

print(self_ip)

server = Server()
print(server.create_socket(9090, self_ip))
# print(server.create_socket(9091, self_ip))