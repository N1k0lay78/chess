import socket
from core.online.Server import Server

self_ip = socket.gethostbyname(socket.gethostname())

print(self_ip)

server = Server(self_ip, 8080)
print(server.create_game())