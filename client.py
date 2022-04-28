import socket
import time


# print(help(socket))
sock = socket.socket()
sock.connect(("127.0.0.1", 1080))
# data = input()
data = "newn nikolausus"

while True:
    # sock.send(bytes(data, encoding="utf-8"))
    # print(sock.recv(1024).decode())
    time.sleep(0.1)
    # break
