import socket
import time


sock = socket.socket()
sock.connect(("127.0.0.1", 1080))
# data = input()
data = "Высылаю данные"

while True:
    sock.send(bytes(data, encoding="utf-8"))
    print(sock.recv(1024).decode())
    time.sleep(0.1)
